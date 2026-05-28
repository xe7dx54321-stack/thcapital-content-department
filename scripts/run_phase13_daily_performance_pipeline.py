#!/usr/bin/env python3
"""Run the Phase 13 daily performance pipeline."""

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
from content_system.phase7_report_utils import PipelineStep, list_payload, python_command, read_json, repo_relative, run_step, safe_int, today_token, utc_now, write_json_and_markdown  # noqa: E402


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class Phase13DailyPerformanceReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    steps: tuple[PipelineStep, ...]
    summary: dict[str, Any]
    outputs: dict[str, str]
    warnings: tuple[str, ...]


def output_paths(run_date: str) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    return {
        "dated_json": paths.logs_root / f"{run_date}__phase13-daily-performance-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase13-daily-performance-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase13_daily_performance_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase13_daily_performance_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__phase13-daily-performance-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase13_daily_performance_pipeline_board.md",
    }


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    publishing_root = paths.market_content_root / "07_publishing"
    return {
        "phase12_daily": paths.logs_root / "latest_phase12_daily_finalization_pipeline.json",
        "manual_publish_sessions": publishing_root / "latest_manual_publish_sessions.json",
        "post_publish_metrics": publishing_root / "latest_post_publish_metrics.json",
        "content_performance_memory": publishing_root / "content_performance_memory.json",
        "performance_learning_feedback": paths.logs_root / "latest_performance_learning_feedback.json",
        "wechat_workbench": paths.frontstage_root / "latest_wechat_workbench.html",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    phase12 = read_json(outputs["phase12_daily"])
    sessions = read_json(outputs["manual_publish_sessions"])
    metrics = read_json(outputs["post_publish_metrics"])
    memory = read_json(outputs["content_performance_memory"])
    feedback = read_json(outputs["performance_learning_feedback"])
    session_summary = sessions.get("summary") if isinstance(sessions.get("summary"), dict) else {}
    metrics_summary = metrics.get("summary") if isinstance(metrics.get("summary"), dict) else {}
    memory_summary = memory.get("summary") if isinstance(memory.get("summary"), dict) else {}
    feedback_summary = feedback.get("summary") if isinstance(feedback.get("summary"), dict) else {}
    return {
        "phase12_status": phase12.get("status") or "UNKNOWN",
        "manual_publish_session_count": safe_int(session_summary.get("session_count")),
        "manual_published_count": safe_int(session_summary.get("published")),
        "post_publish_metrics_count": safe_int(metrics_summary.get("metrics_count")),
        "performance_record_count": safe_int(memory_summary.get("record_count")),
        "high_or_excellent_count": safe_int(memory_summary.get("high_or_excellent_count")),
        "low_count": safe_int(memory_summary.get("low_count")),
        "learning_suggestion_count": safe_int(feedback_summary.get("suggestion_count")),
        "no_auto_publish": True,
    }


def render_markdown(report: Phase13DailyPerformanceReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 13 Daily Performance Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Summary

- phase12_status: `{report.summary.get('phase12_status')}`
- manual_publish_session_count: `{report.summary.get('manual_publish_session_count')}`
- manual_published_count: `{report.summary.get('manual_published_count')}`
- post_publish_metrics_count: `{report.summary.get('post_publish_metrics_count')}`
- performance_record_count: `{report.summary.get('performance_record_count')}`
- high_or_excellent_count: `{report.summary.get('high_or_excellent_count')}`
- low_count: `{report.summary.get('low_count')}`
- learning_suggestion_count: `{report.summary.get('learning_suggestion_count')}`
- no_auto_publish: `{report.summary.get('no_auto_publish')}`

## Policy

- No publish session is created automatically.
- No session is marked published automatically.
- No metrics are recorded automatically.
- No WeChat API or backend scraping is performed.

## Outputs

{outputs}

## Warnings

{warnings}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 13 daily performance pipeline.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()
    planned = [
        ("phase12_daily", python_command("scripts/run_phase12_daily_finalization_pipeline.py")),
        ("publish_session_board", python_command("scripts/build_publish_session_board.py")),
        ("post_publish_metrics_board", python_command("scripts/build_post_publish_metrics_board.py")),
        ("content_performance_memory", python_command("scripts/update_content_performance_memory.py")),
        ("performance_learning_feedback", python_command("scripts/build_performance_learning_feedback.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps: list[PipelineStep] = []
    warnings: list[str] = []
    for name, command in planned:
        step = run_step(name, command, REPO_ROOT)
        steps.append(step)
        if step.returncode != 0:
            warnings.append(f"{name} exited with return code {step.returncode}.")
            if not args.continue_on_error:
                break
    outputs = collect_outputs()
    summary = build_summary(outputs)
    status = "FAILED" if any(step.returncode != 0 for step in steps) else "DEGRADED" if warnings or summary.get("phase12_status") == "DEGRADED" else "SUCCESS"
    report = Phase13DailyPerformanceReport(
        SCHEMA_VERSION,
        utc_now(),
        today_token(),
        status,
        tuple(steps),
        summary,
        {key: repo_relative(path, REPO_ROOT) for key, path in outputs.items()},
        tuple(warnings),
    )
    written = write_json_and_markdown(asdict(report), render_markdown(report), output_paths(report.run_date))
    if args.json:
        print(json.dumps({**asdict(report), "pipeline_outputs": {key: str(path) for key, path in written.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Phase 13 Daily Performance Pipeline")
        print("===================================")
        print(f"status: {report.status}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
