#!/usr/bin/env python3
"""Run the Phase 9 daily WeChat workbench pipeline."""

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
class Phase9DailyWorkbenchPipelineReport:
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
        "dated_json": paths.logs_root / f"{run_date}__phase9-daily-workbench-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase9-daily-workbench-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase9_daily_workbench_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase9_daily_workbench_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__phase9-daily-workbench-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase9_daily_workbench_pipeline_board.md",
    }


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    return {
        "phase8_daily": paths.logs_root / "latest_phase8_daily_production_pipeline.json",
        "workbench_data": paths.frontstage_root / "latest_wechat_workbench_data.json",
        "article_preview": paths.frontstage_root / "latest_wechat_article_preview.html",
        "workbench_context": paths.logs_root / "latest_workbench_context.json",
        "workbench_html": paths.frontstage_root / "latest_wechat_workbench.html",
        "feedback_memory": paths.market_content_root / "09_workbench_actions" / "workbench_feedback_memory.json",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    phase8 = read_json(outputs["phase8_daily"])
    data = read_json(outputs["workbench_data"])
    context = read_json(outputs["workbench_context"])
    memory = read_json(outputs["feedback_memory"])
    data_summary = data.get("summary") if isinstance(data.get("summary"), dict) else {}
    return {
        "phase8_status": phase8.get("status") or "UNKNOWN",
        "topic_count": safe_int(data_summary.get("topic_count")),
        "article_count": safe_int(data_summary.get("article_count")),
        "ready_count": safe_int(data_summary.get("ready_count")),
        "selected_article_id": data.get("selected_article_id") or "",
        "context_selected_article": (context.get("selected_article") or {}).get("article_id") if isinstance(context.get("selected_article"), dict) else "",
        "feedback_preference_count": len(memory.get("preferences") or []) if isinstance(memory.get("preferences"), list) else 0,
    }


def render_markdown(report: Phase9DailyWorkbenchPipelineReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 9 Daily Workbench Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Key Metrics

- phase8_status: `{report.summary.get('phase8_status')}`
- topic_count: `{report.summary.get('topic_count')}`
- article_count: `{report.summary.get('article_count')}`
- ready_count: `{report.summary.get('ready_count')}`
- selected_article_id: `{report.summary.get('selected_article_id')}`
- feedback_preference_count: `{report.summary.get('feedback_preference_count')}`

## Outputs

{outputs}

## Warnings

{warnings}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 9 daily workbench pipeline.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()
    planned = [
        ("phase8_daily", python_command("scripts/run_phase8_daily_production_pipeline.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_article_preview", python_command("scripts/render_wechat_article_preview.py")),
        ("workbench_context", python_command("scripts/build_workbench_context.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
        ("workbench_feedback_memory", python_command("scripts/update_workbench_feedback_memory.py")),
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
    output_map = collect_outputs()
    summary = build_summary(output_map)
    status = "FAILED" if any(step.returncode != 0 for step in steps) else "DEGRADED" if warnings or summary.get("phase8_status") == "DEGRADED" else "SUCCESS"
    report = Phase9DailyWorkbenchPipelineReport(
        SCHEMA_VERSION,
        utc_now(),
        today_token(),
        status,
        tuple(steps),
        summary,
        {key: repo_relative(path, REPO_ROOT) for key, path in output_map.items()},
        tuple(warnings),
    )
    written = write_json_and_markdown(asdict(report), render_markdown(report), output_paths(report.run_date))
    if args.json:
        print(json.dumps({**asdict(report), "pipeline_outputs": {key: str(path) for key, path in written.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Phase 9 Daily Workbench Pipeline")
        print("================================")
        print(f"status: {report.status}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
