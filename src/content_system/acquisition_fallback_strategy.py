"""Fallback, backfill, and confirmation strategy validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.acquisition_lane_registry import load_acquisition_lanes
from content_system.acquisition_playbook_common import basic_markdown, check, load_config, mapping, validation_payload


def load_fallback_strategies(repo_root: Path) -> dict[str, Any]:
    return mapping(load_config(repo_root, "acquisition_fallback_strategies.yaml"), "strategies")


def summarize_fallback_strategies(strategies: dict[str, Any]) -> dict[str, int]:
    return {
        "strategy_count": len(strategies),
        "primary_source_required": sum(1 for item in strategies.values() if isinstance(item, dict) and item.get("status") == "PRIMARY_SOURCE_REQUIRED"),
        "second_source_required": sum(1 for item in strategies.values() if isinstance(item, dict) and item.get("status") == "SECOND_SOURCE_REQUIRED"),
        "manual_review_required": sum(1 for item in strategies.values() if isinstance(item, dict) and item.get("status") == "MANUAL_REVIEW_REQUIRED"),
    }


def validate_fallback_strategies(repo_root: Path) -> dict[str, Any]:
    payload = load_config(repo_root, "acquisition_fallback_strategies.yaml")
    strategies = mapping(payload, "strategies")
    statuses = set(payload.get("statuses") if isinstance(payload.get("statuses"), list) else [])
    lanes = load_acquisition_lanes(repo_root)
    checks: list[dict[str, Any]] = []
    check(checks, "statuses_present", bool(statuses), "fallback statuses present")
    missing = sorted(set(lanes) - set(strategies))
    check(checks, "all_lanes_have_fallback", not missing, f"missing={missing}")
    for lane, item in strategies.items():
        if not isinstance(item, dict):
            check(checks, f"{lane}_mapping", False, "strategy must be mapping")
            continue
        check(checks, f"{lane}_status_allowed", item.get("status") in statuses, f"status={item.get('status')}")
        check(checks, f"{lane}_actions", isinstance(item.get("actions"), list) and bool(item.get("actions")), "actions present")
        check(checks, f"{lane}_confirmation_bool", isinstance(item.get("confirmation_required"), bool), "confirmation_required boolean")
        if lane in {"reddit_llm_discussion", "youtube_signal", "x_signal", "trend_heat_validation", "wechat_metadata"}:
            check(checks, f"{lane}_not_hard_evidence", item.get("hard_evidence_allowed", False) is False, "weak/manual lane not hard evidence")
        if lane == "wechat_metadata":
            check(checks, f"{lane}_no_full_text", item.get("full_text_fetch", False) is False, "wechat full_text_fetch false")
    return validation_payload(checks, summarize_fallback_strategies(strategies) | {"strategies": strategies})


def render_fallback_strategy_validation(payload: dict[str, Any]) -> str:
    return basic_markdown(
        "Acquisition Fallback Strategy Validation",
        {
            "status": payload.get("status"),
            "strategy_count": payload.get("strategy_count", 0),
            "primary_source_required": payload.get("primary_source_required", 0),
            "second_source_required": payload.get("second_source_required", 0),
            "manual_review_required": payload.get("manual_review_required", 0),
        },
    )
