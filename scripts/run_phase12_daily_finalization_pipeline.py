#!/usr/bin/env python3
"""Run the Phase 12 daily finalization pipeline."""

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
class Phase12DailyFinalizationReport:
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
        "dated_json": paths.logs_root / f"{run_date}__phase12-daily-finalization-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase12-daily-finalization-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase12_daily_finalization_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase12_daily_finalization_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__phase12-daily-finalization-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase12_daily_finalization_pipeline_board.md",
    }


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    publishing_root = paths.market_content_root / "07_publishing"
    return {
        "phase11_daily": paths.logs_root / "latest_phase11_daily_quality_loop_pipeline.json",
        "promoted_versions": versions_root / "latest_promoted_versions.json",
        "final_article_candidates": publishing_root / "latest_final_article_candidates.json",
        "final_publish_checklist": publishing_root / "latest_final_publish_checklist.json",
        "final_candidate_memory": publishing_root / "final_candidate_memory.json",
        "multiday_version_analytics": paths.logs_root / "latest_multiday_version_analytics.json",
        "wechat_workbench": paths.frontstage_root / "latest_wechat_workbench.html",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    phase11 = read_json(outputs["phase11_daily"])
    promoted = read_json(outputs["promoted_versions"])
    final_candidates = read_json(outputs["final_article_candidates"])
    checklist = read_json(outputs["final_publish_checklist"])
    memory = read_json(outputs["final_candidate_memory"])
    analytics = read_json(outputs["multiday_version_analytics"])
    promoted_summary = promoted.get("summary") if isinstance(promoted.get("summary"), dict) else {}
    final_summary = final_candidates.get("summary") if isinstance(final_candidates.get("summary"), dict) else {}
    checklist_summary = checklist.get("summary") if isinstance(checklist.get("summary"), dict) else {}
    memory_summary = memory.get("summary") if isinstance(memory.get("summary"), dict) else {}
    analytics_summary = analytics.get("summary") if isinstance(analytics.get("summary"), dict) else {}
    return {
        "phase11_status": phase11.get("status") or "UNKNOWN",
        "accepted_version_count": safe_int(promoted_summary.get("accepted_version_count")),
        "promoted_count": safe_int(promoted_summary.get("promoted_count")),
        "skipped_count": safe_int(promoted_summary.get("skipped_count")),
        "final_candidate_count": safe_int(final_summary.get("candidate_count")),
        "ready_for_final_review": safe_int(final_summary.get("ready_for_final_review")),
        "needs_final_check": safe_int(final_summary.get("needs_final_check")),
        "hold": safe_int(final_summary.get("hold")),
        "checklist_ready": safe_int(checklist_summary.get("ready")),
        "checklist_needs_attention": safe_int(checklist_summary.get("needs_attention")),
        "checklist_blocked": safe_int(checklist_summary.get("blocked")),
        "memory_final_candidate_count": safe_int(memory_summary.get("final_candidate_count")),
        "quality_trend": analytics_summary.get("quality_trend") or "UNKNOWN",
        "all_would_publish_false": all(item.get("would_publish") is False for item in list_payload(final_candidates, "candidates")),
    }


def render_markdown(report: Phase12DailyFinalizationReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 12 Daily Finalization Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Summary

- phase11_status: `{report.summary.get('phase11_status')}`
- accepted_version_count: `{report.summary.get('accepted_version_count')}`
- promoted_count: `{report.summary.get('promoted_count')}`
- final_candidate_count: `{report.summary.get('final_candidate_count')}`
- ready_for_final_review: `{report.summary.get('ready_for_final_review')}`
- needs_final_check: `{report.summary.get('needs_final_check')}`
- checklist_ready: `{report.summary.get('checklist_ready')}`
- checklist_needs_attention: `{report.summary.get('checklist_needs_attention')}`
- checklist_blocked: `{report.summary.get('checklist_blocked')}`
- quality_trend: `{report.summary.get('quality_trend')}`
- all_would_publish_false: `{report.summary.get('all_would_publish_false')}`

## Policy

- No version is accepted automatically.
- No final candidate is published automatically.
- No WeChat API or draft-box call is executed.

## Outputs

{outputs}

## Warnings

{warnings}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 12 daily finalization pipeline.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()
    planned = [
        ("phase11_daily", python_command("scripts/run_phase11_daily_quality_loop_pipeline.py")),
        ("promote_accepted_versions", python_command("scripts/promote_accepted_versions.py")),
        ("final_article_candidates", python_command("scripts/build_final_article_candidates.py")),
        ("final_publish_checklist", python_command("scripts/build_final_publish_checklist.py")),
        ("final_candidate_memory", python_command("scripts/update_final_candidate_memory.py")),
        ("multiday_version_analytics", python_command("scripts/build_multiday_version_analytics.py")),
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
    status = "FAILED" if any(step.returncode != 0 for step in steps) else "DEGRADED" if warnings or summary.get("phase11_status") == "DEGRADED" else "SUCCESS"
    report = Phase12DailyFinalizationReport(
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
        print("Phase 12 Daily Finalization Pipeline")
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
