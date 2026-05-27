#!/usr/bin/env python3
"""Run the Phase 8 daily production dry-run pipeline."""

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
class Phase8DailyProductionPipelineReport:
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
        "dated_json": paths.logs_root / f"{run_date}__phase8-daily-production-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase8-daily-production-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase8_daily_production_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase8_daily_production_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__phase8-daily-production-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase8_daily_production_pipeline_board.md",
    }


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    return {
        "phase7_daily": paths.logs_root / "latest_phase7_daily_pipeline.json",
        "runtime_store_summary": paths.logs_root / "latest_runtime_store_summary.json",
        "artifact_repository_summary": paths.logs_root / "latest_artifact_repository_summary.json",
        "publishing_dry_run": paths.market_content_root / "07_publishing" / "latest_publishing_dry_run.json",
        "human_review_console": paths.logs_root / "latest_human_review_console.json",
        "cost_budget_guard": paths.logs_root / "latest_cost_budget_guard.json",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    phase7 = read_json(outputs["phase7_daily"])
    runtime = read_json(outputs["runtime_store_summary"])
    repo = read_json(outputs["artifact_repository_summary"])
    publishing = read_json(outputs["publishing_dry_run"])
    console = read_json(outputs["human_review_console"])
    cost = read_json(outputs["cost_budget_guard"])
    runtime_summary = runtime.get("summary") if isinstance(runtime.get("summary"), dict) else {}
    repo_summary = repo.get("summary") if isinstance(repo.get("summary"), dict) else {}
    publishing_summary = publishing.get("summary") if isinstance(publishing.get("summary"), dict) else {}
    console_summary = console.get("summary") if isinstance(console.get("summary"), dict) else {}
    return {
        "phase7_status": phase7.get("status") or "UNKNOWN",
        "runtime_pipeline_runs": safe_int(runtime_summary.get("pipeline_runs")),
        "runtime_agent_runs": safe_int(runtime_summary.get("agent_runs")),
        "runtime_content_artifacts": safe_int(runtime_summary.get("content_artifacts")),
        "runtime_publishing_candidates": safe_int(runtime_summary.get("publishing_candidates")),
        "repository_recent_artifacts": len(repo_summary.get("recent_artifacts") or []) if isinstance(repo_summary.get("recent_artifacts"), list) else 0,
        "publishing_dry_run_status": publishing.get("status") or "UNKNOWN",
        "publishing_ready_count": safe_int(publishing_summary.get("ready_count")),
        "publishing_not_ready_count": safe_int(publishing_summary.get("not_ready_count")),
        "publishing_hold_count": safe_int(publishing_summary.get("hold_count")),
        "human_review_console_status": console.get("status") or "UNKNOWN",
        "pending_feedback": safe_int(console_summary.get("pending_feedback")),
        "cost_budget_status": cost.get("status") or "UNKNOWN",
        "cost_recommended_mode": cost.get("recommended_mode") or "UNKNOWN",
    }


def determine_status(steps: list[PipelineStep], summary: dict[str, Any], warnings: list[str]) -> str:
    if any(step.returncode != 0 for step in steps):
        return "FAILED"
    if warnings or summary.get("publishing_not_ready_count") or summary.get("cost_budget_status") == "BLOCK":
        return "DEGRADED"
    return "SUCCESS"


def render_markdown(report: Phase8DailyProductionPipelineReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 8 Daily Production Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Key Metrics

- phase7_status: `{report.summary.get('phase7_status')}`
- runtime_pipeline_runs: `{report.summary.get('runtime_pipeline_runs')}`
- runtime_agent_runs: `{report.summary.get('runtime_agent_runs')}`
- runtime_content_artifacts: `{report.summary.get('runtime_content_artifacts')}`
- runtime_publishing_candidates: `{report.summary.get('runtime_publishing_candidates')}`
- publishing_dry_run_status: `{report.summary.get('publishing_dry_run_status')}`
- publishing_ready_count: `{report.summary.get('publishing_ready_count')}`
- publishing_not_ready_count: `{report.summary.get('publishing_not_ready_count')}`
- human_review_console_status: `{report.summary.get('human_review_console_status')}`
- pending_feedback: `{report.summary.get('pending_feedback')}`
- cost_budget_status: `{report.summary.get('cost_budget_status')}`
- cost_recommended_mode: `{report.summary.get('cost_recommended_mode')}`

## Outputs

{outputs}

## Warnings

{warnings}
"""


def write_report(report: Phase8DailyProductionPipelineReport) -> dict[str, Path]:
    outputs = output_paths(report.run_date)
    return write_json_and_markdown(asdict(report), render_markdown(report), outputs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 8 daily production pipeline.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()
    planned = [
        ("phase7_daily", python_command("scripts/run_phase7_daily_pipeline.py")),
        ("runtime_store_init", python_command("scripts/init_runtime_store.py")),
        ("runtime_store_sync", python_command("scripts/sync_runtime_store.py")),
        ("runtime_store_summary", python_command("scripts/build_runtime_store_summary.py")),
        ("artifact_repository_sync", python_command("scripts/sync_artifact_repository.py")),
        ("publishing_dry_run", python_command("scripts/run_publishing_dry_run.py")),
        ("human_review_console", python_command("scripts/run_human_review_console.py", "--summary")),
        ("cost_budget_guard", python_command("scripts/check_cost_budget_guard.py")),
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
    outputs_map = collect_outputs()
    summary = build_summary(outputs_map)
    outputs = {key: repo_relative(path, REPO_ROOT) for key, path in outputs_map.items()}
    report = Phase8DailyProductionPipelineReport(
        SCHEMA_VERSION,
        utc_now(),
        today_token(),
        determine_status(steps, summary, warnings),
        tuple(steps),
        summary,
        outputs,
        tuple(warnings),
    )
    written = write_report(report)
    if args.json:
        print(json.dumps({**asdict(report), "pipeline_outputs": {key: str(path) for key, path in written.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Phase 8 Daily Production Pipeline")
        print("=================================")
        print(f"status: {report.status}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
