#!/usr/bin/env python3
"""Run the Phase 2 daily content production quality pipeline."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402


@dataclass(frozen=True)
class PipelineStep:
    name: str
    command: str
    returncode: int
    status: str
    started_at: str
    finished_at: str
    stdout_tail: str
    stderr_tail: str


@dataclass(frozen=True)
class Phase2DailyPipelineReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    steps: tuple[PipelineStep, ...]
    summary: dict[str, Any]
    outputs: dict[str, str]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def tail_text(text: str, max_lines: int = 20) -> str:
    sanitized = text.replace(str(REPO_ROOT), "<repo_root>")
    lines = sanitized.strip().splitlines()
    return "\n".join(lines[-max_lines:])


def run_step(name: str, command: list[str]) -> PipelineStep:
    started_at = utc_now()
    completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    finished_at = utc_now()
    return PipelineStep(
        name=name,
        command=" ".join(command),
        returncode=completed.returncode,
        status="OK" if completed.returncode == 0 else "FAILED",
        started_at=started_at,
        finished_at=finished_at,
        stdout_tail=tail_text(completed.stdout),
        stderr_tail=tail_text(completed.stderr),
    )


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def collect_output_paths() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    draft_root = paths.market_content_root / "05_draft_packs"
    return {
        "phase1_pipeline": paths.logs_root / "latest_phase1_daily_pipeline.json",
        "content_briefs": draft_root / "latest_content_briefs.json",
        "content_outlines": draft_root / "latest_content_outlines.json",
        "content_drafts": draft_root / "latest_content_drafts.json",
        "quality_review": draft_root / "latest_content_quality_review.json",
        "platform_packages": draft_root / "latest_platform_packages.json",
        "content_workbench": paths.logs_root / "latest_content_workbench.json",
    }


def build_summary(output_paths: dict[str, Path]) -> dict[str, Any]:
    phase1 = read_json(output_paths["phase1_pipeline"])
    briefs = read_json(output_paths["content_briefs"])
    outlines = read_json(output_paths["content_outlines"])
    drafts = read_json(output_paths["content_drafts"])
    reviews = read_json(output_paths["quality_review"])
    packages = read_json(output_paths["platform_packages"])
    workbench = read_json(output_paths["content_workbench"])
    workbench_summary = workbench.get("summary") if isinstance(workbench.get("summary"), dict) else {}
    return {
        "phase1_status": phase1.get("status") or "UNKNOWN",
        "high_value_candidate_count": safe_int((phase1.get("summary") or {}).get("high_value_candidate_count")),
        "brief_count": safe_int(briefs.get("brief_count")),
        "outline_count": safe_int(outlines.get("outline_count")),
        "draft_count": safe_int(drafts.get("draft_count")),
        "quality_review_count": safe_int(reviews.get("review_count")),
        "platform_package_count": safe_int(packages.get("package_count")),
        "blocked_package_count": safe_int(packages.get("blocked_count")),
        "ready_for_human_review": safe_int(workbench_summary.get("ready_for_human_review")),
        "needs_edit": safe_int(workbench_summary.get("needs_edit")),
        "hold": safe_int(workbench_summary.get("hold")),
    }


def determine_status(steps: list[PipelineStep], summary: dict[str, Any], warnings: list[str]) -> str:
    if any(step.returncode != 0 for step in steps):
        return "FAILED"
    if warnings:
        return "DEGRADED"
    if safe_int(summary.get("brief_count")) == 0 or safe_int(summary.get("draft_count")) == 0:
        return "DEGRADED"
    if safe_int(summary.get("platform_package_count")) == 0:
        return "DEGRADED"
    return "SUCCESS"


def render_markdown(report: Phase2DailyPipelineReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    output_lines = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 2 Daily Content Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Key Metrics

- phase1_status: `{report.summary.get('phase1_status')}`
- high_value_candidate_count: `{report.summary.get('high_value_candidate_count')}`
- brief_count: `{report.summary.get('brief_count')}`
- outline_count: `{report.summary.get('outline_count')}`
- draft_count: `{report.summary.get('draft_count')}`
- quality_review_count: `{report.summary.get('quality_review_count')}`
- platform_package_count: `{report.summary.get('platform_package_count')}`
- blocked_package_count: `{report.summary.get('blocked_package_count')}`
- ready_for_human_review: `{report.summary.get('ready_for_human_review')}`
- needs_edit: `{report.summary.get('needs_edit')}`
- hold: `{report.summary.get('hold')}`

## Outputs

{output_lines}

## Warnings

{warnings}
"""


