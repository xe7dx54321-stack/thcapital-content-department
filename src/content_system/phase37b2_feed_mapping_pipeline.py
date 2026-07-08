"""Phase37B2 all-feed RSS validation and competitor mapping pipeline."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import get_project_paths
from content_system.wechat_competitor_feed_mapping import apply_competitor_feed_mapping
from content_system.wechat_feed_discovery import discover_wechat_feed_ids, today_token


SCHEMA_VERSION = "v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def phase_status(mapping_status: str) -> str:
    if mapping_status == "PASS":
        return "SUCCESS"
    if mapping_status in {"LOCAL_MAPPING_MISSING", "NO_MATCHES", "PARTIAL"}:
        return "ACTIONABLE"
    return "SUCCESS"


def build_pipeline_payload(discovery: dict[str, Any], mapping: dict[str, Any]) -> dict[str, Any]:
    discovery_summary = discovery.get("summary") if isinstance(discovery.get("summary"), dict) else {}
    mapping_summary = mapping.get("summary") if isinstance(mapping.get("summary"), dict) else {}
    mapping_status = str(mapping.get("status") or "UNKNOWN")
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "pipeline": "phase37b2_feed_mapping",
        "status": phase_status(mapping_status),
        "steps": [
            {"step": "wechat_feed_id_discovery", "status": "SUCCESS"},
            {"step": "wechat_competitor_feed_mapping", "status": mapping_status},
        ],
        "summary": {
            "all_feed_item_count": discovery_summary.get("all_feed_item_count", 0),
            "cleaned_count": discovery_summary.get("cleaned_count", 0),
            "duplicate_count": discovery_summary.get("duplicate_count", 0),
            "intelligence_article_count": discovery_summary.get("intelligence_article_count", 0),
            "competitive_coverage_count": discovery_summary.get("competitive_coverage_count", 0),
            "differentiated_angle_count": discovery_summary.get("differentiated_angle_count", 0),
            "style_pattern_count": discovery_summary.get("style_pattern_count", 0),
            "feed_group_count": discovery_summary.get("feed_group_count", 0),
            "mapping_status": mapping_status,
            "target_competitor_count": mapping_summary.get("target_competitor_count", 0),
            "matched_competitor_count": mapping_summary.get("matched_competitor_count", 0),
            "missing_competitor_count": mapping_summary.get("missing_competitor_count", 0),
            "matched_competitors": mapping_summary.get("matched_competitors", []),
            "missing_competitors": mapping_summary.get("missing_competitors", []),
            "competitor_article_count": mapping_summary.get("competitor_article_count", 0),
            "metadata_title_issue_detected": bool(discovery_summary.get("metadata_title_issue_detected")),
            "metadata_title_example": (discovery.get("metadata_title_issue") or {}).get("example_title", ""),
        },
        "next_action": mapping.get("next_action") or "Review discovery report.",
    }


def render_pipeline_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Phase37B2 Feed Mapping Pipeline

- generated_at: `{payload.get('generated_at')}`
- status: `{payload.get('status')}`
- all_feed_item_count: `{summary.get('all_feed_item_count', 0)}`
- cleaned_count: `{summary.get('cleaned_count', 0)}`
- duplicate_count: `{summary.get('duplicate_count', 0)}`
- intelligence_article_count: `{summary.get('intelligence_article_count', 0)}`
- competitive_coverage_count: `{summary.get('competitive_coverage_count', 0)}`
- differentiated_angle_count: `{summary.get('differentiated_angle_count', 0)}`
- style_pattern_count: `{summary.get('style_pattern_count', 0)}`
- feed_group_count: `{summary.get('feed_group_count', 0)}`
- mapping_status: `{summary.get('mapping_status')}`
- matched_competitor_count: `{summary.get('matched_competitor_count', 0)}`
- missing_competitor_count: `{summary.get('missing_competitor_count', 0)}`
- metadata_title_issue_detected: `{summary.get('metadata_title_issue_detected', False)}`
- metadata_title_example: `{summary.get('metadata_title_example')}`

## Missing Competitors

{chr(10).join(f"- {item}" for item in summary.get('missing_competitors', [])) if summary.get('missing_competitors') else "- None"}

## Next Action

{payload.get('next_action') or '-'}
"""


def write_pipeline_outputs(payload: dict[str, Any], repo_root: Path) -> dict[str, Path]:
    paths = get_project_paths(repo_root)
    paths.logs_root.mkdir(parents=True, exist_ok=True)
    run_date = str(payload.get("run_date") or today_token())
    dated_json = paths.logs_root / f"{run_date}__phase37b2-feed-mapping-pipeline.json"
    dated_md = paths.logs_root / f"{run_date}__phase37b2-feed-mapping-pipeline.md"
    latest_json = paths.logs_root / "latest_phase37b2_feed_mapping_pipeline.json"
    latest_md = paths.logs_root / "latest_phase37b2_feed_mapping_pipeline.md"
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    markdown = render_pipeline_markdown(payload)
    for path in (dated_json, latest_json):
        path.write_text(text + "\n", encoding="utf-8")
    for path in (dated_md, latest_md):
        path.write_text(markdown, encoding="utf-8")
    return {"dated_json": dated_json, "dated_md": dated_md, "latest_json": latest_json, "latest_md": latest_md}


def run_phase37b2_pipeline(repo_root: Path | None = None, limit: int = 50, xml_content: str | None = None) -> tuple[dict[str, Any], dict[str, Path]]:
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    discovery, _discovery_outputs = discover_wechat_feed_ids(root, limit=limit, xml_content=xml_content)
    mapping, _mapping_outputs = apply_competitor_feed_mapping(root, discovery)
    payload = build_pipeline_payload(discovery, mapping)
    outputs = write_pipeline_outputs(payload, root)
    return payload, outputs
