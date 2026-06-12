"""Acquisition lane taxonomy loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.acquisition_playbook_common import SCHEMA_VERSION, basic_markdown, check, load_config, mapping, validation_payload
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import today_token, utc_now


REQUIRED_LANES = {
    "official_ai_lab", "model_release", "agent_framework", "open_source", "paper_research",
    "funding_startup", "product_launch", "builder_research", "developer_community",
    "reddit_llm_discussion", "global_ai_media", "china_ai_media", "wechat_metadata",
    "youtube_signal", "x_signal", "trend_heat_validation", "ai_infra",
    "industry_deep_research", "manual_url_backfill", "keyword_discovery",
}


def load_acquisition_lanes(repo_root: Path) -> dict[str, Any]:
    return mapping(load_config(repo_root, "acquisition_lanes.yaml"), "lanes")


def validate_acquisition_lanes(repo_root: Path) -> dict[str, Any]:
    lanes = load_acquisition_lanes(repo_root)
    checks: list[dict[str, Any]] = []
    check(checks, "schema_present", bool(lanes), "acquisition_lanes.yaml defines lanes")
    missing = sorted(REQUIRED_LANES - set(lanes))
    check(checks, "required_lanes_present", not missing, f"missing={missing}")
    for lane_id, lane in lanes.items():
        if not isinstance(lane, dict):
            check(checks, f"lane_mapping_{lane_id}", False, "lane must be mapping")
            continue
        for key in ("label", "purpose", "evidence_role", "default_priority", "source_tiers", "downstream"):
            check(checks, f"{lane_id}_{key}", key in lane, f"{lane_id}.{key} present")
        check(checks, f"{lane_id}_weak_bool", isinstance(lane.get("weak_signal"), bool), f"{lane_id}.weak_signal boolean")
    active = [lane for lane, item in lanes.items() if isinstance(item, dict) and item.get("active", True)]
    weak = [lane for lane, item in lanes.items() if isinstance(item, dict) and item.get("weak_signal") is True]
    return validation_payload(
        checks,
        {
            "schema_version": SCHEMA_VERSION,
            "generated_at": utc_now(),
            "run_date": today_token(),
            "lane_count": len(lanes),
            "active_lane_count": len(active),
            "weak_signal_lane_count": len(weak),
            "lanes": lanes,
        },
    )


def render_lane_validation(payload: dict[str, Any]) -> str:
    rows = [
        {"lane": lane, "role": item.get("evidence_role"), "weak": item.get("weak_signal"), "priority": item.get("default_priority")}
        for lane, item in (payload.get("lanes") or {}).items()
        if isinstance(item, dict)
    ]
    return basic_markdown(
        "Acquisition Lane Taxonomy Validation",
        {
            "status": payload.get("status"),
            "lane_count": payload.get("lane_count", 0),
            "active_lane_count": payload.get("active_lane_count", 0),
            "weak_signal_lane_count": payload.get("weak_signal_lane_count", 0),
        },
        rows,
        ("lane", "role", "weak", "priority"),
    )
