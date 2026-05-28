#!/usr/bin/env python3
"""Run the Phase 11 daily quality loop pipeline."""

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
from content_system.phase7_report_utils import PipelineStep, list_payload, python_command, read_json, repo_relative, run_step, safe_float, safe_int, today_token, utc_now, write_json_and_markdown  # noqa: E402


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class Phase11DailyQualityLoopReport:
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
        "dated_json": paths.logs_root / f"{run_date}__phase11-daily-quality-loop-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase11-daily-quality-loop-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase11_daily_quality_loop_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase11_daily_quality_loop_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__phase11-daily-quality-loop-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase11_daily_quality_loop_pipeline_board.md",
    }


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "phase10_daily": paths.logs_root / "latest_phase10_daily_action_pipeline.json",
        "version_comparison_scores": versions_root / "latest_version_comparison_scores.json",
        "version_review_decisions": versions_root / "latest_version_review_decisions.json",
        "article_version_memory": versions_root / "article_version_memory.json",
        "action_effectiveness": paths.logs_root / "latest_action_effectiveness_analytics.json",
        "prompt_rule_regression": paths.logs_root / "latest_prompt_rule_regression_dashboard.json",
        "wechat_workbench": paths.frontstage_root / "latest_wechat_workbench.html",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    phase10 = read_json(outputs["phase10_daily"])
    comparisons = read_json(outputs["version_comparison_scores"])
    decisions = read_json(outputs["version_review_decisions"])
    memory = read_json(outputs["article_version_memory"])
    analytics = read_json(outputs["action_effectiveness"])
    regression = read_json(outputs["prompt_rule_regression"])
    comp_summary = comparisons.get("summary") if isinstance(comparisons.get("summary"), dict) else {}
    decision_summary = decisions.get("summary") if isinstance(decisions.get("summary"), dict) else {}
    memory_summary = memory.get("summary") if isinstance(memory.get("summary"), dict) else {}
    analytics_summary = analytics.get("summary") if isinstance(analytics.get("summary"), dict) else {}
    return {
        "phase10_status": phase10.get("status") or "UNKNOWN",
        "comparison_count": safe_int(comp_summary.get("comparison_count")),
        "accept_recommended": safe_int(comp_summary.get("accept_recommended")),
        "reject_recommended": safe_int(comp_summary.get("reject_recommended")),
        "revise_more_recommended": safe_int(comp_summary.get("revise_more_recommended")),
        "human_review_recommended": safe_int(comp_summary.get("human_review_recommended")),
        "version_decision_accepted": safe_int(decision_summary.get("accepted")),
        "version_decision_rejected": safe_int(decision_summary.get("rejected")),
        "version_memory_count": safe_int(memory_summary.get("version_count")),
        "action_average_score_delta": safe_float(analytics_summary.get("average_score_delta")),
        "regression_suggestion_count": len(list_payload(regression, "suggestions")),
    }


def render_markdown(report: Phase11DailyQualityLoopReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 11 Daily Quality Loop Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Summary

- phase10_status: `{report.summary.get('phase10_status')}`
- comparison_count: `{report.summary.get('comparison_count')}`
- accept_recommended: `{report.summary.get('accept_recommended')}`
- reject_recommended: `{report.summary.get('reject_recommended')}`
- revise_more_recommended: `{report.summary.get('revise_more_recommended')}`
- human_review_recommended: `{report.summary.get('human_review_recommended')}`
- accepted decisions: `{report.summary.get('version_decision_accepted')}`
- rejected decisions: `{report.summary.get('version_decision_rejected')}`
- version_memory_count: `{report.summary.get('version_memory_count')}`
- action_average_score_delta: `{report.summary.get('action_average_score_delta')}`
- regression_suggestion_count: `{report.summary.get('regression_suggestion_count')}`

## Policy

- No version is accepted automatically.
- No original draft is overwritten.
- No prompt or rule file is modified automatically.

## Outputs

{outputs}

## Warnings

{warnings}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 11 daily quality loop pipeline.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()
    planned = [
        ("phase10_daily", python_command("scripts/run_phase10_daily_action_pipeline.py")),
        ("version_comparison_score", python_command("scripts/score_article_versions.py")),
        ("version_review_board", python_command("scripts/build_version_review_board.py")),
        ("article_version_memory", python_command("scripts/update_article_version_memory.py")),
        ("action_effectiveness", python_command("scripts/build_action_effectiveness_analytics.py")),
        ("prompt_rule_regression", python_command("scripts/build_prompt_rule_regression_dashboard.py")),
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
    status = "FAILED" if any(step.returncode != 0 for step in steps) else "DEGRADED" if warnings or summary.get("phase10_status") == "DEGRADED" else "SUCCESS"
    report = Phase11DailyQualityLoopReport(
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
        print("Phase 11 Daily Quality Loop Pipeline")
        print("====================================")
        print(f"status: {report.status}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
