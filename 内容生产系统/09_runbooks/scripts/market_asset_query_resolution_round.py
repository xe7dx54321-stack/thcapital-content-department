#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import re
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlencode, urlparse

from market_business_day import day_token, path_in_business_window
from market_topic_capture_round import compact_snippet, fetch_text, format_dt, now_cn, slugify, write_text
from market_asset_derivation_round import (
    ASSET_DIR,
    LOG_DIR,
    PUBLISHER_IGNORE_HOSTS,
    SOCIAL_HOST_PATTERNS,
    STATE_DIR,
    choose_official_site,
    classify_links,
    extract_emails,
    extract_founder_names,
    extract_urls_from_html,
    filter_emails,
    generate_search_queries,
    host_of,
    is_ignored_evidence_url,
    parse_markdown_fields,
    root_url,
    unique,
)


RESOLVED_DIR = ASSET_DIR / "resolved"
RESOLVED_RAW_DIR = RESOLVED_DIR / "raw"
RESOLUTION_STATE_PATH = STATE_DIR / "market_asset_query_resolution_state.json"
DEFAULT_SOURCE_IDS = [
    "trend__yc_launches_ai",
    "web__techcrunch_ai",
    "web__finsmes_ai_gnews",
]
SEARCH_HOST_IGNORE = {
    "bing.com",
    "www.bing.com",
    "r.bing.com",
    "th.bing.com",
    "search.brave.com",
    "www.startpage.com",
    "html.duckduckgo.com",
    "duckduckgo.com",
    "r.jina.ai",
}
ENTITY_TOKEN_STOPWORDS = {
    "ai",
    "app",
    "apps",
    "co",
    "company",
    "corp",
    "corporation",
    "group",
    "holdings",
    "inc",
    "incorporated",
    "lab",
    "labs",
    "limited",
    "llc",
    "ltd",
    "sa",
    "sas",
    "systems",
    "system",
    "tech",
    "technology",
    "technologies",
}
GENERIC_QUERY_TAILS = (
    "official site",
    "company",
    "funding",
    "demo",
    "youtube demo",
)
GENERIC_QUERY_TAILS_CN = (
    "官网",
    "公司",
    "融资",
    "产品演示",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve weak asset chains via one-hop web search.")
    parser.add_argument("--date", help="Logical date. Default: today in Asia/Shanghai.")
    parser.add_argument("--source-id", action="append", dest="source_ids", help="Filter by source id.")
    parser.add_argument("--entity-name", help="Only resolve chains whose entity name contains this string.")
    parser.add_argument("--limit", type=int, default=5, help="Max weak chains to process.")
    parser.add_argument("--write", action="store_true", help="Actually write resolved artifacts.")
    parser.add_argument("--force", action="store_true", help="Re-resolve even if a resolution already exists.")
    return parser.parse_args()


def ensure_dirs() -> None:
    RESOLVED_DIR.mkdir(parents=True, exist_ok=True)
    RESOLVED_RAW_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def logical_date_token(logical_date: str) -> str:
    return day_token(logical_date)


def path_matches_logical_date(path_value: str | Path | None, logical_date: str) -> bool:
    return path_in_business_window(path_value, logical_date)


def parse_json_blocks(markdown_text: str) -> list[dict]:
    blocks = re.findall(r"```json\n(.*?)\n```", markdown_text, re.S)
    parsed: list[dict] = []
    for block in blocks:
        try:
            parsed.append(json.loads(block))
        except json.JSONDecodeError:
            parsed.append({})
    return parsed


def parse_chain_artifact(chain_path: Path) -> dict | None:
    chain_text = chain_path.read_text(encoding="utf-8")
    fields = parse_markdown_fields(chain_text)
    raw_path = Path(fields.get("raw_derivation_path", ""))
    if not raw_path.exists():
        return None
    json_blocks = parse_json_blocks(raw_path.read_text(encoding="utf-8"))
    packet_fields = json_blocks[0] if len(json_blocks) > 0 else {}
    raw_fields = json_blocks[1] if len(json_blocks) > 1 else {}
    derived = json_blocks[2] if len(json_blocks) > 2 else {}
    official_site = fields.get("official_site", "")
    if official_site == "unknown":
        official_site = ""
    return {
        "chain_path": str(chain_path),
        "raw_path": str(raw_path),
        "source_packet_path": fields.get("source_packet_path", ""),
        "source_id": fields.get("source_id", ""),
        "entity_name": fields.get("entity_name", ""),
        "official_site": official_site,
        "packet_fields": packet_fields,
        "raw_fields": raw_fields,
        "derived": derived,
    }


def latest_chain_candidates(source_ids: list[str], limit: int, logical_date: str, entity_name_filter: str | None = None) -> list[dict]:
    all_paths = sorted(ASSET_DIR.glob("*__asset-chain.md"), key=lambda path: path.stat().st_mtime, reverse=True)
    latest_by_packet: dict[str, dict] = {}
    lowered_filter = (entity_name_filter or "").strip().lower()
    for chain_path in all_paths:
        if not path_matches_logical_date(chain_path, logical_date):
            continue
        parsed = parse_chain_artifact(chain_path)
        if not parsed:
            continue
        if source_ids and parsed["source_id"] not in source_ids:
            continue
        if lowered_filter and lowered_filter not in parsed["entity_name"].lower():
            continue
        if not (
            path_matches_logical_date(parsed["source_packet_path"], logical_date)
            or path_matches_logical_date(parsed["chain_path"], logical_date)
        ):
            continue
        packet_key = parsed["source_packet_path"] or parsed["chain_path"]
        if packet_key in latest_by_packet:
            continue
        latest_by_packet[packet_key] = parsed
    weak: list[dict] = []
    for parsed in latest_by_packet.values():
        derived = parsed["derived"]
        official_site = parsed["official_site"]
        if official_site:
            continue
        if derived.get("company_social") or derived.get("demo") or derived.get("docs"):
            continue
        weak.append(parsed)
    weak.sort(key=lambda row: Path(row["chain_path"]).stat().st_mtime, reverse=True)
    return weak[:limit]


def needs_resolution(parsed_chain: dict, state: dict, force: bool) -> bool:
    key = parsed_chain["source_packet_path"] or parsed_chain["chain_path"]
    if force:
        return True
    return key not in state.setdefault("chains", {})


def decode_bing_redirect(url: str) -> str | None:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    encoded = query.get("u", [])
    if not encoded:
        return None
    value = unquote(encoded[0])
    if value.startswith("a1"):
        payload = value[2:]
        payload += "=" * ((4 - len(payload) % 4) % 4)
        try:
            decoded = base64.b64decode(payload).decode("utf-8", "replace")
        except Exception:
            return None
        return decoded if decoded.startswith("http") else None
    return value if value.startswith("http") else None


def decode_duckduckgo_redirect(url: str) -> str | None:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    encoded = query.get("uddg", [])
    if not encoded:
        return None
    value = unquote(encoded[0])
    return value if value.startswith("http") else None


def normalize_search_target(url: str) -> str | None:
    lowered = url.lower().strip()
    if not lowered or lowered.startswith("javascript:") or lowered.startswith("blob:"):
        return None
    parsed = urlparse(url)
    host = host_of(url)
    if host in SEARCH_HOST_IGNORE:
        if host in {"bing.com", "www.bing.com"} and parsed.path in {"/ck/a", "/aclk"}:
            return decode_bing_redirect(url)
        if host in {"duckduckgo.com", "www.duckduckgo.com"} and parsed.path.startswith("/l/"):
            return decode_duckduckgo_redirect(url)
        return None
    return url


def search_markdown_links(markdown_text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for line in markdown_text.splitlines():
        for title, raw_url in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", line):
            target_url = normalize_search_target(raw_url)
            if not target_url:
                continue
            cleaned_title = re.sub(r"!\[[^\]]*\]\s*", "", title).strip()
            if not cleaned_title:
                cleaned_title = compact_snippet(target_url, 120)
            pairs.append((cleaned_title, target_url))
    deduped: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for title, url in pairs:
        key = (title, url)
        if key in seen:
            continue
        seen.add(key)
        deduped.append((title, url))
    return deduped


def search_bing_jina(query: str) -> list[dict]:
    search_url = "https://r.jina.ai/http://https://www.bing.com/search?" + urlencode({"q": query})
    markdown = fetch_text(search_url)
    results: list[dict] = []
    for title, target_url in search_markdown_links(markdown):
        host = host_of(target_url)
        if not host or host in SEARCH_HOST_IGNORE:
            continue
        results.append(
            {
                "engine": "bing-jina",
                "query": query,
                "title": compact_snippet(title, 160),
                "target_url": target_url,
                "host": host,
            }
        )
    return results


def search_duckduckgo_html(query: str) -> list[dict]:
    search_url = "https://html.duckduckgo.com/html/?" + urlencode({"q": query, "kl": "us-en"})
    html = fetch_text(search_url)
    results: list[dict] = []
    for raw_url, raw_title in re.findall(
        r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        html,
        re.I | re.S,
    ):
        target_url = normalize_search_target(unescape(raw_url))
        if not target_url:
            continue
        host = host_of(target_url)
        if not host or host in SEARCH_HOST_IGNORE:
            continue
        clean_title = compact_snippet(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", unescape(raw_title))).strip(), 160)
        results.append(
            {
                "engine": "duckduckgo-html",
                "query": query,
                "title": clean_title or compact_snippet(target_url, 120),
                "target_url": target_url,
                "host": host,
            }
        )
    return results


def dedupe_search_results(results: list[dict]) -> list[dict]:
    deduped: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for row in results:
        key = (row.get("target_url", ""), row.get("engine", ""))
        if not key[0] or key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def entity_tokens(entity_name: str) -> list[str]:
    tokens = [token for token in re.split(r"[^a-z0-9]+", entity_name.lower()) if len(token) > 2]
    return [token for token in tokens if token not in ENTITY_TOKEN_STOPWORDS]


def normalize_for_match(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def normalize_compact(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def result_match_profile(result: dict, entity_name: str) -> dict[str, int | bool]:
    parsed = urlparse(result["target_url"])
    host = str(result.get("host") or "").lower()
    host_without_www = host[4:] if host.startswith("www.") else host
    host_main = host_without_www.split(":", 1)[0]
    path = parsed.path.strip("/").lower()
    title = str(result.get("title") or "").lower()
    entity_phrase = normalize_for_match(entity_name)
    entity_compact = normalize_compact(entity_name)
    title_norm = normalize_for_match(title)
    path_norm = normalize_for_match(path)
    host_norm = normalize_for_match(host_main.replace(".", " "))
    host_compact = normalize_compact(host_main)
    haystack = " ".join(part for part in [title_norm, host_norm, path_norm] if part)
    tokens = entity_tokens(entity_name)
    matched_tokens = sum(1 for token in tokens if token in haystack or token in host_compact)
    exact_phrase = bool(entity_phrase) and entity_phrase in haystack
    compact_phrase = bool(entity_compact) and entity_compact in host_compact
    return {
        "token_count": len(tokens),
        "matched_tokens": matched_tokens,
        "exact_phrase": exact_phrase,
        "compact_phrase": compact_phrase,
        "has_any_match": exact_phrase or compact_phrase or matched_tokens > 0,
    }


def build_queries(parsed_chain: dict) -> list[str]:
    entity_name = parsed_chain["entity_name"]
    derived = parsed_chain["derived"]
    packet_fields = parsed_chain["packet_fields"]
    official_site = parsed_chain["official_site"] or None
    queries = generate_search_queries(entity_name, derived.get("founder_names", []), official_site)
    if entity_name:
        queries.extend([f'"{entity_name}" {tail}' for tail in GENERIC_QUERY_TAILS])
        if packet_fields.get("language", "").lower() == "en":
            queries.extend([f'"{entity_name}" {tail}' for tail in GENERIC_QUERY_TAILS_CN])
    title = packet_fields.get("title", "")
    if title:
        queries.extend([title, f'"{title}"'])
    return unique([query for query in queries if query.strip()])[:8]


def search_score(result: dict, entity_name: str) -> int:
    host = result["host"]
    title = result["title"].lower()
    query = result["query"].lower()
    parsed = urlparse(result["target_url"])
    path = parsed.path.strip("/").lower()
    profile = result_match_profile(result, entity_name)
    score = 0
    if profile["compact_phrase"]:
        score += 10
    elif profile["exact_phrase"]:
        score += 8
    if profile["matched_tokens"] >= 2:
        score += 5
    elif profile["matched_tokens"] == 1:
        score += 2
    if "official site" in query:
        score += 4
    if "company" in query or "funding" in query:
        score += 1
    if not path:
        score += 3
    elif len(path.split("/")) == 1:
        score += 1
    if not profile["has_any_match"]:
        score -= 8
    elif profile["matched_tokens"] < min(2, max(int(profile["token_count"]) - 1, 1)) and "official site" in query:
        score -= 4
    if any(word in path for word in ("careers", "contact", "privacy", "terms", "about")):
        score -= 1
    if host in PUBLISHER_IGNORE_HOSTS or any(social in host for social in SOCIAL_HOST_PATTERNS):
        score -= 10
    return score


def resolve_official_site(search_results: list[dict], entity_name: str) -> tuple[str, str, list[dict]]:
    ranked: dict[str, dict] = {}
    for result in search_results:
        target = result["target_url"]
        host = host_of(target)
        if not host or host in SEARCH_HOST_IGNORE or host in PUBLISHER_IGNORE_HOSTS:
            continue
        if any(social in host for social in SOCIAL_HOST_PATTERNS):
            continue
        root = root_url(target)
        score = search_score(result, entity_name)
        profile = result_match_profile(result, entity_name)
        bucket = ranked.setdefault(
            root,
            {
                "score": 0,
                "hits": [],
                "root_url": root,
                "best_matched_tokens": 0,
                "any_exact_phrase": False,
                "any_compact_phrase": False,
            },
        )
        bucket["score"] += score
        bucket["hits"].append(result)
        bucket["best_matched_tokens"] = max(bucket["best_matched_tokens"], int(profile["matched_tokens"]))
        bucket["any_exact_phrase"] = bool(bucket["any_exact_phrase"] or profile["exact_phrase"])
        bucket["any_compact_phrase"] = bool(bucket["any_compact_phrase"] or profile["compact_phrase"])
    if not ranked:
        return "", "low", []
    ordered = sorted(ranked.values(), key=lambda row: (-row["score"], -len(row["hits"]), len(row["root_url"])))
    best = ordered[0]
    if not best["any_exact_phrase"] and not best["any_compact_phrase"] and best["best_matched_tokens"] < 2:
        return "", "low", []
    confidence = "high" if best["score"] >= 12 or len(best["hits"]) >= 3 else "medium" if best["score"] >= 7 else "low"
    return choose_official_site([best["root_url"]], entity_name) or best["root_url"], confidence, best["hits"]


def resolve_chain(parsed_chain: dict) -> dict:
    queries = build_queries(parsed_chain)
    search_results: list[dict] = []
    for query in queries[:6]:
        try:
            search_results.extend(search_bing_jina(query))
        except Exception:
            continue
        try:
            search_results.extend(search_duckduckgo_html(query))
        except Exception:
            continue
    search_results = dedupe_search_results(search_results)[:40]

    entity_name = parsed_chain["entity_name"]
    original = parsed_chain["derived"]
    official_site, confidence, official_hits = resolve_official_site(search_results, entity_name)
    founder_names = unique(original.get("founder_names", []))
    company_social = unique(original.get("company_social", []))
    founder_social = unique(original.get("founder_social", []))
    demo = unique(original.get("demo", []))
    docs = unique(original.get("docs", []))
    founder_contacts = unique(original.get("founder_contacts", []))
    evidence = unique(original.get("evidence", []))

    if official_site:
        evidence.append(official_site)
        evidence.extend([row["target_url"] for row in official_hits[:8] if row.get("target_url")])
        try:
            site_html = fetch_text(official_site)
            site_links = extract_urls_from_html(site_html, official_site)
            founder_contacts.extend(filter_emails(extract_emails(site_html), official_site))
            founder_names.extend(extract_founder_names(site_html))
            classified_site = classify_links(site_links, official_site, entity_name, founder_names=founder_names)
            company_social.extend(classified_site["company_social"])
            founder_social.extend(classified_site["founder_social"])
            demo.extend(classified_site["demo"])
            docs.extend(classified_site["docs"])
            evidence.extend(demo)
            evidence.extend(docs)
        except Exception:
            pass

    notes = [
        "query-only resolver 当前使用多引擎轻量补查：Bing（经 r.jina.ai 包裹）+ DuckDuckGo HTML。",
        "补查规则优先寻找官网、创始人原链、产品页与 docs，而不是停留在媒体页或搜索页。",
    ]
    if official_site:
        notes.append(f"本轮已从搜索结果回链到官网，置信度为 {confidence}。")
    else:
        notes.append("本轮仍未稳定命中官网，因此只保留搜索查询链与候选结果，等待后续继续补查。")

    return {
        "entity_name": entity_name,
        "official_site": official_site,
        "official_site_confidence": confidence,
        "company_social": unique(company_social),
        "founder_social": unique(founder_social),
        "demo": unique(demo),
        "docs": unique(docs),
        "founder_contacts": filter_emails(founder_contacts, official_site) if official_site else [],
        "founder_names": unique(founder_names),
        "evidence": unique([url for url in evidence if url and not is_ignored_evidence_url(url)]),
        "queries": queries[:6],
        "search_results": search_results[:30],
        "official_hits": official_hits,
        "notes": notes,
    }


def render_resolution(resolution_id: str, parsed_chain: dict, resolved: dict, raw_path: Path) -> str:
    def bullet_list(values: list[str], fallback: str = "- none") -> str:
        if not values:
            return fallback
        return "\n".join(f"- `{compact_snippet(value, 180)}`" for value in values)

    search_hits = [
        f"{row.get('engine', 'search')} => {row['query']} => {row['title']} => {row['target_url']}"
        for row in resolved.get("official_hits", [])[:8]
    ]
    return (
        "# Asset Resolution\n\n"
        "## Header\n\n"
        f"- `resolution_id`: `{resolution_id}`\n"
        f"- `source_chain_path`: `{parsed_chain['chain_path']}`\n"
        f"- `source_packet_path`: `{parsed_chain['source_packet_path']}`\n"
        f"- `source_id`: `{parsed_chain['source_id']}`\n"
        f"- `entity_name`: `{resolved.get('entity_name', parsed_chain['entity_name'])}`\n"
        f"- `resolved_at`: `{format_dt(now_cn())}`\n"
        "- `status`: `resolved`\n\n"
        "## Resolved Chain\n\n"
        f"- `official_site`: `{resolved.get('official_site') or 'unknown'}`\n"
        f"- `official_site_confidence`: `{resolved.get('official_site_confidence', 'low')}`\n"
        "- `company_social_candidates`:\n"
        f"{bullet_list(resolved.get('company_social', []))}\n"
        "- `founder_name_candidates`:\n"
        f"{bullet_list(resolved.get('founder_names', []))}\n"
        "- `founder_contact_candidates`:\n"
        f"{bullet_list(resolved.get('founder_contacts', []))}\n"
        "- `founder_social_candidates`:\n"
        f"{bullet_list(resolved.get('founder_social', []))}\n"
        "- `demo_candidates`:\n"
        f"{bullet_list(resolved.get('demo', []))}\n"
        "- `docs_or_repo_candidates`:\n"
        f"{bullet_list(resolved.get('docs', []))}\n\n"
        "## Queries Used\n\n"
        f"{bullet_list(resolved.get('queries', []))}\n\n"
        "## Official Hit Trail\n\n"
        f"{bullet_list(search_hits)}\n\n"
        "## Evidence Links\n\n"
        f"{bullet_list(resolved.get('evidence', []))}\n\n"
        "## Notes\n\n"
        f"{bullet_list(resolved.get('notes', []), '- none')}\n\n"
        "## Raw Resolution Path\n\n"
        f"- `raw_resolution_path`: `{raw_path}`\n"
    )


def render_raw_resolution(parsed_chain: dict, resolved: dict) -> str:
    payload = {
        "chain": {
            "chain_path": parsed_chain["chain_path"],
            "source_packet_path": parsed_chain["source_packet_path"],
            "source_id": parsed_chain["source_id"],
            "entity_name": parsed_chain["entity_name"],
            "official_site": parsed_chain["official_site"],
        },
        "packet_fields": parsed_chain["packet_fields"],
        "raw_fields": parsed_chain["raw_fields"],
        "original_derived": parsed_chain["derived"],
        "resolved_result": resolved,
    }
    return "# Raw Asset Resolution\n\n" f"```json\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n```\n"


def process_chain(parsed_chain: dict, state: dict, logical_date: str, write_mode: bool) -> tuple[dict, Path | None]:
    resolved = resolve_chain(parsed_chain)
    timestamp = f"{logical_date_token(logical_date)}_{now_cn().strftime('%H%M%S')}"
    entity_slug = slugify(resolved.get("entity_name", "") or parsed_chain["entity_name"], "asset")
    resolution_id = f"resolution_{timestamp}_{entity_slug}"
    raw_path = RESOLVED_RAW_DIR / f"{timestamp}__{entity_slug}__asset-resolution-raw.md"
    resolution_path = RESOLVED_DIR / f"{timestamp}__{entity_slug}__asset-resolution.md"
    if write_mode:
        write_text(raw_path, render_raw_resolution(parsed_chain, resolved))
        write_text(resolution_path, render_resolution(resolution_id, parsed_chain, resolved, raw_path))
        key = parsed_chain["source_packet_path"] or parsed_chain["chain_path"]
        state.setdefault("chains", {})[key] = {
            "chain_path": parsed_chain["chain_path"],
            "resolution_path": str(resolution_path),
            "raw_resolution_path": str(raw_path),
            "entity_name": resolved.get("entity_name", ""),
            "official_site": resolved.get("official_site", ""),
            "resolved_at": format_dt(now_cn()),
        }
    return {
        "entity_name": resolved.get("entity_name", ""),
        "source_id": parsed_chain["source_id"],
        "official_site": resolved.get("official_site", ""),
        "resolution_path": str(resolution_path),
        "confidence": resolved.get("official_site_confidence", "low"),
    }, resolution_path if write_mode else None


def main() -> int:
    args = parse_args()
    ensure_dirs()
    run_at = now_cn()
    logical_date = args.date or run_at.strftime("%Y-%m-%d")
    resolution_state = load_json(RESOLUTION_STATE_PATH, {"chains": {}})
    selected_source_ids = args.source_ids or DEFAULT_SOURCE_IDS
    chains = latest_chain_candidates(selected_source_ids, args.limit, logical_date, args.entity_name)
    processed: list[dict] = []
    skipped: list[str] = []
    errors: list[str] = []

    for parsed_chain in chains:
        key = parsed_chain["source_packet_path"] or parsed_chain["chain_path"]
        if not needs_resolution(parsed_chain, resolution_state, args.force):
            skipped.append(key)
            continue
        try:
            result, _ = process_chain(parsed_chain, resolution_state, logical_date, args.write)
            processed.append(result)
        except Exception as exc:
            errors.append(f"{parsed_chain['chain_path']}: {exc}")

    summary = (
        "# 同行资本市场内容系统｜弱链自动补查轮\n\n"
        f"- `run_at`: `{format_dt(run_at)}`\n"
        f"- `logical_date`: `{logical_date}`\n"
        f"- `write_mode`: `{str(args.write).lower()}`\n"
        f"- `sources`: `{', '.join(selected_source_ids)}`\n"
        f"- `resolved`: `{len(processed)}`\n"
        f"- `skipped_existing`: `{len(skipped)}`\n"
        f"- `errors`: `{len(errors)}`\n\n"
        "## Resolved Chains\n\n"
        + ("\n".join(
            f"- `{row['source_id']}` → `{row['entity_name']}` → `{row['official_site'] or 'unknown'}` → `{row['confidence']}` → `{row['resolution_path']}`"
            for row in processed
        ) if processed else "- none")
        + "\n\n## Skipped Existing\n\n"
        + ("\n".join(f"- `{item}`" for item in skipped) if skipped else "- none")
        + "\n\n## Errors\n\n"
        + ("\n".join(f"- {item}" for item in errors) if errors else "- none")
        + "\n"
    )

    print(summary)
    if args.write:
        resolution_state["last_updated_at"] = format_dt(now_cn())
        save_json(RESOLUTION_STATE_PATH, resolution_state)
        summary_path = LOG_DIR / f"{logical_date_token(logical_date)}_{run_at.strftime('%H%M%S')}__market-asset-query-resolution-summary.md"
        write_text(summary_path, summary)
        print(f"\nSummary log written to: {summary_path}")
        print(f"Resolution state updated: {RESOLUTION_STATE_PATH}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
