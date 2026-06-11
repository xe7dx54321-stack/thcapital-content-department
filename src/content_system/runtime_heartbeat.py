"""Runtime heartbeat read/write and health summary."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.runtime_state_store import connect_runtime_db, initialize_runtime_state, latest_heartbeat, upsert_heartbeat


def write_runtime_heartbeat(
    paths: ProjectPaths,
    runtime_instance_id: str,
    status: str,
    current_job_id: str = "",
    next_scheduled_run: str = "",
    last_successful_daily_run: str = "",
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    db_path = initialize_runtime_state(paths)
    with connect_runtime_db(paths, db_path) as conn:
        upsert_heartbeat(
            conn,
            runtime_instance_id=runtime_instance_id,
            pid=os.getpid(),
            status=status,
            current_job_id=current_job_id,
            next_scheduled_run=next_scheduled_run,
            last_successful_daily_run=last_successful_daily_run,
            payload=payload or {},
        )
        return latest_heartbeat(conn)


def read_runtime_heartbeat(paths: ProjectPaths) -> dict[str, Any]:
    db_path = initialize_runtime_state(paths)
    with connect_runtime_db(paths, db_path) as conn:
        return latest_heartbeat(conn)


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__runtime-health-summary.json",
        "dated_md": paths.logs_root / f"{run_date}__runtime-health-summary.md",
        "latest_json": paths.logs_root / "latest_runtime_health_summary.json",
        "latest_md": paths.logs_root / "latest_runtime_health_summary.md",
    }


def build_runtime_health_summary(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    heartbeat = read_runtime_heartbeat(paths)
    status = heartbeat.get("status") or "UNKNOWN"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "runtime_status": status,
        "heartbeat": heartbeat,
        "summary": {
            "has_heartbeat": bool(heartbeat),
            "runtime_status": status,
            "current_job_id": heartbeat.get("current_job_id", ""),
            "next_scheduled_run": heartbeat.get("next_scheduled_run", ""),
            "last_successful_daily_run": heartbeat.get("last_successful_daily_run", ""),
        },
    }
    outputs = output_paths(paths, payload["run_date"])
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    heartbeat = payload.get("heartbeat") if isinstance(payload.get("heartbeat"), dict) else {}
    return f"""# Runtime Health Summary

- runtime_status: `{payload.get('runtime_status')}`
- last_heartbeat_at: `{heartbeat.get('last_heartbeat_at', '')}`
- current_job_id: `{heartbeat.get('current_job_id', '')}`
- next_scheduled_run: `{heartbeat.get('next_scheduled_run', '')}`
"""
