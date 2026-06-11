"""Local failure notification artifacts for the autonomous runtime."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def build_failure_notifications(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    health = read_json(paths.logs_root / "latest_runtime_health_summary.json")
    retry = read_json(paths.logs_root / "latest_runtime_retry_queue.json")
    ledger = read_json(paths.logs_root / "latest_runtime_ledger_summary.json")
    notifications: list[dict[str, Any]] = []
    health_summary = health.get("summary") if isinstance(health.get("summary"), dict) else {}
    retry_summary = retry.get("summary") if isinstance(retry.get("summary"), dict) else {}
    ledger_summary = ledger.get("summary") if isinstance(ledger.get("summary"), dict) else {}
    if not health_summary.get("has_heartbeat"):
        notifications.append({"level": "WARN", "reason": "missing_heartbeat", "message": "Runtime heartbeat has not been written yet."})
    if int(ledger_summary.get("failed") or 0) > 0:
        notifications.append({"level": "ERROR", "reason": "failed_jobs", "message": f"{ledger_summary.get('failed')} job(s) failed."})
    if int(retry_summary.get("blocked_count") or 0) > 0:
        notifications.append({"level": "ERROR", "reason": "blocked_retries", "message": f"{retry_summary.get('blocked_count')} retry item(s) are blocked."})
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "notifications": notifications,
        "summary": {
            "notification_count": len(notifications),
            "info": sum(1 for item in notifications if item.get("level") == "INFO"),
            "warn": sum(1 for item in notifications if item.get("level") == "WARN"),
            "error": sum(1 for item in notifications if item.get("level") == "ERROR"),
            "critical": sum(1 for item in notifications if item.get("level") == "CRITICAL"),
        },
    }
    outputs = {
        "dated_json": paths.logs_root / f"{payload['run_date']}__runtime-failure-notifications.json",
        "dated_md": paths.logs_root / f"{payload['run_date']}__runtime-failure-notifications.md",
        "latest_json": paths.logs_root / "latest_runtime_failure_notifications.json",
        "latest_md": paths.logs_root / "latest_runtime_failure_notifications.md",
    }
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(f"- `{item.get('level')}` {item.get('reason')}: {item.get('message')}" for item in payload.get("notifications", [])) or "- None"
    return f"""# Runtime Failure Notifications

{rows}
"""
