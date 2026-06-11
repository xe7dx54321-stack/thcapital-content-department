"""Execution ledger summaries and convenience helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.runtime_state_store import connect_runtime_db, default_runtime_db_path, initialize_runtime_state, latest_heartbeat, list_job_runs, status_counts


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__runtime-ledger-summary.json",
        "dated_md": paths.logs_root / f"{run_date}__runtime-ledger-summary.md",
        "latest_json": paths.logs_root / "latest_runtime_ledger_summary.json",
        "latest_md": paths.logs_root / "latest_runtime_ledger_summary.md",
    }


def build_runtime_ledger_summary(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    db_path = initialize_runtime_state(paths)
    with connect_runtime_db(paths, db_path) as conn:
        counts = status_counts(conn)
        runs = list_job_runs(conn, limit=25)
        heartbeat = latest_heartbeat(conn)
    summary = {
        "job_run_count": sum(counts.values()),
        "pending": counts.get("PENDING", 0),
        "running": counts.get("RUNNING", 0),
        "success": counts.get("SUCCESS", 0),
        "actionable": counts.get("ACTIONABLE", 0),
        "degraded": counts.get("DEGRADED", 0),
        "failed": counts.get("FAILED", 0),
        "skipped": counts.get("SKIPPED", 0),
        "cancelled": counts.get("CANCELLED", 0),
    }
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "runtime_db_path": repo_relative(default_runtime_db_path(paths), repo_root),
        "summary": summary,
        "status_counts": counts,
        "latest_heartbeat": heartbeat,
        "recent_job_runs": runs,
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"- `{item.get('job_run_id')}` {item.get('job_id')} {item.get('status')} attempts={item.get('attempt_count')}"
        for item in payload.get("recent_job_runs", [])
    ) or "- None"
    return f"""# Runtime Ledger Summary

- job_run_count: `{summary.get('job_run_count', 0)}`
- success: `{summary.get('success', 0)}`
- failed: `{summary.get('failed', 0)}`
- running: `{summary.get('running', 0)}`
- pending: `{summary.get('pending', 0)}`

## Recent Runs

{rows}
"""
