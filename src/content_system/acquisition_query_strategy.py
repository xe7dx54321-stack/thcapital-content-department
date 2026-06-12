"""Query, keyword, and lookback strategy validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.acquisition_lane_registry import load_acquisition_lanes
from content_system.acquisition_playbook_common import basic_markdown, check, load_config, mapping, validation_payload


def load_query_strategies(repo_root: Path) -> dict[str, Any]:
    return mapping(load_config(repo_root, "acquisition_query_strategies.yaml"), "strategies")


def summarize_query_strategies(strategies: dict[str, Any]) -> dict[str, int]:
    keyword_count = 0
    expansion = 0
    for item in strategies.values():
        if not isinstance(item, dict):
            continue
        keywords = item.get("keywords") if isinstance(item.get("keywords"), dict) else {}
        for values in keywords.values():
            if isinstance(values, list):
                keyword_count += len(values)
        if isinstance(item.get("expansion_trigger"), dict):
            expansion += 1
    return {"strategy_count": len(strategies), "keyword_count": keyword_count, "expansion_trigger_count": expansion}


def validate_query_strategies(repo_root: Path) -> dict[str, Any]:
    strategies = load_query_strategies(repo_root)
    lanes = load_acquisition_lanes(repo_root)
    checks: list[dict[str, Any]] = []
    missing = sorted(set(lanes) - set(strategies))
    check(checks, "all_lanes_have_query_strategy", not missing, f"missing={missing}")
    for lane, item in strategies.items():
        if not isinstance(item, dict):
            check(checks, f"{lane}_mapping", False, "strategy must be mapping")
            continue
        keywords = item.get("keywords") if isinstance(item.get("keywords"), dict) else {}
        check(checks, f"{lane}_primary_keywords", bool(keywords.get("primary")), "primary keywords present")
        check(checks, f"{lane}_lookback", int(item.get("lookback_hours") or 0) > 0, "lookback positive")
        check(checks, f"{lane}_max_items", int(item.get("max_items_per_source") or 0) > 0, "max items positive")
        check(checks, f"{lane}_sort", bool(item.get("sort") or item.get("rank")), "sort or rank present")
        check(checks, f"{lane}_zero_result_fallback", bool(item.get("zero_result_fallback")), "zero result fallback present")
        check(checks, f"{lane}_expansion_trigger", isinstance(item.get("expansion_trigger"), dict), "expansion trigger present")
    return validation_payload(checks, summarize_query_strategies(strategies) | {"strategies": strategies})


def render_query_strategy_validation(payload: dict[str, Any]) -> str:
    return basic_markdown(
        "Acquisition Query Strategy Validation",
        {
            "status": payload.get("status"),
            "strategy_count": payload.get("strategy_count", 0),
            "keyword_count": payload.get("keyword_count", 0),
            "expansion_trigger_count": payload.get("expansion_trigger_count", 0),
        },
    )
