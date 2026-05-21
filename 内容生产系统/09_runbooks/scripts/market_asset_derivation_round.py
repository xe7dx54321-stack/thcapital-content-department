#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

from market_business_day import day_token, path_in_business_window, text_timestamp_in_business_window
from market_topic_capture_round import (
    ROOT,
    LOG_DIR,
    STATE_DIR,
    compact_snippet,
    fetch_json,
    fetch_text,
    format_dt,
    now_cn,
    slugify,
    write_text,
)


PACKET_DIR = ROOT / "02_topic_radar" / "source_packets"
ASSET_DIR = ROOT / "02_topic_radar" / "asset_chains"
ASSET_RAW_DIR = ASSET_DIR / "raw"
CAPTURE_STATE_PATH = STATE_DIR / "market_topic_capture_state.json"
DERIVATION_STATE_PATH = STATE_DIR / "market_asset_derivation_state.json"

DEFAULT_SOURCE_IDS = [
    "trend__yc_launches_ai",
    "web__techcrunch_ai",
    "web__finsmes_ai_gnews",
]

SOCIAL_HOST_PATTERNS = (
    "x.com",
    "twitter.com",
    "linkedin.com",
    "youtube.com",
    "github.com",
    "instagram.com",
    "threads.net",
    "bsky.app",
    "mstdn.social",
    "tiktok.com",
)
SOCIAL_SHARE_PATTERNS = (
    "twitter.com/intent/",
    "x.com/intent/",
    "linkedin.com/sharearticle",
    "facebook.com/sharer",
    "reddit.com/submit",
)
PUBLISHER_IGNORE_HOSTS = {
    "techcrunch.com",
    "news.google.com",
    "www.ycombinator.com",
    "ycombinator.com",
    "trend-hunt.com",
    "producthunt.com",
    "www.producthunt.com",
    "hollywoodreporter.com",
    "www.hollywoodreporter.com",
    "strictlyvc.com",
    "www.strictlyvc.com",
    "crunchboard.com",
    "www.crunchboard.com",
    "gettyimages.com",
    "www.gettyimages.com",
    "facebook.com",
    "www.facebook.com",
    "reddit.com",
    "www.reddit.com",
}
INTERNAL_DEMO_KEYWORDS = (
    "demo",
    "book",
    "waitlist",
    "signup",
    "sign-up",
    "sign_in",
    "sign-in",
    "get-started",
    "app",
    "try",
    "trial",
    "playground",
)
INTERNAL_DOC_KEYWORDS = ("docs", "documentation", "github", "api", "developers", "developer", "blog", "youtube")
GENERIC_CATEGORY_TERMS = {
    "ai",
    "artificial intelligence",
    "in brief",
    "climate",
    "data centers",
    "startups",
    "venture",
    "technology",
    "news",
}
MEDIA_PROJECT_CUE_PATTERNS = (
    r"\braises?\b",
    r"\bsecures?\b",
    r"\bcloses\b",
    r"\blaunch(?:es|ed)?\b",
    r"\bunveil(?:s|ed)?\b",
    r"\bintroduc(?:es|ed)\b",
    r"\bdebut(?:s|ed)\b",
    r"\breleases?\b",
    r"\bships?\b",
    r"\bacquires?\b",
    r"\bbuys?\b",
    r"\bopens?\b",
    r"\bstarts?\b",
)
INFRA_IGNORE_HOSTS = {
    "google.com",
    "gstatic.com",
    "googleusercontent.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "stats.wp.com",
    "public.servenobid.com",
    "challenges.cloudflare.com",
    "ak.sail-horizon.com",
    "ssl.gstatic.com",
    "google-analytics.com",
}
STATIC_ASSET_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".css",
    ".js",
    ".woff",
    ".woff2",
    ".ico",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Derive one-hop official asset chains from market-content source packets.")
    parser.add_argument("--date", help="Logical date. Default: today in Asia/Shanghai.")
    parser.add_argument("--source-id", action="append", dest="source_ids", help="Source ids to derive from.")
    parser.add_argument("--limit", type=int, default=5, help="Max packets to process per source.")
    parser.add_argument("--write", action="store_true", help="Actually write asset-chain artifacts.")
    parser.add_argument("--force", action="store_true", help="Re-derive even if a chain already exists.")
    return parser.parse_args()


def ensure_dirs() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_RAW_DIR.mkdir(parents=True, exist_ok=True)
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


