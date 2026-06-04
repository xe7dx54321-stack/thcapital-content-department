#!/usr/bin/env python3
"""Run Phase 20 hardening pipeline."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase20-daily-hardening-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase20-daily-hardening-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase20_daily_hardening_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase20_daily_hardening_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase20-daily-hardening-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase20_daily_hardening_pipeline_board.md",
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
    summary = payload.get("summary", {})
    rows = "\n".join(f"- {step.get('name')}: {step.get('status')} ({step.get('returncode')})" for step in payload.get("steps", []))
    return f"""# Phase 20 Daily Hardening Pipeline

## Summary

- status: `{payload.get('status')}`
- phase19_status: `{summary.get('phase19_status')}`
- trial_days: `{summary.get('trial_days')}`
- failure_issue_count: `{summary.get('failure_issue_count')}`
- regression_status: `{summary.get('regression_status')}`
- trial_readiness_status: `{summary.get('trial_readiness_status')}`
- no_auto_publish: `true`
- no_wechat_api: `true`

## Steps

{rows}
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [
        ("phase19_daily", python_command("scripts/run_phase19_daily_ops_pipeline.py")),
        ("one_week_trial_protocol", python_command("scripts/build_one_week_trial_protocol.py")),
        ("content_ops_failure_handling", python_command("scripts/build_content_ops_failure_handling.py")),
        ("publishing_checklist_regression", python_command("scripts/run_publishing_checklist_regression.py")),
        ("operator_runbook", python_command("scripts/build_operator_runbook.py")),
        ("phase0_19_system_closeout", python_command("scripts/build_phase0_19_system_closeout.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, ROOT) for name, command in commands]
    status = "SUCCESS" if all(step.returncode == 0 for step in steps) else "DEGRADED"
    trial = read_json(paths.logs_root / "latest_one_week_trial_run_protocol.json")
    failure = read_json(paths.logs_root / "latest_content_ops_failure_handling.json")
    regression = read_json(paths.logs_root / "latest_publishing_checklist_regression.json")
    closeout = read_json(paths.logs_root / "latest_phase0_19_system_closeout.json")
    phase19 = read_json(paths.logs_root / "latest_phase19_daily_ops_pipeline.json")
    failure_summary = failure.get("summary") if isinstance(failure.get("summary"), dict) else {}
    regression_summary = regression.get("summary") if isinstance(regression.get("summary"), dict) else {}
    readiness = closeout.get("trial_readiness") if isinstance(closeout.get("trial_readiness"), dict) else {}
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "summary": {
            "phase19_status": phase19.get("status", "UNKNOWN"),
            "trial_days": (trial.get("trial_period") or {}).get("days", 7) if isinstance(trial.get("trial_period"), dict) else 7,
            "daily_checklist_count": len(trial.get("daily_checklist", [])),
            "failure_issue_count": failure_summary.get("issue_count", 0),
            "failure_blocker_count": failure_summary.get("blocker_count", 0),
            "regression_status": regression_summary.get("regression_status", "UNKNOWN"),
            "trial_readiness_status": readiness.get("status", "UNKNOWN"),
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_session_creation": True,
            "no_auto_metrics_input": True,
            "no_auto_image_generation": True,
            "no_auto_config_changes": True,
        },
        "steps": [step_payload(step) for step in steps],
        "policy": {
            "hardening_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_config_prompt_rule_changes": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 20 Daily Hardening Pipeline")
    print("=================================")
    print(f"status: {status}")
    for key, value in payload["summary"].items():
        print(f"{key}: {value}")
    print("Steps:")
    for step in steps:
        print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
