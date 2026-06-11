"""Local runtime control API used by CLI and workbench actions."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json
from content_system.runtime_config import load_runtime_config
from content_system.runtime_state_store import connect_runtime_db, get_control_state, initialize_runtime_state, list_job_runs, set_control_state


def runtime_status(paths: ProjectPaths) -> dict[str, Any]:
    initialize_runtime_state(paths)
    health = read_json(paths.logs_root / "latest_runtime_health_summary.json")
    ledger = read_json(paths.logs_root / "latest_runtime_ledger_summary.json")
    retry = read_json(paths.logs_root / "latest_runtime_retry_queue.json")
    with connect_runtime_db(paths) as conn:
        paused = bool(get_control_state(conn, "paused", False))
        shutdown_requested = bool(get_control_state(conn, "shutdown_requested", False))
    return {
        "status": "PAUSED" if paused else (health.get("runtime_status") or "UNKNOWN"),
        "paused": paused,
        "shutdown_requested": shutdown_requested,
        "health": health.get("summary") if isinstance(health.get("summary"), dict) else {},
        "ledger": ledger.get("summary") if isinstance(ledger.get("summary"), dict) else {},
        "retry": retry.get("summary") if isinstance(retry.get("summary"), dict) else {},
    }


def list_jobs(repo_root: Path) -> dict[str, Any]:
    bundle = load_runtime_config(repo_root)
    jobs = bundle.jobs.get("jobs") if isinstance(bundle.jobs.get("jobs"), dict) else {}
    return {"job_count": len(jobs), "jobs": jobs}


def list_runs(paths: ProjectPaths, limit: int = 30) -> dict[str, Any]:
    initialize_runtime_state(paths)
    with connect_runtime_db(paths) as conn:
        runs = list_job_runs(conn, limit=limit)
    return {"run_count": len(runs), "runs": runs}


def set_pause(paths: ProjectPaths, paused: bool) -> dict[str, Any]:
    initialize_runtime_state(paths)
    with connect_runtime_db(paths) as conn:
        set_control_state(conn, "paused", paused)
    return {"paused": paused}


def request_shutdown(paths: ProjectPaths) -> dict[str, Any]:
    initialize_runtime_state(paths)
    with connect_runtime_db(paths) as conn:
        set_control_state(conn, "shutdown_requested", True)
    return {"shutdown_requested": True}


def cancel_run(paths: ProjectPaths, job_run_id: str) -> dict[str, Any]:
    initialize_runtime_state(paths)
    with connect_runtime_db(paths) as conn:
        conn.execute("UPDATE job_run SET status='CANCELLED', updated_at=datetime('now') WHERE job_run_id=?", (job_run_id,))
        changed = conn.total_changes
        conn.commit()
    return {"job_run_id": job_run_id, "cancelled": changed > 0}


def run_named(repo_root: Path, name: str) -> dict[str, Any]:
    allowed = {
        "daily-end-to-end": [sys.executable, "scripts/run_daily_end_to_end_pipeline.py", "--dry-run"],
        "scheduler-once": [sys.executable, "scripts/run_scheduler_once.py"],
    }
    if name not in allowed:
        return {"status": "REJECTED", "reason": "unknown_or_unsafe_run_target", "name": name}
    completed = subprocess.run(allowed[name], cwd=repo_root, text=True, capture_output=True, check=False)
    return {
        "status": "SUCCESS" if completed.returncode == 0 else "FAILED",
        "name": name,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
    }
