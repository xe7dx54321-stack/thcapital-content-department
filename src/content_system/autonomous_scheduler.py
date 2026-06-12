"""Internal scheduler for the Content Factory autonomous runtime."""

from __future__ import annotations

import os
import subprocess
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths, get_project_paths
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.runtime_config import load_runtime_config
from content_system.runtime_idempotency import duplicate_run_prevented, idempotency_key
from content_system.runtime_job_registry import load_job_registry
from content_system.runtime_process_lock import RuntimeLockError, RuntimeProcessLock
from content_system.runtime_retry_manager import classify_error, next_retry_time
from content_system.runtime_state_store import (
    connect_runtime_db,
    default_runtime_db_path,
    due_validation_slots,
    get_control_state,
    get_job_run_by_idempotency,
    increment_attempt_count,
    initialize_runtime_state,
    insert_job_attempt,
    set_control_state,
    upsert_job_run,
    upsert_scheduled_run,
    update_job_run_status,
    update_validation_slot,
)


def _shutdown_requested(paths: ProjectPaths) -> bool:
    initialize_runtime_state(paths)
    with connect_runtime_db(paths) as conn:
        return bool(get_control_state(conn, "shutdown_requested", False))


def _clear_shutdown_and_mark_stopping(paths: ProjectPaths) -> None:
    initialize_runtime_state(paths)
    with connect_runtime_db(paths) as conn:
        set_control_state(conn, "shutdown_requested", False)
        conn.execute(
            "UPDATE heartbeat SET last_heartbeat_at=?, status=?, current_job_id='' WHERE runtime_instance_id=(SELECT runtime_instance_id FROM heartbeat ORDER BY last_heartbeat_at DESC LIMIT 1)",
            (utc_now(), "STOPPING"),
        )
        conn.commit()


def runtime_lock_path(paths: ProjectPaths) -> Path:
    return paths.market_content_root / "12_runtime_store" / "content_factory_runtime.lock"


def parse_slot_datetime(now: datetime, slot_time: str) -> datetime:
    hour, minute = [int(part) for part in slot_time.split(":")]
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)


def due_daily_slots(bundle: Any, now: datetime, force_slot: str = "") -> list[dict[str, Any]]:
    daily = bundle.schedule.get("daily_schedule") if isinstance(bundle.schedule.get("daily_schedule"), dict) else {}
    tick_seconds = int(((bundle.schedule.get("runtime") or {}).get("scheduler_tick_seconds") or 30))
    if force_slot:
        slot = daily.get(force_slot)
        if isinstance(slot, dict):
            return [{"slot_id": force_slot, "slot": slot, "scheduled_at": parse_slot_datetime(now, str(slot.get("time", "00:00"))).isoformat()}]
        return []
    due: list[dict[str, Any]] = []
    for slot_id, slot in daily.items():
        if not isinstance(slot, dict) or slot.get("enabled", True) is False:
            continue
        scheduled_at = parse_slot_datetime(now, str(slot.get("time", "00:00")))
        if scheduled_at <= now < scheduled_at + timedelta(seconds=max(60, tick_seconds * 2)):
            due.append({"slot_id": slot_id, "slot": slot, "scheduled_at": scheduled_at.isoformat()})
    return due


def next_daily_slot(bundle: Any, now: datetime) -> str:
    daily = bundle.schedule.get("daily_schedule") if isinstance(bundle.schedule.get("daily_schedule"), dict) else {}
    candidates = []
    for slot_id, slot in daily.items():
        if not isinstance(slot, dict) or slot.get("enabled", True) is False:
            continue
        dt = parse_slot_datetime(now, str(slot.get("time", "00:00")))
        if dt <= now:
            dt += timedelta(days=1)
        candidates.append((dt, slot_id))
    if not candidates:
        return ""
    dt, slot_id = min(candidates, key=lambda item: item[0])
    return f"{slot_id}@{dt.isoformat()}"


