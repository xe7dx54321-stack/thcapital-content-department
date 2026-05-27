"""Retry / fallback planning runner for Phase 7."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.sources import load_source_registry


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class RetryFallbackRunnerReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    retry_plan: tuple[dict[str, Any], ...]
    fallback_candidates: tuple[dict[str, Any], ...]
    executed_actions: tuple[dict[str, Any], ...]
    manual_actions_required: tuple[str, ...]
    warnings: tuple[str, ...]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__retry-fallback-runner.json",
        "dated_md": paths.logs_root / f"{run_date}__retry-fallback-runner.md",
        "latest_json": paths.logs_root / "latest_retry_fallback_runner.json",
        "latest_md": paths.logs_root / "latest_retry_fallback_runner.md",
    }


def registry_by_source_id(repo_root: Path) -> dict[str, Any]:
    registry = load_source_registry(repo_root=repo_root)
    return {source.source_id: source for source in registry.sources}


def build_retry_fallback_runner_report(paths: ProjectPaths, repo_root: Path) -> RetryFallbackRunnerReport:
    runtime = read_json(paths.logs_root / "latest_source_runtime_health.json")
    failure = read_json(paths.logs_root / "latest_failure_notification.json")
    run_date = str(runtime.get("run_date") or today_token()).replace("-", "")[:8]
    registry = registry_by_source_id(repo_root)
    records = list_payload(runtime, "records")
    retry_plan: list[dict[str, Any]] = []
    fallback_candidates: list[dict[str, Any]] = []
    warnings: list[str] = []
    if not records:
        warnings.append("No source runtime health records available.")
    for record in records:
        status = str(record.get("runtime_status") or "")
        source_id = str(record.get("source_id") or "")
        if status not in {"MISSING_EXPECTED", "OBSERVED_WITH_ERROR_HINTS"} and safe_int(record.get("error_hint_count")) <= 0:
            continue
        source = registry.get(source_id)
        fallback_methods = tuple(source.fallback_methods) if source else ()
        retry_plan.append(
            {
                "source_id": source_id,
                "runtime_status": status,
                "reason": record.get("runtime_reason", ""),
                "recommended_retry": "rerun_official_lane_health_check" if record.get("category") == "official" else "manual_check",
                "safe_to_auto_execute": False,
            }
        )
        if fallback_methods:
            fallback_candidates.append(
                {
                    "source_id": source_id,
                    "fallback_methods": list(fallback_methods),
                    "notes": "Plan only; fetcher fallback is not executed in v1.",
                }
            )
    failures = list_payload(failure, "failures")
    manual_actions = []
    if failures:
        manual_actions.append("Resolve failure notification items before executing retries.")
    if retry_plan:
        manual_actions.append("Review retry plan manually; v1 does not rewrite fetchers or run broad refetches.")
    if not retry_plan:
        manual_actions.append("No retry action required from current runtime health.")
    status = "DEGRADED" if warnings else "SUCCESS"
    return RetryFallbackRunnerReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date,
        status=status,
        retry_plan=tuple(retry_plan),
        fallback_candidates=tuple(fallback_candidates),
        executed_actions=(),
        manual_actions_required=tuple(manual_actions),
        warnings=tuple(warnings),
    )


def render_markdown(report: RetryFallbackRunnerReport) -> str:
    retry_rows = "\n".join(
        f"| {item.get('source_id')} | {item.get('runtime_status')} | {item.get('recommended_retry')} | {item.get('safe_to_auto_execute')} |"
        for item in report.retry_plan
    ) or "| - | - | - | false |"
    fallback_lines = "\n".join(f"- `{item.get('source_id')}`: {', '.join(item.get('fallback_methods', []))}" for item in report.fallback_candidates) or "- None"
    manual = "\n".join(f"- {item}" for item in report.manual_actions_required)
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Retry / Fallback Runner v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**
- Retry plan items: `{len(report.retry_plan)}`
- Fallback candidates: `{len(report.fallback_candidates)}`
- Executed actions: `{len(report.executed_actions)}`

## Retry Plan

| Source | Runtime Status | Recommended Retry | Safe To Auto Execute |
|---|---|---|---|
{retry_rows}

## Fallback Candidates

{fallback_lines}

## Manual Actions Required

{manual}

## Warnings

{warnings}
"""


def write_retry_fallback_runner_report(report: RetryFallbackRunnerReport, paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    outputs = output_paths(paths, report.run_date)
    payload = asdict(report)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return write_json_and_markdown(payload, render_markdown(report), outputs)


def report_to_dict(report: RetryFallbackRunnerReport) -> dict[str, Any]:
    return asdict(report)
