"""Dry-run validation for the autonomous acquisition playbook."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.acquisition_fallback_strategy import load_fallback_strategies
from content_system.acquisition_lane_registry import load_acquisition_lanes
from content_system.acquisition_playbook_common import SCHEMA_VERSION, basic_markdown, list_value, today_token, utc_now, write_latest_report
from content_system.acquisition_playbook_regression import run_acquisition_playbook_regression
from content_system.acquisition_playbook_runtime import build_runtime_acquisition_plan
from content_system.acquisition_source_playbook import load_source_playbooks
from content_system.paths import ProjectPaths


def run_autonomous_acquisition_dry_run(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    lanes = load_acquisition_lanes(repo_root)
    sources = load_source_playbooks(repo_root)
    fallbacks = load_fallback_strategies(repo_root)
    runtime_plan, _ = build_runtime_acquisition_plan(paths, repo_root)
    regression, _ = run_acquisition_playbook_regression(paths, repo_root)
    lane_runs = list_value(runtime_plan.get("lane_runs"))
    connector_runs = list_value(runtime_plan.get("connector_runs"))
    active_lanes = [lane for lane, item in lanes.items() if isinstance(item, dict) and item.get("active", True)]
    simulated_items: list[dict[str, Any]] = []
    fallback_tasks = 0
    confirmation_tasks = 0
    downstream_routes = 0
    for run in connector_runs:
        if not isinstance(run, dict):
            continue
        source_id = str(run.get("source_id") or "")
        source = sources.get(source_id) if isinstance(sources.get(source_id), dict) else {}
        if source.get("fetch_method") in {"disabled", "manual_only"}:
            fallback_tasks += 1
            continue
        # Dry-run item counts are conservative metadata probes, not full fetches.
        item_count = 1 if source.get("metadata_only", True) else 0
        for index in range(item_count):
            simulated_items.append(
                {
                    "item_id": f"dry_acq_{len(simulated_items) + 1:04d}",
                    "source_id": source_id,
                    "lane": run.get("lane") or source.get("lane"),
                    "title": f"Metadata dry-run item {index + 1} from {source_id}",
                    "metadata_only": True,
                    "copyright_safe": True,
                    "hard_evidence_allowed": bool(source.get("hard_evidence_allowed", source.get("evidence_role") == "hard_evidence")),
                }
            )
        lane = str(run.get("lane") or source.get("lane") or "")
        fallback = fallbacks.get(lane) if isinstance(fallbacks.get(lane), dict) else {}
        if fallback.get("confirmation_required", True):
            confirmation_tasks += 1
        if fallback.get("status") and fallback.get("status") != "NO_FALLBACK_REQUIRED":
            fallback_tasks += 1
        downstream_routes += 1
    failure_count = 1 if regression.get("summary", {}).get("blocking_failures", 0) else 0
    warning_count = int(regression.get("summary", {}).get("warn", 0) or 0)
    summary = {
        "lane_count": len(active_lanes),
        "scheduled_lane_runs": len(lane_runs),
        "shared_source_dedup_count": int((runtime_plan.get("summary") or {}).get("shared_source_dedup_count") or 0),
        "connector_runs": len(connector_runs),
        "item_count": len(simulated_items),
        "fallback_tasks": fallback_tasks,
        "confirmation_tasks": confirmation_tasks,
        "downstream_routes": downstream_routes,
        "success": 1 if failure_count == 0 else 0,
        "warnings": warning_count,
        "failures": failure_count,
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "SUCCESS" if failure_count == 0 else "ACTIONABLE",
        "mode": "dry_run",
        "runtime_plan_summary": runtime_plan.get("summary", {}),
        "regression_status": regression.get("status", "UNKNOWN"),
        "simulated_items": simulated_items[:80],
        "summary": summary,
        "policy": {
            "dry_run": True,
            "no_live_llm": True,
            "no_full_text": True,
            "no_auto_publish": True,
            "no_image_generation": True,
            "no_openclaw_mutation": True,
        },
    }
    outputs = write_latest_report(
        paths,
        repo_root,
        "autonomous_acquisition_dry_run",
        payload,
        basic_markdown("Autonomous Acquisition Dry Run", summary, simulated_items[:40], ("item_id", "source_id", "lane", "metadata_only")),
    )
    return payload, outputs
