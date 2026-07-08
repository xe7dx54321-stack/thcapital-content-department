"""Apply local feed id to competitor mapping for WeChat RSS discovery."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from content_system.paths import get_project_paths
from content_system.wechat_feed_discovery import DEFAULT_TARGET_COMPETITORS, today_token


SCHEMA_VERSION = "v1"
LOCAL_MAPPING_PATH = Path("config/wechat_competitor_feed_map.local.yaml")
EXAMPLE_MAPPING_PATH = Path("config/wechat_competitor_feed_map.example.yaml")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_competitors() -> list[dict[str, Any]]:
    return [{"name": name, "feed_ids": [], "aliases": [name]} for name in DEFAULT_TARGET_COMPETITORS]


def load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
    return loaded if isinstance(loaded, dict) else {}


def load_competitor_mapping(repo_root: Path) -> tuple[str, list[dict[str, Any]], Path]:
    local_path = repo_root / LOCAL_MAPPING_PATH
    example_path = repo_root / EXAMPLE_MAPPING_PATH
    if local_path.exists():
        payload = load_yaml(local_path)
        competitors = payload.get("competitors") if isinstance(payload.get("competitors"), list) else []
        return "LOCAL_MAPPING_LOADED", [normalize_competitor(item) for item in competitors], local_path
    if example_path.exists():
        payload = load_yaml(example_path)
        competitors = payload.get("competitors") if isinstance(payload.get("competitors"), list) else default_competitors()
        return "LOCAL_MAPPING_MISSING", [normalize_competitor(item) for item in competitors], local_path
    return "LOCAL_MAPPING_MISSING", default_competitors(), local_path


def normalize_competitor(item: Any) -> dict[str, Any]:
    data = item if isinstance(item, dict) else {}
    name = str(data.get("name") or "").strip()
    aliases = [str(value).strip() for value in data.get("aliases", []) if str(value).strip()] if isinstance(data.get("aliases"), list) else []
    feed_ids = [str(value).strip() for value in data.get("feed_ids", []) if str(value).strip()] if isinstance(data.get("feed_ids"), list) else []
    if name and name not in aliases:
        aliases.insert(0, name)
    return {"name": name, "feed_ids": feed_ids, "aliases": aliases}


def match_item(item: dict[str, Any], competitors: list[dict[str, Any]]) -> tuple[str, str]:
    feed_id = str(item.get("possible_feed_id") or "").strip()
    text = "\n".join(
        [
            str(item.get("title") or ""),
            str(item.get("description_excerpt") or ""),
            str(item.get("content_excerpt") or ""),
        ]
    )
    for competitor in competitors:
        name = str(competitor.get("name") or "")
        if feed_id and feed_id in set(competitor.get("feed_ids") or []):
            return name, "feed_id"
    for competitor in competitors:
        name = str(competitor.get("name") or "")
        for alias in competitor.get("aliases") or []:
            if alias and alias in text:
                return name, "alias"
    for competitor in competitors:
        name = str(competitor.get("name") or "")
        if name and name in str(item.get("title") or ""):
            return name, "title_hint"
    return "", "none"


def apply_mapping(discovery_payload: dict[str, Any], competitors: list[dict[str, Any]], mapping_status: str) -> dict[str, Any]:
    items = discovery_payload.get("items") if isinstance(discovery_payload.get("items"), list) else []
    enriched: list[dict[str, Any]] = []
    articles_by_competitor = {str(item.get("name")): 0 for item in competitors if item.get("name")}
    matched_names: set[str] = set()
    for item in items:
        name, reason = match_item(item, competitors)
        competitor_matched = bool(name)
        if competitor_matched:
            matched_names.add(name)
            articles_by_competitor[name] = articles_by_competitor.get(name, 0) + 1
        enriched.append(
            {
                "title": item.get("title") or "",
                "link": item.get("link") or "",
                "id": item.get("id") or "",
                "group_key": item.get("group_key") or "",
                "possible_feed_id": item.get("possible_feed_id") or "",
                "competitor_name": name,
                "competitor_matched": competitor_matched,
                "match_reason": reason,
            }
        )
    target_names = [str(item.get("name")) for item in competitors if item.get("name")]
    missing = [name for name in target_names if name not in matched_names]
    status = mapping_status
    if mapping_status == "LOCAL_MAPPING_LOADED":
        status = "PASS" if not missing else ("PARTIAL" if matched_names else "NO_MATCHES")
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": status,
        "mapping_status": mapping_status,
        "articles": enriched,
        "summary": {
            "target_competitor_count": len(target_names),
            "matched_competitor_count": len(matched_names),
            "missing_competitor_count": len(missing),
            "matched_competitors": sorted(matched_names),
            "missing_competitors": missing,
            "article_count": len(items),
            "competitor_article_count": sum(1 for item in enriched if item.get("competitor_matched")),
            "articles_by_competitor": articles_by_competitor,
        },
        "next_action": next_action(status),
        "safety": {
            "local_mapping_only": True,
            "auth_api_called": False,
            "external_fulltext_fetch": False,
            "full_text_persisted": False,
        },
    }


def next_action(status: str) -> str:
    if status == "LOCAL_MAPPING_MISSING":
        return "Fill config/wechat_competitor_feed_map.local.yaml with feed_ids from latest_wechat_feed_id_discovery.md, then rerun make wechat-competitor-feed-mapping."
    if status == "NO_MATCHES":
        return "Review feed_id discovery groups and add the correct feed_ids to the local mapping file."
    if status == "PARTIAL":
        return "Complete missing competitor feed_ids in the local mapping file."
    return "Competitor feed mapping is available for local observation."


def render_mapping_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    lines = [
        "# WeChat Competitor Feed Mapping",
        "",
        f"- generated_at: `{payload.get('generated_at')}`",
        f"- status: `{payload.get('status')}`",
        f"- target_competitor_count: `{summary.get('target_competitor_count', 0)}`",
        f"- matched_competitor_count: `{summary.get('matched_competitor_count', 0)}`",
        f"- missing_competitor_count: `{summary.get('missing_competitor_count', 0)}`",
        f"- matched_competitors: `{', '.join(summary.get('matched_competitors') or []) or '-'}`",
        f"- missing_competitors: `{', '.join(summary.get('missing_competitors') or []) or '-'}`",
        f"- competitor_article_count: `{summary.get('competitor_article_count', 0)}`",
        "",
        "## Articles By Competitor",
        "",
    ]
    articles_by = summary.get("articles_by_competitor") if isinstance(summary.get("articles_by_competitor"), dict) else {}
    if not articles_by:
        lines.append("- No competitors configured.")
    for name, count in articles_by.items():
        lines.append(f"- {name}: `{count}`")
    lines.extend(["", "## Next Action", "", str(payload.get("next_action") or "-")])
    return "\n".join(lines) + "\n"


def write_mapping_outputs(payload: dict[str, Any], repo_root: Path) -> dict[str, Path]:
    paths = get_project_paths(repo_root)
    paths.logs_root.mkdir(parents=True, exist_ok=True)
    run_date = str(payload.get("run_date") or today_token())
    dated_json = paths.logs_root / f"{run_date}__wechat-competitor-feed-mapping.json"
    dated_md = paths.logs_root / f"{run_date}__wechat-competitor-feed-mapping.md"
    latest_json = paths.logs_root / "latest_wechat_competitor_feed_mapping.json"
    latest_md = paths.logs_root / "latest_wechat_competitor_feed_mapping.md"
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    markdown = render_mapping_markdown(payload)
    for path in (dated_json, latest_json):
        path.write_text(text + "\n", encoding="utf-8")
    for path in (dated_md, latest_md):
        path.write_text(markdown, encoding="utf-8")
    return {"dated_json": dated_json, "dated_md": dated_md, "latest_json": latest_json, "latest_md": latest_md}


def apply_competitor_feed_mapping(repo_root: Path | None = None, discovery_payload: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Path]]:
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    if discovery_payload is None:
        latest_discovery = get_project_paths(root).logs_root / "latest_wechat_feed_id_discovery.json"
        discovery_payload = json.loads(latest_discovery.read_text(encoding="utf-8")) if latest_discovery.exists() else {"items": []}
    mapping_status, competitors, _mapping_path = load_competitor_mapping(root)
    payload = apply_mapping(discovery_payload, competitors, mapping_status)
    return payload, write_mapping_outputs(payload, root)
