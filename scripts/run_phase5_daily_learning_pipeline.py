#!/usr/bin/env python3
"""Run the Phase 5 daily learning pipeline."""

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
class Phase5DailyLearningPipelineReport:
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


def tail_text(text: str, max_lines: int = 20) -> str:
    sanitized = text.replace(str(REPO_ROOT), "<repo_root>")
    lines = sanitized.strip().splitlines()
    return "\n".join(lines[-max_lines:])


def run_step(name: str, command: list[str]) -> PipelineStep:
    started_at = utc_now()
    completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    finished_at = utc_now()
    return PipelineStep(name, " ".join(command), completed.returncode, "OK" if completed.returncode == 0 else "FAILED", started_at, finished_at, tail_text(completed.stdout), tail_text(completed.stderr))


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def collect_output_paths() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    root = paths.market_content_root / "08_learning_patterns"
    return {
        "head_media_pattern_library": root / "head_media_pattern_library.json",
        "title_patterns": root / "latest_title_patterns.json",
        "opening_patterns": root / "latest_opening_patterns.json",
        "structure_patterns": root / "latest_structure_patterns.json",
        "content_recipe_suggestions": root / "latest_content_recipe_suggestions.json",
        "pattern_adapters": root / "latest_pattern_adapters.json",
    }


def build_summary(output_paths: dict[str, Path]) -> dict[str, Any]:
    library = read_json(output_paths["head_media_pattern_library"])
    title = read_json(output_paths["title_patterns"])
    opening = read_json(output_paths["opening_patterns"])
    structure = read_json(output_paths["structure_patterns"])
    recipe = read_json(output_paths["content_recipe_suggestions"])
    adapter = read_json(output_paths["pattern_adapters"])
    return {
        "pattern_library_count": safe_int((library.get("summary") or {}).get("pattern_count")),
        "title_pattern_count": safe_int(title.get("pattern_count")),
        "opening_pattern_count": safe_int(opening.get("pattern_count")),
        "structure_pattern_count": safe_int(structure.get("pattern_count")),
        "content_recipe_suggestion_count": safe_int(recipe.get("suggestion_count")),
        "pattern_adapter_count": safe_int(adapter.get("adapter_count")),
    }


def determine_status(steps: list[PipelineStep], summary: dict[str, Any], warnings: list[str]) -> str:
    if any(step.returncode != 0 for step in steps):
        return "FAILED"
    if warnings:
        return "DEGRADED"
    if safe_int(summary.get("pattern_library_count")) == 0:
        return "DEGRADED"
    return "SUCCESS"


def render_markdown(report: Phase5DailyLearningPipelineReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 5 Daily Learning Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Key Metrics

- pattern_library_count: `{report.summary.get('pattern_library_count')}`
- title_pattern_count: `{report.summary.get('title_pattern_count')}`
- opening_pattern_count: `{report.summary.get('opening_pattern_count')}`
- structure_pattern_count: `{report.summary.get('structure_pattern_count')}`
- content_recipe_suggestion_count: `{report.summary.get('content_recipe_suggestion_count')}`
- pattern_adapter_count: `{report.summary.get('pattern_adapter_count')}`

## Outputs

{outputs}

## Warnings

{warnings}
"""


def write_outputs(report: Phase5DailyLearningPipelineReport) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    paths.logs_root.mkdir(parents=True, exist_ok=True)
    paths.frontstage_root.mkdir(parents=True, exist_ok=True)
    outputs = {
        "dated_json": paths.logs_root / f"{report.run_date}__phase5-daily-learning-pipeline.json",
        "dated_md": paths.logs_root / f"{report.run_date}__phase5-daily-learning-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase5_daily_learning_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase5_daily_learning_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{report.run_date}__phase5-daily-learning-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase5_daily_learning_pipeline_board.md",
    }
    payload = json.dumps(asdict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (outputs["dated_json"], outputs["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (outputs["dated_md"], outputs["latest_md"], outputs["frontstage_dated_md"], outputs["frontstage_latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return outputs


def build_report(steps: list[PipelineStep], warnings: list[str]) -> Phase5DailyLearningPipelineReport:
    output_paths = collect_output_paths()
    summary = build_summary(output_paths)
    status = determine_status(steps, summary, warnings)
    return Phase5DailyLearningPipelineReport("v1", utc_now(), today_token(), status, tuple(steps), summary, {k: repo_relative(v) for k, v in output_paths.items()}, tuple(warnings))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 5 daily learning pipeline.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    parser.add_argument("--continue-on-error", action="store_true", help="Attempt downstream steps after failure.")
    args = parser.parse_args()
    planned = [
        ("head_media_patterns", [sys.executable, "scripts/build_head_media_pattern_library.py"]),
        ("title_patterns", [sys.executable, "scripts/extract_title_patterns.py"]),
        ("opening_patterns", [sys.executable, "scripts/extract_opening_patterns.py"]),
        ("structure_patterns", [sys.executable, "scripts/extract_structure_patterns.py"]),
        ("content_recipe_suggestions", [sys.executable, "scripts/build_content_recipe_suggestions.py"]),
        ("pattern_adapters", [sys.executable, "scripts/build_pattern_adapters.py"]),
    ]
    steps: list[PipelineStep] = []
    warnings: list[str] = []
    for name, command in planned:
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
        print("Phase 5 Daily Learning Pipeline")
        print("===============================")
        print(f"status: {report.status}")
        print(f"run_date: {report.run_date}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
        print("\nReports:")
        for name, path in written.items():
            print(f"  {name}: {path}")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
