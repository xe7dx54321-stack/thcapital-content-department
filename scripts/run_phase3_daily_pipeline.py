#!/usr/bin/env python3
"""Run the Phase 3 daily agent review pipeline."""

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
class Phase3DailyPipelineReport:
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
    review_root = paths.market_content_root / "06_review_queue"
    return {
        "phase2_pipeline": paths.logs_root / "latest_phase2_daily_pipeline.json",
        "agent_review_queue": review_root / "latest_agent_review_queue.json",
        "proponent_reviews": review_root / "latest_proponent_reviews.json",
        "critic_reviews": review_root / "latest_critic_reviews.json",
        "judge_gate": review_root / "latest_judge_gate.json",
        "revision_instructions": review_root / "latest_revision_instructions.json",
        "human_exception_queue": review_root / "latest_human_exception_queue.json",
        "agent_review_dashboard": paths.logs_root / "latest_agent_review_dashboard.json",
    }


def build_summary(output_paths: dict[str, Path]) -> dict[str, Any]:
    phase2 = read_json(output_paths["phase2_pipeline"])
    queue = read_json(output_paths["agent_review_queue"])
    prop = read_json(output_paths["proponent_reviews"])
    critic = read_json(output_paths["critic_reviews"])
    judge = read_json(output_paths["judge_gate"])
    revisions = read_json(output_paths["revision_instructions"])
    exceptions = read_json(output_paths["human_exception_queue"])
    dashboard = read_json(output_paths["agent_review_dashboard"])
    dashboard_summary = dashboard.get("summary") if isinstance(dashboard.get("summary"), dict) else {}
    return {
        "phase2_status": phase2.get("status") or "UNKNOWN",
        "review_item_count": safe_int(queue.get("item_count")),
        "proponent_review_count": safe_int(prop.get("review_count")),
        "critic_review_count": safe_int(critic.get("review_count")),
        "judge_decision_count": safe_int(judge.get("decision_count")),
        "revision_instruction_count": safe_int(revisions.get("revision_count")),
        "human_exception_count": safe_int(exceptions.get("exception_count")),
        "approved_for_queue": safe_int(dashboard_summary.get("approved_for_queue")),
        "needs_revision": safe_int(dashboard_summary.get("needs_revision")),
        "hold": safe_int(dashboard_summary.get("hold")),
        "escalated_to_human": safe_int(dashboard_summary.get("escalated_to_human")),
        "estimated_human_review_minutes": safe_int(dashboard_summary.get("estimated_human_review_minutes")),
    }


def determine_status(steps: list[PipelineStep], summary: dict[str, Any], warnings: list[str]) -> str:
    if any(step.returncode != 0 for step in steps):
        return "FAILED"
    if warnings:
        return "DEGRADED"
    if safe_int(summary.get("review_item_count")) == 0:
        return "DEGRADED"
    if safe_int(summary.get("judge_decision_count")) == 0:
        return "DEGRADED"
    return "SUCCESS"


def render_markdown(report: Phase3DailyPipelineReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    output_lines = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 3 Daily Agent Review Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Key Metrics

- phase2_status: `{report.summary.get('phase2_status')}`
- review_item_count: `{report.summary.get('review_item_count')}`
- proponent_review_count: `{report.summary.get('proponent_review_count')}`
- critic_review_count: `{report.summary.get('critic_review_count')}`
- judge_decision_count: `{report.summary.get('judge_decision_count')}`
- revision_instruction_count: `{report.summary.get('revision_instruction_count')}`
- human_exception_count: `{report.summary.get('human_exception_count')}`
- approved_for_queue: `{report.summary.get('approved_for_queue')}`
- needs_revision: `{report.summary.get('needs_revision')}`
- hold: `{report.summary.get('hold')}`
- escalated_to_human: `{report.summary.get('escalated_to_human')}`
- estimated_human_review_minutes: `{report.summary.get('estimated_human_review_minutes')}`

## Outputs

{output_lines}

## Warnings

{warnings}
"""


def write_outputs(report: Phase3DailyPipelineReport) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    logs_root = paths.logs_root
    frontstage_root = paths.frontstage_root
    logs_root.mkdir(parents=True, exist_ok=True)
    frontstage_root.mkdir(parents=True, exist_ok=True)
    dated_json = logs_root / f"{report.run_date}__phase3-daily-pipeline.json"
    dated_md = logs_root / f"{report.run_date}__phase3-daily-pipeline.md"
    latest_json = logs_root / "latest_phase3_daily_pipeline.json"
    latest_md = logs_root / "latest_phase3_daily_pipeline.md"
    frontstage_dated = frontstage_root / f"{report.run_date}__phase3-daily-pipeline-board.md"
    frontstage_latest = frontstage_root / "latest_phase3_daily_pipeline_board.md"
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


def build_report(steps: list[PipelineStep], warnings: list[str]) -> Phase3DailyPipelineReport:
    output_paths = collect_output_paths()
    outputs = {name: repo_relative(path, REPO_ROOT) for name, path in output_paths.items()}
    summary = build_summary(output_paths)
    status = determine_status(steps, summary, warnings)
    return Phase3DailyPipelineReport(
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
    parser = argparse.ArgumentParser(description="Run Phase 3 daily agent review pipeline.")
    parser.add_argument("--json", action="store_true", help="Print JSON pipeline report to stdout.")
    parser.add_argument("--continue-on-error", action="store_true", help="Attempt downstream steps after a failed step.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    planned_steps = [
        ("phase2_daily", [sys.executable, "scripts/run_phase2_daily_pipeline.py"]),
        ("review_queue", [sys.executable, "scripts/build_agent_review_queue.py"]),
        ("proponent_reviews", [sys.executable, "scripts/build_proponent_reviews.py"]),
        ("critic_reviews", [sys.executable, "scripts/build_critic_reviews.py"]),
        ("judge_gate", [sys.executable, "scripts/build_judge_gate.py"]),
        ("revision_instructions", [sys.executable, "scripts/build_revision_instructions.py"]),
        ("human_exception_queue", [sys.executable, "scripts/build_human_exception_queue.py"]),
        ("agent_review_dashboard", [sys.executable, "scripts/build_agent_review_dashboard.py"]),
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
        print("Phase 3 Daily Agent Review Pipeline")
        print("===================================")
        print(f"status: {report.status}")
        print(f"run_date: {report.run_date}")
        print(f"review_item_count: {report.summary.get('review_item_count')}")
        print(f"judge_decision_count: {report.summary.get('judge_decision_count')}")
        print(f"human_exception_count: {report.summary.get('human_exception_count')}")
        print(f"approved_for_queue: {report.summary.get('approved_for_queue')}")
        print(f"needs_revision: {report.summary.get('needs_revision')}")
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
