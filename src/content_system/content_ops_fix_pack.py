"""Build a daily content operations fix and suggestion pack."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__content-ops-fix-pack.json",
        "dated_md": paths.logs_root / f"{run_date}__content-ops-fix-pack.md",
        "latest_json": paths.logs_root / "latest_content_ops_fix_pack.json",
        "latest_md": paths.logs_root / "latest_content_ops_fix_pack.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__content-ops-fix-pack-board.md",
        "board_latest_md": paths.frontstage_root / "latest_content_ops_fix_pack_board.md",
    }


def command_hint(area: str, description: str) -> str:
    lowered = description.lower()
    if area == "visual":
        return "make article-visual-plans && make image-asset-requests && make visual-publishing-checklist"
    if area == "publishing" or "today" in lowered:
        return "make content-queue-priority && make publishing-session-calendar"
    if area == "metrics":
        return "python3 scripts/record_post_publish_metrics.py --list-sessions"
    if area == "topic":
        return "make methodology-topic-score && make content-queue-priority"
    if area == "draft":
        return "make methodology-article-review && make methodology-drafts"
    if area == "workbench":
        return "make wechat-workbench"
    return "make phase22-daily"


def build_content_ops_fix_pack(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    tracker = read_json(paths.logs_root / "latest_recurring_issue_tracker.json")
    trial_fix_pack = read_json(paths.logs_root / "latest_trial_fix_pack.json")
    queue = read_json(paths.market_content_root / "07_publishing" / "latest_content_queue_priority.json")
    fixes: list[dict[str, Any]] = []

    for item in list_payload(tracker, "issues"):
        area = str(item.get("area") or "system")
        urgency = str(item.get("urgency") or "P2")
        fix_type = "quick_fix" if item.get("quick_fix_candidate") else "manual_intervention"
        fixes.append(
            {
                "content_fix_id": make_id("ops_fix", run_date, item.get("recurring_issue_id"), fix_type),
                "source_issue_id": item.get("recurring_issue_id", ""),
                "source_type": "recurring_issue",
                "area": area,
                "priority": item.get("severity") or "LOW",
                "urgency": urgency,
                "fix_type": fix_type,
                "recommended_order": item.get("recommended_order", len(fixes) + 1),
                "action": item.get("recommended_fix") or "按 issue tracker 建议处理。",
                "expected_result": "降低 recurring issue 发生频率，并让今日运营队列更可执行。",
                "command_hint": command_hint(area, str(item.get("description") or "")),
                "manual_required": True,
                "auto_apply": False,
                "status": "PLANNED",
            }
        )

    for item in list_payload(trial_fix_pack, "fixes"):
        if str(item.get("fix_type")) == "next_phase":
            continue
        area = str(item.get("area") or "system")
        fixes.append(
            {
                "content_fix_id": make_id("ops_fix", run_date, item.get("fix_id"), "trial"),
                "source_issue_id": item.get("fix_id", ""),
                "source_type": "trial_fix",
                "area": area,
                "priority": item.get("severity") or "LOW",
                "urgency": "P1" if item.get("severity") == "HIGH" else "P2",
                "fix_type": item.get("fix_type") or "manual_ops_note",
                "recommended_order": len(fixes) + 1,
                "action": item.get("recommended_change") or item.get("description") or "按 trial fix pack 处理。",
                "expected_result": "把 Phase21 trial 暴露的问题转为可跟进人工动作。",
                "command_hint": command_hint(area, str(item.get("description") or "")),
                "manual_required": True,
                "auto_apply": False,
                "status": "PLANNED",
            }
        )

    for queue_item in list_payload(queue, "items"):
        readiness = str(queue_item.get("readiness_status") or "")
        if readiness not in {"NEEDS_VISUAL_ASSET", "NEEDS_EVIDENCE", "NEEDS_REWRITE", "BLOCKED"}:
            continue
        area = "visual" if readiness == "NEEDS_VISUAL_ASSET" else "draft" if readiness == "NEEDS_REWRITE" else "topic"
        fixes.append(
            {
                "content_fix_id": make_id("ops_fix", run_date, queue_item.get("queue_item_id"), readiness),
                "source_issue_id": queue_item.get("queue_item_id", ""),
                "source_type": "queue_item",
                "area": area,
                "priority": "MEDIUM",
                "urgency": "P1" if queue_item.get("priority") in {"TODAY", "THIS_WEEK"} else "P2",
                "fix_type": "quick_fix" if readiness in {"NEEDS_VISUAL_ASSET", "NEEDS_REWRITE"} else "manual_intervention",
                "recommended_order": len(fixes) + 1,
                "action": f"{queue_item.get('title') or queue_item.get('queue_item_id')}: {queue_item.get('recommended_next_action') or readiness}",
                "expected_result": "提高内容队列 readiness，减少 TODAY 为空或 blocked 的情况。",
                "command_hint": command_hint(area, readiness),
                "manual_required": True,
                "auto_apply": False,
                "status": "PLANNED",
            }
        )

    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in sorted(fixes, key=lambda value: (str(value.get("urgency") or "P9"), safe_int(value.get("recommended_order")))):
        key = f"{item.get('source_issue_id')}::{item.get('action')}"
        if key in seen:
            continue
        seen.add(key)
        item["recommended_order"] = len(deduped) + 1
        deduped.append(item)

    summary = {
        "fix_count": len(deduped),
        "quick_fix": sum(1 for item in deduped if item.get("fix_type") == "quick_fix"),
        "manual_intervention": sum(1 for item in deduped if item.get("fix_type") in {"manual_intervention", "manual_ops_note"}),
        "next_phase": sum(1 for item in deduped if item.get("fix_type") == "next_phase"),
        "high_priority": sum(1 for item in deduped if item.get("priority") == "HIGH" or item.get("urgency") == "P0"),
        "auto_apply": False,
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "fixes": deduped,
        "summary": summary,
        "policy": {"sidecar_only": True, "manual_required": True, "auto_apply": False, "no_auto_publish": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| {item.get('recommended_order')} | `{item.get('urgency')}` | `{item.get('fix_type')}` | {item.get('area')} | {item.get('action')} | `{item.get('command_hint')}` |"
        for item in list_payload(payload, "fixes")
    ]
    return f"""# Content Ops Fix Pack

## Summary

- fix_count: `{summary.get('fix_count', 0)}`
- quick_fix: `{summary.get('quick_fix', 0)}`
- manual_intervention: `{summary.get('manual_intervention', 0)}`
- next_phase: `{summary.get('next_phase', 0)}`
- high_priority: `{summary.get('high_priority', 0)}`

| Order | Urgency | Type | Area | Action | Command hint |
|---:|---|---|---|---|---|
{chr(10).join(rows) or "| - | - | - | - | No fix needed | - |"}

All fixes are sidecar suggestions and `auto_apply=false`.
"""
