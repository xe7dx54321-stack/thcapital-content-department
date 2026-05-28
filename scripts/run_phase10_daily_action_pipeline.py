#!/usr/bin/env python3
"""Run the Phase 10 daily action pipeline."""

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
class Phase10DailyActionPipelineReport:
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
        "dated_json": paths.logs_root / f"{run_date}__phase10-daily-action-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase10-daily-action-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase10_daily_action_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase10_daily_action_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__phase10-daily-action-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase10_daily_action_pipeline_board.md",
    }


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "phase9_daily": paths.logs_root / "latest_phase9_daily_workbench_pipeline.json",
        "approved_actions": paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json",
        "rewrite_versions": versions_root / "latest_rewrite_versions.json",
        "evidence_expansion": versions_root / "latest_evidence_expansion.json",
        "topic_replacements": versions_root / "latest_topic_replacements.json",
        "versioned_article_preview": paths.frontstage_root / "latest_versioned_article_preview.html",
        "versioned_article_preview_json": paths.logs_root / "latest_versioned_article_preview.json",
        "feedback_memory": paths.market_content_root / "09_workbench_actions" / "workbench_feedback_memory.json",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    phase9 = read_json(outputs["phase9_daily"])
    approval = read_json(outputs["approved_actions"])
    rewrite = read_json(outputs["rewrite_versions"])
    evidence = read_json(outputs["evidence_expansion"])
    topic = read_json(outputs["topic_replacements"])
    preview = read_json(outputs["versioned_article_preview_json"])
    actions = list_payload(approval, "actions")
    return {
        "phase9_status": phase9.get("status") or "UNKNOWN",
        "action_count": len(actions),
        "approved_count": sum(1 for item in actions if item.get("approval_status") == "APPROVED"),
        "rewrite_version_count": len(list_payload(rewrite, "versions")),
        "evidence_expansion_count": len(list_payload(evidence, "expansions")),
        "topic_replacement_count": len(list_payload(topic, "replacements")),
        "versioned_preview_count": safe_int(preview.get("version_count")),
        "do_not_overwrite_original": preview.get("do_not_overwrite_original") is True,
    }


def render_markdown(report: Phase10DailyActionPipelineReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 10 Daily Action Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Summary

- phase9_status: `{report.summary.get('phase9_status')}`
- action_count: `{report.summary.get('action_count')}`
- approved_count: `{report.summary.get('approved_count')}`
- rewrite_version_count: `{report.summary.get('rewrite_version_count')}`
- evidence_expansion_count: `{report.summary.get('evidence_expansion_count')}`
- topic_replacement_count: `{report.summary.get('topic_replacement_count')}`
- do_not_overwrite_original: `{report.summary.get('do_not_overwrite_original')}`

## Outputs

{outputs}

## Warnings

{warnings}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 10 daily action pipeline.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()
    planned = [
        ("phase9_daily", python_command("scripts/run_phase9_daily_workbench_pipeline.py")),
        ("action_approval_board", python_command("scripts/build_action_approval_board.py")),
        ("rewrite_actions", python_command("scripts/execute_rewrite_actions.py")),
        ("evidence_actions", python_command("scripts/execute_evidence_expansion_actions.py")),
        ("topic_actions", python_command("scripts/execute_topic_replacement_actions.py")),
        ("versioned_article_preview", python_command("scripts/build_versioned_article_preview.py")),
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
    status = "FAILED" if any(step.returncode != 0 for step in steps) else "DEGRADED" if warnings or summary.get("phase9_status") == "DEGRADED" else "SUCCESS"
    report = Phase10DailyActionPipelineReport(
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
        print("Phase 10 Daily Action Pipeline")
        print("==============================")
        print(f"status: {report.status}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
