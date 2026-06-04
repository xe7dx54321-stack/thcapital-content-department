"""Build a one-week/multi-week publishing calendar for manual content ops."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__weekly-publishing-calendar.json",
        "dated_md": root / f"{run_date}__weekly-publishing-calendar.md",
        "latest_json": root / "latest_weekly_publishing_calendar.json",
        "latest_md": root / "latest_weekly_publishing_calendar.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__weekly-publishing-calendar-board.md",
        "board_latest_md": paths.frontstage_root / "latest_weekly_publishing_calendar_board.md",
    }


def next_days(days: int) -> list[datetime]:
    today = datetime.now().date()
    return [datetime.combine(today + timedelta(days=offset), datetime.min.time()) for offset in range(days)]


def content_status(item: dict[str, Any]) -> str:
    readiness = item.get("readiness_status")
    if readiness == "READY_TO_PUBLISH":
        return "READY"
    if readiness == "NEEDS_VISUAL_ASSET":
        return "BLOCKED"
    if readiness in {"NEEDS_EVIDENCE", "NEEDS_REWRITE", "BLOCKED"}:
        return "HOLD"
    return "OPEN"


def build_weekly_publishing_calendar(paths: ProjectPaths, repo_root: Path, days: int = 7) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing = paths.market_content_root / "07_publishing"
    phase19_calendar = read_json(publishing / "latest_publishing_session_calendar.json")
    queue = read_json(publishing / "latest_content_queue_priority.json")
    rhythm = read_json(publishing / "latest_weekly_publishing_rhythm.json")
    issue_tracker = read_json(paths.logs_root / "latest_recurring_issue_tracker.json")
    queue_items = list_payload(queue, "items")
    rhythm_items = {item.get("date"): item for item in list_payload(rhythm, "rhythm_plan")}
    existing_slots = {
        slot.get("publish_session_id") or slot.get("copy_pack_id") or slot.get("final_candidate_id"): slot
        for day in list_payload(phase19_calendar, "calendar")
        for slot in day.get("slots", [])
        if isinstance(slot, dict)
    }
    high_issue_count = safe_int((issue_tracker.get("summary") or {}).get("high")) if isinstance(issue_tracker.get("summary"), dict) else 0
    used: set[str] = set()
    calendar: list[dict[str, Any]] = []
    preferred = [item for item in queue_items if item.get("priority") in {"TODAY", "THIS_WEEK"}]
    fallback = [item for item in queue_items if item.get("priority") in {"WATCH", "DEFER"}]
    candidates = preferred + fallback
    for index, dt in enumerate(next_days(days), start=1):
        date = dt.strftime("%Y-%m-%d")
        weekday = dt.strftime("%A")
        rhythm_item = rhythm_items.get(date, {})
        chosen = None
        for item in candidates:
            item_id = item.get("queue_item_id") or item.get("source_id") or item.get("title")
            if item_id in used:
                continue
            if index == 1 and item.get("priority") not in {"TODAY", "THIS_WEEK"}:
                continue
            chosen = item
            used.add(item_id)
            break
        if chosen:
            status = content_status(chosen)
            blockers = list(chosen.get("blockers") or [])
            if high_issue_count and status == "READY":
                status = "NEEDS_REVIEW"
                blockers.append("recurring_issue_high_priority_review")
            slot = {
                "calendar_item_id": make_id("wkcal", run_date, date, chosen.get("queue_item_id")),
                "date": date,
                "weekday": weekday,
                "recommended_slot": rhythm_item.get("recommended_slot") or ("morning" if index <= 5 else "optional"),
                "queue_item_id": chosen.get("queue_item_id", ""),
                "source_id": chosen.get("source_id", ""),
                "title": chosen.get("title") or rhythm_item.get("title") or "Untitled candidate",
                "content_type": chosen.get("content_type") or rhythm_item.get("recommended_content_type") or "unknown",
                "status": status,
                "priority": chosen.get("priority") or "WATCH",
                "readiness_status": chosen.get("readiness_status") or "UNKNOWN",
                "blockers": blockers,
                "recommended_next_action": chosen.get("recommended_next_action") or "review",
                "manual_confirmation_required": True,
            }
        else:
            slot = {
                "calendar_item_id": make_id("wkcal", run_date, date, "open"),
                "date": date,
                "weekday": weekday,
                "recommended_slot": rhythm_item.get("recommended_slot") or ("morning" if index <= 5 else "optional"),
                "queue_item_id": "",
                "source_id": "",
                "title": rhythm_item.get("title") or "Open slot",
                "content_type": rhythm_item.get("recommended_content_type") or "unknown",
                "status": "OPEN" if index <= 5 else "OPTIONAL",
                "priority": "OPEN",
                "readiness_status": "NO_READY_CONTENT",
                "blockers": ["no_ready_queue_item"] if index <= 5 else [],
                "recommended_next_action": "fill_slot_or_hold",
                "manual_confirmation_required": True,
            }
        matched_existing = existing_slots.get(slot.get("source_id")) or existing_slots.get(slot.get("queue_item_id"))
        if matched_existing:
            slot["publish_session_id"] = matched_existing.get("publish_session_id", "")
            slot["copy_pack_id"] = matched_existing.get("copy_pack_id", "")
        calendar.append(slot)
    summary = {
        "calendar_days": len(calendar),
        "ready_days": sum(1 for item in calendar if item.get("status") == "READY"),
        "hold_days": sum(1 for item in calendar if item.get("status") in {"HOLD", "NEEDS_REVIEW"}),
        "blocked_days": sum(1 for item in calendar if item.get("status") == "BLOCKED"),
        "open_days": sum(1 for item in calendar if item.get("status") in {"OPEN", "OPTIONAL"}),
        "manual_confirmation_required": True,
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "window_days": days,
        "calendar": calendar,
        "summary": summary,
        "policy": {"manual_calendar_only": True, "no_auto_session_creation": True, "no_auto_publish": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| {item.get('date')} | {item.get('weekday')} | `{item.get('status')}` | {item.get('title')} | {item.get('recommended_next_action')} |"
        for item in list_payload(payload, "calendar")
    ]
    return f"""# Weekly Publishing Calendar

## Summary

- calendar_days: `{summary.get('calendar_days', 0)}`
- ready_days: `{summary.get('ready_days', 0)}`
- hold_days: `{summary.get('hold_days', 0)}`
- blocked_days: `{summary.get('blocked_days', 0)}`
- open_days: `{summary.get('open_days', 0)}`

| Date | Weekday | Status | Title | Next action |
|---|---|---|---|---|
{chr(10).join(rows)}

This calendar does not create publish sessions and does not publish.
"""
