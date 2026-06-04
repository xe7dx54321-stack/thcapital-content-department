"""Calibrate weekly publishing calendar readiness from repaired queue status."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__publishing-calendar-readiness-calibration.json",
        "dated_md": root / f"{run_date}__publishing-calendar-readiness-calibration.md",
        "latest_json": root / "latest_publishing_calendar_readiness_calibration.json",
        "latest_md": root / "latest_publishing_calendar_readiness_calibration.md",
    }


def calibrate_day(day: dict[str, Any], repair_by_id: dict[str, dict[str, Any]], copy_pack_ready: bool) -> dict[str, Any]:
    previous = str(day.get("status") or "NO_READY_CONTENT")
    queue_item_id = str(day.get("queue_item_id") or "")
    repair = repair_by_id.get(queue_item_id, {})
    repaired_status = str(repair.get("repaired_readiness_status") or day.get("readiness_status") or "NO_READY_CONTENT")
    if repaired_status == "READY_TO_PUBLISH" and copy_pack_ready:
        calibrated = "READY"
        reason = "queue item is publish-ready and copy pack exists."
        action = "人工检查 checklist 后可创建/确认 publish session。"
        can_ready = True
        blocking = ""
    elif repaired_status in {"READY_TO_PUBLISH", "READY_FOR_REVIEW"} or repair.get("can_move_to_this_week"):
        calibrated = "ACTIONABLE"
        reason = "content is not fully ready, but operator has a concrete next action."
        action = repair.get("next_operator_action") or day.get("recommended_next_action") or "人工复审并补齐发布准备。"
        can_ready = True
        blocking = ""
    elif repaired_status in {"NEEDS_EVIDENCE", "NEEDS_VISUAL_ASSET", "NEEDS_REWRITE"}:
        calibrated = "HOLD"
        reason = f"queue item remains {repaired_status}."
        action = repair.get("next_operator_action") or "先处理 blocker，再排期。"
        can_ready = False
        blocking = repaired_status
    elif previous in {"OPEN", "OPTIONAL"}:
        calibrated = "OPEN"
        reason = "calendar slot has no ready queue item yet."
        action = "从 THIS_WEEK/WATCH 中选择可行动内容，或明确保持空档。"
        can_ready = False
        blocking = "no_ready_content"
    else:
        calibrated = "NEEDS_REVIEW"
        reason = "status requires operator review."
        action = day.get("recommended_next_action") or "人工确认排期状态。"
        can_ready = False
        blocking = previous
    return {
        "date": day.get("date", ""),
        "previous_status": previous,
        "calibrated_status": calibrated,
        "recommended_queue_item_id": queue_item_id,
        "readiness_reason": reason,
        "required_operator_action": action,
        "can_be_ready_after_action": can_ready,
        "blocking_reason": blocking,
    }


def build_publishing_calendar_readiness_calibration(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing = paths.market_content_root / "07_publishing"
    weekly_calendar = read_json(publishing / "latest_weekly_publishing_calendar.json")
    queue_repair = read_json(publishing / "latest_content_queue_readiness_repair.json")
    session_calendar = read_json(publishing / "latest_publishing_session_calendar.json")
    copy_pack = read_json(publishing / "latest_wechat_copy_pack_with_images.json")
    repair_by_id = {str(item.get("queue_item_id") or ""): item for item in list_payload(queue_repair, "items")}
    copy_pack_ready = any(item.get("pack_status") == "READY_FOR_MANUAL_COPY" for item in list_payload(copy_pack, "packs"))
    days = [calibrate_day(day, repair_by_id, copy_pack_ready) for day in list_payload(weekly_calendar, "calendar")]
    if not days:
        days = [
            {
                "date": "",
                "previous_status": "NO_READY_CONTENT",
                "calibrated_status": "NO_READY_CONTENT",
                "recommended_queue_item_id": "",
                "readiness_reason": "No weekly publishing calendar found.",
                "required_operator_action": "Run weekly-publishing-calendar first.",
                "can_be_ready_after_action": False,
                "blocking_reason": "missing_calendar",
            }
        ]
    planned_slots = sum(len(day.get("slots", [])) for day in list_payload(session_calendar, "calendar"))
    summary = {
        "calendar_days": len(days),
        "ready_days": sum(1 for item in days if item.get("calibrated_status") == "READY"),
        "actionable_days": sum(1 for item in days if item.get("calibrated_status") == "ACTIONABLE"),
        "hold_days": sum(1 for item in days if item.get("calibrated_status") in {"HOLD", "NEEDS_REVIEW"}),
        "open_days": sum(1 for item in days if item.get("calibrated_status") in {"OPEN", "NO_READY_CONTENT"}),
        "blocked_days": sum(1 for item in days if item.get("blocking_reason") and not item.get("can_be_ready_after_action")),
        "planned_session_slots": planned_slots,
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "days": days,
        "summary": summary,
        "policy": {"sidecar_only": True, "does_not_create_publish_session": True, "no_auto_publish": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| {item.get('date')} | `{item.get('previous_status')}` | `{item.get('calibrated_status')}` | {item.get('readiness_reason')} | {item.get('required_operator_action')} |"
        for item in list_payload(payload, "days")
    ]
    return f"""# Publishing Calendar Readiness Calibration

## Summary

- calendar_days: `{summary.get('calendar_days', 0)}`
- ready_days: `{summary.get('ready_days', 0)}`
- actionable_days: `{summary.get('actionable_days', 0)}`
- hold_days: `{summary.get('hold_days', 0)}`
- open_days: `{summary.get('open_days', 0)}`
- blocked_days: `{summary.get('blocked_days', 0)}`

| Date | Previous | Calibrated | Reason | Required action |
|---|---|---|---|---|
{chr(10).join(rows)}
"""
