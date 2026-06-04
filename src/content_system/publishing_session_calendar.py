"""Build a manual publishing session calendar view."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__publishing-session-calendar.json",
        "dated_md": root / f"{run_date}__publishing-session-calendar.md",
        "latest_json": root / "latest_publishing_session_calendar.json",
        "latest_md": root / "latest_publishing_session_calendar.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__publishing-session-calendar-board.md",
        "board_latest_md": paths.frontstage_root / "latest_publishing_session_calendar_board.md",
    }


def parse_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return text[:10] if len(text) >= 10 else ""


def date_range(days: int = 7) -> list[datetime]:
    today = datetime.now().date()
    return [datetime.combine(today + timedelta(days=offset), datetime.min.time()) for offset in range(days)]


def pack_lookup(copy_packs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item.get("copy_pack_id") or item.get("visual_final_candidate_id") or ""): item for item in copy_packs}


def candidate_lookup(candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item.get("final_candidate_id") or ""): item for item in candidates}


def checklist_lookup(checklists: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item.get("copy_pack_id") or item.get("visual_final_candidate_id") or ""): item for item in checklists}


def status_from_session(session: dict[str, Any], pack: dict[str, Any], checklist: dict[str, Any]) -> str:
    publish_status = str(session.get("publish_status") or "")
    if publish_status == "MANUALLY_PUBLISHED":
        return "PUBLISHED"
    if publish_status == "DEFERRED":
        return "DEFERRED"
    if publish_status == "CANCELLED":
        return "CANCELLED"
    pack_status = str(pack.get("pack_status") or "")
    checklist_status = str(checklist.get("status") or "")
    if pack_status == "READY_FOR_MANUAL_COPY" and checklist_status == "READY":
        return "READY"
    if pack_status == "NEEDS_VISUAL_ASSET":
        return "NEEDS_ASSET"
    if checklist_status in {"NEEDS_ATTENTION", "BLOCKED"}:
        return "NEEDS_REVIEW"
    return "PLANNED"


def status_from_pack(pack: dict[str, Any], checklist: dict[str, Any]) -> str:
    pack_status = str(pack.get("pack_status") or "")
    checklist_status = str(checklist.get("status") or "")
    if pack_status == "READY_FOR_MANUAL_COPY" and checklist_status == "READY":
        return "READY"
    if pack_status == "NEEDS_VISUAL_ASSET":
        return "NEEDS_ASSET"
    if pack_status == "BLOCKED" or checklist_status == "BLOCKED":
        return "NEEDS_REVIEW"
    if checklist_status == "NEEDS_ATTENTION":
        return "NEEDS_REVIEW"
    return "PLANNED"


def readiness(pack: dict[str, Any], checklist: dict[str, Any]) -> dict[str, bool]:
    return {
        "has_copy_pack": bool(pack),
        "has_visual_checklist": bool(checklist),
        "needs_visual_asset": str(pack.get("pack_status") or "") == "NEEDS_VISUAL_ASSET",
        "manual_confirmation_required": True,
    }


def slot_from_session(run_date: str, session: dict[str, Any], pack: dict[str, Any], candidate: dict[str, Any], checklist: dict[str, Any]) -> dict[str, Any]:
    final_candidate_id = str(session.get("final_candidate_id") or candidate.get("final_candidate_id") or "")
    title = pack.get("title_to_copy") or candidate.get("wechat_title") or candidate.get("title") or ""
    return {
        "slot_id": make_id("pubslot", run_date, session.get("publish_session_id"), final_candidate_id),
        "planned_time": "10:00",
        "platform": session.get("platform") or "wechat",
        "publish_session_id": session.get("publish_session_id") or "",
        "copy_pack_id": pack.get("copy_pack_id") or "",
        "final_candidate_id": final_candidate_id,
        "title": title,
        "content_type": candidate.get("recipe_id") or "unknown",
        "status": status_from_session(session, pack, checklist),
        "readiness": readiness(pack, checklist),
        "notes": [session.get("manual_note")] if session.get("manual_note") else [],
    }


def slot_from_pack(run_date: str, pack: dict[str, Any], checklist: dict[str, Any]) -> dict[str, Any]:
    return {
        "slot_id": make_id("pubslot", run_date, pack.get("copy_pack_id"), "candidate"),
        "planned_time": "10:00",
        "platform": "wechat",
        "publish_session_id": "",
        "copy_pack_id": pack.get("copy_pack_id") or "",
        "final_candidate_id": "",
        "title": pack.get("title_to_copy") or "",
        "content_type": "unknown",
        "status": status_from_pack(pack, checklist),
        "readiness": readiness(pack, checklist),
        "notes": ["Scheduling candidate generated from copy pack; no publish session was created."],
    }


def summarize(calendar: list[dict[str, Any]]) -> dict[str, int]:
    slots = [slot for day in calendar for slot in day.get("slots", []) if isinstance(slot, dict)]
    return {
        "calendar_days": len(calendar),
        "planned_slots": len(slots),
        "ready_slots": sum(1 for slot in slots if slot.get("status") == "READY"),
        "needs_asset": sum(1 for slot in slots if slot.get("status") == "NEEDS_ASSET"),
        "published": sum(1 for slot in slots if slot.get("status") == "PUBLISHED"),
        "deferred": sum(1 for slot in slots if slot.get("status") == "DEFERRED"),
    }


def build_publishing_session_calendar(paths: ProjectPaths, repo_root: Path, days: int = 7) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing_root = paths.market_content_root / "07_publishing"
    sessions = list_payload(read_json(publishing_root / "latest_manual_publish_sessions.json"), "sessions")
    copy_packs = list_payload(read_json(publishing_root / "latest_wechat_copy_pack_with_images.json"), "packs")
    checklists = list_payload(read_json(publishing_root / "latest_visual_publishing_checklist.json"), "checklists")
    candidates = list_payload(read_json(publishing_root / "latest_final_article_candidates.json"), "candidates")
    packs_by_id = pack_lookup(copy_packs)
    candidates_by_id = candidate_lookup(candidates)
    checklists_by_pack = checklist_lookup(checklists)
    calendar_days = date_range(days)
    day_slots: dict[str, list[dict[str, Any]]] = {day.date().isoformat(): [] for day in calendar_days}
    used_pack_ids: set[str] = set()
    for session in sessions:
        date_key = parse_date(session.get("planned_publish_at")) or parse_date(session.get("actual_publish_at")) or calendar_days[0].date().isoformat()
        if date_key not in day_slots:
            continue
        final_candidate_id = str(session.get("final_candidate_id") or "")
        candidate = candidates_by_id.get(final_candidate_id, {})
        pack = next((item for item in copy_packs if item.get("visual_final_candidate_id") == candidate.get("visual_final_candidate_id")), {})
        if not pack and copy_packs:
            pack = copy_packs[0]
        used_pack_ids.add(str(pack.get("copy_pack_id") or ""))
        checklist = checklists_by_pack.get(str(pack.get("copy_pack_id") or ""), {})
        day_slots[date_key].append(slot_from_session(run_date, session, pack, candidate, checklist))
    if not any(day_slots.values()):
        for pack in copy_packs[:3]:
            checklist = checklists_by_pack.get(str(pack.get("copy_pack_id") or ""), {})
            day_slots[calendar_days[0].date().isoformat()].append(slot_from_pack(run_date, pack, checklist))
            used_pack_ids.add(str(pack.get("copy_pack_id") or ""))
    calendar = [
        {"date": day.date().isoformat(), "weekday": day.strftime("%A"), "slots": day_slots.get(day.date().isoformat(), [])}
        for day in calendar_days
    ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "calendar": calendar,
        "summary": summarize(calendar),
        "policy": {"manual_calendar_only": True, "no_auto_publish": True, "no_auto_session_creation": True, "no_wechat_api": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = []
    for day in list_payload(payload, "calendar"):
        slots = day.get("slots") if isinstance(day.get("slots"), list) else []
        if not slots:
            rows.append(f"| {day.get('date')} | {day.get('weekday')} | - | OPEN | - |")
        for slot in slots:
            if isinstance(slot, dict):
                rows.append(f"| {day.get('date')} | {day.get('weekday')} | `{slot.get('slot_id')}` | `{slot.get('status')}` | {slot.get('title') or ''} |")
    return f"""# Publishing Session Calendar

## Summary

- calendar_days: `{summary.get('calendar_days', 0)}`
- planned_slots: `{summary.get('planned_slots', 0)}`
- ready_slots: `{summary.get('ready_slots', 0)}`
- needs_asset: `{summary.get('needs_asset', 0)}`
- published: `{summary.get('published', 0)}`
- deferred: `{summary.get('deferred', 0)}`
- no_auto_publish: `true`

| Date | Weekday | Slot | Status | Title |
|---|---|---|---|---|
{chr(10).join(rows) if rows else '| - | - | - | - | No calendar slots |'}
"""
