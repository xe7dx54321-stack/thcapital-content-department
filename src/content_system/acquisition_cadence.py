"""Build and validate lane-specific acquisition cadence."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.acquisition_lane_registry import load_acquisition_lanes
from content_system.acquisition_playbook_common import (
    SCHEMA_VERSION,
    basic_markdown,
    check,
    grouped_runtime_runs,
    load_config,
    mapping,
    parse_minutes,
    today_token,
    utc_now,
    validation_payload,
    write_latest_report,
)
from content_system.paths import ProjectPaths


VALID_CATCHUP = {"latest_only", "consolidated", "skip_if_stale"}


def load_acquisition_cadence(repo_root: Path) -> dict[str, Any]:
    return load_config(repo_root, "acquisition_cadence.yaml")


def build_acquisition_cadence_plan(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    payload = load_acquisition_cadence(repo_root)
    lanes = mapping(payload, "lanes")
    source_config = load_config(repo_root, "acquisition_source_playbooks.yaml")
    sources = mapping(source_config, "sources")
    window = int((payload.get("policies") or {}).get("grouped_window_minutes", 20)) if isinstance(payload.get("policies"), dict) else 20
    lane_runs, grouped = grouped_runtime_runs(lanes, sources, window)
    summary = {
        "lane_count": len(lanes),
        "schedule_slot_count": len(lane_runs),
        "grouped_slots": len(grouped),
        "shared_source_dedup_enabled": bool((payload.get("policies") or {}).get("shared_source_dedup_enabled", True)) if isinstance(payload.get("policies"), dict) else True,
    }
    report = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "lanes": lanes,
        "lane_runs": lane_runs,
        "grouped_slots": grouped,
        "summary": summary,
        "policy": payload.get("policies", {}),
    }
    rows = [{"time": run["time"], "lane": run["lane"], "catchup": run["catchup_policy"], "network": run["network_requirement"]} for run in lane_runs[:60]]
    outputs = write_latest_report(paths, repo_root, "acquisition_cadence_plan", report, basic_markdown("Acquisition Cadence Plan", summary, rows, ("time", "lane", "catchup", "network")))
    return report, outputs


def validate_acquisition_cadence(repo_root: Path) -> dict[str, Any]:
    payload = load_acquisition_cadence(repo_root)
    lanes = mapping(payload, "lanes")
    registry = load_acquisition_lanes(repo_root)
    checks: list[dict[str, Any]] = []
    active_lanes = [lane for lane, item in registry.items() if isinstance(item, dict) and item.get("active", True)]
    missing = sorted(set(active_lanes) - set(lanes))
    check(checks, "active_lanes_have_cadence", not missing, f"missing={missing}")
    for lane, item in lanes.items():
        if not isinstance(item, dict):
            check(checks, f"{lane}_mapping", False, "cadence must be mapping")
            continue
        schedules = item.get("schedules")
        check(checks, f"{lane}_schedules", isinstance(schedules, list) and bool(schedules), "schedules present")
        for time_value in schedules or []:
            try:
                parse_minutes(str(time_value))
            except ValueError:
                check(checks, f"{lane}_time_{time_value}", False, "invalid HH:MM")
            else:
                check(checks, f"{lane}_time_{time_value}", True, "valid HH:MM")
        check(checks, f"{lane}_timezone", item.get("timezone") == "system_local", "timezone=system_local")
        check(checks, f"{lane}_catchup", item.get("catchup_policy") in VALID_CATCHUP, f"catchup={item.get('catchup_policy')}")
        check(checks, f"{lane}_rationale", bool(item.get("rationale")), "rationale present")
    too_frequent = [lane for lane, item in lanes.items() if isinstance(item, dict) and len(item.get("schedules") or []) > 3]
    check(checks, "max_three_schedules_per_lane", not too_frequent, f"too_frequent={too_frequent}")
    return validation_payload(checks, {"lane_count": len(lanes), "schedule_slot_count": sum(len((item or {}).get("schedules") or []) for item in lanes.values() if isinstance(item, dict))})


def render_cadence_validation(payload: dict[str, Any]) -> str:
    return basic_markdown("Acquisition Cadence Validation", {"status": payload.get("status"), **(payload.get("summary") or {})})
