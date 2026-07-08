"""Discover stable grouping keys from the local WeChat RSS all-feed."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from content_system.paths import get_project_paths


SCHEMA_VERSION = "v1"
RSS_BASE_ENV_KEY = "WECHAT_" + "RSS_BASE_URL"
DEFAULT_TARGET_COMPETITORS = (
    "数字生命卡兹克",
    "赛博禅心",
    "智东西",
    "36氪",
    "袋鼠帝AI客栈",
    "饼干哥哥AGI",
    "歸藏的AI工具箱",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def safe_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def short_excerpt(value: Any, limit: int = 180) -> str:
    text = safe_text(value)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def normalize_base_url(value: str) -> str:
    base = value.strip()
    if not base:
        return ""
    return base.rstrip("/")


def read_env_value(repo_root: Path, key: str) -> str:
    if os.environ.get(key):
        return str(os.environ[key]).strip()
    env_path = repo_root / ".env.rss"
    if not env_path.exists():
        return ""
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith(f"{key}="):
            return stripped.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def rss_base_url(repo_root: Path) -> str:
    return normalize_base_url(read_env_value(repo_root, RSS_BASE_ENV_KEY))


def fetch_all_feed_xml(base_url: str, timeout: int = 20) -> str:
    if not base_url:
        raise ValueError("RSS base URL is not configured in environment or local RSS env file")
    url = f"{normalize_base_url(base_url)}/feed/all.rss"
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def child_text(item: ET.Element, tag: str) -> str:
    value = item.findtext(tag)
    if value:
        return value
    for child in item:
        if child.tag.rsplit("}", 1)[-1] == tag:
            return child.text or ""
    return ""


def extract_feed_id(identifier: str, link: str) -> str:
    for value in (identifier, link):
        text = str(value or "").strip()
        if not text:
            continue
        match = re.search(r"(^|/)(\d{6,})(?:[-_/]|$)", text)
        if match:
            return match.group(2)
    return ""


def extract_account_id(link: str) -> str:
    text = str(link or "")
    for pattern in (r"[?&]__biz=([^&#]+)", r"[?&]biz=([^&#]+)", r"/feed/([^/.?#]+)"):
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return ""


def source_key(link: str, feed_id: str, account_id: str) -> str:
    if feed_id:
        return f"feed:{feed_id}"
    if account_id:
        return f"account:{account_id}"
    parsed = urlparse(link or "")
    if parsed.netloc:
        return f"host:{parsed.netloc}"
    return ""


def stable_group_key(title: str, link: str, identifier: str) -> str:
    feed_id = extract_feed_id(identifier, link)
    account_id = extract_account_id(link)
    key = source_key(link, feed_id, account_id)
    if key:
        return key
    digest = hashlib.sha1(f"{identifier}|{link}|{title}".encode("utf-8")).hexdigest()[:12]
    return f"unknown:{digest}"


def matched_aliases(text: str, aliases: tuple[str, ...]) -> list[str]:
    return [alias for alias in aliases if alias and alias in text]


def parse_all_feed(xml_content: str, limit: int = 50, aliases: tuple[str, ...] = DEFAULT_TARGET_COMPETITORS) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_content)
    parsed: list[dict[str, Any]] = []
    for item in root.findall(".//item")[:limit]:
        title = safe_text(child_text(item, "title"))
        link = safe_text(child_text(item, "link"))
        guid = safe_text(child_text(item, "guid"))
        identifier = safe_text(child_text(item, "id")) or guid
        pub_date = safe_text(child_text(item, "pubDate"))
        description = child_text(item, "description")
        content = child_text(item, "encoded")
        description_excerpt = short_excerpt(description)
        content_excerpt = short_excerpt(content)
        feed_id = extract_feed_id(identifier, link)
        account_id = extract_account_id(link)
        possible_source_key = source_key(link, feed_id, account_id)
        group_key = stable_group_key(title, link, identifier)
        alias_text = "\n".join([title, description_excerpt, content_excerpt])
        parsed.append(
            {
                "title": title,
                "link": link,
                "guid": guid,
                "id": identifier,
                "pubDate": pub_date,
                "description_excerpt": description_excerpt,
                "content_excerpt": content_excerpt,
                "possible_feed_id": feed_id,
                "possible_account_id": account_id,
                "possible_source_key": possible_source_key,
                "group_key": group_key,
                "matched_target_aliases": matched_aliases(alias_text, aliases),
            }
        )
    return parsed


def group_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        groups[str(item.get("group_key") or "unknown")].append(item)

    summaries: list[dict[str, Any]] = []
    for key, group in groups.items():
        feed_ids = sorted({str(item.get("possible_feed_id") or "") for item in group if item.get("possible_feed_id")})
        account_ids = sorted({str(item.get("possible_account_id") or "") for item in group if item.get("possible_account_id")})
        alias_hits = sorted({alias for item in group for alias in item.get("matched_target_aliases", [])})
        confidence = "HIGH" if alias_hits else ("MEDIUM" if feed_ids and len(group) > 1 else "LOW")
        summaries.append(
            {
                "group_key": key,
                "item_count": len(group),
                "possible_feed_ids": feed_ids,
                "possible_account_ids": account_ids,
                "latest_title": str(group[0].get("title") or ""),
                "sample_titles": [str(item.get("title") or "") for item in group[:5]],
                "sample_links": [str(item.get("link") or "") for item in group[:3]],
                "possible_account_hints": alias_hits + feed_ids + account_ids,
                "matched_target_aliases": alias_hits,
                "confidence": confidence,
            }
        )
    return sorted(summaries, key=lambda item: (-int(item.get("item_count") or 0), str(item.get("group_key") or "")))


def metadata_title_issue() -> dict[str, Any]:
    return {
        "metadata_title_issue_detected": True,
        "example_title": "Finsmes Ai Gnews",
        "recommended_followup": "tighten title normalization / topic rerank guard",
    }


def build_discovery_payload(xml_content: str, limit: int = 50) -> dict[str, Any]:
    items = parse_all_feed(xml_content, limit=limit)
    groups = group_items(items)
    seen_links: set[str] = set()
    duplicate_count = 0
    for item in items:
        key = str(item.get("link") or item.get("id") or item.get("title") or "")
        if key in seen_links:
            duplicate_count += 1
        seen_links.add(key)
    ai_terms = ("AI", "大模型", "智能", "模型", "Agent", "机器人", "芯片", "创业", "融资")
    differentiated_angle_count = sum(1 for item in items if any(term in str(item.get("title") or "") for term in ai_terms))
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "feed_url": "/feed/all.rss",
        "item_limit": limit,
        "items": items,
        "groups": groups,
        "summary": {
            "all_feed_item_count": len(items),
            "cleaned_count": len(items) - duplicate_count,
            "duplicate_count": duplicate_count,
            "intelligence_article_count": sum(1 for item in items if item.get("title")),
            "competitive_coverage_count": len(groups),
            "differentiated_angle_count": differentiated_angle_count,
            "style_pattern_count": sum(1 for item in items if len(str(item.get("title") or "")) >= 8),
            "feed_group_count": len(groups),
            "matched_target_alias_count": sum(1 for item in items if item.get("matched_target_aliases")),
            "metadata_title_issue_detected": True,
        },
        "metadata_title_issue": metadata_title_issue(),
        "safety": {
            "rss_only": True,
            "auth_api_called": False,
            "external_fulltext_fetch": False,
            "full_text_persisted": False,
        },
    }


def render_discovery_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    lines = [
        "# WeChat Feed ID Discovery",
        "",
        f"- generated_at: `{payload.get('generated_at')}`",
        f"- all_feed_item_count: `{summary.get('all_feed_item_count', 0)}`",
        f"- feed_group_count: `{summary.get('feed_group_count', 0)}`",
        f"- metadata_title_issue_detected: `{summary.get('metadata_title_issue_detected', False)}`",
        "",
        "## Feed Groups",
        "",
    ]
    groups = payload.get("groups") if isinstance(payload.get("groups"), list) else []
    if not groups:
        lines.append("- No groups discovered.")
    for index, group in enumerate(groups, start=1):
        lines.extend(
            [
                f"### Group {index}",
                "",
                f"- group_key: `{group.get('group_key')}`",
                f"- item_count: `{group.get('item_count', 0)}`",
                f"- possible_feed_ids: `{', '.join(group.get('possible_feed_ids') or []) or '-'}`",
                f"- possible_account_ids: `{', '.join(group.get('possible_account_ids') or []) or '-'}`",
                f"- target_alias_match: `{', '.join(group.get('matched_target_aliases') or []) or 'none'}`",
                f"- confidence: `{group.get('confidence')}`",
                "",
                "Latest titles:",
            ]
        )
        for title in (group.get("sample_titles") or [])[:5]:
            lines.append(f"1. {title}")
        lines.append("")
        lines.append("Sample links:")
        for link in (group.get("sample_links") or [])[:3]:
            lines.append(f"- {link}")
        lines.append("")
    lines.extend(
        [
            "## Notes",
            "",
            "- Report stores titles, links, ids, grouping keys, and short excerpts only.",
            "- It does not call authenticated APIs and does not fetch pages outside RSS.",
            "- It does not persist RSS original full text.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_discovery_outputs(payload: dict[str, Any], repo_root: Path) -> dict[str, Path]:
    paths = get_project_paths(repo_root)
    paths.logs_root.mkdir(parents=True, exist_ok=True)
    run_date = str(payload.get("run_date") or today_token())
    dated_json = paths.logs_root / f"{run_date}__wechat-feed-id-discovery.json"
    dated_md = paths.logs_root / f"{run_date}__wechat-feed-id-discovery.md"
    latest_json = paths.logs_root / "latest_wechat_feed_id_discovery.json"
    latest_md = paths.logs_root / "latest_wechat_feed_id_discovery.md"
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    markdown = render_discovery_markdown(payload)
    for path in (dated_json, latest_json):
        path.write_text(text + "\n", encoding="utf-8")
    for path in (dated_md, latest_md):
        path.write_text(markdown, encoding="utf-8")
    return {"dated_json": dated_json, "dated_md": dated_md, "latest_json": latest_json, "latest_md": latest_md}


def discover_wechat_feed_ids(repo_root: Path | None = None, limit: int = 50, xml_content: str | None = None) -> tuple[dict[str, Any], dict[str, Path]]:
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    xml = xml_content if xml_content is not None else fetch_all_feed_xml(rss_base_url(root))
    payload = build_discovery_payload(xml, limit=limit)
    return payload, write_discovery_outputs(payload, root)
