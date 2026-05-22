#!/usr/bin/env python3
"""Run the combined Phase 4 + Phase 5 learning daily pipeline."""

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
class LearningDailyPipelineReport:
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
    return PipelineStep(name, " ".join(command), completed.returncode, "OK" if completed.returncode == 0 else "FAILED", started_at, finished_at, tail_text(completed.stdout), tail_text(completed.stderr))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def collect_summary_and_outputs() -> tuple[dict[str, Any], dict[str, str]]:
    paths = get_project_paths(REPO_ROOT)
    outputs = {
        "phase3_pipeline": paths.logs_root / "latest_phase3_daily_pipeline.json",
        "phase4_pipeline": paths.logs_root / "latest_phase4_daily_pipeline.json",
        "phase5_pipeline": paths.logs_root / "latest_phase5_daily_learning_pipeline.json",
        "learning_loop_dashboard": paths.logs_root / "latest_learning_loop_dashboard.json",
    }
    phase3 = read_json(outputs["phase3_pipeline"])
    phase4 = read_json(outputs["phase4_pipeline"])
    phase5 = read_json(outputs["phase5_pipeline"])
    return (
        {
            "phase3_status": phase3.get("status") or "UNKNOWN",
            "phase4_status": phase4.get("status") or "UNKNOWN",
            "phase5_status": phase5.get("status") or "UNKNOWN",
            "publishing_candidate_count": (phase4.get("summary") or {}).get("publishing_candidate_count", 0),
            "pattern_library_count": (phase5.get("summary") or {}).get("pattern_library_count", 0),
        },
        {key: repo_relative(value) for key, value in outputs.items()},
    )


def render_markdown(report: LearningDailyPipelineReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    outputs = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Learning Daily Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Key Metrics

- phase3_status: `{report.summary.get('phase3_status')}`
- phase4_status: `{report.summary.get('phase4_status')}`
- phase5_status: `{report.summary.get('phase5_status')}`
- publishing_candidate_count: `{report.summary.get('publishing_candidate_count')}`
- pattern_library_count: `{report.summary.get('pattern_library_count')}`

## Outputs

{outputs}

## Warnings

{warnings}
"""


def write_outputs(report: LearningDailyPipelineReport) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    outputs = {
        "dated_json": paths.logs_root / f"{report.run_date}__learning-daily-pipeline.json",
        "dated_md": paths.logs_root / f"{report.run_date}__learning-daily-pipeline.md",
        "latest_json": paths.logs_root / "latest_learning_daily_pipeline.json",
        "latest_md": paths.logs_root / "latest_learning_daily_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{report.run_date}__learning-daily-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_learning_daily_pipeline_board.md",
    }
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(asdict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (outputs["dated_json"], outputs["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (outputs["dated_md"], outputs["latest_md"], outputs["frontstage_dated_md"], outputs["frontstage_latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Run learning daily pipeline.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    parser.add_argument("--continue-on-error", action="store_true", help="Attempt downstream steps after failure.")
    args = parser.parse_args()
    planned = [
        ("phase3_daily", [sys.executable, "scripts/run_phase3_daily_pipeline.py"]),
        ("phase4_daily", [sys.executable, "scripts/run_phase4_daily_pipeline.py"]),
        ("phase5_daily", [sys.executable, "scripts/run_phase5_daily_learning_pipeline.py"]),
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
    summary, outputs = collect_summary_and_outputs()
    status = "FAILED" if any(step.returncode != 0 for step in steps) else "DEGRADED" if warnings else "SUCCESS"
    report = LearningDailyPipelineReport("v1", utc_now(), today_token(), status, tuple(steps), summary, outputs, tuple(warnings))
    written = write_outputs(report)
    if args.json:
        print(json.dumps({**asdict(report), "pipeline_outputs": {k: str(v) for k, v in written.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Learning Daily Pipeline")
        print("=======================")
        print(f"status: {report.status}")
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
