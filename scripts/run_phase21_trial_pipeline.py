#!/usr/bin/env python3
"""Run the Phase 21 trial pipeline scaffold."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase21-trial-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase21-trial-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase21_trial_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase21_trial_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase21-trial-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase21_trial_pipeline_board.md",
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
    return f"""# Phase 21 Trial Pipeline

## Summary

- status: `{payload.get('status')}`
- phase20_status: `{summary.get('phase20_status')}`
- days_recorded: `{summary.get('days_recorded')}`
- warn_days: `{summary.get('warn_days')}`
- blocked_days: `{summary.get('blocked_days')}`
- fix_count: `{summary.get('fix_count')}`
- scaffold_only: `true`
- no_auto_publish: `true`
- no_wechat_api: `true`

## Steps

{rows}
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [("phase20_daily", python_command("scripts/run_phase20_daily_hardening_pipeline.py"))]
    commands.extend((f"trial_day_{day}", python_command("scripts/run_trial_day.py", "--day", str(day), "--skip-phase20")) for day in range(1, 6))
    commands.extend(
        [
            ("weekly_trial_retrospective", python_command("scripts/build_weekly_trial_retrospective.py")),
            ("trial_fix_pack", python_command("scripts/build_trial_fix_pack.py")),
            ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
            ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
        ]
    )
    steps = [run_step(name, command, ROOT) for name, command in commands]
    status = "SUCCESS" if all(step.returncode == 0 for step in steps) else "DEGRADED"
    phase20 = read_json(paths.logs_root / "latest_phase20_daily_hardening_pipeline.json")
    retrospective = read_json(paths.logs_root / "latest_weekly_trial_retrospective.json")
    fix_pack = read_json(paths.logs_root / "latest_trial_fix_pack.json")
    retro_summary = retrospective.get("trial_summary") if isinstance(retrospective.get("trial_summary"), dict) else {}
    fix_summary = fix_pack.get("summary") if isinstance(fix_pack.get("summary"), dict) else {}
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "summary": {
            "phase20_status": phase20.get("status", "UNKNOWN"),
            "days_recorded": retro_summary.get("days_recorded", 0),
            "pass_days": retro_summary.get("pass_days", 0),
            "warn_days": retro_summary.get("warn_days", 0),
            "blocked_days": retro_summary.get("blocked_days", 0),
            "fix_count": fix_summary.get("fix_count", 0),
            "scaffold_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_metrics_input": True,
            "no_auto_image_generation": True,
            "no_live_default": True,
            "no_config_prompt_rule_changes": True,
        },
        "steps": [step_payload(step) for step in steps],
        "notes": [
            "phase21-trial generates 5-day trial execution scaffolds from current artifacts.",
            "It does not represent five natural days of real publishing operations.",
            "For real trial execution, run trial-day-N once per operator day.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 21 Trial Pipeline")
    print("=======================")
    print(f"status: {status}")
    for key, value in payload["summary"].items():
        print(f"{key}: {value}")
    print("Steps:")
    for step in steps:
        print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
