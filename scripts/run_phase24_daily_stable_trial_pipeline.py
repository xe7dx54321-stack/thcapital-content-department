#!/usr/bin/env python3
"""Run the Phase 24 daily stable trial pipeline."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase24-daily-stable-trial-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase24-daily-stable-trial-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase24_daily_stable_trial_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase24_daily_stable_trial_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase24-daily-stable-trial-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase24_daily_stable_trial_pipeline_board.md",
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
    return f"""# Phase 24 Daily Stable Trial Pipeline

## Summary

- status: `{payload.get('status')}`
- readiness_status: `{summary.get('readiness_status')}`
- stable_trial_days: `{summary.get('stable_trial_days')}`
- actionable_days: `{summary.get('actionable_days')}`
- quality_issue_count: `{summary.get('quality_issue_count')}`
- methodology_feedback_count: `{summary.get('methodology_feedback_count')}`
- sidecar_only: `true`

## Steps

{rows}
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [
        ("phase23_daily", python_command("scripts/run_phase23_daily_stability_pipeline.py")),
        ("stable_trial_day_1", python_command("scripts/run_stable_trial_day.py", "--day", "1")),
        ("stable_trial_day_2", python_command("scripts/run_stable_trial_day.py", "--day", "2")),
        ("stable_trial_day_3", python_command("scripts/run_stable_trial_day.py", "--day", "3")),
        ("content_quality_calibration", python_command("scripts/build_content_quality_calibration.py")),
        ("ops_to_methodology_feedback", python_command("scripts/build_ops_to_methodology_feedback.py")),
        ("stable_ops_readiness_review", python_command("scripts/build_stable_ops_readiness_review.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, ROOT) for name, command in commands]
    failed = [step for step in steps if step.returncode != 0]
    readiness = read_json(paths.logs_root / "latest_stable_ops_readiness_review.json")
    quality = read_json(paths.logs_root / "latest_content_quality_calibration.json")
    methodology = read_json(paths.logs_root / "latest_ops_to_methodology_feedback.json")
    phase23 = read_json(paths.logs_root / "latest_phase23_daily_stability_pipeline.json")
    readiness_summary = readiness.get("summary") if isinstance(readiness.get("summary"), dict) else {}
    quality_summary = quality.get("summary") if isinstance(quality.get("summary"), dict) else {}
    methodology_summary = methodology.get("summary") if isinstance(methodology.get("summary"), dict) else {}
    readiness_status = readiness.get("readiness_status", "UNKNOWN")
    if failed:
        status = "FAILED"
    elif readiness_status == "READY_FOR_DAILY_OPS":
        status = "SUCCESS"
    elif readiness_status == "ACTIONABLE_WITH_WARNINGS":
        status = "ACTIONABLE"
    else:
        status = "WARN"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "summary": {
            "readiness_status": readiness_status,
            "stable_trial_days": readiness_summary.get("stable_trial_days", 0),
            "ready_days": readiness_summary.get("ready_days", 0),
            "actionable_days": readiness_summary.get("actionable_days", 0),
            "blocked_days": readiness_summary.get("blocked_days", 0),
            "blocking_issues": readiness_summary.get("blocking_issues", 0),
            "quality_issue_count": quality_summary.get("quality_issue_count", 0),
            "publish_blocking_quality_issues": quality_summary.get("publish_blocking_quality_issues", 0),
            "methodology_feedback_count": methodology_summary.get("feedback_count", 0),
            "phase23_status": phase23.get("status", "UNKNOWN"),
            "sidecar_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_config_prompt_rule_changes": True,
            "no_mainline_overwrite": True,
        },
        "steps": [step_payload(step) for step in steps],
        "notes": [
            "Phase 24 turns Phase 23 ACTIONABLE status into a three-day stable ops trial scaffold and calibration loop.",
            "No publish, WeChat API, image generation, prompt/config/rule mutation, or mainline overwrite occurs.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 24 Daily Stable Trial Pipeline")
    print("====================================")
    print(f"status: {status}")
    for key, value in payload["summary"].items():
        print(f"{key}: {value}")
    print("Steps:")
    for step in steps:
        print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if status in {"SUCCESS", "ACTIONABLE", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
