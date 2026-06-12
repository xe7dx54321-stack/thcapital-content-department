"""Source fetch method playbook loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.acquisition_lane_registry import load_acquisition_lanes
from content_system.acquisition_playbook_common import (
    ALLOWED_FETCH_METHODS,
    FORBIDDEN_FETCH_METHODS,
    basic_markdown,
    check,
    load_config,
    mapping,
    validation_payload,
)


def load_source_playbooks(repo_root: Path) -> dict[str, Any]:
    return mapping(load_config(repo_root, "acquisition_source_playbooks.yaml"), "sources")


def summarize_source_playbooks(sources: dict[str, Any]) -> dict[str, int]:
    manual = 0
    disabled = 0
    metadata = 0
    for source in sources.values():
        if not isinstance(source, dict):
            continue
        method = str(source.get("fetch_method") or "")
        role = str(source.get("evidence_role") or "")
        if method == "disabled":
            disabled += 1
        elif method in {"manual_only", "manual_url"} or role == "manual_only":
            manual += 1
        else:
            metadata += 1
    return {"source_count": len(sources), "metadata_sources": metadata, "manual_only_sources": manual, "disabled_sources": disabled}


def validate_source_playbooks(repo_root: Path) -> dict[str, Any]:
    sources = load_source_playbooks(repo_root)
    lanes = load_acquisition_lanes(repo_root)
    checks: list[dict[str, Any]] = []
    primary_lane_by_source: dict[str, str] = {}
    for source_id, source in sources.items():
        if not isinstance(source, dict):
            check(checks, f"{source_id}_mapping", False, "source must be mapping")
            continue
        lane = str(source.get("lane") or "")
        primary_lane_by_source[str(source_id)] = lane
        check(checks, f"{source_id}_lane_exists", lane in lanes, f"lane={lane}")
        method = str(source.get("fetch_method") or "")
        check(checks, f"{source_id}_fetch_method_allowed", method in ALLOWED_FETCH_METHODS, f"method={method}")
        check(checks, f"{source_id}_no_forbidden_fetch", method not in FORBIDDEN_FETCH_METHODS, f"method={method}")
        check(checks, f"{source_id}_metadata_only", source.get("metadata_only", True) is True, "metadata_only true")
        check(checks, f"{source_id}_no_full_text", source.get("full_text_allowed", False) is False, "full_text_allowed false")
        check(checks, f"{source_id}_no_login", source.get("requires_login", False) is False, "requires_login false")
        check(checks, f"{source_id}_no_api_key", source.get("requires_api_key", False) is False, "requires_api_key false")
        check(checks, f"{source_id}_lookback", int(source.get("lookback_hours") or 0) > 0, "lookback_hours positive")
        check(checks, f"{source_id}_max_items", int(source.get("max_items") or 0) > 0, "max_items positive")
        if source.get("evidence_role") in {"weak_signal", "heat_validation"}:
            check(checks, f"{source_id}_weak_not_hard", source.get("hard_evidence_allowed", False) is False, "weak signal not hard evidence")
    # YAML mapping already enforces one primary source entry per source_id; this check documents it.
    check(checks, "source_primary_lane_unique", len(primary_lane_by_source) == len(sources), "each source has one primary lane entry")
    return validation_payload(checks, summarize_source_playbooks(sources) | {"sources": sources})


def render_source_playbook_validation(payload: dict[str, Any]) -> str:
    sources = payload.get("sources") if isinstance(payload.get("sources"), dict) else {}
    rows = [
        {"source": source_id, "lane": item.get("lane"), "method": item.get("fetch_method"), "role": item.get("evidence_role")}
        for source_id, item in sources.items()
        if isinstance(item, dict)
    ]
    return basic_markdown(
        "Acquisition Source Playbook Validation",
        {
            "status": payload.get("status"),
            "source_count": payload.get("source_count", 0),
            "metadata_sources": payload.get("metadata_sources", 0),
            "manual_only_sources": payload.get("manual_only_sources", 0),
            "disabled_sources": payload.get("disabled_sources", 0),
        },
        rows[:60],
        ("source", "lane", "method", "role"),
    )