def write_outputs(report: Phase2DailyPipelineReport) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    logs_root = paths.logs_root
    frontstage_root = paths.frontstage_root
    logs_root.mkdir(parents=True, exist_ok=True)
    frontstage_root.mkdir(parents=True, exist_ok=True)
    dated_json = logs_root / f"{report.run_date}__phase2-daily-pipeline.json"
    dated_md = logs_root / f"{report.run_date}__phase2-daily-pipeline.md"
    latest_json = logs_root / "latest_phase2_daily_pipeline.json"
    latest_md = logs_root / "latest_phase2_daily_pipeline.md"
    frontstage_dated = frontstage_root / f"{report.run_date}__phase2-daily-pipeline-board.md"
    frontstage_latest = frontstage_root / "latest_phase2_daily_pipeline_board.md"
    payload = json.dumps(asdict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (dated_json, latest_json):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (dated_md, latest_md, frontstage_dated, frontstage_latest):
        path.write_text(markdown, encoding="utf-8")
    return {
        "dated_json": dated_json,
        "dated_md": dated_md,
        "latest_json": latest_json,
        "latest_md": latest_md,
        "frontstage_dated_md": frontstage_dated,
        "frontstage_latest_md": frontstage_latest,
    }


def build_report(steps: list[PipelineStep], warnings: list[str]) -> Phase2DailyPipelineReport:
    output_paths = collect_output_paths()
    outputs = {name: repo_relative(path, REPO_ROOT) for name, path in output_paths.items()}
    summary = build_summary(output_paths)
    status = determine_status(steps, summary, warnings)
    return Phase2DailyPipelineReport(
        schema_version="v1",
        generated_at=utc_now(),
        run_date=today_token(),
        status=status,
        steps=tuple(steps),
        summary=summary,
        outputs=outputs,
        warnings=tuple(warnings),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 2 daily content pipeline.")
    parser.add_argument("--json", action="store_true", help="Print JSON pipeline report to stdout.")
    parser.add_argument("--continue-on-error", action="store_true", help="Attempt downstream steps after a failed step.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    planned_steps = [
        ("phase1_daily", [sys.executable, "scripts/run_phase1_daily_pipeline.py"]),
        ("content_briefs", [sys.executable, "scripts/build_content_briefs.py"]),
        ("content_outlines", [sys.executable, "scripts/build_content_outlines.py"]),
        ("content_drafts", [sys.executable, "scripts/build_content_drafts.py"]),
        ("content_quality_review", [sys.executable, "scripts/review_content_quality.py"]),
        ("platform_packages", [sys.executable, "scripts/build_platform_packages.py"]),
        ("content_workbench", [sys.executable, "scripts/build_content_workbench.py"]),
    ]
    steps: list[PipelineStep] = []
    warnings: list[str] = []

    for name, command in planned_steps:
        step = run_step(name, command)
        steps.append(step)
        if step.returncode != 0:
            warnings.append(f"{name} exited with return code {step.returncode}.")
            if not args.continue_on_error:
                warnings.append(f"Stopped after {name}; use --continue-on-error to attempt downstream reports.")
                break

    report = build_report(steps, warnings)
    written = write_outputs(report)

    if args.json:
        print(json.dumps({**asdict(report), "pipeline_outputs": {k: str(v) for k, v in written.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Phase 2 Daily Content Pipeline")
        print("==============================")
        print(f"status: {report.status}")
        print(f"run_date: {report.run_date}")
        print(f"brief_count: {report.summary.get('brief_count')}")
        print(f"outline_count: {report.summary.get('outline_count')}")
        print(f"draft_count: {report.summary.get('draft_count')}")
        print(f"quality_review_count: {report.summary.get('quality_review_count')}")
        print(f"platform_package_count: {report.summary.get('platform_package_count')}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
        print("\nReports:")
        for name, path in written.items():
            print(f"  {name}: {path}")
        if report.warnings:
            print("\nWarnings:")
            for warning in report.warnings:
                print(f"  - {warning}")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
