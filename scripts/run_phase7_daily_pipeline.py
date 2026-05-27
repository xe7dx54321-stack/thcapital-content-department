#!/usr/bin/env python3
"""Run the Phase 7 daily live-mode grey release pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import PipelineStep, python_command, read_json, repo_relative, run_step, safe_int, today_token, utc_now, write_json_and_markdown  # noqa: E402


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class Phase7DailyPipelineReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    steps: tuple[PipelineStep, ...]
    summary: dict[str, Any]
    outputs: dict[str, str]
    warnings: tuple[str, ...]


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    return {
        "phase6_daily": paths.logs_root / "latest_phase6_daily_agent_pipeline.json",
        "minimax_proponent_live_pilot": paths.logs_root / "latest_minimax_proponent_live_pilot.json",
        "claude_critic_live_pilot": paths.logs_root / "latest_claude_critic_live_pilot.json",
        "claude_judge_live_pilot": paths.logs_root / "latest_claude_judge_live_pilot.json",
        "claude_rewrite_live_pilot": paths.logs_root / "latest_claude_rewrite_live_pilot.json",
        "llm_ab_comparison": paths.logs_root / "latest_llm_ab_comparison.json",
        "daily_scheduler": paths.logs_root / "latest_daily_scheduler.json",
        "failure_notification": paths.logs_root / "latest_failure_notification.json",
        "retry_fallback_runner": paths.logs_root / "latest_retry_fallback_runner.json",
        "weekly_content_retro": paths.logs_root / "latest_weekly_content_retro.json",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    phase6 = read_json(outputs["phase6_daily"])
    minimax = read_json(outputs["minimax_proponent_live_pilot"])
    critic = read_json(outputs["claude_critic_live_pilot"])
    judge = read_json(outputs["claude_judge_live_pilot"])
    rewrite = read_json(outputs["claude_rewrite_live_pilot"])
    ab = read_json(outputs["llm_ab_comparison"])
    failure = read_json(outputs["failure_notification"])
    retry = read_json(outputs["retry_fallback_runner"])
    retro = read_json(outputs["weekly_content_retro"])
    ab_summary = ab.get("summary") if isinstance(ab.get("summary"), dict) else {}
    failure_summary = failure.get("summary") if isinstance(failure.get("summary"), dict) else {}
    return {
        "phase6_status": phase6.get("status") or "UNKNOWN",
        "minimax_proponent_pilot_status": minimax.get("status") or "UNKNOWN",
        "claude_critic_pilot_status": critic.get("status") or "UNKNOWN",
        "claude_judge_pilot_status": judge.get("status") or "UNKNOWN",
        "claude_rewrite_pilot_status": rewrite.get("status") or "UNKNOWN",
        "llm_ab_status": ab.get("status") or "UNKNOWN",
        "judge_conflict_count": safe_int(ab_summary.get("judge_decision_conflict_count")),
        "fallback_count": safe_int(ab_summary.get("fallback_count")),
        "failure_count": safe_int(failure_summary.get("pipeline_failure_count")) + safe_int(failure_summary.get("live_failure_count")),
        "retry_plan_count": len(retry.get("retry_plan") or []) if isinstance(retry.get("retry_plan"), list) else 0,
        "weekly_retro_status": retro.get("status") or "UNKNOWN",
    }


def output_paths(run_date: str) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    return {
        "dated_json": paths.logs_root / f"{run_date}__phase7-daily-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase7-daily-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase7_daily_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase7_daily_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__phase7-daily-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase7_daily_pipeline_board.md",
    }


def determine_status(steps: list[PipelineStep], summary: dict[str, Any], warnings: list[str]) -> str:
    if any(step.returncode != 0 for step in steps):
        return "FAILED"
    if warnings or safe_int(summary.get("failure_count")) > 0:
        return "DEGRADED"
    return "SUCCESS"


def render_markdown(report: Phase7DailyPipelineReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 7 Daily Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Key Metrics

- phase6_status: `{report.summary.get('phase6_status')}`
- minimax_proponent_pilot_status: `{report.summary.get('minimax_proponent_pilot_status')}`
- claude_critic_pilot_status: `{report.summary.get('claude_critic_pilot_status')}`
- claude_judge_pilot_status: `{report.summary.get('claude_judge_pilot_status')}`
- claude_rewrite_pilot_status: `{report.summary.get('claude_rewrite_pilot_status')}`
- llm_ab_status: `{report.summary.get('llm_ab_status')}`
- judge_conflict_count: `{report.summary.get('judge_conflict_count')}`
- fallback_count: `{report.summary.get('fallback_count')}`
- failure_count: `{report.summary.get('failure_count')}`
- retry_plan_count: `{report.summary.get('retry_plan_count')}`
- weekly_retro_status: `{report.summary.get('weekly_retro_status')}`

## Outputs

{outputs}

## Warnings

{warnings}
"""


def write_report(report: Phase7DailyPipelineReport) -> dict[str, Path]:
    outputs = output_paths(report.run_date)
    return write_json_and_markdown(asdict(report), render_markdown(report), outputs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 7 daily pipeline.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()
    planned = [
        ("phase6_daily", python_command("scripts/run_phase6_daily_agent_pipeline.py")),
        ("minimax_proponent_live_pilot", python_command("scripts/run_minimax_proponent_live_pilot.py")),
        ("claude_critic_live_pilot", python_command("scripts/run_claude_critic_live_pilot.py")),
        ("claude_judge_live_pilot", python_command("scripts/run_claude_judge_live_pilot.py")),
        ("claude_rewrite_live_pilot", python_command("scripts/run_claude_rewrite_live_pilot.py")),
        ("llm_ab_comparison", python_command("scripts/build_llm_ab_comparison.py")),
        ("daily_scheduler", python_command("scripts/run_daily_scheduler.py", "--dry-run")),
        ("failure_notification", python_command("scripts/build_failure_notification_report.py")),
        ("retry_fallback_runner", python_command("scripts/run_retry_fallback_runner.py")),
        ("weekly_content_retro", python_command("scripts/build_weekly_content_retro.py")),
    ]
    steps: list[PipelineStep] = []
    warnings: list[str] = []
    for name, command in planned:
        step = run_step(name, command, REPO_ROOT)
        steps.append(step)
        if step.returncode != 0:
            warnings.append(f"{name} exited with return code {step.returncode}.")
            if not args.continue_on_error:
                warnings.append(f"Stopped after {name}; use --continue-on-error to attempt downstream reports.")
                break
    output_map = collect_outputs()
    summary = build_summary(output_map)
    outputs = {key: repo_relative(path, REPO_ROOT) for key, path in output_map.items()}
    status = determine_status(steps, summary, warnings)
    report = Phase7DailyPipelineReport(SCHEMA_VERSION, utc_now(), today_token(), status, tuple(steps), summary, outputs, tuple(warnings))
    written = write_report(report)
    if args.json:
        print(json.dumps({**asdict(report), "pipeline_outputs": {key: str(value) for key, value in written.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Phase 7 Daily Pipeline")
        print("======================")
        print(f"status: {report.status}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
        print("\nReports:")
        for key, path in written.items():
            print(f"  {key}: {path}")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
