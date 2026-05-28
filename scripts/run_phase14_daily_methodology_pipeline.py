#!/usr/bin/env python3
"""Run the Phase 14 daily methodology pipeline."""

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
class Phase14DailyMethodologyReport:
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
        "dated_json": paths.logs_root / f"{run_date}__phase14-daily-methodology-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase14-daily-methodology-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase14_daily_methodology_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase14_daily_methodology_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__phase14-daily-methodology-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase14_daily_methodology_pipeline_board.md",
    }


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    return {
        "phase13_daily": paths.logs_root / "latest_phase13_daily_performance_pipeline.json",
        "methodology_topic_scores": paths.market_content_root / "03_topic_candidates" / "latest_methodology_topic_scores.json",
        "methodology_article_review": paths.market_content_root / "05_draft_packs" / "latest_methodology_article_review.json",
        "chief_editor_methodology_context": paths.logs_root / "latest_chief_editor_methodology_context.json",
        "methodology_performance_alignment": paths.logs_root / "latest_methodology_performance_alignment.json",
        "wechat_workbench": paths.frontstage_root / "latest_wechat_workbench.html",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    phase13 = read_json(outputs["phase13_daily"])
    topic_scores = read_json(outputs["methodology_topic_scores"])
    article_review = read_json(outputs["methodology_article_review"])
    context = read_json(outputs["chief_editor_methodology_context"])
    alignment = read_json(outputs["methodology_performance_alignment"])
    topic_summary = topic_scores.get("summary") if isinstance(topic_scores.get("summary"), dict) else {}
    article_summary = article_review.get("summary") if isinstance(article_review.get("summary"), dict) else {}
    alignment_summary = alignment.get("summary") if isinstance(alignment.get("summary"), dict) else {}
    return {
        "phase13_status": phase13.get("status") or "UNKNOWN",
        "topic_count": safe_int(topic_summary.get("topic_count")),
        "write": safe_int(topic_summary.get("write")),
        "watch": safe_int(topic_summary.get("watch")),
        "hold": safe_int(topic_summary.get("hold")),
        "reject": safe_int(topic_summary.get("reject")),
        "article_count": safe_int(article_summary.get("article_count")),
        "ready": safe_int(article_summary.get("ready")),
        "revise": safe_int(article_summary.get("revise")),
        "article_hold": safe_int(article_summary.get("hold")),
        "chief_editor_context_selected_article": context.get("selected_article_id") or "",
        "alignment_insight_count": safe_int(alignment_summary.get("insight_count")),
        "auto_apply": False,
        "no_auto_publish": True,
    }


def render_markdown(report: Phase14DailyMethodologyReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 14 Daily Methodology Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Summary

- phase13_status: `{report.summary.get('phase13_status')}`
- topic_count: `{report.summary.get('topic_count')}`
- write / watch / hold / reject: `{report.summary.get('write')}` / `{report.summary.get('watch')}` / `{report.summary.get('hold')}` / `{report.summary.get('reject')}`
- article_count: `{report.summary.get('article_count')}`
- ready / revise / hold: `{report.summary.get('ready')}` / `{report.summary.get('revise')}` / `{report.summary.get('article_hold')}`
- chief_editor_context_selected_article: `{report.summary.get('chief_editor_context_selected_article')}`
- alignment_insight_count: `{report.summary.get('alignment_insight_count')}`
- auto_apply: `{report.summary.get('auto_apply')}`
- no_auto_publish: `{report.summary.get('no_auto_publish')}`

## Policy

- Methodology scores are advisory and do not replace human judgment.
- Methodology feedback does not auto-change config, prompts, or rules.
- No publishing, WeChat API, or draft-box integration is performed.

## Outputs

{outputs}

## Warnings

{warnings}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 14 daily methodology pipeline.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()
    planned = [
        ("phase13_daily", python_command("scripts/run_phase13_daily_performance_pipeline.py")),
        ("topic_methodology_validate", python_command("scripts/validate_topic_selection_methodology.py")),
        ("article_methodology_validate", python_command("scripts/validate_article_quality_methodology.py")),
        ("content_recipes_validate", python_command("scripts/validate_content_strategy_recipes.py")),
        ("methodology_topic_score", python_command("scripts/score_topics_with_methodology.py")),
        ("methodology_article_review", python_command("scripts/review_articles_with_methodology.py")),
        ("chief_editor_methodology_context", python_command("scripts/build_chief_editor_methodology_context.py")),
        ("methodology_performance_alignment", python_command("scripts/build_methodology_performance_alignment.py")),
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
    status = "FAILED" if any(step.returncode != 0 for step in steps) else "DEGRADED" if warnings or summary.get("phase13_status") == "DEGRADED" else "SUCCESS"
    report = Phase14DailyMethodologyReport(
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
        print("Phase 14 Daily Methodology Pipeline")
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
