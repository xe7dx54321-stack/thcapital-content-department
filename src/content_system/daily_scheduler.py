"""Local daily scheduler runner for Phase 7."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import PipelineStep, python_command, repo_relative, run_step, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class DailySchedulerReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    pipeline: str
    dry_run: bool
    steps: tuple[PipelineStep, ...]
    summary: dict[str, Any]
    warnings: tuple[str, ...]


PIPELINES = {
    "learning-daily": python_command("scripts/run_learning_daily_pipeline.py"),
    "phase6-daily": python_command("scripts/run_phase6_daily_agent_pipeline.py"),
}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__daily-scheduler.json",
        "dated_md": paths.logs_root / f"{run_date}__daily-scheduler.md",
        "latest_json": paths.logs_root / "latest_daily_scheduler.json",
        "latest_md": paths.logs_root / "latest_daily_scheduler.md",
    }


def build_daily_scheduler_report(paths: ProjectPaths, repo_root: Path, pipeline: str = "learning-daily", dry_run: bool = False) -> DailySchedulerReport:
    warnings: list[str] = []
    command = PIPELINES.get(pipeline)
    if command is None:
        warnings.append(f"Unknown pipeline `{pipeline}`; defaulted to learning-daily.")
        pipeline = "learning-daily"
        command = PIPELINES[pipeline]
    step = run_step(pipeline, command, repo_root, dry_run=dry_run)
    status = "SUCCESS"
    if step.returncode != 0:
        status = "FAILED"
        warnings.append(f"{pipeline} exited with return code {step.returncode}.")
    elif dry_run:
        status = "DEGRADED"
        warnings.append("Scheduler ran in dry-run mode; no downstream pipeline was executed.")
    summary = {
        "pipeline": pipeline,
        "dry_run": dry_run,
        "step_status": step.status,
        "returncode": step.returncode,
        "command": step.command,
    }
    return DailySchedulerReport(SCHEMA_VERSION, utc_now(), today_token(), status, pipeline, dry_run, (step,), summary, tuple(warnings))


def render_markdown(report: DailySchedulerReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} | `{step.command}` |" for step in report.steps)
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Daily Scheduler v1

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**
- Pipeline: `{report.pipeline}`
- Dry-run: `{report.dry_run}`

## Steps

| Step | Status | Return Code | Command |
|---|---|---:|---|
{step_rows}

## Safety

- This local scheduler runner does not create cron or launchd jobs.
- It does not enable live LLM calls by itself.
- Live mode still requires explicit environment variables and allowlist.

## Warnings

{warnings}
"""


def write_daily_scheduler_report(report: DailySchedulerReport, paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    outputs = output_paths(paths, report.run_date)
    payload = asdict(report)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return write_json_and_markdown(payload, render_markdown(report), outputs)


def report_to_dict(report: DailySchedulerReport) -> dict[str, Any]:
    return asdict(report)
