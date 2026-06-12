"""SQLite-backed state store for the autonomous runtime."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import utc_now


SCHEMA_VERSION = "v1"
RUNTIME_DB_ENV = "THCAP_AUTONOMOUS_RUNTIME_DB"


def runtime_store_root(paths: ProjectPaths) -> Path:
    return paths.market_content_root / "12_runtime_store"


def default_runtime_db_path(paths: ProjectPaths) -> Path:
    override = os.environ.get(RUNTIME_DB_ENV, "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return runtime_store_root(paths) / "autonomous_runtime.sqlite"


def connect_runtime_db(paths: ProjectPaths | None = None, db_path: Path | None = None) -> sqlite3.Connection:
    if db_path is None:
        if paths is None:
            raise ValueError("paths or db_path is required")
        db_path = default_runtime_db_path(paths)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA foreign_keys=ON")
    return connection


def initialize_runtime_state(paths: ProjectPaths | None = None, db_path: Path | None = None) -> Path:
    if db_path is None:
        if paths is None:
            raise ValueError("paths or db_path is required")
        db_path = default_runtime_db_path(paths)
    with connect_runtime_db(paths, db_path) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS runtime_instance (
              runtime_instance_id TEXT PRIMARY KEY,
              pid INTEGER,
              started_at TEXT,
              status TEXT,
              metadata TEXT
            );

            CREATE TABLE IF NOT EXISTS scheduled_run (
              scheduled_run_id TEXT PRIMARY KEY,
              business_date TEXT,
              schedule_slot TEXT,
              scheduled_at TEXT,
              status TEXT,
              created_at TEXT,
              updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS job_run (
              job_run_id TEXT PRIMARY KEY,
              scheduled_run_id TEXT,
              job_id TEXT,
              business_date TEXT,
              schedule_slot TEXT,
              scheduled_at TEXT,
              started_at TEXT,
              finished_at TEXT,
              status TEXT,
              attempt_count INTEGER DEFAULT 0,
              exit_code INTEGER DEFAULT 0,
              checkpoint TEXT,
              idempotency_key TEXT UNIQUE,
              artifact_refs TEXT,
              error_class TEXT,
              error_message TEXT,
              next_retry_at TEXT,
              created_at TEXT,
              updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS job_attempt (
              attempt_id TEXT PRIMARY KEY,
              job_run_id TEXT,
              attempt_number INTEGER,
              started_at TEXT,
              finished_at TEXT,
              status TEXT,
              exit_code INTEGER,
              error_class TEXT,
              error_message TEXT,
              stdout_tail TEXT,
              stderr_tail TEXT,
              FOREIGN KEY(job_run_id) REFERENCES job_run(job_run_id)
            );

            CREATE TABLE IF NOT EXISTS checkpoint (
              checkpoint_id TEXT PRIMARY KEY,
              job_run_id TEXT,
              checkpoint TEXT,
              status TEXT,
              payload TEXT,
              updated_at TEXT,
              FOREIGN KEY(job_run_id) REFERENCES job_run(job_run_id)
            );

            CREATE TABLE IF NOT EXISTS artifact_reference (
              artifact_id TEXT PRIMARY KEY,
              job_run_id TEXT,
              path TEXT,
              kind TEXT,
              created_at TEXT,
              FOREIGN KEY(job_run_id) REFERENCES job_run(job_run_id)
            );

            CREATE TABLE IF NOT EXISTS heartbeat (
              runtime_instance_id TEXT PRIMARY KEY,
              pid INTEGER,
              started_at TEXT,
              last_heartbeat_at TEXT,
              status TEXT,
              current_job_id TEXT,
              next_scheduled_run TEXT,
              last_successful_daily_run TEXT,
              payload TEXT
            );

            CREATE TABLE IF NOT EXISTS runtime_event (
              event_id TEXT PRIMARY KEY,
              created_at TEXT,
              level TEXT,
              event_type TEXT,
              message TEXT,
              context TEXT
            );

            CREATE TABLE IF NOT EXISTS control_state (
              key TEXT PRIMARY KEY,
              value TEXT,
              updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS validation_slot (
              validation_slot_id TEXT PRIMARY KEY,
              job_id TEXT,
              business_date TEXT,
              schedule_slot TEXT,
              scheduled_at TEXT,
              status TEXT,
              trigger_source TEXT,
              job_run_id TEXT,
              created_at TEXT,
              started_at TEXT,
              finished_at TEXT,
              updated_at TEXT,
              payload TEXT
            );
            """
        )
        conn.commit()
    return db_path


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any]:
    if row is None:
        return {}
    result = dict(row)
    for key in ("artifact_refs", "metadata", "payload", "context", "value"):
        if key in result and isinstance(result.get(key), str) and result.get(key):
            try:
                result[key] = json.loads(result[key])
            except json.JSONDecodeError:
                pass
    return result


