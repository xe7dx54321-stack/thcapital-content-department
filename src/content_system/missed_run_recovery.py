"""Missed-run detection and compressed catch-up planning."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.runtime_config import load_runtime_config
from content_system.runtime_state_store import connect_runtime_db, initialize_runtime_state, list_job_runs


def detect_missed_runs(repo_root: Path, paths: ProjectPaths, now: datetime | None = None) -> dict[str, Any]:
    now = (now or datetime.now()).replace(microsecond=0)
    bundle = load_runtime_config(repo_root)
    runtime = bundle.schedule.get("runtime") if isinstance(bundle.schedule.get("runtime"), dict) else {}
    lookback_hours = int(runtime.get("catchup_max_age_hours") or 24)
    cutoff = now - timedelta(hours=lookback_hours)
    daily = bundle.schedule.get("daily_schedule") if isinstance(bundle.schedule.get("daily_schedule"), dict) else {}
    db_path = initialize_runtime_state(paths)
    with connect_runtime_db(paths, db_path) as conn:
        runs = list_job_runs(conn, limit=500)
    completed_keys = {(item.get("business_date"), item.get("schedule_slot")) for item in runs if item.get("status") in {"SUCCESS", "ACTIONABLE", "DEGRADED", "SKIPPED"}}
    missed = []
    for day_offset in (1, 0):
        day = (now.date() - timedelta(days=day_offset))
        for slot_id, slot in daily.items():
            if not isinstance(slot, dict) or slot.get("enabled", True) is False:
                continue
            hour, minute = [int(part) for part in str(slot.get("time", "00:00")).split(":")]
            scheduled_at = datetime.combine(day, datetime.min.time()).replace(hour=hour, minute=minute)
            if cutoff <= scheduled_at < now and (day.isoformat(), slot_id) not in completed_keys:
                missed.append({"business_date": day.isoformat(), "schedule_slot": slot_id, "scheduled_at": scheduled_at.isoformat(), "jobs": slot.get("jobs", [])})
    catchup_plan = compress_catchup_plan(missed, now)
    return {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "missed_runs": missed,
        "catchup_plan": catchup_plan,
        "summary": {
            "missed_count": len(missed),
            "catchup_count": len(catchup_plan),
            "compressed": len(catchup_plan) < len(missed),
        },
    }


def compress_catchup_plan(missed: list[dict[str, Any]], now: datetime) -> list[dict[str, Any]]:
    if not missed:
        return []
    slots = {str(item.get("schedule_slot")) for item in missed}
    if now.hour >= 18 and len(missed) > 1:
        return [
            {
                "catchup_id": f"catchup_{today_token()}_evening_consolidated",
                "action": "RUN_EVENING_CONSOLIDATED",
                "source_slots": sorted(slots),
                "reason": "compress stale acquisition slots into one evening consolidated run",
            }
        ]
    return [
        {
            "catchup_id": f"catchup_{item.get('business_date')}_{item.get('schedule_slot')}",
            "action": "RUN_SLOT",
            "source_slots": [item.get("schedule_slot")],
            "reason": "recent missed slot still valuable",
        }
        for item in missed
    ]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__missed-run-recovery-plan.json",
        "dated_md": paths.logs_root / f"{run_date}__missed-run-recovery-plan.md",
        "latest_json": paths.logs_root / "latest_missed_run_recovery_plan.json",
        "latest_md": paths.logs_root / "latest_missed_run_recovery_plan.md",
    }


def build_missed_run_recovery_plan(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    payload = detect_missed_runs(repo_root, paths)
    outputs = output_paths(paths, payload["run_date"])
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def execute_missed_run_recovery(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    payload, _ = build_missed_run_recovery_plan(paths, repo_root)
    payload["execution_mode"] = "PLAN_ONLY"
    payload["executed"] = []
    return payload, {}


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(f"- {item.get('action')}: {item.get('source_slots')}" for item in payload.get("catchup_plan", [])) or "- None"
    return f"""# Missed-run Recovery Plan

- missed_count: `{summary.get('missed_count', 0)}`
- catchup_count: `{summary.get('catchup_count', 0)}`
- compressed: `{summary.get('compressed', False)}`

## Catch-up Plan

{rows}
"""
