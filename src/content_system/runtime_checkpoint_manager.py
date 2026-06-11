"""Checkpoint helpers for restartable runtime jobs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.runtime_state_store import connect_runtime_db, initialize_runtime_state, read_checkpoint, record_checkpoint


def checkpoint_id(job_run_id: str, checkpoint_name: str) -> str:
    return f"{job_run_id}:{checkpoint_name}"


def write_checkpoint(paths: ProjectPaths, job_run_id: str, checkpoint_name: str, status: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    db_path = initialize_runtime_state(paths)
    ident = checkpoint_id(job_run_id, checkpoint_name)
    with connect_runtime_db(paths, db_path) as conn:
        record_checkpoint(conn, ident, job_run_id, checkpoint_name, status, payload or {})
        return read_checkpoint(conn, ident)


def load_checkpoint(paths: ProjectPaths, job_run_id: str, checkpoint_name: str) -> dict[str, Any]:
    db_path = initialize_runtime_state(paths)
    with connect_runtime_db(paths, db_path) as conn:
        return read_checkpoint(conn, checkpoint_id(job_run_id, checkpoint_name))
