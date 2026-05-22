#!/usr/bin/env python3
"""Run the Phase 1 daily evidence pipeline end to end."""

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
class Phase1DailyPipelineReport:
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


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    topic_root = paths.market_content_root / "03_topic_candidates"
    return {
        "official_daily_full_run": paths.logs_root / "latest_official_daily_full_run.json",
        "runtime_baseline": paths.logs_root / "official_runtime_baseline.json",
        "source_coverage": paths.logs_root / "latest_source_coverage_alignment.json",
        "evidence_packets": topic_root / "latest_evidence_packets.json",
        "topic_clusters": topic_root / "latest_topic_clusters.json",
        "value_scores": topic_root / "latest_topic_cluster_scores.json",
        "high_value_candidates": topic_root / "latest_high_value_candidates.json",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    full_run = read_json(outputs["official_daily_full_run"])
    evidence = read_json(outputs["evidence_packets"])
    clusters = read_json(outputs["topic_clusters"])
    scores = read_json(outputs["value_scores"])
    candidates = read_json(outputs["high_value_candidates"])
    return {
        "official_full_run_status": full_run.get("status") or "UNKNOWN",
        "quality_gate_status": (full_run.get("summary") or {}).get("quality_gate_status") or "UNKNOWN",
        "source_count": safe_int((full_run.get("summary") or {}).get("source_count")),
        "total_items_found": safe_int((full_run.get("summary") or {}).get("total_items_found")),
        "evidence_count": safe_int(evidence.get("evidence_count")),
        "topic_cluster_count": safe_int(clusters.get("cluster_count")),
        "scored_cluster_count": safe_int(scores.get("scored_cluster_count")),
        "high_value_candidate_count": safe_int(candidates.get("candidate_count")),
    }


def determine_status(steps: list[PipelineStep], summary: dict[str, Any], warnings: list[str]) -> str:
    if any(step.returncode != 0 for step in steps):
        return "FAILED"
    if warnings:
        return "DEGRADED"
    if summary.get("official_full_run_status") != "SUCCESS":
        return "DEGRADED"
    if safe_int(summary.get("evidence_count")) == 0 or safe_int(summary.get("topic_cluster_count")) == 0:
        return "DEGRADED"
    return "SUCCESS"


def render_markdown(report: Phase1DailyPipelineReport) -> str:
    step_rows = "\n".join(
        f"| {step.name} | {step.status} | {step.returncode} |"
        for step in report.steps
    )
    output_lines = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 1 Daily Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Key Metrics

- official_full_run_status: `{report.summary.get('official_full_run_status')}`
- quality_gate_status: `{report.summary.get('quality_gate_status')}`
- source_count: `{report.summary.get('source_count')}`
- total_items_found: `{report.summary.get('total_items_found')}`
- evidence_count: `{report.summary.get('evidence_count')}`
- topic_cluster_count: `{report.summary.get('topic_cluster_count')}`
- scored_cluster_count: `{report.summary.get('scored_cluster_count')}`
- high_value_candidate_count: `{report.summary.get('high_value_candidate_count')}`

## Outputs

{output_lines}

## Warnings

{warnings}
"""


def write_outputs(report: Phase1DailyPipelineReport) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    logs_root = paths.logs_root
    frontstage_root = paths.frontstage_root
    logs_root.mkdir(parents=True, exist_ok=True)
    frontstage_root.mkdir(parents=True, exist_ok=True)
    dated_json = logs_root / f"{report.run_date}__phase1-daily-pipeline.json"
    dated_md = logs_root / f"{report.run_date}__phase1-daily-pipeline.md"
    latest_json = logs_root / "latest_phase1_daily_pipeline.json"
    latest_md = logs_root / "latest_phase1_daily_pipeline.md"
    frontstage_dated = frontstage_root / f"{report.run_date}__phase1-daily-pipeline-board.md"
    frontstage_latest = frontstage_root / "latest_phase1_daily_pipeline_board.md"
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


def build_report(steps: list[PipelineStep], warnings: list[str]) -> Phase1DailyPipelineReport:
    output_paths = collect_outputs()
    outputs = {name: repo_relative(path, REPO_ROOT) for name, path in output_paths.items()}
    summary = build_summary(output_paths)
    run_date = today_token()
    status = determine_status(steps, summary, warnings)
    return Phase1DailyPipelineReport(
        schema_version="v1",
        generated_at=utc_now(),
        run_date=run_date,
        status=status,
        steps=tuple(steps),
        summary=summary,
        outputs=outputs,
        warnings=tuple(warnings),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 1 daily pipeline.")
    parser.add_argument("--json", action="store_true", help="Print JSON pipeline report to stdout.")
    parser.add_argument("--continue-on-error", action="store_true", help="Attempt downstream steps after a failed step.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    planned_steps = [
        ("official_daily_full_run", [sys.executable, "scripts/run_official_daily_full_run.py"]),
        ("runtime_baseline", [sys.executable, "scripts/update_official_runtime_baseline.py"]),
        ("source_coverage", [sys.executable, "scripts/build_source_coverage_alignment.py"]),
        ("evidence_packets", [sys.executable, "scripts/build_evidence_packets.py"]),
        ("topic_clusters", [sys.executable, "scripts/build_topic_clusters.py"]),
        ("value_scores", [sys.executable, "scripts/score_topic_clusters.py"]),
        ("high_value_candidates", [sys.executable, "scripts/build_high_value_candidate_pool.py"]),
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
        print("Phase 1 Daily Pipeline")
        print("======================")
        print(f"status: {report.status}")
        print(f"run_date: {report.run_date}")
        print(f"evidence_count: {report.summary.get('evidence_count')}")
        print(f"topic_cluster_count: {report.summary.get('topic_cluster_count')}")
        print(f"scored_cluster_count: {report.summary.get('scored_cluster_count')}")
        print(f"high_value_candidate_count: {report.summary.get('high_value_candidate_count')}")
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
