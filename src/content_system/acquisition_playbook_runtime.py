"""Runtime acquisition plan built from Phase31C playbooks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.acquisition_cadence import load_acquisition_cadence
from content_system.acquisition_downstream_router import load_downstream_routes
from content_system.acquisition_fallback_strategy import load_fallback_strategies
from content_system.acquisition_lane_registry import load_acquisition_lanes
from content_system.acquisition_playbook_common import (
    SCHEMA_VERSION,
    basic_markdown,
    grouped_runtime_runs,
    list_value,
    mapping,
    today_token,
    utc_now,
    write_latest_report,
)
from content_system.acquisition_query_strategy import load_query_strategies
from content_system.acquisition_source_playbook import load_source_playbooks
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json


def _network_action(requirement: str, readiness: str) -> str:
    requirement = requirement or "mixed"
    readiness = readiness or "UNKNOWN"
    if readiness == "FULL":
        return "RUN_NOW"
    if readiness == "OFFLINE":
        return "DELAY_EXTERNAL" if requirement != "local" else "RUN_LOCAL"
    if readiness == "DOMESTIC_ONLY":
        if requirement in {"domestic", "local"}:
            return "RUN_NOW"
        return "DELAY_RETRY"
    if readiness == "INTERNATIONAL_ONLY":
        if requirement in {"international", "local"}:
            return "RUN_NOW"
        return "DELAY_RETRY"
    return "ROUTE_UNKNOWN"


def _connector_runs_with_context(grouped_runs: list[dict[str, Any]], sources: dict[str, Any]) -> list[dict[str, Any]]:
    connector_runs: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for group in grouped_runs:
        group_key = str(group.get("group_key") or "")
        for run in list_value(group.get("connector_runs")):
            if not isinstance(run, dict):
                continue
            source_id = str(run.get("source_id") or "")
            source = sources.get(source_id) if isinstance(sources.get(source_id), dict) else {}
            fetch_method = str(source.get("fetch_method") or run.get("fetch_method") or "")
            dedup_key = (fetch_method, str(source.get("url") or source_id), group_key)
            if dedup_key in seen:
                continue
            seen.add(dedup_key)
            connector_runs.append(
                {
                    "connector_run_id": f"acqrun_{len(connector_runs) + 1:04d}",
                    "source_id": source_id,
                    "source_name": source.get("source_name") or source_id,
                    "lane": run.get("lane") or source.get("lane") or "",
                    "group_key": group_key,
                    "fetch_method": fetch_method,
                    "source_type": source.get("source_type") or "",
                    "lookback_hours": source.get("lookback_hours", 0),
                    "max_items": source.get("max_items", 0),
                    "metadata_only": bool(source.get("metadata_only", True)),
                    "hard_evidence_allowed": bool(source.get("hard_evidence_allowed", source.get("evidence_role") == "hard_evidence")),
                }
            )
    return connector_runs


def build_runtime_acquisition_plan(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    lanes = load_acquisition_lanes(repo_root)
    cadence_payload = load_acquisition_cadence(repo_root)
    cadence = mapping(cadence_payload, "lanes")
    sources = load_source_playbooks(repo_root)
    queries = load_query_strategies(repo_root)
    fallbacks = load_fallback_strategies(repo_root)
    routes = load_downstream_routes(repo_root)
    network = read_json(paths.logs_root / "latest_runtime_network_readiness.json")
    readiness = str(network.get("status") or "UNKNOWN")
    policies = cadence_payload.get("policies") if isinstance(cadence_payload.get("policies"), dict) else {}
    window = int(policies.get("grouped_window_minutes") or 20)
    lane_runs, grouped_runs = grouped_runtime_runs(cadence, sources, window)
    connector_runs = _connector_runs_with_context(grouped_runs, sources)
    lane_run_rows: list[dict[str, Any]] = []
    for run in lane_runs:
        lane = str(run.get("lane") or "")
        source_count = sum(1 for source in sources.values() if isinstance(source, dict) and (source.get("lane") == lane or lane in list_value(source.get("secondary_lanes"))))
        lane_run_rows.append(
            {
                "lane_run_id": f"lane_{lane}_{run.get('time')}",
                "lane": lane,
                "time": run.get("time"),
                "catchup_policy": run.get("catchup_policy"),
                "network_requirement": run.get("network_requirement"),
                "route_action": _network_action(str(run.get("network_requirement") or "mixed"), readiness),
                "source_count": source_count,
                "query_lookback_hours": (queries.get(lane) if isinstance(queries.get(lane), dict) else {}).get("lookback_hours", 0),
                "fallback_status": (fallbacks.get(lane) if isinstance(fallbacks.get(lane), dict) else {}).get("status", ""),
                "downstream_outputs": (routes.get(lane) if isinstance(routes.get(lane), dict) else {}).get("outputs", []),
                "evidence_role": (lanes.get(lane) if isinstance(lanes.get(lane), dict) else {}).get("evidence_role", ""),
            }
        )
    duplicate_without_dedup = sum(len(list_value(group.get("connector_runs"))) for group in grouped_runs)
    shared_source_dedup_count = max(0, duplicate_without_dedup - len(connector_runs))
    summary = {
        "lane_runs": len(lane_run_rows),
        "grouped_runs": len(grouped_runs),
        "connector_runs": len(connector_runs),
        "shared_source_dedup_count": shared_source_dedup_count,
        "network_status": readiness,
        "run_now": sum(1 for item in lane_run_rows if item.get("route_action") in {"RUN_NOW", "RUN_LOCAL"}),
        "delayed_retry": sum(1 for item in lane_run_rows if item.get("route_action") in {"DELAY_RETRY", "DELAY_EXTERNAL"}),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "runtime_acquisition_plan": {
            "business_date": today_token(),
            "timezone": policies.get("timezone", "system_local"),
            "grouped_window_minutes": window,
            "max_parallel_lane_batches": policies.get("max_parallel_lane_batches", 2),
            "shared_source_dedup_enabled": bool(policies.get("shared_source_dedup_enabled", True)),
        },
        "lane_runs": lane_run_rows,
        "grouped_runs": grouped_runs,
        "connector_runs": connector_runs,
        "downstream_dispatch": [
            {
                "lane": lane,
                "outputs": (route if isinstance(route, dict) else {}).get("outputs", []),
                "promotion": (route if isinstance(route, dict) else {}).get("promotion", {}),
            }
            for lane, route in routes.items()
        ],
        "summary": summary,
        "policy": {
            "no_openclaw_gateway": True,
            "no_openclaw_cron_migration": True,
            "metadata_only": True,
            "shared_connector_fetch_once": True,
            "weak_signal_not_hard_evidence": True,
        },
    }
    rows = [
        {"time": item.get("time"), "lane": item.get("lane"), "route": item.get("route_action"), "sources": item.get("source_count")}
        for item in lane_run_rows[:80]
    ]
    outputs = write_latest_report(
        paths,
        repo_root,
        "runtime_acquisition_plan",
        payload,
        basic_markdown("Runtime Acquisition Plan", summary, rows, ("time", "lane", "route", "sources")),
    )
    return payload, outputs
