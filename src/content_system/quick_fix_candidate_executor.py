"""Execute safe quick-fix candidates as sidecar results."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__quick-fix-execution-results.json",
        "dated_md": paths.logs_root / f"{run_date}__quick-fix-execution-results.md",
        "latest_json": paths.logs_root / "latest_quick_fix_execution_results.json",
        "latest_md": paths.logs_root / "latest_quick_fix_execution_results.md",
    }


def fix_type_for(area: str, title: str) -> str:
    lowered = title.lower()
    if area == "visual" or "visual" in lowered or "asset" in lowered or "图片" in title:
        return "visual_asset_reminder"
    if area == "publishing" or "today" in lowered or "publish" in lowered:
        return "operator_action"
    if area == "topic" or "evidence" in lowered:
        return "queue_status_note"
    if area == "draft" or "rewrite" in lowered:
        return "readiness_explanation"
    if area == "metrics":
        return "operator_action"
    return "monitoring_note"


def sidecar_payload(resolution: dict[str, Any], fix_type: str, queue_items: list[dict[str, Any]]) -> dict[str, Any]:
    area = str(resolution.get("area") or "system")
    title = str(resolution.get("title") or "")
    payload: dict[str, Any] = {
        "area": area,
        "title": title,
        "recommended_fix": resolution.get("recommended_fix", ""),
        "manual_required": True,
    }
    if fix_type == "operator_action":
        payload["operator_action"] = resolution.get("recommended_fix") or "Review and decide next manual operation."
        payload["command_hint"] = "make content-queue-priority && make weekly-publishing-calendar"
    elif fix_type == "visual_asset_reminder":
        payload["visual_asset_reminder"] = "补齐图片资产、视觉 checklist 或将内容降级为本周候选。"
        payload["command_hint"] = "make article-visual-plans && make visual-publishing-checklist"
    elif fix_type == "queue_status_note":
        affected = [item.get("queue_item_id") for item in queue_items if item.get("readiness_status") in {"NEEDS_EVIDENCE", "BLOCKED"}][:5]
        payload["queue_status_note"] = "缺证据内容不得进入 TODAY；需要补 evidence 或保持 WATCH/DEFER。"
        payload["affected_queue_item_ids"] = affected
    elif fix_type == "readiness_explanation":
        affected = [item.get("queue_item_id") for item in queue_items if item.get("readiness_status") == "NEEDS_REWRITE"][:5]
        payload["readiness_explanation"] = "需重写项可进入 THIS_WEEK action list，但不能直接 READY_TO_PUBLISH。"
        payload["affected_queue_item_ids"] = affected
    else:
        payload["monitoring_note"] = "该问题不应阻塞稳定试运行，但应继续显示在 operator board。"
    return payload


def build_quick_fix_execution_results(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    plan = read_json(paths.logs_root / "latest_high_priority_issue_resolution_plan.json")
    content_fix = read_json(paths.logs_root / "latest_content_ops_fix_pack.json")
    publishing = paths.market_content_root / "07_publishing"
    queue = read_json(publishing / "latest_content_queue_priority.json")
    weekly_calendar = read_json(publishing / "latest_weekly_publishing_calendar.json")
    copy_pack = read_json(publishing / "latest_wechat_copy_pack_with_images.json")
    visual_checklist = read_json(publishing / "latest_visual_publishing_checklist.json")
    queue_items = list_payload(queue, "items")
    results: list[dict[str, Any]] = []
    fix_ids = {str(item.get("source_issue_id") or ""): item for item in list_payload(content_fix, "fixes")}
    for resolution in list_payload(plan, "issues"):
        resolution_type = str(resolution.get("resolution_type") or "")
        area = str(resolution.get("area") or "system")
        source_issue_id = str(resolution.get("source_issue_id") or "")
        fix_type = fix_type_for(area, str(resolution.get("title") or ""))
        if resolution_type == "quick_fix" and resolution.get("safe_to_execute", False):
            status = "APPLIED_SIDECAR"
            payload = sidecar_payload(resolution, fix_type, queue_items)
            change_summary = f"Generated sidecar {fix_type} for {area} issue; no mainline content changed."
        elif resolution_type in {"manual_intervention", "next_phase"}:
            status = "NEEDS_MANUAL"
            payload = {
                "area": area,
                "manual_note": resolution.get("recommended_fix") or "Operator decision required.",
                "linked_content_fix": fix_ids.get(source_issue_id, {}).get("content_fix_id", ""),
            }
            change_summary = "Marked as needing manual intervention; no fake resolution."
        else:
            status = "SKIPPED"
            payload = {"area": area, "monitoring_note": "Monitor-only issue; no execution required."}
            change_summary = "Skipped because monitor-only or unsafe to execute."
        results.append(
            {
                "fix_result_id": make_id("qfix", run_date, resolution.get("resolution_id"), status),
                "resolution_id": resolution.get("resolution_id", ""),
                "source_issue_id": source_issue_id,
                "fix_type": fix_type,
                "status": status,
                "sidecar_payload": payload,
                "change_summary": change_summary,
                "verification_hint": resolution.get("verification_method") or "Check verification board.",
                "auto_apply_to_config": False,
                "overwrites_mainline": False,
            }
        )
    if not results:
        results.append(
            {
                "fix_result_id": make_id("qfix", run_date, "empty"),
                "resolution_id": "",
                "source_issue_id": "",
                "fix_type": "monitoring_note",
                "status": "SKIPPED",
                "sidecar_payload": {"monitoring_note": "No quick fix candidate found."},
                "change_summary": "No quick fix execution required.",
                "verification_hint": "Stable gate should continue monitoring.",
                "auto_apply_to_config": False,
                "overwrites_mainline": False,
            }
        )
    summary = {
        "fix_count": len(results),
        "applied_sidecar": sum(1 for item in results if item.get("status") == "APPLIED_SIDECAR"),
        "skipped": sum(1 for item in results if item.get("status") == "SKIPPED"),
        "needs_manual": sum(1 for item in results if item.get("status") == "NEEDS_MANUAL"),
        "failed": sum(1 for item in results if item.get("status") == "FAILED"),
        "queue_items_seen": len(queue_items),
        "calendar_days_seen": len(list_payload(weekly_calendar, "calendar")),
        "copy_pack_count": len(list_payload(copy_pack, "packs")),
        "visual_checklist_count": len(list_payload(visual_checklist, "checklists")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "fix_results": results,
        "summary": summary,
        "policy": {"sidecar_only": True, "auto_apply_to_config": False, "overwrites_mainline": False, "no_auto_publish": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| `{item.get('status')}` | `{item.get('fix_type')}` | {item.get('source_issue_id')} | {item.get('change_summary')} |"
        for item in list_payload(payload, "fix_results")
    ]
    return f"""# Quick Fix Execution Results

## Summary

- fix_count: `{summary.get('fix_count', 0)}`
- applied_sidecar: `{summary.get('applied_sidecar', 0)}`
- skipped: `{summary.get('skipped', 0)}`
- needs_manual: `{summary.get('needs_manual', 0)}`
- failed: `{summary.get('failed', 0)}`

| Status | Fix type | Source issue | Change summary |
|---|---|---|---|
{chr(10).join(rows)}

No config/prompt/rule changes. No mainline overwrite.
"""
