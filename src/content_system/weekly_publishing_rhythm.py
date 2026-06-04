"""Plan a weekly manual publishing rhythm."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, write_json_and_markdown, utc_now


DEFAULT_MIX = {
    "Monday": "trend_judgment",
    "Tuesday": "company_project_deep_dive",
    "Wednesday": "technical_route_analysis",
    "Thursday": "industry_chain_repricing",
    "Friday": "investment_framework",
}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__weekly-publishing-rhythm.json",
        "dated_md": root / f"{run_date}__weekly-publishing-rhythm.md",
        "latest_json": root / "latest_weekly_publishing_rhythm.json",
        "latest_md": root / "latest_weekly_publishing_rhythm.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__weekly-publishing-rhythm-board.md",
        "board_latest_md": paths.frontstage_root / "latest_weekly_publishing_rhythm_board.md",
    }


def week_dates() -> list[date]:
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    return [monday + timedelta(days=offset) for offset in range(7)]


def find_item(items: list[dict[str, Any]], content_type: str, used: set[str]) -> dict[str, Any]:
    ready = [item for item in items if item.get("queue_item_id") not in used and item.get("readiness_status") == "READY_TO_PUBLISH"]
    same_type = next((item for item in ready if item.get("content_type") == content_type), {})
    return same_type or (ready[0] if ready else {})


def find_backup(items: list[dict[str, Any]], used: set[str]) -> dict[str, Any]:
    return next((item for item in items if item.get("queue_item_id") not in used and item.get("priority") in {"TODAY", "THIS_WEEK"}), {})


def build_weekly_publishing_rhythm(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing_root = paths.market_content_root / "07_publishing"
    queue_payload = read_json(publishing_root / "latest_content_queue_priority.json")
    calendar_payload = read_json(publishing_root / "latest_publishing_session_calendar.json")
    items = sorted(list_payload(queue_payload, "items"), key=lambda item: (-float(item.get("priority_score") or 0), str(item.get("title") or "")))
    used: set[str] = set()
    rhythm = []
    content_mix = {key: 0 for key in DEFAULT_MIX.values()}
    for day in week_dates():
        weekday = day.strftime("%A")
        content_type = DEFAULT_MIX.get(weekday, "")
        selected = find_item(items, content_type, used) if content_type else {}
        backup = find_backup(items, used)
        status = "OPEN"
        reason = "Weekend optional slot; no forced publishing." if not content_type else "Default weekly rhythm slot."
        if selected:
            status = "PLANNED"
            used.add(str(selected.get("queue_item_id") or ""))
            content_mix[content_type] = content_mix.get(content_type, 0) + 1
            reason = f"Ready queue item matches {content_type} rhythm." if selected.get("content_type") == content_type else "Ready queue item fills this slot."
        elif content_type and backup:
            status = "NEEDS_REVIEW"
            reason = "No ready item for preferred content type; backup needs review."
        elif content_type:
            status = "NO_READY_CONTENT"
            reason = "No ready queue content for this default rhythm slot."
        rhythm.append(
            {
                "date": day.isoformat(),
                "weekday": weekday,
                "recommended_slot": "morning" if weekday in {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"} else "afternoon",
                "recommended_content_type": content_type or "optional",
                "recommended_queue_item_id": selected.get("queue_item_id") or "",
                "title": selected.get("title") or "",
                "reason": reason,
                "backup_queue_item_id": "" if selected else backup.get("queue_item_id", ""),
                "status": status,
            }
        )
    summary = {
        "planned_days": len(rhythm),
        "ready_days": sum(1 for item in rhythm if item.get("status") == "PLANNED"),
        "open_days": sum(1 for item in rhythm if item.get("status") == "OPEN"),
        "no_ready_content": sum(1 for item in rhythm if item.get("status") == "NO_READY_CONTENT"),
    }
    dates = week_dates()
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "week_start": dates[0].isoformat(),
        "week_end": dates[-1].isoformat(),
        "rhythm_plan": rhythm,
        "content_mix": content_mix,
        "summary": summary,
        "calendar_summary": calendar_payload.get("summary") if isinstance(calendar_payload.get("summary"), dict) else {},
        "policy": {"advisory_only": True, "no_auto_publish": True, "no_auto_session_creation": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| {item.get('date')} | {item.get('weekday')} | `{item.get('recommended_content_type')}` | `{item.get('status')}` | {item.get('title') or item.get('reason') or ''} |"
        for item in list_payload(payload, "rhythm_plan")
    ) or "| - | - | - | - | No rhythm plan |"
    return f"""# Weekly Publishing Rhythm

## Summary

- planned_days: `{summary.get('planned_days', 0)}`
- ready_days: `{summary.get('ready_days', 0)}`
- open_days: `{summary.get('open_days', 0)}`
- no_ready_content: `{summary.get('no_ready_content', 0)}`

| Date | Weekday | Content Type | Status | Title / Reason |
|---|---|---|---|---|
{rows}
"""
