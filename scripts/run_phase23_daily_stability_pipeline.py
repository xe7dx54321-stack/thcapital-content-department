#!/usr/bin/env python3
"""Run the Phase 23 daily stability pipeline."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.phase7_report_utils import PipelineStep, python_command, read_json, repo_relative, run_step, today_token, utc_now, write_json_and_markdown


def output_paths(paths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__phase23-daily-stability-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase23-daily-stability-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase23_daily_stability_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase23_daily_stability_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase23-daily-stability-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase23_daily_stability_pipeline_board.md",
    }


def step_payload(step: PipelineStep) -> dict[str, Any]:
    return {
        "name": step.name,
        "command": step.command,
        "returncode": step.returncode,
        "status": step.status,
        "started_at": step.started_at,
        "finished_at": step.finished_at,
        "stdout_tail": step.stdout_tail,
        "stderr_tail": step.stderr_tail,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(f"- {step.get('name')}: {step.get('status')} ({step.get('returncode')})" for step in payload.get("steps", []))
    return f"""# Phase 23 Daily Stability Pipeline

## Summary

- status: `{payload.get('status')}`
- gate_status: `{summary.get('gate_status')}`
- high_priority: `{summary.get('high_priority')}`
- quick_fix_applied_sidecar: `{summary.get('quick_fix_applied_sidecar')}`
- queue_improved: `{summary.get('queue_improved')}`
- calendar_actionable_days: `{summary.get('calendar_actionable_days')}`
- stabilizer_status_after: `{summary.get('stabilizer_status_after')}`
- verification_unresolved: `{summary.get('verification_unresolved')}`
- sidecar_only: `true`

## Steps

{rows}
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [
        ("phase22_daily", python_command("scripts/run_phase22_daily_ops_pipeline.py")),
        ("high_priority_issue_resolution_plan", python_command("scripts/build_high_priority_issue_resolution_plan.py")),
        ("quick_fix_candidate_executor", python_command("scripts/execute_quick_fix_candidates.py")),
        ("content_queue_readiness_repair", python_command("scripts/repair_content_queue_readiness.py")),
        ("publishing_calendar_readiness_calibration", python_command("scripts/calibrate_publishing_calendar_readiness.py")),
        ("trial_day_status_stabilizer", python_command("scripts/stabilize_trial_day_status.py")),
        ("issue_resolution_verification", python_command("scripts/build_issue_resolution_verification_board.py")),
        ("stable_trial_readiness_gate", python_command("scripts/build_stable_trial_readiness_gate.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, ROOT) for name, command in commands]
    failed = [step for step in steps if step.returncode != 0]
    plan = read_json(paths.logs_root / "latest_high_priority_issue_resolution_plan.json")
    quick = read_json(paths.logs_root / "latest_quick_fix_execution_results.json")
    queue = read_json(paths.market_content_root / "07_publishing" / "latest_content_queue_readiness_repair.json")
    calendar = read_json(paths.market_content_root / "07_publishing" / "latest_publishing_calendar_readiness_calibration.json")
    stabilizer = read_json(paths.logs_root / "latest_trial_day_status_stabilizer.json")
    verification = read_json(paths.logs_root / "latest_issue_resolution_verification.json")
    gate = read_json(paths.logs_root / "latest_stable_trial_readiness_gate.json")
    plan_summary = plan.get("summary") if isinstance(plan.get("summary"), dict) else {}
    quick_summary = quick.get("summary") if isinstance(quick.get("summary"), dict) else {}
    queue_summary = queue.get("summary") if isinstance(queue.get("summary"), dict) else {}
    calendar_summary = calendar.get("summary") if isinstance(calendar.get("summary"), dict) else {}
    verification_summary = verification.get("summary") if isinstance(verification.get("summary"), dict) else {}
    gate_summary = gate.get("summary") if isinstance(gate.get("summary"), dict) else {}
    gate_status = gate.get("gate_status") or "UNKNOWN"
    if failed:
        status = "FAILED"
    elif gate_status in {"READY_FOR_STABLE_TRIAL", "ACTIONABLE_WITH_WARNINGS"}:
        status = "SUCCESS" if gate_status == "READY_FOR_STABLE_TRIAL" else "ACTIONABLE"
    else:
        status = "DEGRADED"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "summary": {
            "gate_status": gate_status,
            "criteria_pass": gate_summary.get("pass", 0),
            "criteria_warn": gate_summary.get("warn", 0),
            "criteria_fail": gate_summary.get("fail", 0),
            "blocking_failures": gate_summary.get("blocking_failures", 0),
            "high_priority": plan_summary.get("high_priority", 0),
            "quick_fix_applied_sidecar": quick_summary.get("applied_sidecar", 0),
            "quick_fix_needs_manual": quick_summary.get("needs_manual", 0),
            "queue_improved": queue_summary.get("improved", 0),
            "queue_still_blocked": queue_summary.get("still_blocked", 0),
            "calendar_ready_days": calendar_summary.get("ready_days", 0),
            "calendar_actionable_days": calendar_summary.get("actionable_days", 0),
            "stabilizer_status_after": stabilizer.get("status_after", "UNKNOWN"),
            "verification_verified": verification_summary.get("verified", 0),
            "verification_partial": verification_summary.get("partial", 0),
            "verification_unresolved": verification_summary.get("unresolved", 0),
            "sidecar_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_mainline_overwrite": True,
            "no_config_prompt_rule_changes": True,
        },
        "steps": [step_payload(step) for step in steps],
        "notes": [
            "Phase 23 resolves high-priority recurring issues through sidecar planning, quick-fix execution, and stable readiness gating.",
            "No publish, WeChat API call, image generation, prompt/config/rule mutation, or mainline overwrite occurs.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 23 Daily Stability Pipeline")
    print("=================================")
    print(f"status: {status}")
    for key, value in payload["summary"].items():
        print(f"{key}: {value}")
    print("Steps:")
    for step in steps:
        print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if status in {"SUCCESS", "ACTIONABLE", "DEGRADED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