def upsert_runtime_instance(conn: sqlite3.Connection, runtime_instance_id: str, pid: int, status: str, metadata: dict[str, Any] | None = None) -> None:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO runtime_instance(runtime_instance_id, pid, started_at, status, metadata)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(runtime_instance_id) DO UPDATE SET pid=excluded.pid, status=excluded.status, metadata=excluded.metadata
        """,
        (runtime_instance_id, pid, now, status, _json_dumps(metadata or {})),
    )
    conn.commit()


def upsert_heartbeat(
    conn: sqlite3.Connection,
    runtime_instance_id: str,
    pid: int,
    status: str,
    current_job_id: str = "",
    next_scheduled_run: str = "",
    last_successful_daily_run: str = "",
    payload: dict[str, Any] | None = None,
) -> None:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO heartbeat(runtime_instance_id, pid, started_at, last_heartbeat_at, status, current_job_id, next_scheduled_run, last_successful_daily_run, payload)
        VALUES (?, ?, COALESCE((SELECT started_at FROM heartbeat WHERE runtime_instance_id=?), ?), ?, ?, ?, ?, ?, ?)
        ON CONFLICT(runtime_instance_id) DO UPDATE SET
          pid=excluded.pid,
          last_heartbeat_at=excluded.last_heartbeat_at,
          status=excluded.status,
          current_job_id=excluded.current_job_id,
          next_scheduled_run=excluded.next_scheduled_run,
          last_successful_daily_run=excluded.last_successful_daily_run,
          payload=excluded.payload
        """,
        (runtime_instance_id, pid, runtime_instance_id, now, now, status, current_job_id, next_scheduled_run, last_successful_daily_run, _json_dumps(payload or {})),
    )
    conn.commit()


def latest_heartbeat(conn: sqlite3.Connection) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM heartbeat ORDER BY last_heartbeat_at DESC LIMIT 1").fetchone()
    return _row_to_dict(row)


