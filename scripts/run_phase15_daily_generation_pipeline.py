#!/usr/bin/env python3
"""Run the Phase 15 daily generation and visual strategy pipeline."""

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
class Phase15DailyGenerationReport:
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
        "dated_json": paths.logs_root / f"{run_date}__phase15-daily-generation-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase15-daily-generation-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase15_daily_generation_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase15_daily_generation_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__phase15-daily-generation-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase15_daily_generation_pipeline_board.md",
    }


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    draft_root = paths.market_content_root / "05_draft_packs"
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "phase14_daily": paths.logs_root / "latest_phase14_daily_methodology_pipeline.json",
        "methodology_briefs": draft_root / "latest_methodology_content_briefs.json",
        "methodology_outlines": draft_root / "latest_methodology_content_outlines.json",
        "methodology_drafts": draft_root / "latest_methodology_content_drafts.json",
        "methodology_rewrite_versions": versions_root / "latest_methodology_rewrite_versions.json",
        "article_visual_plans": draft_root / "latest_article_visual_plans.json",
        "image_asset_requests": draft_root / "latest_image_asset_requests.json",
        "methodology_regression_tests": paths.logs_root / "latest_methodology_regression_tests.json",
        "human_methodology_calibration": paths.logs_root / "latest_human_methodology_calibration.json",
        "wechat_workbench": paths.frontstage_root / "latest_wechat_workbench.html",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    phase14 = read_json(outputs["phase14_daily"])
    briefs = read_json(outputs["methodology_briefs"])
    outlines = read_json(outputs["methodology_outlines"])
    drafts = read_json(outputs["methodology_drafts"])
    rewrites = read_json(outputs["methodology_rewrite_versions"])
    visual_plans = read_json(outputs["article_visual_plans"])
    image_requests = read_json(outputs["image_asset_requests"])
    regression = read_json(outputs["methodology_regression_tests"])
    calibration = read_json(outputs["human_methodology_calibration"])
    return {
        "phase14_status": phase14.get("status") or "UNKNOWN",
        "brief_count": safe_int((briefs.get("summary") or {}).get("brief_count")) if isinstance(briefs.get("summary"), dict) else 0,
        "outline_count": safe_int((outlines.get("summary") or {}).get("outline_count")) if isinstance(outlines.get("summary"), dict) else 0,
        "draft_count": safe_int((drafts.get("summary") or {}).get("draft_count")) if isinstance(drafts.get("summary"), dict) else 0,
        "methodology_rewrite_version_count": safe_int((rewrites.get("summary") or {}).get("version_count")) if isinstance(rewrites.get("summary"), dict) else 0,
        "visual_plan_count": safe_int((visual_plans.get("summary") or {}).get("plan_count")) if isinstance(visual_plans.get("summary"), dict) else 0,
        "visual_count": safe_int((visual_plans.get("summary") or {}).get("visual_count")) if isinstance(visual_plans.get("summary"), dict) else 0,
        "image_request_count": safe_int((image_requests.get("summary") or {}).get("request_count")) if isinstance(image_requests.get("summary"), dict) else 0,
        "regression_fail_count": safe_int((regression.get("summary") or {}).get("fail_count")) if isinstance(regression.get("summary"), dict) else 0,
        "calibration_topic_count": safe_int((calibration.get("summary") or {}).get("topic_count")) if isinstance(calibration.get("summary"), dict) else 0,
        "do_not_auto_generate_images": True,
        "do_not_auto_publish": True,
        "auto_apply": False,
    }


def render_markdown(report: Phase15DailyGenerationReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 15 Daily Generation Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Summary

- phase14_status: `{report.summary.get('phase14_status')}`
- brief_count: `{report.summary.get('brief_count')}`
- outline_count: `{report.summary.get('outline_count')}`
- draft_count: `{report.summary.get('draft_count')}`
- methodology_rewrite_version_count: `{report.summary.get('methodology_rewrite_version_count')}`
- visual_plan_count: `{report.summary.get('visual_plan_count')}`
- visual_count: `{report.summary.get('visual_count')}`
- image_request_count: `{report.summary.get('image_request_count')}`
- regression_fail_count: `{report.summary.get('regression_fail_count')}`
- do_not_auto_generate_images: `{report.summary.get('do_not_auto_generate_images')}`
- do_not_auto_publish: `{report.summary.get('do_not_auto_publish')}`
- auto_apply: `{report.summary.get('auto_apply')}`

## Policy

- No image generation model is called.
- No image file is created or committed.
- No WeChat API or draft-box integration is performed.
- No config, prompt, or rule is modified automatically.

## Outputs

{outputs}

## Warnings

{warnings}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 15 daily generation pipeline.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()
    planned = [
        ("phase14_daily", python_command("scripts/run_phase14_daily_methodology_pipeline.py")),
        ("methodology_briefs", python_command("scripts/build_methodology_briefs.py")),
        ("methodology_outlines", python_command("scripts/build_methodology_outlines.py")),
        ("methodology_drafts", python_command("scripts/build_methodology_drafts.py")),
        ("methodology_rewrite_actions", python_command("scripts/execute_methodology_rewrite_actions.py")),
        ("visual_methodology_validate", python_command("scripts/validate_article_visual_methodology.py")),
        ("article_visual_plans", python_command("scripts/build_visual_plans.py")),
        ("image_asset_requests", python_command("scripts/build_image_asset_requests.py")),
        ("methodology_regression_tests", python_command("scripts/run_methodology_regression_tests.py")),
        ("human_methodology_calibration", python_command("scripts/build_human_methodology_calibration_board.py")),
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
    status = "FAILED" if any(step.returncode != 0 for step in steps) else "DEGRADED" if warnings or summary.get("phase14_status") == "DEGRADED" else "SUCCESS"
    report = Phase15DailyGenerationReport(
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
        print("Phase 15 Daily Generation Pipeline")
        print("==================================")
        print(f"status: {report.status}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