def entry_matches_logical_date(entry: dict, logical_date: str) -> bool:
    packet_path = entry.get("packet_path")
    if path_matches_logical_date(packet_path, logical_date):
        return True
    captured_at = str(entry.get("captured_at") or "").strip()
    if captured_at:
        return text_timestamp_in_business_window(captured_at, logical_date)
    if packet_path:
        return False
    return False


def unique(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        cleaned = value.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    return result


def host_of(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        return ""
    if host.startswith("www."):
        host = host[4:]
    return host


def normalized_tokens(value: str | None) -> list[str]:
    if not value:
        return []
    return [token for token in re.split(r"[^a-z0-9]+", value.lower()) if len(token) > 2]


def root_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url
    return f"{parsed.scheme}://{parsed.netloc}/"


def normalize_url(link: str, base_url: str) -> str | None:
    link = (link or "").strip()
    if not link:
        return None
    if link.startswith("#") or link.startswith("javascript:") or link.startswith("tel:"):
        return None
    if link.startswith("mailto:"):
        return link
    if link.startswith("//"):
        link = "https:" + link
    if link.startswith("/"):
        return urljoin(base_url, link)
    if re.match(r"^https?://", link, re.I):
        return link
    return urljoin(base_url, link)


def parse_markdown_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("- `") or "`:" not in line:
            continue
        match = re.match(r"- `([^`]+)`: (?:`([^`]*)`|(.*))", line)
        if not match:
            continue
        key = match.group(1).strip()
        value = (match.group(2) if match.group(2) is not None else match.group(3) or "").strip()
        fields[key] = value
    return fields


def read_packet_entry(packet_path: str, raw_path: str | None) -> tuple[dict[str, str], dict[str, str], str, str]:
    packet_text = Path(packet_path).read_text(encoding="utf-8")
    raw_text = Path(raw_path).read_text(encoding="utf-8") if raw_path and Path(raw_path).exists() else ""
    packet_fields = parse_markdown_fields(packet_text)
    raw_fields = parse_markdown_fields(raw_text)
    return packet_fields, raw_fields, packet_text, raw_text


def extract_urls_from_html(html: str, base_url: str) -> list[str]:
    links: list[str] = []
    for match in re.findall(r"""href=["']([^"']+)["']""", html, re.I):
        normalized = normalize_url(match, base_url)
        if normalized:
            links.append(normalized)
    return unique(links)


def extract_emails(text: str) -> list[str]:
    return unique(re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", text, re.I))


def extract_markdown_links(text: str, base_url: str) -> list[str]:
    links: list[str] = []
    for _, url in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text):
        normalized = normalize_url(url, base_url)
        if normalized:
            links.append(normalized)
    return unique(links)


def extract_founder_names(text: str) -> list[str]:
    patterns = [
        r"([A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2}),?\s+(?:Co-)?Founder",
        r"(?:Co-)?Founder[s]?\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2})",
        r"CEO\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2})",
    ]
    names: list[str] = []
    for pattern in patterns:
        names.extend(re.findall(pattern, text, re.I))
    return unique(names)


def extract_categories(raw_fields: dict[str, str]) -> list[str]:
    raw = raw_fields.get("categories", "")
    return unique([part.strip() for part in raw.split(",") if part.strip()])


def choose_category_entity(categories: list[str]) -> str:
    kept = [category for category in categories if category.lower() not in GENERIC_CATEGORY_TERMS]
    if not kept:
        return ""
    return " / ".join(kept[:2])


def email_matches_host(email: str, host: str) -> bool:
    if not email or "@" not in email or not host:
        return False
    email_host = email.split("@", 1)[1].lower()
    return email_host == host or email_host.endswith("." + host)


def filter_emails(emails: list[str], official_site: str | None = None) -> list[str]:
    official_host = host_of(official_site or "")
    if not official_host:
        return []
    return unique([email for email in emails if email_matches_host(email, official_host)])


def social_handle(link: str) -> str:
    parsed = urlparse(link)
    path = parsed.path.strip("/")
    if not path:
        return ""
    segments = [segment for segment in path.split("/") if segment]
    if not segments:
        return ""
    if "linkedin.com" in parsed.netloc.lower() and segments[0] in {"in", "company"} and len(segments) > 1:
        return segments[1].lower()
    return segments[0].lower()


def matches_tokens(value: str, tokens: list[str]) -> bool:
    lower = value.lower()
    return bool(tokens) and any(token in lower for token in tokens)


def is_ignored_evidence_url(link: str, article_url: str | None = None) -> bool:
    lower = link.lower()
    host = host_of(link)
    parsed = urlparse(link)
    path = parsed.path.lower()
    if host and any(host == infra or host.endswith("." + infra) for infra in INFRA_IGNORE_HOSTS):
        return True
    if any(path.endswith(ext) for ext in STATIC_ASSET_EXTENSIONS):
        return True
    if any(pattern in lower for pattern in SOCIAL_SHARE_PATTERNS):
        return True
    if article_url and link == article_url:
        return False
    if host and host in PUBLISHER_IGNORE_HOSTS and host != host_of(article_url or ""):
        return True
    if article_url and host == host_of(article_url) and "/wp-content/" in lower:
        return True
    return False


def classify_links(
    links: list[str],
    official_site: str | None,
    entity_name: str | None,
    founder_names: list[str] | None = None,
    publisher_host: str | None = None,
) -> dict[str, list[str]]:
    official_host = host_of(official_site or "")
    entity_tokens = normalized_tokens(entity_name or "")
    founder_tokens = normalized_tokens(" ".join(founder_names or []))
    publisher_tokens = normalized_tokens(publisher_host or "")
    buckets = {
        "company_social": [],
        "founder_social": [],
        "demo": [],
        "docs": [],
        "official_candidates": [],
        "other_evidence": [],
    }
    for link in links:
        parsed = urlparse(link)
        host = host_of(link)
        lower = link.lower()
        if lower.startswith("mailto:"):
            continue
        if any(pattern in lower for pattern in SOCIAL_SHARE_PATTERNS):
            continue
        if any(social in host for social in SOCIAL_HOST_PATTERNS):
            handle = social_handle(link)
            if publisher_tokens and matches_tokens(handle, publisher_tokens):
                continue
            if official_host:
                if founder_tokens and matches_tokens(handle, founder_tokens):
                    buckets["founder_social"].append(link)
                else:
                    buckets["company_social"].append(link)
            elif matches_tokens(handle, entity_tokens):
                buckets["company_social"].append(link)
            elif founder_tokens and matches_tokens(handle, founder_tokens):
                buckets["founder_social"].append(link)
            else:
                continue
            continue

        if official_host and host == official_host:
            if any(keyword in lower for keyword in INTERNAL_DEMO_KEYWORDS):
                buckets["demo"].append(link)
            elif any(keyword in lower for keyword in INTERNAL_DOC_KEYWORDS):
                buckets["docs"].append(link)
            else:
                buckets["other_evidence"].append(link)
            continue

        if host and host not in PUBLISHER_IGNORE_HOSTS and entity_tokens and any(token in host for token in entity_tokens):
            buckets["official_candidates"].append(link)
        elif host and host not in PUBLISHER_IGNORE_HOSTS:
            buckets["other_evidence"].append(link)

    return {key: unique(value) for key, value in buckets.items()}


def choose_official_site(candidates: list[str], entity_name: str | None) -> str | None:
    candidates = unique(candidates)
    if not candidates:
        return None
    entity_tokens = normalized_tokens(entity_name or "")
    ranked: list[tuple[int, str]] = []
    for candidate in candidates:
        host = host_of(candidate)
        if not host or host in PUBLISHER_IGNORE_HOSTS:
            continue
        score = 0
        if entity_tokens and any(token in host for token in entity_tokens):
            score += 5
        path = urlparse(candidate).path.strip("/")
        if not path:
            score += 3
        elif len(path.split("/")) == 1:
            score += 1
        if any(term in path.lower() for term in ("blog", "news", "press", "post", "article", "story", "stories", "index")):
            score -= 2
        ranked.append((score, candidate))
    if not ranked:
        return None
    ranked.sort(key=lambda item: (-item[0], len(item[1])))
    return root_url(ranked[0][1])


def guess_entity_name(title: str, raw_fields: dict[str, str], source_id: str) -> str:
    if raw_fields.get("company_name"):
        return raw_fields["company_name"]
    if source_id.startswith("trend__yc_launches"):
        author = raw_fields.get("company_name") or title.split(":")[0]
        return author.strip()
    patterns = [
        r"^(.*?)\s+(?:Raises|Secures|Closes|Lands|Launches|Unveils|Buys|Acquires)\b",
        r"^(.*?):",
        r"^(.*?)\s+was\b",
        r"^(.*?)\s+is\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, title, re.I)
        if match:
            return match.group(1).strip(" -—–:")
    category_entity = choose_category_entity(extract_categories(raw_fields))
    if category_entity:
        return category_entity
    return title.split("-")[0].strip()


def safe_fetch_text(url: str) -> str:
    try:
        return fetch_text(url)
    except Exception:
        return ""


def derive_from_yc(packet_fields: dict[str, str], raw_fields: dict[str, str], raw_text: str) -> dict[str, list[str] | str]:
    official_site = raw_fields.get("company_url")
    launch_url = raw_fields.get("launch_url") or packet_fields.get("canonical_url", "")
    launch_json_url = launch_url + ".json" if launch_url and not launch_url.endswith(".json") else launch_url
    body_text = raw_text
    evidence = [launch_url]
    demo = []
    docs = []
    company_social = []
    founder_social = []
    founder_contacts = extract_emails(raw_text)
    founder_names = extract_founder_names(raw_text)

    if launch_json_url:
        try:
            launch_payload = fetch_json(launch_json_url)
            body = launch_payload.get("body", "")
            body_text = body_text + "\n\n" + body
            founder_contacts.extend(extract_emails(body))
            founder_names.extend(extract_founder_names(body))
            launch_links = extract_markdown_links(body, launch_url)
            classified = classify_links(launch_links, official_site, raw_fields.get("company_name"), founder_names=founder_names)
            demo.extend(classified["demo"])
            docs.extend(classified["docs"])
            company_social.extend(classified["company_social"])
            founder_social.extend(classified["founder_social"])
            evidence.extend(classified["other_evidence"])
            evidence.extend(classified["official_candidates"])
        except Exception:
            pass

    site_links = []
    if official_site:
        evidence.append(official_site)
        site_html = safe_fetch_text(official_site)
        site_links = extract_urls_from_html(site_html, official_site)
        founder_contacts.extend(filter_emails(extract_emails(site_html), official_site))
        classified_site = classify_links(site_links, official_site, raw_fields.get("company_name"), founder_names=founder_names)
        demo.extend(classified_site["demo"])
        docs.extend(classified_site["docs"])
        company_social.extend(classified_site["company_social"])
        founder_social.extend(classified_site["founder_social"])
        evidence.extend([url for url in classified_site["other_evidence"] if not is_ignored_evidence_url(url, launch_url)])

    return {
        "entity_name": raw_fields.get("company_name") or packet_fields.get("title", ""),
        "official_site": official_site or "",
        "company_social": unique(company_social),
        "founder_social": unique(founder_social),
        "demo": unique([url for url in demo if url != official_site]),
        "docs": unique(docs),
        "founder_contacts": filter_emails(founder_contacts, official_site),
        "founder_names": unique(founder_names),
        "evidence": unique([url for url in evidence if url and not is_ignored_evidence_url(url, launch_url)]),
        "notes": [
            "YC Launches 可稳定给出 launch 页 + 官方站点，是最适合做一跳对象派生的融资 / newco 入口之一。",
            "若 launch body 里只出现 founders@ 域名邮箱，没有个人账号，这轮先保留 founder contact 和后续查询链。",
        ],
    }


def derive_from_website_seed(packet_fields: dict[str, str], raw_fields: dict[str, str], packet_text: str, raw_text: str) -> dict[str, list[str] | str]:
    title = packet_fields.get("title", "")
    source_id = packet_fields.get("source_id", "")
    entity_name = guess_entity_name(title, raw_fields, source_id)
    article_url = packet_fields.get("canonical_url", "")
    official_candidates = []
    demo = []
    docs = []
    company_social = []
    founder_social = []
    founder_contacts: list[str] = []
    founder_names = extract_founder_names(packet_text + "\n" + raw_text)
    evidence = [article_url]

    if source_id.startswith("trend__trend_hunt"):
        official_candidates.extend([raw_fields.get("website_url", ""), packet_fields.get("canonical_url", "")])
        if raw_fields.get("product_hunt_url"):
            evidence.append(raw_fields["product_hunt_url"])
    elif source_id == "trend__yc_launches_ai":
        return derive_from_yc(packet_fields, raw_fields, raw_text)
    else:
        if source_id != "web__finsmes_ai_gnews":
            article_html = safe_fetch_text(article_url)
            article_links = extract_urls_from_html(article_html, article_url)
            classified_article = classify_links(
                article_links,
                None,
                entity_name,
                founder_names=founder_names,
                publisher_host=host_of(article_url),
            )
            official_candidates.extend(classified_article["official_candidates"])
            demo.extend(classified_article["demo"])
            docs.extend(classified_article["docs"])
            company_social.extend(classified_article["company_social"])
            founder_social.extend(classified_article["founder_social"])
            evidence.extend([url for url in classified_article["other_evidence"] if not is_ignored_evidence_url(url, article_url)])

    official_site = choose_official_site([candidate for candidate in official_candidates if candidate], entity_name)
    if official_site:
        evidence.append(official_site)
        evidence.extend([url for url in official_candidates if not is_ignored_evidence_url(url, article_url)])
        site_html = safe_fetch_text(official_site)
        site_links = extract_urls_from_html(site_html, official_site)
        founder_contacts.extend(filter_emails(extract_emails(site_html), official_site))
        founder_names.extend(extract_founder_names(site_html))
        classified_site = classify_links(site_links, official_site, entity_name, founder_names=founder_names)
        demo.extend(classified_site["demo"])
        docs.extend(classified_site["docs"])
        company_social.extend(classified_site["company_social"])
        founder_social.extend(classified_site["founder_social"])
        evidence.extend([url for url in classified_site["other_evidence"] if not is_ignored_evidence_url(url, article_url)])

    notes = []
    if source_id == "web__finsmes_ai_gnews":
        notes.append("FinSMEs 当前仍是 Google News fallback；若本轮未直接抠出官网，后续应继续沿公司名做人工 / 程序化补查。")
    if source_id == "web__techcrunch_ai":
        notes.append("TechCrunch 文章里的外链常能给出官方站、X 账号或权威补证链接，适合做一跳回链。")
    if source_id.startswith("trend__trend_hunt"):
        notes.append("Trend Hunt 已直接给出官网 / Product Hunt 页，所以这条链的关键是继续从官网抠 demo / docs / social。")

    return {
        "entity_name": entity_name,
        "official_site": official_site or "",
        "company_social": unique(company_social),
        "founder_social": unique(founder_social),
        "demo": unique(demo),
        "docs": unique(docs),
        "founder_contacts": filter_emails(founder_contacts, official_site),
        "founder_names": unique(founder_names),
        "evidence": unique([url for url in evidence if url and not is_ignored_evidence_url(url, article_url)]),
        "notes": notes,
    }


def should_emit_chain(source_id: str, packet_fields: dict[str, str], derived: dict[str, list[str] | str]) -> tuple[bool, str]:
    if source_id == "trend__yc_launches_ai":
        return True, ""
    title = packet_fields.get("title", "")
    official_site = str(derived.get("official_site", "")).strip()
    company_social = derived.get("company_social", []) or []
    demo = derived.get("demo", []) or []
    docs = derived.get("docs", []) or []
    entity_name = str(derived.get("entity_name", "")).strip()
    has_object_signal = bool(official_site or company_social or demo or docs)
    if has_object_signal:
        return True, ""
    if source_id == "web__finsmes_ai_gnews" and entity_name and len(entity_name.split()) <= 6:
        return True, ""
    if source_id == "web__techcrunch_ai":
        looks_like_project_title = any(re.search(pattern, title, re.I) for pattern in MEDIA_PROJECT_CUE_PATTERNS)
        looks_like_entity = entity_name and len(entity_name.split()) <= 6
        if looks_like_project_title and looks_like_entity:
            return True, ""
    return False, "no clear company/project signal"


def generate_search_queries(entity_name: str, founder_names: list[str], official_site: str | None) -> list[str]:
    queries = []
    if entity_name:
        queries.extend(
            [
                f"{entity_name} official site",
                f"{entity_name} founder x",
                f"{entity_name} demo",
                f"{entity_name} youtube demo",
            ]
        )
    for founder_name in founder_names[:3]:
        queries.extend([f"{founder_name} x", f"{founder_name} linkedin"])
    if official_site:
        queries.append(f"site:{host_of(official_site)} founder")
    return unique(queries)


def render_asset_chain(chain_id: str, chain_key: str, packet_path: str, packet_fields: dict[str, str], derived: dict[str, list[str] | str], raw_path: Path) -> str:
    def bullet_list(values: list[str], fallback: str = "- none") -> str:
        if not values:
            return fallback
        return "\n".join(f"- `{compact_snippet(value, 180)}`" for value in values)

    entity_name = str(derived.get("entity_name", "")).strip()
    official_site = str(derived.get("official_site", "")).strip()
    founder_names = derived.get("founder_names", [])
    founder_contacts = derived.get("founder_contacts", [])
    founder_social = derived.get("founder_social", [])
    company_social = derived.get("company_social", [])
    demo = derived.get("demo", [])
    docs = derived.get("docs", [])
    evidence = derived.get("evidence", [])
    notes = derived.get("notes", [])
    queries = generate_search_queries(entity_name, founder_names, official_site)

    return (
        "# Asset Chain\n\n"
        "## Header\n\n"
        f"- `chain_id`: `{chain_id}`\n"
        f"- `chain_key`: `{chain_key}`\n"
        f"- `source_packet_path`: `{packet_path}`\n"
        f"- `source_id`: `{packet_fields.get('source_id', '')}`\n"
        f"- `entity_name`: `{entity_name}`\n"
        f"- `derived_at`: `{format_dt(now_cn())}`\n"
        "- `status`: `derived`\n\n"
        "## Official Chain\n\n"
        f"- `official_site`: `{official_site or 'unknown'}`\n"
        "- `company_social_candidates`:\n"
        f"{bullet_list(company_social)}\n"
        "- `founder_name_candidates`:\n"
        f"{bullet_list(founder_names)}\n"
        "- `founder_contact_candidates`:\n"
        f"{bullet_list(founder_contacts)}\n"
        "- `founder_social_candidates`:\n"
        f"{bullet_list(founder_social)}\n"
        "- `demo_candidates`:\n"
        f"{bullet_list(demo)}\n"
        "- `docs_or_repo_candidates`:\n"
        f"{bullet_list(docs)}\n\n"
        "## Evidence Links\n\n"
        f"{bullet_list(evidence)}\n\n"
        "## Suggested Queries\n\n"
        f"{bullet_list(queries)}\n\n"
        "## Notes\n\n"
        f"{bullet_list(notes, '- none')}\n\n"
        "## Raw Derivation Path\n\n"
        f"- `raw_derivation_path`: `{raw_path}`\n"
    )


def render_raw_derivation(packet_fields: dict[str, str], raw_fields: dict[str, str], derived: dict[str, list[str] | str]) -> str:
    return (
        "# Raw Derivation\n\n"
        "## Packet Fields\n\n"
        f"```json\n{json.dumps(packet_fields, ensure_ascii=False, indent=2)}\n```\n\n"
        "## Raw Fields\n\n"
        f"```json\n{json.dumps(raw_fields, ensure_ascii=False, indent=2)}\n```\n\n"
        "## Derived Result\n\n"
        f"```json\n{json.dumps(derived, ensure_ascii=False, indent=2)}\n```\n"
    )


def load_capture_state() -> dict:
    return load_json(CAPTURE_STATE_PATH, {"sources": {}})


def process_entry(
    source_id: str,
    item_key: str,
    entry: dict,
    derivation_state: dict,
    logical_date: str,
    write_mode: bool,
    force: bool,
) -> tuple[dict | None, dict | None]:
    packet_path = entry.get("packet_path")
    raw_path = entry.get("raw_path")
    if not packet_path or not Path(packet_path).exists():
        return None, {"error": f"missing packet path for {source_id}:{item_key}"}
    if not force and item_key in derivation_state.setdefault("sources", {}).setdefault(source_id, {}):
        return {"skipped": True, "packet_path": packet_path, "item_key": item_key}, None

    packet_fields, raw_fields, packet_text, raw_text = read_packet_entry(packet_path, raw_path)
    if source_id == "trend__yc_launches_ai":
        derived = derive_from_yc(packet_fields, raw_fields, raw_text)
    else:
        derived = derive_from_website_seed(packet_fields, raw_fields, packet_text, raw_text)
    should_emit, skip_reason = should_emit_chain(source_id, packet_fields, derived)
    if not should_emit:
        return {
            "skipped": True,
            "packet_path": packet_path,
            "item_key": item_key,
            "reason": skip_reason,
        }, None

    timestamp = f"{logical_date_token(logical_date)}_{now_cn().strftime('%H%M%S')}"
    entity_slug = slugify(str(derived.get("entity_name", "")) or item_key, item_key)
    chain_key = f"{logical_date_token(logical_date)}__{entity_slug}__asset_chain"
    chain_id = f"chain_{timestamp}_{slugify(item_key, item_key)}"
    raw_derivation_path = ASSET_RAW_DIR / f"{timestamp}__{entity_slug}__asset-chain-raw.md"
    chain_path = ASSET_DIR / f"{timestamp}__{entity_slug}__asset-chain.md"

    if write_mode:
        derivation_state.setdefault("sources", {}).setdefault(source_id, {})
        write_text(raw_derivation_path, render_raw_derivation(packet_fields, raw_fields, derived))
        write_text(chain_path, render_asset_chain(chain_id, chain_key, packet_path, packet_fields, derived, raw_derivation_path))
        derivation_state["sources"][source_id][item_key] = {
            "packet_path": packet_path,
            "chain_path": str(chain_path),
            "raw_derivation_path": str(raw_derivation_path),
            "entity_name": derived.get("entity_name", ""),
            "official_site": derived.get("official_site", ""),
            "derived_at": format_dt(now_cn()),
        }

    result = {
        "source_id": source_id,
        "item_key": item_key,
        "packet_path": packet_path,
        "chain_path": str(chain_path),
        "entity_name": derived.get("entity_name", ""),
        "official_site": derived.get("official_site", ""),
    }
    return result, None


def main() -> int:
    args = parse_args()
    ensure_dirs()
    run_at = now_cn()
    logical_date = args.date or run_at.strftime("%Y-%m-%d")
    capture_state = load_capture_state()
    derivation_state = load_json(DERIVATION_STATE_PATH, {"sources": {}})
    derivation_state.setdefault("sources", {})

    selected_source_ids = args.source_ids or DEFAULT_SOURCE_IDS
    processed: list[dict] = []
    skipped: list[dict] = []
    errors: list[str] = []

    for source_id in selected_source_ids:
        entries = capture_state.get("sources", {}).get(source_id, {})
        if not entries:
            continue
        sorted_entries = sorted(
            ((item_key, entry) for item_key, entry in entries.items() if entry_matches_logical_date(entry, logical_date)),
            key=lambda kv: kv[1].get("captured_at", ""),
            reverse=True,
        )[: args.limit]
        for item_key, entry in sorted_entries:
            result, error = process_entry(source_id, item_key, entry, derivation_state, logical_date, args.write, args.force)
            if error:
                errors.append(error["error"])
                continue
            if result and result.get("skipped"):
                skipped.append(result)
            elif result:
                processed.append(result)

    summary = (
        "# 同行资本市场内容系统｜对象一跳派生轮\n\n"
        f"- `run_at`: `{format_dt(run_at)}`\n"
        f"- `logical_date`: `{logical_date}`\n"
        f"- `write_mode`: `{str(args.write).lower()}`\n"
        f"- `sources`: `{', '.join(selected_source_ids)}`\n"
        f"- `derived`: `{len(processed)}`\n"
        f"- `skipped_existing`: `{len(skipped)}`\n"
        f"- `errors`: `{len(errors)}`\n\n"
        "## Derived Chains\n\n"
        + ("\n".join(
            f"- `{row['source_id']}` → `{row['entity_name']}` → `{row['chain_path']}`" for row in processed
        ) if processed else "- none")
        + "\n\n## Skipped Existing\n\n"
        + ("\n".join(
            f"- `{row['packet_path']}`" + (f" (`{row['reason']}`)" if row.get("reason") else "") for row in skipped
        ) if skipped else "- none")
        + "\n\n## Errors\n\n"
        + ("\n".join(f"- {error}" for error in errors) if errors else "- none")
        + "\n"
    )

    print(summary)
    if args.write:
        derivation_state["last_updated_at"] = format_dt(now_cn())
        save_json(DERIVATION_STATE_PATH, derivation_state)
        summary_path = LOG_DIR / f"{logical_date_token(logical_date)}_{run_at.strftime('%H%M%S')}__market-asset-derivation-summary.md"
        write_text(summary_path, summary)
        print(f"\nSummary log written to: {summary_path}")
        print(f"Derivation state updated: {DERIVATION_STATE_PATH}")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
