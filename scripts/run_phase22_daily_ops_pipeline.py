#!/usr/bin/env python3
"""Run the Phase 22 stable content operations daily pipeline."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase22-daily-ops-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase22-daily-ops-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase22_daily_ops_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase22_daily_ops_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase22-daily-ops-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase22_daily_ops_pipeline_board.md",
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
    return f"""# Phase 22 Daily Ops Pipeline

## Summary

- status: `{payload.get('status')}`
- issue_count: `{summary.get('issue_count')}`
- high_issues: `{summary.get('high_issues')}`
- daily_action_count: `{summary.get('daily_action_count')}`
- ready_actions: `{summary.get('ready_actions')}`
- calendar_days: `{summary.get('calendar_days')}`
- feedback_recommendations: `{summary.get('feedback_recommendations')}`
- sidecar_only: `true`

## Steps

{rows}
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [
        ("phase21_trial", python_command("scripts/run_phase21_trial_pipeline.py")),
        ("recurring_issue_tracker", python_command("scripts/build_recurring_issue_board.py")),
        ("content_ops_fix_pack", python_command("scripts/build_content_ops_fix_pack.py")),
        ("daily_content_ops_runner", python_command("scripts/run_daily_content_ops.py", "--mode", "dry_run")),
        ("weekly_publishing_calendar", python_command("scripts/build_weekly_publishing_calendar.py", "--days", "7")),
        ("post_publish_feedback", python_command("scripts/build_post_publish_feedback.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, ROOT) for name, command in commands]
    failed = [step for step in steps if step.returncode != 0]
    issue_tracker = read_json(paths.logs_root / "latest_recurring_issue_tracker.json")
    runner = read_json(paths.logs_root / "latest_daily_content_ops_runner.json")
    calendar = read_json(paths.market_content_root / "07_publishing" / "latest_weekly_publishing_calendar.json")
    feedback = read_json(paths.logs_root / "latest_post_publish_feedback.json")
    issue_summary = issue_tracker.get("summary") if isinstance(issue_tracker.get("summary"), dict) else {}
    runner_summary = runner.get("summary") if isinstance(runner.get("summary"), dict) else {}
    calendar_summary = calendar.get("summary") if isinstance(calendar.get("summary"), dict) else {}
    feedback_summary = feedback.get("summary") if isinstance(feedback.get("summary"), dict) else {}
    high_issues = int(issue_summary.get("high") or 0)
    status = "FAILED" if failed else "DEGRADED" if high_issues or runner.get("status") == "DEGRADED" else "SUCCESS"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "summary": {
            "issue_count": issue_summary.get("issue_count", 0),
            "high_issues": high_issues,
            "quick_fix_candidates": issue_summary.get("quick_fix_candidates", 0),
            "daily_action_count": runner_summary.get("action_count", 0),
            "ready_actions": runner_summary.get("ready_actions", 0),
            "blocked_actions": runner_summary.get("blocked_actions", 0),
            "calendar_days": calendar_summary.get("calendar_days", 0),
            "ready_days": calendar_summary.get("ready_days", 0),
            "blocked_days": calendar_summary.get("blocked_days", 0),
            "feedback_recommendations": feedback_summary.get("recommendation_count", 0),
            "sidecar_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_mainline_overwrite": True,
            "no_config_prompt_rule_changes": True,
        },
        "steps": [step_payload(step) for step in steps],
        "notes": [
            "phase22-daily turns Phase21 trial signals into prioritized manual ops actions.",
            "SUCCESS or DEGRADED are both recorded with explicit reasons; no publish/API/image generation occurs.",
            "All outputs are sidecar artifacts for operator review.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 22 Daily Ops Pipeline")
    print("===========================")
    print(f"status: {status}")
    for key, value in payload["summary"].items():
        print(f"{key}: {value}")
    print("Steps:")
    for step in steps:
        print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if status in {"SUCCESS", "DEGRADED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
