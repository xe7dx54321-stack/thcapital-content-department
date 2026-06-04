"""Build content operations queue priority."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__content-queue-priority.json",
        "dated_md": root / f"{run_date}__content-queue-priority.md",
        "latest_json": root / "latest_content_queue_priority.json",
        "latest_md": root / "latest_content_queue_priority.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__content-queue-priority-board.md",
        "board_latest_md": paths.frontstage_root / "latest_content_queue_priority_board.md",
    }


def priority_from_score(score: float, readiness: str, blockers: list[str]) -> str:
    if readiness == "BLOCKED":
        return "HOLD"
    if readiness == "STALE":
        return "REJECT"
    if readiness == "READY_TO_PUBLISH" and score >= 85:
        return "TODAY"
    if readiness in {"READY_TO_PUBLISH", "READY_FOR_REVIEW"} and score >= 60:
        return "THIS_WEEK"
    if readiness in {"NEEDS_VISUAL_ASSET", "NEEDS_REWRITE"}:
        return "DEFER" if blockers else "THIS_WEEK"
    if readiness == "NEEDS_EVIDENCE":
        return "WATCH"
    return "WATCH" if score >= 40 else "HOLD"


def next_action(priority: str, readiness: str) -> str:
    if priority == "TODAY":
        return "publish_today"
    if priority == "THIS_WEEK" and readiness == "NEEDS_VISUAL_ASSET":
        return "finish_visuals"
    if priority == "THIS_WEEK":
        return "schedule_this_week"
    if readiness == "NEEDS_EVIDENCE":
        return "collect_evidence"
    if readiness == "NEEDS_REWRITE":
        return "rewrite"
    if priority == "REJECT":
        return "reject"
    return "hold"


def copy_pack_item(run_date: str, pack: dict[str, Any], checklist: dict[str, Any]) -> dict[str, Any]:
    pack_status = str(pack.get("pack_status") or "")
    checklist_status = str(checklist.get("status") or "")
    blockers: list[str] = []
    reasons = ["Copy pack exists for manual WeChat publishing."]
    if pack_status == "READY_FOR_MANUAL_COPY" and checklist_status == "READY":
        readiness = "READY_TO_PUBLISH"
        score = 92
        reasons.append("Copy pack and visual checklist are ready.")
    elif pack_status == "NEEDS_VISUAL_ASSET":
        readiness = "NEEDS_VISUAL_ASSET"
        score = 68
        blockers.append("Image assets are not ready.")
    elif checklist_status == "NEEDS_ATTENTION":
        readiness = "READY_FOR_REVIEW"
        score = 72
        blockers.append("Visual publishing checklist still has warnings.")
    elif pack_status == "BLOCKED" or checklist_status == "BLOCKED":
        readiness = "BLOCKED"
        score = 20
        blockers.append("Publishing pack or checklist is blocked.")
    else:
        readiness = "READY_FOR_REVIEW"
        score = 60
    priority = priority_from_score(score, readiness, blockers)
    return {
        "queue_item_id": make_id("qitem", run_date, pack.get("copy_pack_id"), "copy_pack"),
        "source_id": pack.get("copy_pack_id") or "",
        "source_type": "copy_pack",
        "title": pack.get("title_to_copy") or "",
        "content_type": "unknown",
        "priority": priority,
        "readiness_status": readiness,
        "priority_score": score,
        "reasons": reasons,
        "blockers": blockers,
        "recommended_next_action": next_action(priority, readiness),
    }


def generic_item(run_date: str, source_type: str, source_id: str, title: str, content_type: str, score: float, readiness: str, reasons: list[str], blockers: list[str]) -> dict[str, Any]:
    priority = priority_from_score(score, readiness, blockers)
    return {
        "queue_item_id": make_id("qitem", run_date, source_type, source_id),
        "source_id": source_id,
        "source_type": source_type,
        "title": title,
        "content_type": content_type or "unknown",
        "priority": priority,
        "readiness_status": readiness,
        "priority_score": round(score, 2),
        "reasons": reasons,
        "blockers": blockers,
        "recommended_next_action": next_action(priority, readiness),
    }


def summarize(items: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "item_count": len(items),
        "today": sum(1 for item in items if item.get("priority") == "TODAY"),
        "this_week": sum(1 for item in items if item.get("priority") == "THIS_WEEK"),
        "watch": sum(1 for item in items if item.get("priority") == "WATCH"),
        "defer": sum(1 for item in items if item.get("priority") == "DEFER"),
        "hold": sum(1 for item in items if item.get("priority") == "HOLD"),
        "reject": sum(1 for item in items if item.get("priority") == "REJECT"),
    }


def build_content_queue_priority(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    market = paths.market_content_root
    publishing_root = market / "07_publishing"
    draft_root = market / "05_draft_packs"
    topic_payload = read_json(market / "03_topic_candidates" / "latest_methodology_topic_scores.json")
    brief_payload = read_json(draft_root / "latest_methodology_content_briefs.json")
    draft_payload = read_json(draft_root / "latest_methodology_content_drafts.json")
    pack_payload = read_json(publishing_root / "latest_wechat_copy_pack_with_images.json")
    checklist_payload = read_json(publishing_root / "latest_visual_publishing_checklist.json")
    calendar_payload = read_json(publishing_root / "latest_publishing_session_calendar.json")
    checklists = {str(item.get("copy_pack_id") or ""): item for item in list_payload(checklist_payload, "checklists")}
    items: list[dict[str, Any]] = []
    used_sources: set[str] = set()
    for pack in list_payload(pack_payload, "packs"):
        item = copy_pack_item(run_date, pack, checklists.get(str(pack.get("copy_pack_id") or ""), {}))
        items.append(item)
        used_sources.add(str(item.get("source_id") or ""))
    scheduled_sources = {str(slot.get("copy_pack_id") or "") for day in list_payload(calendar_payload, "calendar") for slot in day.get("slots", []) if isinstance(slot, dict)}
    for draft in list_payload(draft_payload, "drafts")[:8]:
        source_id = str(draft.get("draft_id") or "")
        if source_id in used_sources:
            continue
        score = 58 if draft.get("status") == "READY_FOR_REVIEW" else 45
        readiness = "READY_FOR_REVIEW" if draft.get("status") == "READY_FOR_REVIEW" else "NEEDS_REWRITE"
        items.append(generic_item(run_date, "draft", source_id, str(draft.get("selected_title") or ""), str(draft.get("recipe_id") or "unknown"), score, readiness, ["Methodology draft available."], []))
    for brief in list_payload(brief_payload, "briefs")[:8]:
        source_id = str(brief.get("brief_id") or "")
        if source_id in used_sources:
            continue
        score = safe_float(brief.get("methodology_topic_score"))
        readiness = "READY_FOR_REVIEW" if brief.get("status") == "READY_FOR_OUTLINE" else "NEEDS_EVIDENCE"
        blockers = ["Evidence plan still needs completion."] if readiness == "NEEDS_EVIDENCE" else []
        items.append(generic_item(run_date, "brief", source_id, str(brief.get("title") or ""), str(brief.get("recommended_recipe_id") or "unknown"), score, readiness, ["Methodology brief is in queue."], blockers))
    for topic in list_payload(topic_payload, "topics")[:8]:
        source_id = str(topic.get("topic_id") or "")
        if source_id in used_sources:
            continue
        score = safe_float(topic.get("methodology_total_score"))
        readiness = "NEEDS_EVIDENCE" if topic.get("missing_requirements") else "READY_FOR_REVIEW"
        blockers = [str(item) for item in topic.get("missing_requirements", [])[:3]] if isinstance(topic.get("missing_requirements"), list) else []
        items.append(generic_item(run_date, "topic", source_id, str(topic.get("title") or ""), str(topic.get("recommended_recipe_id") or "unknown"), score, readiness, ["Methodology topic score available."], blockers))
    for item in items:
        if item.get("source_id") in scheduled_sources:
            item.setdefault("reasons", []).append("Already appears on publishing calendar.")
    items = sorted(items, key=lambda item: (-safe_float(item.get("priority_score")), str(item.get("title") or "")))[:30]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "items": items,
        "summary": summarize(items),
        "policy": {"advisory_only": True, "no_auto_publish": True, "no_auto_session_creation": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('queue_item_id')}` | `{item.get('priority')}` | `{item.get('readiness_status')}` | {item.get('priority_score')} | {item.get('title') or ''} |"
        for item in list_payload(payload, "items")
    ) or "| - | - | - | 0 | No queue items |"
    return f"""# Content Queue Priority

## Summary

- item_count: `{summary.get('item_count', 0)}`
- today: `{summary.get('today', 0)}`
- this_week: `{summary.get('this_week', 0)}`
- watch: `{summary.get('watch', 0)}`
- defer: `{summary.get('defer', 0)}`
- hold: `{summary.get('hold', 0)}`
- reject: `{summary.get('reject', 0)}`

| Queue Item | Priority | Readiness | Score | Title |
|---|---|---|---:|---|
{rows}
"""
