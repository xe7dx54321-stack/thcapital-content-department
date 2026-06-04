"""Stabilize trial-day status by separating blockers from actionable warnings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__trial-day-status-stabilizer.json",
        "dated_md": paths.logs_root / f"{run_date}__trial-day-status-stabilizer.md",
        "latest_json": paths.logs_root / "latest_trial_day_status_stabilizer.json",
        "latest_md": paths.logs_root / "latest_trial_day_status_stabilizer.md",
    }


def build_trial_day_status_stabilizer(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    runner = read_json(paths.logs_root / "latest_daily_content_ops_runner.json")
    failure = read_json(paths.logs_root / "latest_content_ops_failure_handling.json")
    plan = read_json(paths.logs_root / "latest_high_priority_issue_resolution_plan.json")
    quick = read_json(paths.logs_root / "latest_quick_fix_execution_results.json")
    queue_repair = read_json(paths.market_content_root / "07_publishing" / "latest_content_queue_readiness_repair.json")
    runner_summary = runner.get("summary") if isinstance(runner.get("summary"), dict) else {}
    failure_summary = failure.get("summary") if isinstance(failure.get("summary"), dict) else {}
    status_before = runner.get("status") or "UNKNOWN"
    blockers: list[str] = []
    actionable: list[str] = []
    notes: list[str] = []
    for item in list_payload(failure, "issues"):
        if item.get("severity") == "BLOCKER":
            blockers.append(item.get("description") or item.get("issue_id") or "Failure blocker")
    for item in list_payload(plan, "issues"):
        if item.get("current_status") in {"READY_TO_FIX", "NEEDS_MANUAL"}:
            actionable.append(f"{item.get('area')}: {item.get('title')}")
        elif item.get("current_status") == "MONITOR":
            notes.append(f"{item.get('area')}: {item.get('title')}")
    for item in list_payload(quick, "fix_results"):
        if item.get("status") == "APPLIED_SIDECAR":
            notes.append(f"quick fix sidecar applied: {item.get('fix_type')}")
        elif item.get("status") == "NEEDS_MANUAL":
            actionable.append(f"manual required: {item.get('source_issue_id')}")
    for item in list_payload(queue_repair, "items"):
        if item.get("next_operator_action"):
            actionable.append(f"queue {item.get('queue_item_id')}: {item.get('next_operator_action')}")
    ready_actions = int(runner_summary.get("ready_actions") or 0)
    blocked_actions = int(runner_summary.get("blocked_actions") or 0)
    blocker_count = len(blockers) + int(failure_summary.get("blocker_count") or 0)
    if status_before == "FAILED":
        status_after = "FAILED"
    elif blocker_count:
        status_after = "DEGRADED"
    elif status_before == "DEGRADED" and ready_actions > 0 and blocked_actions == 0:
        status_after = "ACTIONABLE"
    elif status_before in {"SUCCESS", "ACTIONABLE"}:
        status_after = status_before
    else:
        status_after = "ACTIONABLE" if actionable else "SUCCESS"
    summary = {
        "blocker_count": blocker_count,
        "actionable_warning_count": len(actionable),
        "operator_note_count": len(notes),
        "can_continue": status_after in {"SUCCESS", "ACTIONABLE"},
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "status_before": status_before,
        "status_after": status_after,
        "blockers": blockers,
        "actionable_warnings": actionable[:20],
        "operator_notes": notes[:20],
        "stabilization_summary": summary,
        "policy": {"does_not_hide_blockers": True, "sidecar_only": True, "no_auto_publish": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("stabilization_summary") if isinstance(payload.get("stabilization_summary"), dict) else {}
    blockers = "\n".join(f"- {item}" for item in payload.get("blockers", [])) or "- None."
    actions = "\n".join(f"- {item}" for item in payload.get("actionable_warnings", [])) or "- None."
    notes = "\n".join(f"- {item}" for item in payload.get("operator_notes", [])) or "- None."
    return f"""# Trial Day Status Stabilizer

## Summary

- status_before: `{payload.get('status_before')}`
- status_after: `{payload.get('status_after')}`
- blocker_count: `{summary.get('blocker_count', 0)}`
- actionable_warning_count: `{summary.get('actionable_warning_count', 0)}`
- operator_note_count: `{summary.get('operator_note_count', 0)}`
- can_continue: `{summary.get('can_continue', True)}`

## Blockers

{blockers}

## Actionable Warnings

{actions}

## Operator Notes

{notes}
"""
