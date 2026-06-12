"""Downstream routing playbook validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.acquisition_lane_registry import load_acquisition_lanes
from content_system.acquisition_playbook_common import WEAK_LANES, basic_markdown, check, load_config, mapping, validation_payload


def load_downstream_routes(repo_root: Path) -> dict[str, Any]:
    return mapping(load_config(repo_root, "acquisition_downstream_routing.yaml"), "routes")


def summarize_downstream_routes(routes: dict[str, Any]) -> dict[str, int]:
    topic = 0
    backfill = 0
    watch = 0
    for route in routes.values():
        if not isinstance(route, dict):
            continue
        text = str(route)
        topic += text.count("topic_scoring")
        backfill += text.count("evidence_backfill")
        watch += text.count("watch")
    return {"route_count": len(routes), "topic_scoring_routes": topic, "evidence_backfill_routes": backfill, "watch_routes": watch}


def validate_downstream_routes(repo_root: Path) -> dict[str, Any]:
    payload = load_config(repo_root, "acquisition_downstream_routing.yaml")
    routes = mapping(payload, "routes")
    allowed = set(payload.get("allowed_outputs") if isinstance(payload.get("allowed_outputs"), list) else [])
    lanes = load_acquisition_lanes(repo_root)
    checks: list[dict[str, Any]] = []
    check(checks, "allowed_outputs_present", bool(allowed), "allowed outputs present")
    missing = sorted(set(lanes) - set(routes))
    check(checks, "all_lanes_have_downstream_route", not missing, f"missing={missing}")
    for lane, route in routes.items():
        if not isinstance(route, dict):
            check(checks, f"{lane}_mapping", False, "route must be mapping")
            continue
        outputs = route.get("outputs") if isinstance(route.get("outputs"), list) else []
        unknown_outputs = [item for item in outputs if item not in allowed]
        check(checks, f"{lane}_outputs_allowed", not unknown_outputs, f"unknown={unknown_outputs}")
        check(checks, f"{lane}_outputs_present", bool(outputs), "outputs present")
        text = str(route)
        if lane in WEAK_LANES:
            check(checks, f"{lane}_weak_no_brief", "brief_candidate" not in text, "weak signal not direct brief")
        if lane in {"wechat_metadata", "manual_url_backfill"}:
            route_str = str(route.get("outputs", []))
            check(checks, f"{lane}_manual_no_direct_topic_output", "topic_scoring" not in route_str, "manual outputs not direct topic_scoring")
    guards = payload.get("guards") if isinstance(payload.get("guards"), dict) else {}
    check(checks, "weak_signal_no_hard_evidence_guard", guards.get("weak_signal_no_hard_evidence") is True, "weak guard true")
    check(checks, "no_auto_publish_route_guard", guards.get("no_auto_publish_route") is True, "no auto publish route")
    return validation_payload(checks, summarize_downstream_routes(routes) | {"routes": routes})


def render_downstream_route_validation(payload: dict[str, Any]) -> str:
    return basic_markdown(
        "Acquisition Downstream Route Validation",
        {
            "status": payload.get("status"),
            "route_count": payload.get("route_count", 0),
            "topic_scoring_routes": payload.get("topic_scoring_routes", 0),
            "evidence_backfill_routes": payload.get("evidence_backfill_routes", 0),
            "watch_routes": payload.get("watch_routes", 0),
        },
    )