def execute_job(job: Any, repo_root: Path, timeout_seconds: int) -> tuple[int, str, str]:
    completed = subprocess.run(
        list(job.command),
        cwd=repo_root,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    return completed.returncode, completed.stdout[-4000:], completed.stderr[-4000:]


def _execute_registered_job(conn: Any, job: Any, repo_root: Path, run: dict[str, Any], execute: bool) -> dict[str, Any]:
    existing = get_job_run_by_idempotency(conn, str(run.get("idempotency_key", "")))
    if duplicate_run_prevented(existing):
        return {
            "job_run_id": existing.get("job_run_id", ""),
            "job_id": job.job_id,
            "status": "SKIPPED_DUPLICATE",
            "reason": "idempotency_prevented_duplicate",
            "existing_status": existing.get("status"),
        }
    run = dict(run)
    run["job_run_id"] = existing.get("job_run_id") or run.get("job_run_id") or f"jobrun_{uuid.uuid4().hex[:12]}"
    run["status"] = "RUNNING" if execute else "SKIPPED"
    run["started_at"] = utc_now() if execute else ""
    upsert_job_run(conn, run)
    if not execute:
        return {"job_run_id": run["job_run_id"], "job_id": job.job_id, "status": "SKIPPED_DRY_RUN"}
    attempt_number = increment_attempt_count(conn, run["job_run_id"])
    started_at = utc_now()
    try:
        exit_code, stdout_tail, stderr_tail = execute_job(job, repo_root, job.timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        exit_code, stdout_tail, stderr_tail = 124, exc.stdout or "", exc.stderr or "timeout"
    finished_at = utc_now()
    status = "SUCCESS" if exit_code == 0 else "FAILED"
    error_class = "" if exit_code == 0 else classify_error(stderr_tail or stdout_tail)
    next_retry_at = "" if exit_code == 0 else next_retry_time({"attempt_count": attempt_number, "job_id": job.job_id}, repo_root)
    insert_job_attempt(
        conn,
        {
            "attempt_id": f"attempt_{uuid.uuid4().hex[:12]}",
            "job_run_id": run["job_run_id"],
            "attempt_number": attempt_number,
            "started_at": started_at,
            "finished_at": finished_at,
            "status": status,
            "exit_code": exit_code,
            "error_class": error_class,
            "error_message": stderr_tail or stdout_tail,
            "stdout_tail": stdout_tail,
            "stderr_tail": stderr_tail,
        },
    )
    update_job_run_status(conn, run["job_run_id"], status, exit_code, checkpoint="FINISHED", error_class=error_class, error_message=stderr_tail or stdout_tail, next_retry_at=next_retry_at)
    return {"job_run_id": run["job_run_id"], "job_id": job.job_id, "status": status, "exit_code": exit_code, "started_at": started_at, "finished_at": finished_at}


def run_scheduler_once(repo_root: Path, execute: bool = False, force_slot: str = "") -> tuple[dict[str, Any], dict[str, Path]]:
    paths = get_project_paths(repo_root)
    run_date = today_token()
    initialize_runtime_state(paths)
    bundle = load_runtime_config(repo_root)
    registry = load_job_registry(repo_root)
    lock_seconds = int((((bundle.policies.get("locking") or {}).get("stale_lock_minutes") or 120) * 60))
    lock = RuntimeProcessLock(runtime_lock_path(paths), stale_after_seconds=lock_seconds)
    runtime_instance_id = f"runtime_{os.getpid()}"
    executed: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    errors: list[str] = []
    now = datetime.now().replace(microsecond=0)
    next_run = next_daily_slot(bundle, now)
    try:
        lock.acquire()
    except RuntimeLockError as exc:
        payload = _scheduler_payload(run_date, "LOCKED", [], [], [str(exc)], next_run)
        return _write_scheduler_once(payload, paths, repo_root)
    try:
        with connect_runtime_db(paths) as conn:
            paused = bool(get_control_state(conn, "paused", False))
            if paused:
                payload = _scheduler_payload(run_date, "PAUSED", [], [{"reason": "runtime_paused"}], [], next_run)
                return _write_scheduler_once(payload, paths, repo_root)
            conn.execute(
                "INSERT OR REPLACE INTO runtime_instance(runtime_instance_id, pid, started_at, status, metadata) VALUES (?, ?, ?, ?, ?)",
                (runtime_instance_id, os.getpid(), utc_now(), "RUNNING", "{}"),
            )
            conn.commit()
            conn.execute(
                """
                INSERT INTO heartbeat(runtime_instance_id, pid, started_at, last_heartbeat_at, status, current_job_id, next_scheduled_run, last_successful_daily_run, payload)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(runtime_instance_id) DO UPDATE SET last_heartbeat_at=excluded.last_heartbeat_at, status=excluded.status, next_scheduled_run=excluded.next_scheduled_run
                """,
                (runtime_instance_id, os.getpid(), utc_now(), utc_now(), "RUNNING", "", next_run, "", "{}"),
            )
            conn.commit()
            now_iso = now.isoformat()
            for validation_slot in due_validation_slots(conn, now_iso):
                job = registry.get(str(validation_slot.get("job_id") or ""))
                if not job:
                    errors.append(f"Unknown validation job {validation_slot.get('job_id')}.")
                    update_validation_slot(conn, str(validation_slot.get("validation_slot_id")), status="FAILED", finished_at=utc_now(), trigger_source="AUTONOMOUS_SCHEDULER")
                    continue
                schedule_slot = str(validation_slot.get("schedule_slot") or f"validation_{validation_slot.get('validation_slot_id')}")
                idem_key = idempotency_key(job.job_id, str(validation_slot.get("business_date") or now.date().isoformat()), schedule_slot, job.idempotency_scope)
                update_validation_slot(conn, str(validation_slot.get("validation_slot_id")), status="RUNNING", started_at=utc_now(), trigger_source="AUTONOMOUS_SCHEDULER")
                result = _execute_registered_job(
                    conn,
                    job,
                    repo_root,
                    {
                        "job_run_id": f"jobrun_{uuid.uuid4().hex[:12]}",
                        "scheduled_run_id": str(validation_slot.get("validation_slot_id")),
                        "job_id": job.job_id,
                        "business_date": str(validation_slot.get("business_date") or now.date().isoformat()),
                        "schedule_slot": schedule_slot,
                        "scheduled_at": str(validation_slot.get("scheduled_at") or ""),
                        "idempotency_key": idem_key,
                        "checkpoint": "VALIDATION_SLOT",
                    },
                    execute=execute,
                )
                update_validation_slot(
                    conn,
                    str(validation_slot.get("validation_slot_id")),
                    status="SUCCESS" if result.get("status") == "SUCCESS" else str(result.get("status") or "FAILED"),
                    job_run_id=str(result.get("job_run_id") or ""),
                    finished_at=result.get("finished_at") or utc_now(),
                    trigger_source="AUTONOMOUS_SCHEDULER",
                )
                if result.get("status") == "SKIPPED_DUPLICATE":
                    skipped.append(result)
                else:
                    executed.append(result)
            for due in due_daily_slots(bundle, now, force_slot=force_slot):
                slot_id = str(due["slot_id"])
                scheduled_run_id = f"srun_{run_date}_{slot_id}"
                upsert_scheduled_run(
                    conn,
                    {
                        "scheduled_run_id": scheduled_run_id,
                        "business_date": now.date().isoformat(),
                        "schedule_slot": slot_id,
                        "scheduled_at": due.get("scheduled_at", ""),
                        "status": "RUNNING",
                    },
                )
                for job_id in due["slot"].get("jobs", []) or []:
                    job = registry.get(str(job_id))
                    if not job:
                        errors.append(f"Unknown job {job_id}.")
                        continue
                    idem_key = idempotency_key(job.job_id, now.date().isoformat(), slot_id, job.idempotency_scope)
                    result = _execute_registered_job(
                        conn,
                        job,
                        repo_root,
                        {
                            "job_run_id": f"jobrun_{uuid.uuid4().hex[:12]}",
                            "scheduled_run_id": scheduled_run_id,
                            "job_id": job.job_id,
                            "business_date": now.date().isoformat(),
                            "schedule_slot": slot_id,
                            "scheduled_at": due.get("scheduled_at", ""),
                            "idempotency_key": idem_key,
                            "checkpoint": "SCHEDULED",
                        },
                        execute=execute,
                    )
                    if result.get("status") in {"SKIPPED_DRY_RUN", "SKIPPED_DUPLICATE"}:
                        result["schedule_slot"] = slot_id
                        skipped.append(result)
                    else:
                        executed.append(result)
            conn.execute(
                "UPDATE heartbeat SET last_heartbeat_at=?, status=?, current_job_id='' WHERE runtime_instance_id=?",
                (utc_now(), "IDLE", runtime_instance_id),
            )
            conn.commit()
    finally:
        lock.release()
    status = "SUCCESS" if not errors else "ACTIONABLE"
    payload = _scheduler_payload(run_date, status, executed, skipped, errors, next_run)
    return _write_scheduler_once(payload, paths, repo_root)


def _scheduler_payload(run_date: str, status: str, executed: list[dict[str, Any]], skipped: list[dict[str, Any]], errors: list[str], next_run: str) -> dict[str, Any]:
    return {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "executed_jobs": executed,
        "skipped_jobs": skipped,
        "errors": errors,
        "summary": {
            "executed_count": len(executed),
            "skipped_count": len(skipped),
            "error_count": len(errors),
            "next_scheduled_run": next_run,
        },
    }


def _write_scheduler_once(payload: dict[str, Any], paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    outputs = {
        "dated_json": paths.logs_root / f"{payload['run_date']}__scheduler-once.json",
        "dated_md": paths.logs_root / f"{payload['run_date']}__scheduler-once.md",
        "latest_json": paths.logs_root / "latest_scheduler_once.json",
        "latest_md": paths.logs_root / "latest_scheduler_once.md",
    }
    write_json_and_markdown(payload, render_scheduler_markdown(payload), outputs)
    payload["runtime_db_path"] = repo_relative(default_runtime_db_path(paths), repo_root)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_scheduler_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Scheduler Once

- status: `{payload.get('status')}`
- executed_count: `{summary.get('executed_count', 0)}`
- skipped_count: `{summary.get('skipped_count', 0)}`
- error_count: `{summary.get('error_count', 0)}`
- next_scheduled_run: `{summary.get('next_scheduled_run', '')}`
"""


def run_autonomous_runtime_loop(repo_root: Path) -> None:
    paths = get_project_paths(repo_root)
    bundle = load_runtime_config(repo_root)
    heartbeat_seconds = int(((bundle.schedule.get("runtime") or {}).get("heartbeat_seconds") or 60))
    while True:
        if _shutdown_requested(paths):
            _clear_shutdown_and_mark_stopping(paths)
            return
        run_scheduler_once(repo_root, execute=True)
        remaining = max(heartbeat_seconds, 10)
        while remaining > 0:
            if _shutdown_requested(paths):
                _clear_shutdown_and_mark_stopping(paths)
                return
            sleep_for = min(5, remaining)
            time.sleep(sleep_for)
            remaining -= sleep_for
