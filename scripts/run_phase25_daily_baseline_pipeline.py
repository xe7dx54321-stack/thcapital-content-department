#!/usr/bin/env python3
"""Run the Phase 25 daily baseline pipeline."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase25-daily-baseline-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase25-daily-baseline-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase25_daily_baseline_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase25_daily_baseline_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase25-daily-baseline-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase25_daily_baseline_pipeline_board.md",
    }


def step_payload(step: PipelineStep) -> dict[str, Any]:
    return {
        "name": step.name,
        "command": step.command,
        "return_code": step.returncode,
        "status": step.status,
        "started_at": step.started_at,
        "finished_at": step.finished_at,
        "stdout_tail": step.stdout_tail,
        "stderr_tail": step.stderr_tail,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(f"- {step.get('name')}: {step.get('status')} ({step.get('return_code')})" for step in payload.get("steps", []))
    return f"""# Phase 25 Daily Baseline Pipeline

## Summary

- status: `{payload.get('status')}`
- stable_daily_ops_status: `{summary.get('stable_daily_ops_status')}`
- v1_status: `{summary.get('v1_status')}`
- recommended_command: `{summary.get('recommended_command')}`
- operator_review_required: `{summary.get('operator_review_required')}`
- no_auto_publish: `true`

## Steps

{rows}
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [
        ("stable_daily_ops", python_command("scripts/run_stable_daily_ops.py")),
        ("content_factory_v1_closeout", python_command("scripts/build_content_factory_v1_closeout.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, ROOT) for name, command in commands]
    failed = [step for step in steps if step.returncode != 0]
    stable = read_json(paths.logs_root / "latest_stable_daily_ops.json")
    closeout = read_json(paths.logs_root / "latest_content_factory_v1_closeout.json")
    stable_summary = stable.get("daily_summary") if isinstance(stable.get("daily_summary"), dict) else {}
    daily_use = closeout.get("daily_use") if isinstance(closeout.get("daily_use"), dict) else {}
    v1_status = closeout.get("v1_status", "UNKNOWN")
    if failed:
        status = "FAILED"
    elif v1_status in {"CLOSED_READY_FOR_DAILY_OPS", "CLOSED_WITH_WARNINGS"} and stable.get("status") in {"SUCCESS", "ACTIONABLE", "DEGRADED"}:
        status = "SUCCESS" if stable.get("status") == "SUCCESS" else "ACTIONABLE"
    elif v1_status == "NEEDS_FIX":
        status = "DEGRADED"
    else:
        status = "FAILED"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "summary": {
            "stable_daily_ops_status": stable.get("status", "UNKNOWN"),
            "baseline_status": stable_summary.get("baseline_status", "UNKNOWN"),
            "operator_acceptance_status": stable_summary.get("operator_acceptance_status", "UNKNOWN"),
            "blocking_issue_count": stable_summary.get("blocking_issue_count", 0),
            "workbench_ready": stable_summary.get("workbench_ready", False),
            "v1_status": v1_status,
            "recommended_command": daily_use.get("recommended_command", "make stable-daily-ops"),
            "operator_review_required": daily_use.get("operator_review_required", True),
            "sidecar_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_config_prompt_rule_changes": True,
            "no_mainline_overwrite": True,
        },
        "steps": [step_payload(step) for step in steps],
        "notes": [
            "Phase 25 freezes the daily ops baseline and operator acceptance surface.",
            "The pipeline is manual-ops only and never publishes or calls WeChat APIs.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 25 Daily Baseline Pipeline")
    print("================================")
    print(f"status: {status}")
    for key, value in payload["summary"].items():
        print(f"{key}: {value}")
    print("Steps:")
    for step in steps:
        print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if status in {"SUCCESS", "ACTIONABLE", "DEGRADED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
