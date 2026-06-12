"""Live scheduler trigger validation using one-time validation slots."""

from __future__ import annotations

import os
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import today_token, utc_now, write_json_and_markdown
from content_system.runtime_go_live_validation import runtime_pids
from content_system.runtime_state_store import connect_runtime_db, create_validation_slot, get_validation_slot, initialize_runtime_state


def create_live_validation_slot(paths: ProjectPaths, delay_seconds: int = 65) -> dict[str, Any]:
    initialize_runtime_state(paths)
    now = datetime.now().replace(microsecond=0)
    slot_id = f"validation_{uuid.uuid4().hex[:10]}"
    slot = {
        "validation_slot_id": slot_id,
        "job_id": "runtime_validation_noop",
        "business_date": now.date().isoformat(),
        "schedule_slot": slot_id,
        "scheduled_at": (now + timedelta(seconds=delay_seconds)).isoformat(),
        "status": "PENDING",
        "payload": {"purpose": "phase31b_live_trigger"},
    }
    with connect_runtime_db(paths) as conn:
        create_validation_slot(conn, slot)
    return slot


def wait_for_validation_slot(paths: ProjectPaths, validation_slot_id: str, timeout_seconds: int = 180) -> dict[str, Any]:
    deadline = time.time() + timeout_seconds
    latest: dict[str, Any] = {}
    while time.time() < deadline:
        with connect_runtime_db(paths) as conn:
            latest = get_validation_slot(conn, validation_slot_id)
        if latest.get("status") in {"SUCCESS", "FAILED", "SKIPPED_DUPLICATE"}:
            return latest
        time.sleep(3)
    return latest


def run_live_trigger_validation(paths: ProjectPaths, repo_root: Path, delay_seconds: int | None = None, timeout_seconds: int = 180) -> tuple[dict[str, Any], dict[str, Path]]:
    delay = delay_seconds if delay_seconds is not None else int(os.environ.get("THCAP_LIVE_TRIGGER_DELAY_SECONDS", "65"))
    pids = runtime_pids()
    slot = create_live_validation_slot(paths, delay_seconds=delay)
    observed = wait_for_validation_slot(paths, slot["validation_slot_id"], timeout_seconds=timeout_seconds)
    status = "SUCCESS" if observed.get("status") == "SUCCESS" and observed.get("trigger_source") == "AUTONOMOUS_SCHEDULER" and pids else "FAILED"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": status,
        "trigger_source": observed.get("trigger_source", ""),
        "manual_command_execution": False,
        "runtime_pid_at_submit": pids[0] if pids else 0,
        "validation_slot": observed or slot,
        "summary": {
            "scheduled_at": slot.get("scheduled_at", ""),
            "started_at": observed.get("started_at", ""),
            "finished_at": observed.get("finished_at", ""),
            "status": observed.get("status", "TIMEOUT"),
        },
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_runtime_live_trigger_validation.json",
        "latest_md": paths.logs_root / "latest_runtime_live_trigger_validation.md",
    }
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Runtime Live Trigger Validation

- status: `{payload.get('status')}`
- trigger_source: `{payload.get('trigger_source')}`
- manual_command_execution: `{payload.get('manual_command_execution')}`
- scheduled_at: `{summary.get('scheduled_at')}`
- started_at: `{summary.get('started_at')}`
- finished_at: `{summary.get('finished_at')}`
"""
