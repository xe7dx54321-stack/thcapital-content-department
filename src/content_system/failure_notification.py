"""Failure notification report for Phase 7."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, safe_int, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class FailureNotificationReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    summary: dict[str, Any]
    failures: tuple[dict[str, Any], ...]
    warnings: tuple[str, ...]
    recommended_actions: tuple[str, ...]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__failure-notification.json",
        "dated_md": paths.logs_root / f"{run_date}__failure-notification.md",
        "latest_json": paths.logs_root / "latest_failure_notification.json",
        "latest_md": paths.logs_root / "latest_failure_notification.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__failure-notification-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_failure_notification_board.md",
    }


def collect_step_failures(payload: dict[str, Any], artifact_name: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    status = str(payload.get("status") or "UNKNOWN")
    if status == "FAILED":
        failures.append({"artifact": artifact_name, "kind": "pipeline_failure", "message": f"{artifact_name} status is FAILED."})
    for step in list_payload(payload, "steps"):
        if step.get("returncode") not in {None, 0} or step.get("status") == "FAILED":
            failures.append(
                {
                    "artifact": artifact_name,
                    "kind": "step_failure",
                    "step": step.get("name", ""),
                    "returncode": step.get("returncode", 0),
                    "message": step.get("stderr_tail") or step.get("stdout_tail") or "Step failed.",
                }
            )
    return failures


def build_failure_notification_report(paths: ProjectPaths) -> FailureNotificationReport:
    run_date = today_token()
    phase6 = read_json(paths.logs_root / "latest_phase6_daily_agent_pipeline.json")
    learning = read_json(paths.logs_root / "latest_learning_daily_pipeline.json")
    scheduler = read_json(paths.logs_root / "latest_daily_scheduler.json")
    agent_summary = read_json(paths.logs_root / "latest_agent_run_summary.json")
    ab = read_json(paths.logs_root / "latest_llm_ab_comparison.json")
    failures = [
        *collect_step_failures(phase6, "latest_phase6_daily_agent_pipeline.json"),
        *collect_step_failures(learning, "latest_learning_daily_pipeline.json"),
        *collect_step_failures(scheduler, "latest_daily_scheduler.json"),
    ]
    summary_payload = agent_summary.get("summary") if isinstance(agent_summary.get("summary"), dict) else {}
    failed_agents = safe_int(summary_payload.get("failed_count"))
    fallback_count = safe_int(summary_payload.get("fallback_count"))
    estimated_cost = safe_float(summary_payload.get("estimated_cost_usd"))
    live_failures = [
        record
        for record in list_payload(agent_summary, "records")
        if record.get("live_call_attempted") and not record.get("live_call_succeeded")
    ]
    for record in live_failures:
        failures.append(
            {
                "artifact": "latest_agent_run_summary.json",
                "kind": "live_agent_failure",
                "agent": record.get("agent_name", ""),
                "provider": record.get("provider_id", ""),
                "message": record.get("fallback_reason") or record.get("error") or "Live call failed or fell back.",
            }
        )
    warnings: list[str] = []
    if not phase6:
        warnings.append("Missing latest_phase6_daily_agent_pipeline.json.")
    if not learning:
        warnings.append("Missing latest_learning_daily_pipeline.json.")
    if fallback_count:
        warnings.append(f"Agent fallback count is {fallback_count}.")
    if estimated_cost > 0:
        warnings.append(f"Estimated live agent cost is {estimated_cost}.")
    recommended_actions: list[str] = []
    if failures:
        recommended_actions.append("Open the failed artifact and inspect stderr_tail before rerunning.")
    if live_failures:
        recommended_actions.append("Check API key, allowlist, provider base URL, and JSON response format.")
    if safe_int((ab.get("summary") or {}).get("human_spot_check_count")):
        recommended_actions.append("Review LLM A/B human spot-check items before publishing.")
    if not recommended_actions:
        recommended_actions.append("No immediate failure action required.")
    summary = {
        "pipeline_failure_count": sum(1 for item in failures if item.get("kind") in {"pipeline_failure", "step_failure"}),
        "agent_failed_count": failed_agents,
        "live_failure_count": len(live_failures),
        "fallback_count": fallback_count,
        "estimated_cost_usd": estimated_cost,
        "warning_count": len(warnings),
    }
    status = "FAILED" if failures else "DEGRADED" if warnings else "SUCCESS"
    return FailureNotificationReport(SCHEMA_VERSION, utc_now(), run_date, status, summary, tuple(failures), tuple(warnings), tuple(recommended_actions))


def render_markdown(report: FailureNotificationReport) -> str:
    failure_lines = "\n".join(f"- `{item.get('kind')}` {item.get('artifact')}: {item.get('message')}" for item in report.failures) or "- None"
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    actions = "\n".join(f"- {item}" for item in report.recommended_actions)
    return f"""# Failure Notification v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**
- Pipeline failures: `{report.summary.get('pipeline_failure_count')}`
- Agent failures: `{report.summary.get('agent_failed_count')}`
- Live failures: `{report.summary.get('live_failure_count')}`
- Fallback count: `{report.summary.get('fallback_count')}`
- Estimated cost USD: `{report.summary.get('estimated_cost_usd')}`

## Failures

{failure_lines}

## Warnings

{warnings}

## Recommended Actions

{actions}
"""


def write_failure_notification_report(report: FailureNotificationReport, paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    outputs = output_paths(paths, report.run_date)
    payload = asdict(report)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return write_json_and_markdown(payload, render_markdown(report), outputs)


def report_to_dict(report: FailureNotificationReport) -> dict[str, Any]:
    return asdict(report)
