"""Repair content queue readiness semantics as a sidecar report."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__content-queue-readiness-repair.json",
        "dated_md": root / f"{run_date}__content-queue-readiness-repair.md",
        "latest_json": root / "latest_content_queue_readiness_repair.json",
        "latest_md": root / "latest_content_queue_readiness_repair.md",
    }


def has_related_quick_fix(item: dict[str, Any], quick_results: list[dict[str, Any]]) -> bool:
    item_id = str(item.get("queue_item_id") or item.get("source_id") or item.get("title") or "")
    if not item_id:
        return False
    for result in quick_results:
        payload = result.get("sidecar_payload") if isinstance(result.get("sidecar_payload"), dict) else {}
        affected = payload.get("affected_queue_item_ids") if isinstance(payload.get("affected_queue_item_ids"), list) else []
        if item_id in affected:
            return True
    return False


def repair_item(item: dict[str, Any], quick_results: list[dict[str, Any]], copy_pack_ready: bool, visual_check_ready: bool) -> dict[str, Any]:
    previous = str(item.get("readiness_status") or "BLOCKED")
    priority = str(item.get("priority") or "WATCH")
    blockers = list(item.get("blockers") or [])
    actions: list[str] = []
    repaired = previous
    can_this_week = priority in {"TODAY", "THIS_WEEK"}
    can_today = False
    confidence = 0.45
    if previous == "READY_TO_PUBLISH":
        repaired = "READY_TO_PUBLISH"
        can_today = copy_pack_ready and visual_check_ready
        confidence = 0.8 if can_today else 0.65
        if not copy_pack_ready:
            blockers.append("copy_pack_not_ready")
            actions.append("确认 copy pack 和图片槽位后再进入 TODAY。")
        if not visual_check_ready:
            blockers.append("visual_checklist_not_ready")
            actions.append("完成 visual publishing checklist。")
    elif previous == "READY_FOR_REVIEW":
        repaired = "READY_FOR_REVIEW"
        actions.append("人工审稿通过后可排入 THIS_WEEK，不直接 TODAY。")
        confidence = 0.7
    elif previous == "NEEDS_VISUAL_ASSET":
        repaired = "READY_FOR_REVIEW" if has_related_quick_fix(item, quick_results) else "NEEDS_VISUAL_ASSET"
        actions.append("补齐图片资产或将视觉缺口明确为 publishing blocker。")
        blockers.append("needs_visual_asset")
        confidence = 0.6 if repaired == "READY_FOR_REVIEW" else 0.45
    elif previous == "NEEDS_REWRITE":
        repaired = "READY_FOR_REVIEW" if has_related_quick_fix(item, quick_results) else "NEEDS_REWRITE"
        actions.append("按方法论重写标题/开头/核心判断后人工复审。")
        blockers.append("needs_rewrite")
        confidence = 0.6 if repaired == "READY_FOR_REVIEW" else 0.45
    elif previous == "NEEDS_EVIDENCE":
        repaired = "NEEDS_EVIDENCE"
        actions.append("补充一手证据或将该题保持 WATCH/DEFER。")
        blockers.append("needs_evidence")
        can_this_week = False
        confidence = 0.35
    elif previous in {"STALE", "BLOCKED"}:
        repaired = previous
        actions.append("确认是否过期；若过期则 HOLD/REJECT，否则补 blocker。")
        blockers.append(previous.lower())
        can_this_week = False
        confidence = 0.3
    else:
        repaired = "READY_FOR_REVIEW" if priority in {"THIS_WEEK", "TODAY"} else "BLOCKED"
        actions.append("补充 readiness reason，并由 operator 判断是否进入本周。")
        confidence = 0.4
    if not actions:
        actions.append(str(item.get("recommended_next_action") or "人工确认下一步。"))
    remaining = list(dict.fromkeys(str(blocker) for blocker in blockers if blocker))
    next_action = actions[0]
    return {
        "queue_item_id": item.get("queue_item_id") or make_id("qitem", item.get("source_id"), item.get("title")),
        "title": item.get("title") or "Untitled queue item",
        "previous_readiness_status": previous,
        "repaired_readiness_status": repaired,
        "repair_actions": actions,
        "remaining_blockers": remaining,
        "next_operator_action": next_action,
        "can_move_to_this_week": bool(can_this_week or repaired in {"READY_TO_PUBLISH", "READY_FOR_REVIEW"}),
        "can_move_to_today": bool(can_today and repaired == "READY_TO_PUBLISH"),
        "confidence": round(confidence, 2),
    }


def build_content_queue_readiness_repair(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing = paths.market_content_root / "07_publishing"
    queue = read_json(publishing / "latest_content_queue_priority.json")
    quick = read_json(paths.logs_root / "latest_quick_fix_execution_results.json")
    visual_checklist = read_json(publishing / "latest_visual_publishing_checklist.json")
    copy_pack = read_json(publishing / "latest_wechat_copy_pack_with_images.json")
    article_review = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_article_review.json")
    visual_plans = read_json(paths.market_content_root / "05_draft_packs" / "latest_article_visual_plans.json")
    quick_results = [item for item in list_payload(quick, "fix_results") if item.get("status") == "APPLIED_SIDECAR"]
    packs = list_payload(copy_pack, "packs")
    checklists = list_payload(visual_checklist, "checklists")
    copy_pack_ready = any(item.get("pack_status") == "READY_FOR_MANUAL_COPY" for item in packs)
    visual_check_ready = any(item.get("status") == "READY" for item in checklists)
    items = [repair_item(item, quick_results, copy_pack_ready, visual_check_ready) for item in list_payload(queue, "items")]
    summary = {
        "item_count": len(items),
        "improved": sum(1 for item in items if item.get("previous_readiness_status") != item.get("repaired_readiness_status")),
        "still_blocked": sum(1 for item in items if item.get("repaired_readiness_status") in {"NEEDS_EVIDENCE", "NEEDS_VISUAL_ASSET", "NEEDS_REWRITE", "STALE", "BLOCKED"}),
        "ready_for_review": sum(1 for item in items if item.get("repaired_readiness_status") == "READY_FOR_REVIEW"),
        "ready_to_publish": sum(1 for item in items if item.get("repaired_readiness_status") == "READY_TO_PUBLISH"),
        "needs_manual": sum(1 for item in items if item.get("remaining_blockers")),
        "article_review_count": len(list_payload(article_review, "articles")),
        "visual_plan_count": len(list_payload(visual_plans, "visual_plans")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "items": items,
        "summary": summary,
        "policy": {"sidecar_only": True, "does_not_mutate_queue": True, "no_auto_publish": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| `{item.get('previous_readiness_status')}` | `{item.get('repaired_readiness_status')}` | {item.get('title')} | {item.get('next_operator_action')} |"
        for item in list_payload(payload, "items")
    ]
    return f"""# Content Queue Readiness Repair

## Summary

- item_count: `{summary.get('item_count', 0)}`
- improved: `{summary.get('improved', 0)}`
- still_blocked: `{summary.get('still_blocked', 0)}`
- ready_for_review: `{summary.get('ready_for_review', 0)}`
- ready_to_publish: `{summary.get('ready_to_publish', 0)}`
- needs_manual: `{summary.get('needs_manual', 0)}`

| Previous | Repaired | Title | Next operator action |
|---|---|---|---|
{chr(10).join(rows)}
"""