def upsert_scheduled_run(conn: sqlite3.Connection, run: dict[str, Any]) -> None:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO scheduled_run(scheduled_run_id, business_date, schedule_slot, scheduled_at, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(scheduled_run_id) DO UPDATE SET status=excluded.status, updated_at=excluded.updated_at
        """,
        (
            run["scheduled_run_id"],
            run.get("business_date", ""),
            run.get("schedule_slot", ""),
            run.get("scheduled_at", ""),
            run.get("status", "PENDING"),
            now,
            now,
        ),
    )
    conn.commit()


def get_job_run_by_idempotency(conn: sqlite3.Connection, idempotency_key: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM job_run WHERE idempotency_key = ?", (idempotency_key,)).fetchone()
    return _row_to_dict(row)


def upsert_job_run(conn: sqlite3.Connection, run: dict[str, Any]) -> dict[str, Any]:
    now = utc_now()
    artifact_refs = run.get("artifact_refs")
    conn.execute(
        """
        INSERT INTO job_run(
          job_run_id, scheduled_run_id, job_id, business_date, schedule_slot, scheduled_at,
          started_at, finished_at, status, attempt_count, exit_code, checkpoint,
          idempotency_key, artifact_refs, error_class, error_message, next_retry_at,
          created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(idempotency_key) DO UPDATE SET
          scheduled_run_id=excluded.scheduled_run_id,
          started_at=COALESCE(excluded.started_at, job_run.started_at),
          finished_at=excluded.finished_at,
          status=excluded.status,
          attempt_count=excluded.attempt_count,
          exit_code=excluded.exit_code,
          checkpoint=excluded.checkpoint,
          artifact_refs=excluded.artifact_refs,
          error_class=excluded.error_class,
          error_message=excluded.error_message,
          next_retry_at=excluded.next_retry_at,
          updated_at=excluded.updated_at
        """,
        (
            run["job_run_id"],
            run.get("scheduled_run_id", ""),
            run.get("job_id", ""),
            run.get("business_date", ""),
            run.get("schedule_slot", ""),
            run.get("scheduled_at", ""),
            run.get("started_at", ""),
            run.get("finished_at", ""),
            run.get("status", "PENDING"),
            int(run.get("attempt_count") or 0),
            int(run.get("exit_code") or 0),
            run.get("checkpoint", ""),
            run.get("idempotency_key", ""),
            _json_dumps(artifact_refs if isinstance(artifact_refs, list) else []),
            run.get("error_class", ""),
            run.get("error_message", ""),
            run.get("next_retry_at", ""),
            now,
            now,
        ),
    )
    conn.commit()
    return get_job_run_by_idempotency(conn, str(run.get("idempotency_key", "")))


def update_job_run_status(
    conn: sqlite3.Connection,
    job_run_id: str,
    status: str,
    exit_code: int = 0,
    checkpoint: str = "",
    error_class: str = "",
    error_message: str = "",
    next_retry_at: str = "",
) -> None:
    conn.execute(
        """
        UPDATE job_run
        SET status=?, exit_code=?, checkpoint=COALESCE(NULLIF(?, ''), checkpoint),
            error_class=?, error_message=?, next_retry_at=?, finished_at=?, updated_at=?
        WHERE job_run_id=?
        """,
        (status, exit_code, checkpoint, error_class, error_message, next_retry_at, utc_now(), utc_now(), job_run_id),
    )
    conn.commit()


def increment_attempt_count(conn: sqlite3.Connection, job_run_id: str) -> int:
    row = conn.execute("SELECT attempt_count FROM job_run WHERE job_run_id=?", (job_run_id,)).fetchone()
    next_count = int(row["attempt_count"] or 0) + 1 if row else 1
    conn.execute("UPDATE job_run SET attempt_count=?, updated_at=? WHERE job_run_id=?", (next_count, utc_now(), job_run_id))
    conn.commit()
    return next_count


def insert_job_attempt(conn: sqlite3.Connection, attempt: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO job_attempt(attempt_id, job_run_id, attempt_number, started_at, finished_at, status, exit_code, error_class, error_message, stdout_tail, stderr_tail)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            attempt["attempt_id"],
            attempt.get("job_run_id", ""),
            int(attempt.get("attempt_number") or 0),
            attempt.get("started_at", ""),
            attempt.get("finished_at", ""),
            attempt.get("status", ""),
            int(attempt.get("exit_code") or 0),
            attempt.get("error_class", ""),
            attempt.get("error_message", ""),
            attempt.get("stdout_tail", ""),
            attempt.get("stderr_tail", ""),
        ),
    )
    conn.commit()


def list_job_runs(conn: sqlite3.Connection, limit: int = 200, statuses: tuple[str, ...] | None = None) -> list[dict[str, Any]]:
    if statuses:
        placeholders = ",".join("?" for _ in statuses)
        rows = conn.execute(f"SELECT * FROM job_run WHERE status IN ({placeholders}) ORDER BY updated_at DESC LIMIT ?", (*statuses, limit)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM job_run ORDER BY updated_at DESC LIMIT ?", (limit,)).fetchall()
    return [_row_to_dict(row) for row in rows]


def record_checkpoint(conn: sqlite3.Connection, checkpoint_id: str, job_run_id: str, checkpoint: str, status: str, payload: dict[str, Any] | None = None) -> None:
    conn.execute(
        """
        INSERT INTO checkpoint(checkpoint_id, job_run_id, checkpoint, status, payload, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(checkpoint_id) DO UPDATE SET checkpoint=excluded.checkpoint, status=excluded.status, payload=excluded.payload, updated_at=excluded.updated_at
        """,
        (checkpoint_id, job_run_id, checkpoint, status, _json_dumps(payload or {}), utc_now()),
    )
    conn.commit()


def read_checkpoint(conn: sqlite3.Connection, checkpoint_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM checkpoint WHERE checkpoint_id=?", (checkpoint_id,)).fetchone()
    return _row_to_dict(row)


def record_runtime_event(conn: sqlite3.Connection, event_id: str, level: str, event_type: str, message: str, context: dict[str, Any] | None = None) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO runtime_event(event_id, created_at, level, event_type, message, context) VALUES (?, ?, ?, ?, ?, ?)",
        (event_id, utc_now(), level, event_type, message, _json_dumps(context or {})),
    )
    conn.commit()


def set_control_state(conn: sqlite3.Connection, key: str, value: Any) -> None:
    conn.execute(
        """
        INSERT INTO control_state(key, value, updated_at) VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
        """,
        (key, _json_dumps(value), utc_now()),
    )
    conn.commit()


def get_control_state(conn: sqlite3.Connection, key: str, default: Any = None) -> Any:
    row = conn.execute("SELECT value FROM control_state WHERE key=?", (key,)).fetchone()
    if row is None:
        return default
    try:
        return json.loads(row["value"])
    except (TypeError, json.JSONDecodeError):
        return row["value"]


def status_counts(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute("SELECT status, COUNT(*) AS count FROM job_run GROUP BY status").fetchall()
    return {str(row["status"] or "UNKNOWN"): int(row["count"] or 0) for row in rows}


def create_validation_slot(conn: sqlite3.Connection, slot: dict[str, Any]) -> None:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO validation_slot(
          validation_slot_id, job_id, business_date, schedule_slot, scheduled_at,
          status, trigger_source, job_run_id, created_at, started_at, finished_at,
          updated_at, payload
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(validation_slot_id) DO UPDATE SET
          job_id=excluded.job_id,
          business_date=excluded.business_date,
          schedule_slot=excluded.schedule_slot,
          scheduled_at=excluded.scheduled_at,
          status=excluded.status,
          trigger_source=excluded.trigger_source,
          job_run_id=excluded.job_run_id,
          started_at=excluded.started_at,
          finished_at=excluded.finished_at,
          updated_at=excluded.updated_at,
          payload=excluded.payload
        """,
        (
            slot["validation_slot_id"],
            slot.get("job_id", ""),
            slot.get("business_date", ""),
            slot.get("schedule_slot", ""),
            slot.get("scheduled_at", ""),
            slot.get("status", "PENDING"),
            slot.get("trigger_source", ""),
            slot.get("job_run_id", ""),
            now,
            slot.get("started_at", ""),
            slot.get("finished_at", ""),
            now,
            _json_dumps(slot.get("payload") if isinstance(slot.get("payload"), dict) else {}),
        ),
    )
    conn.commit()


def due_validation_slots(conn: sqlite3.Connection, now_iso: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT * FROM validation_slot
        WHERE status IN ('PENDING', 'RUNNING') AND scheduled_at <= ?
        ORDER BY scheduled_at ASC
        """,
        (now_iso,),
    ).fetchall()
    return [_row_to_dict(row) for row in rows]


def get_validation_slot(conn: sqlite3.Connection, validation_slot_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM validation_slot WHERE validation_slot_id=?", (validation_slot_id,)).fetchone()
    return _row_to_dict(row)


def update_validation_slot(conn: sqlite3.Connection, validation_slot_id: str, **updates: Any) -> None:
    if not updates:
        return
    allowed = {"status", "trigger_source", "job_run_id", "started_at", "finished_at", "payload"}
    pairs = [(key, value) for key, value in updates.items() if key in allowed]
    if not pairs:
        return
    assignments = ", ".join(f"{key}=?" for key, _ in pairs)
    values = [_json_dumps(value) if key == "payload" and isinstance(value, dict) else value for key, value in pairs]
    values.extend([utc_now(), validation_slot_id])
    conn.execute(f"UPDATE validation_slot SET {assignments}, updated_at=? WHERE validation_slot_id=?", values)
    conn.commit()
