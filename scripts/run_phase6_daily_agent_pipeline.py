#!/usr/bin/env python3
"""Run the Phase 6 daily LLM agent pipeline."""

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
class Phase6DailyAgentPipelineReport:
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


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def collect_outputs() -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    review_root = paths.market_content_root / "06_review_queue"
    draft_root = paths.market_content_root / "05_draft_packs"
    publishing_root = paths.market_content_root / "07_publishing"
    return {
        "learning_daily": paths.logs_root / "latest_learning_daily_pipeline.json",
        "llm_proponent_reviews": review_root / "latest_llm_proponent_reviews.json",
        "llm_critic_reviews": review_root / "latest_llm_critic_reviews.json",
        "llm_judge_gate": review_root / "latest_llm_judge_gate.json",
        "llm_rewrite_suggestions": draft_root / "latest_llm_rewrite_suggestions.json",
        "agent_run_summary": paths.logs_root / "latest_agent_run_summary.json",
        "agent_evaluation_template": publishing_root / "latest_agent_evaluation_template.json",
    }


def build_summary(outputs: dict[str, Path]) -> dict[str, Any]:
    learning = read_json(outputs["learning_daily"])
    prop = read_json(outputs["llm_proponent_reviews"])
    critic = read_json(outputs["llm_critic_reviews"])
    judge = read_json(outputs["llm_judge_gate"])
    rewrite = read_json(outputs["llm_rewrite_suggestions"])
    run_summary = read_json(outputs["agent_run_summary"])
    evaluation = read_json(outputs["agent_evaluation_template"])
    run_summary_payload = run_summary.get("summary") if isinstance(run_summary.get("summary"), dict) else {}
    return {
        "learning_daily_status": learning.get("status") or "UNKNOWN",
        "llm_proponent_review_count": safe_int(prop.get("review_count")),
        "llm_critic_review_count": safe_int(critic.get("review_count")),
        "llm_judge_decision_count": safe_int(judge.get("decision_count")),
        "llm_rewrite_suggestion_count": safe_int(rewrite.get("suggestion_count")),
        "agent_run_record_count": safe_int(run_summary_payload.get("record_count")),
        "agent_run_failed_count": safe_int(run_summary_payload.get("failed_count")),
        "agent_run_estimated_cost_usd": run_summary_payload.get("estimated_cost_usd", 0.0),
        "agent_evaluation_count": safe_int(evaluation.get("evaluation_count")),
    }


def determine_status(steps: list[PipelineStep], summary: dict[str, Any], warnings: list[str]) -> str:
    if any(step.returncode != 0 for step in steps):
        return "FAILED"
    if warnings or safe_int(summary.get("llm_judge_decision_count")) == 0:
        return "DEGRADED"
    return "SUCCESS"


def render_markdown(report: Phase6DailyAgentPipelineReport) -> str:
    step_rows = "\n".join(f"| {step.name} | {step.status} | {step.returncode} |" for step in report.steps)
    output_lines = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Phase 6 Daily Agent Pipeline

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Key Metrics

- learning_daily_status: `{report.summary.get('learning_daily_status')}`
- llm_proponent_review_count: `{report.summary.get('llm_proponent_review_count')}`
- llm_critic_review_count: `{report.summary.get('llm_critic_review_count')}`
- llm_judge_decision_count: `{report.summary.get('llm_judge_decision_count')}`
- llm_rewrite_suggestion_count: `{report.summary.get('llm_rewrite_suggestion_count')}`
- agent_run_record_count: `{report.summary.get('agent_run_record_count')}`
- agent_run_failed_count: `{report.summary.get('agent_run_failed_count')}`
- agent_run_estimated_cost_usd: `{report.summary.get('agent_run_estimated_cost_usd')}`
- agent_evaluation_count: `{report.summary.get('agent_evaluation_count')}`

## Outputs

{output_lines}

## Warnings

{warnings}
"""


def write_outputs(report: Phase6DailyAgentPipelineReport) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    outputs = {
        "dated_json": paths.logs_root / f"{report.run_date}__phase6-daily-agent-pipeline.json",
        "dated_md": paths.logs_root / f"{report.run_date}__phase6-daily-agent-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase6_daily_agent_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase6_daily_agent_pipeline.md",
        "frontstage_dated_md": paths.frontstage_root / f"{report.run_date}__phase6-daily-agent-pipeline-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_phase6_daily_agent_pipeline_board.md",
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
    parser = argparse.ArgumentParser(description="Run Phase 6 daily LLM agent pipeline.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()
    planned = [
        ("learning_daily", [sys.executable, "scripts/run_learning_daily_pipeline.py"]),
        ("llm_config_validate", [sys.executable, "scripts/validate_llm_provider_config.py"]),
        ("agent_prompts_validate", [sys.executable, "scripts/validate_agent_prompts.py"]),
        ("llm_proponent_reviews", [sys.executable, "scripts/run_llm_proponent_reviews.py"]),
        ("llm_critic_reviews", [sys.executable, "scripts/run_llm_critic_reviews.py"]),
        ("llm_judge_gate", [sys.executable, "scripts/run_llm_judge_gate.py"]),
        ("llm_rewrite_suggestions", [sys.executable, "scripts/run_llm_rewrite_suggestions.py"]),
        ("agent_run_summary", [sys.executable, "scripts/build_agent_run_summary.py"]),
        ("agent_evaluation_template", [sys.executable, "scripts/build_agent_evaluation_template.py"]),
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
    output_paths = collect_outputs()
    summary = build_summary(output_paths)
    outputs = {key: repo_relative(path) for key, path in output_paths.items()}
    status = determine_status(steps, summary, warnings)
    report = Phase6DailyAgentPipelineReport("v1", utc_now(), today_token(), status, tuple(steps), summary, outputs, tuple(warnings))
    written = write_outputs(report)
    if args.json:
        print(json.dumps({**asdict(report), "pipeline_outputs": {key: str(value) for key, value in written.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Phase 6 Daily Agent Pipeline")
        print("============================")
        print(f"status: {report.status}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
        print("\nReports:")
        for key, path in written.items():
            print(f"  {key}: {path}")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
