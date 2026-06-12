"""Regression gate for Phase31C acquisition playbooks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.acquisition_cadence import load_acquisition_cadence
from content_system.acquisition_downstream_router import load_downstream_routes
from content_system.acquisition_fallback_strategy import load_fallback_strategies
from content_system.acquisition_lane_registry import load_acquisition_lanes
from content_system.acquisition_playbook_common import (
    SCHEMA_VERSION,
    WEAK_LANES,
    basic_markdown,
    grouped_runtime_runs,
    list_value,
    mapping,
    safe_ratio,
    today_token,
    utc_now,
    write_latest_report,
)
from content_system.acquisition_query_strategy import load_query_strategies
from content_system.acquisition_source_playbook import load_source_playbooks
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json


def _check(checks: list[dict[str, Any]], check_id: str, status: str, message: str, blocking: bool = False) -> None:
    checks.append({"check_id": check_id, "status": status, "message": message, "blocking": blocking})


def _lane_for_job(job: dict[str, Any], lanes: set[str]) -> str:
    lane = str(job.get("inferred_lane") or "")
    if lane in lanes:
        return lane
    purpose = f"{job.get('inferred_purpose', '')} {' '.join(str(item) for item in job.get('source_ids', []) or [])}".lower()
    for candidate in lanes:
        marker = candidate.replace("_", " ")
        if marker in purpose:
            return candidate
    return ""


def run_acquisition_playbook_regression(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    lanes = load_acquisition_lanes(repo_root)
    cadence_payload = load_acquisition_cadence(repo_root)
    cadence = mapping(cadence_payload, "lanes")
    sources = load_source_playbooks(repo_root)
    queries = load_query_strategies(repo_root)
    fallbacks = load_fallback_strategies(repo_root)
    routes = load_downstream_routes(repo_root)
    audit = read_json(paths.logs_root / "latest_openclaw_acquisition_semantics_audit.json")
    if not audit:
        audit = read_json(paths.logs_root / "latest_openclaw_source_inventory.json")
    jobs = audit.get("jobs") if isinstance(audit.get("jobs"), list) else []
    high_value_jobs = [
        job
        for job in jobs
        if isinstance(job, dict) and str(job.get("migration_value") or "").upper() == "HIGH"
    ]
    if not high_value_jobs and isinstance(audit.get("jobs"), list):
        high_value_jobs = [job for job in jobs if isinstance(job, dict) and job.get("enabled") is True][:1]
    lane_ids = set(lanes)
    mapped_jobs = [job for job in high_value_jobs if _lane_for_job(job, lane_ids)]
    unmapped_jobs = [job for job in high_value_jobs if not _lane_for_job(job, lane_ids)]
    lane_runs, grouped = grouped_runtime_runs(cadence, sources, int((cadence_payload.get("policies") or {}).get("grouped_window_minutes", 20)) if isinstance(cadence_payload.get("policies"), dict) else 20)
    connector_occurrences: dict[tuple[str, str, str], int] = {}
    for group in grouped:
        group_key = str(group.get("group_key") or "")
        for run in list_value(group.get("connector_runs")):
            if not isinstance(run, dict):
                continue
            source_id = str(run.get("source_id") or "")
            source = sources.get(source_id) if isinstance(sources.get(source_id), dict) else {}
            key = (str(source.get("fetch_method") or run.get("fetch_method") or ""), str(source.get("url") or source_id), group_key)
            connector_occurrences[key] = connector_occurrences.get(key, 0) + 1
    duplicate_source_slots = sum(count - 1 for count in connector_occurrences.values() if count > 1)
    duplicate_connector_runs = duplicate_source_slots if not bool((cadence_payload.get("policies") or {}).get("shared_source_dedup_enabled", True)) else 0
    conflicting_lane_schedules = 0
    seen_lane_slots: set[tuple[str, str]] = set()
    for run in lane_runs:
        key = (str(run.get("lane")), str(run.get("time")))
        if key in seen_lane_slots:
            conflicting_lane_schedules += 1
        seen_lane_slots.add(key)
    checks: list[dict[str, Any]] = []
    coverage_ratio = safe_ratio(len(mapped_jobs), len(high_value_jobs))
    _check(checks, "high_value_openclaw_job_mapping", "PASS" if coverage_ratio >= 0.8 else "WARN", f"coverage={coverage_ratio}", False)
    active_lanes = [lane for lane, item in lanes.items() if isinstance(item, dict) and item.get("active", True)]
    for lane in active_lanes:
        _check(checks, f"{lane}_has_cadence", "PASS" if lane in cadence else "FAIL", "active lane cadence present", lane not in cadence)
        _check(checks, f"{lane}_has_query", "PASS" if lane in queries else "FAIL", "active lane query strategy present", lane not in queries)
        _check(checks, f"{lane}_has_fallback", "PASS" if lane in fallbacks else "FAIL", "active lane fallback present", lane not in fallbacks)
        _check(checks, f"{lane}_has_downstream", "PASS" if lane in routes else "FAIL", "active lane downstream route present", lane not in routes)
        lane_sources = [source_id for source_id, source in sources.items() if isinstance(source, dict) and (source.get("lane") == lane or lane in list_value(source.get("secondary_lanes")))]
        _check(checks, f"{lane}_has_fetch_method", "PASS" if lane_sources else "FAIL", f"source_count={len(lane_sources)}", not lane_sources)
    for lane in WEAK_LANES:
        route = routes.get(lane) if isinstance(routes.get(lane), dict) else {}
        route_text = str(route)
        _check(checks, f"{lane}_weak_not_hard_evidence", "PASS" if "hard_evidence" not in route_text else "FAIL", "weak signal not routed to hard evidence", "hard_evidence" in route_text)
        _check(checks, f"{lane}_weak_not_direct_brief", "PASS" if "brief_candidate" not in route_text else "FAIL", "weak signal not direct brief", "brief_candidate" in route_text)
    _check(checks, "shared_source_dedup", "PASS" if duplicate_connector_runs == 0 else "FAIL", f"duplicate_connector_runs={duplicate_connector_runs}", duplicate_connector_runs > 0)
    _check(checks, "same_source_same_window_deduped", "PASS" if duplicate_source_slots == 0 or bool((cadence_payload.get("policies") or {}).get("shared_source_dedup_enabled", True)) else "FAIL", f"duplicate_source_slots={duplicate_source_slots}", False)
    _check(checks, "lane_schedule_conflicts", "PASS" if conflicting_lane_schedules == 0 else "WARN", f"conflicting_lane_schedules={conflicting_lane_schedules}", False)
    _check(checks, "schedule_frequency_reasonable", "PASS" if all(len((item or {}).get("schedules") or []) <= 3 for item in cadence.values() if isinstance(item, dict)) else "FAIL", "max 3 schedules per lane", False)
    for source_id, source in sources.items():
        if not isinstance(source, dict):
            continue
        method = str(source.get("fetch_method") or "")
        forbidden = method in {"browser_login", "paywall_bypass", "full_text_scrape", "credentialed_fetch"}
        _check(checks, f"{source_id}_no_forbidden_fetch", "PASS" if not forbidden else "FAIL", f"method={method}", forbidden)
        full_text = source.get("full_text_allowed", False) is True
        _check(checks, f"{source_id}_metadata_only", "PASS" if not full_text and source.get("metadata_only", True) is True else "FAIL", "metadata only and no full text", full_text)
    pass_count = sum(1 for item in checks if item.get("status") == "PASS")
    warn_count = sum(1 for item in checks if item.get("status") == "WARN")
    fail_count = sum(1 for item in checks if item.get("status") == "FAIL")
    blocking = sum(1 for item in checks if item.get("status") == "FAIL" and item.get("blocking"))
    status = "FAIL" if blocking else ("ACTIONABLE" if warn_count or fail_count else "PASS")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": status,
        "checks": checks,
        "coverage": {
            "high_value_openclaw_jobs": len(high_value_jobs),
            "mapped_jobs": len(mapped_jobs),
            "unmapped_jobs": len(unmapped_jobs),
            "coverage_ratio": coverage_ratio,
        },
        "unmapped_jobs": [{"job_id": job.get("job_id"), "lane": job.get("inferred_lane"), "purpose": job.get("inferred_purpose")} for job in unmapped_jobs[:20]],
        "duplicates": {
            "duplicate_source_slots": duplicate_source_slots,
            "duplicate_connector_runs": duplicate_connector_runs,
            "conflicting_lane_schedules": conflicting_lane_schedules,
        },
        "summary": {
            "pass": pass_count,
            "warn": warn_count,
            "fail": fail_count,
            "blocking_failures": blocking,
        },
        "policy": {
            "no_openclaw_job_mutation": True,
            "weak_signal_not_hard_evidence": True,
            "wechat_no_full_text": True,
        },
    }
    outputs = write_latest_report(
        paths,
        repo_root,
        "acquisition_playbook_regression",
        payload,
        basic_markdown("Acquisition Playbook Regression", {"status": status, **payload["coverage"], **payload["duplicates"], **payload["summary"]}, checks[:80], ("check_id", "status", "message")),
    )
    return payload, outputs
