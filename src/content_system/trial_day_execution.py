"""Build one-day trial execution records from current operation artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


AREAS = {"source", "topic", "draft", "visual", "publishing", "metrics", "workbench", "system"}


def output_paths(paths: ProjectPaths, run_date: str, day: int) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__trial-day-{day}-execution.json",
        "dated_md": paths.logs_root / f"{run_date}__trial-day-{day}-execution.md",
        "latest_json": paths.logs_root / f"latest_trial_day_{day}_execution.json",
        "latest_md": paths.logs_root / f"latest_trial_day_{day}_execution.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__trial-day-{day}-board.md",
        "board_latest_md": paths.frontstage_root / f"latest_trial_day_{day}_board.md",
    }


def missing_inputs(paths: ProjectPaths, repo_root: Path) -> list[str]:
    publishing = paths.market_content_root / "07_publishing"
    expected = [
        repo_root / "docs/ONE_WEEK_TRIAL_RUN_PROTOCOL.md",
        repo_root / "docs/OPERATOR_RUNBOOK.md",
        paths.logs_root / "latest_phase20_daily_hardening_pipeline.json",
        paths.logs_root / "latest_content_ops_failure_handling.json",
        paths.logs_root / "latest_publishing_checklist_regression.json",
        paths.logs_root / "latest_content_ops_closeout.json",
        publishing / "latest_content_queue_priority.json",
        publishing / "latest_weekly_publishing_rhythm.json",
        publishing / "latest_publishing_session_calendar.json",
        publishing / "latest_wechat_copy_pack_with_images.json",
    ]
    return [repo_relative(path, repo_root) for path in expected if not path.exists()]


def normalize_area(area: Any) -> str:
    text = str(area or "system")
    return text if text in AREAS else "system"


def pipeline_status(phase20: dict[str, Any], failure: dict[str, Any], regression: dict[str, Any]) -> dict[str, Any]:
    phase20_summary = phase20.get("summary") if isinstance(phase20.get("summary"), dict) else {}
    failure_summary = failure.get("summary") if isinstance(failure.get("summary"), dict) else {}
    regression_summary = regression.get("summary") if isinstance(regression.get("summary"), dict) else {}
    return {
        "phase20_status": phase20.get("status") or "UNKNOWN",
        "phase19_status": phase20_summary.get("phase19_status") or "UNKNOWN",
        "checklist_regression": regression_summary.get("regression_status") or "UNKNOWN",
        "failure_blockers": safe_int(failure_summary.get("blocker_count")),
        "failure_warnings": safe_int(failure_summary.get("warn_count")),
    }


def ops_snapshot(queue: dict[str, Any], calendar: dict[str, Any], archive_published_count: int = 0) -> dict[str, int]:
    queue_summary = queue.get("summary") if isinstance(queue.get("summary"), dict) else {}
    calendar_summary = calendar.get("summary") if isinstance(calendar.get("summary"), dict) else {}
    return {
        "queue_item_count": safe_int(queue_summary.get("item_count")),
        "today_count": safe_int(queue_summary.get("today")),
        "this_week_count": safe_int(queue_summary.get("this_week")),
        "watch_count": safe_int(queue_summary.get("watch")),
        "blocked_count": 0,
        "planned_slots": safe_int(calendar_summary.get("planned_slots")),
        "ready_slots": safe_int(calendar_summary.get("ready_slots")),
        "needs_asset": safe_int(calendar_summary.get("needs_asset")),
        "published_count": archive_published_count,
    }


def publishing_readiness(snapshot: dict[str, int], packs: list[dict[str, Any]], failure: dict[str, Any]) -> dict[str, Any]:
    ready_packs = [pack for pack in packs if pack.get("pack_status") == "READY_FOR_MANUAL_COPY"]
    has_copy_pack = bool(packs)
    has_visual_blocker = snapshot.get("needs_asset", 0) > 0 or any(pack.get("pack_status") == "NEEDS_VISUAL_ASSET" for pack in packs)
    has_publishable = bool(ready_packs) and snapshot.get("ready_slots", 0) > 0 and not has_visual_blocker
    if has_publishable:
        reason = "Copy pack and calendar slot are ready for manual confirmation."
    elif has_visual_blocker:
        reason = "Content exists, but visual assets/checklist still block manual publishing."
    elif has_copy_pack:
        reason = "Copy pack exists, but manual review or calendar readiness is not complete."
    else:
        reason = "No copy pack is available for manual publishing."
    if safe_int((failure.get("summary") or {}).get("blocker_count")):
        reason = "Failure handling reports blockers; do not publish before manual fix."
    return {
        "has_publishable_candidate": has_publishable,
        "has_copy_pack": has_copy_pack,
        "has_visual_blocker": has_visual_blocker,
        "manual_publish_recommended": has_publishable,
        "reason": reason,
    }


def build_issues(run_date: str, day: int, failure: dict[str, Any], queue: dict[str, Any], warnings: list[str]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for item in list_payload(failure, "issues")[:10]:
        severity = str(item.get("severity") or "INFO")
        issues.append(
            {
                "issue_id": make_id("trial_issue", run_date, day, item.get("issue_id"), item.get("description")),
                "area": normalize_area(item.get("area")),
                "severity": severity if severity in {"INFO", "WARN", "BLOCKER"} else "INFO",
                "description": item.get("description") or "",
                "recommended_fix": item.get("recommended_action") or "",
                "fix_phase": "manual_ops" if severity == "INFO" else "phase22",
            }
        )
    queue_items = list_payload(queue, "items")
    for item in queue_items:
        readiness = str(item.get("readiness_status") or "")
        if readiness not in {"NEEDS_VISUAL_ASSET", "NEEDS_EVIDENCE", "BLOCKED"}:
            continue
        issues.append(
            {
                "issue_id": make_id("trial_issue", run_date, day, item.get("queue_item_id"), readiness),
                "area": "visual" if readiness == "NEEDS_VISUAL_ASSET" else "topic",
                "severity": "WARN",
                "description": f"{item.get('title') or item.get('queue_item_id')}: {readiness}",
                "recommended_fix": item.get("recommended_next_action") or "人工处理 queue blocker。",
                "fix_phase": "manual_ops",
            }
        )
    for warning in warnings:
        issues.append(
            {
                "issue_id": make_id("trial_issue", run_date, day, warning),
                "area": "system",
                "severity": "WARN",
                "description": warning,
                "recommended_fix": "补齐输入产物后重跑 trial day。",
                "fix_phase": "phase21",
            }
        )
    return issues[:16]


def build_actions(run_date: str, day: int, readiness: dict[str, Any], closeout: dict[str, Any], issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    raw_actions = closeout.get("operator_actions") if isinstance(closeout.get("operator_actions"), list) else []
    actions = []
    for index, text in enumerate(raw_actions[:6], start=1):
        actions.append(
            {
                "action_id": make_id("trial_action", run_date, day, index, text),
                "area": "publishing" if "可发" in str(text) else "system",
                "action": str(text),
                "priority": "HIGH" if index <= 2 else "MEDIUM",
                "manual_required": True,
                "status": "OPEN",
            }
        )
    if readiness.get("has_visual_blocker"):
        actions.append(
            {
                "action_id": make_id("trial_action", run_date, day, "visual_blocker"),
                "area": "visual",
                "action": "先补齐图片资产或视觉 checklist，再考虑发布。",
                "priority": "HIGH",
                "manual_required": True,
                "status": "OPEN",
            }
        )
    if not actions and issues:
        first = issues[0]
        actions.append(
            {
                "action_id": make_id("trial_action", run_date, day, first.get("issue_id")),
                "area": first.get("area") or "system",
                "action": first.get("recommended_fix") or "按 issue log 处理。",
                "priority": "MEDIUM",
                "manual_required": True,
                "status": "OPEN",
            }
        )
    if not actions:
        actions.append(
            {
                "action_id": make_id("trial_action", run_date, day, "continue"),
                "area": "system",
                "action": "记录今日 trial 无 blocker，继续按 runbook 执行人工运营。",
                "priority": "LOW",
                "manual_required": True,
                "status": "OPEN",
            }
        )
    return actions[:10]


def daily_result(pipeline: dict[str, Any], issues: list[dict[str, Any]]) -> dict[str, Any]:
    blocker_count = sum(1 for item in issues if item.get("severity") == "BLOCKER")
    warn_count = sum(1 for item in issues if item.get("severity") == "WARN")
    if pipeline.get("phase20_status") in {"FAILED"} or blocker_count:
        status = "BLOCKED"
    elif pipeline.get("phase20_status") in {"DEGRADED"} or warn_count:
        status = "WARN"
    else:
        status = "PASS"
    return {
        "can_continue_trial": status != "BLOCKED",
        "day_status": status,
        "summary": f"Trial day recorded with phase20={pipeline.get('phase20_status')} and {warn_count} warnings / {blocker_count} blockers.",
    }


def build_trial_day_execution(paths: ProjectPaths, repo_root: Path, day: int) -> tuple[dict[str, Any], dict[str, Path]]:
    if day < 1 or day > 5:
        raise ValueError("trial day must be between 1 and 5")
    run_date = today_token()
    publishing_root = paths.market_content_root / "07_publishing"
    phase20 = read_json(paths.logs_root / "latest_phase20_daily_hardening_pipeline.json")
    failure = read_json(paths.logs_root / "latest_content_ops_failure_handling.json")
    regression = read_json(paths.logs_root / "latest_publishing_checklist_regression.json")
    closeout = read_json(paths.logs_root / "latest_content_ops_closeout.json")
    queue = read_json(publishing_root / "latest_content_queue_priority.json")
    calendar = read_json(publishing_root / "latest_publishing_session_calendar.json")
    copy_packs = list_payload(read_json(publishing_root / "latest_wechat_copy_pack_with_images.json"), "packs")
    archive = read_json(publishing_root / "published_article_archive.json")
    archive_summary = archive.get("summary") if isinstance(archive.get("summary"), dict) else {}
    warnings = [f"Missing input: {item}" for item in missing_inputs(paths, repo_root)]
    pipeline = pipeline_status(phase20, failure, regression)
    snapshot = ops_snapshot(queue, calendar, safe_int(archive_summary.get("published_count")))
    snapshot["blocked_count"] = safe_int((closeout.get("summary") or {}).get("blocked_count")) if isinstance(closeout.get("summary"), dict) else 0
    readiness = publishing_readiness(snapshot, copy_packs, failure)
    issues = build_issues(run_date, day, failure, queue, warnings)
    actions = build_actions(run_date, day, readiness, closeout, issues)
    result = daily_result(pipeline, issues)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "trial_day": day,
        "trial_mode": "manual_ops_only",
        "pipeline_status": pipeline,
        "content_ops_snapshot": snapshot,
        "publishing_readiness": readiness,
        "operator_actions": actions,
        "issues": issues,
        "daily_result": result,
        "warnings": warnings,
        "safety": {"auto_publish": False, "wechat_api": False, "auto_image_generation": False, "live_default_enabled": False},
    }
    outputs = output_paths(paths, run_date, day)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    pipeline = payload.get("pipeline_status") if isinstance(payload.get("pipeline_status"), dict) else {}
    snapshot = payload.get("content_ops_snapshot") if isinstance(payload.get("content_ops_snapshot"), dict) else {}
    readiness = payload.get("publishing_readiness") if isinstance(payload.get("publishing_readiness"), dict) else {}
    result = payload.get("daily_result") if isinstance(payload.get("daily_result"), dict) else {}
    actions = "\n".join(f"- `{item.get('priority')}` {item.get('area')}: {item.get('action')}" for item in list_payload(payload, "operator_actions")) or "- None."
    issues = "\n".join(f"- `{item.get('severity')}` {item.get('area')}: {item.get('description')} / {item.get('recommended_fix')}" for item in list_payload(payload, "issues")) or "- None."
    return f"""# Trial Day {payload.get('trial_day')} Execution

## Daily Result

- day_status: `{result.get('day_status', 'UNKNOWN')}`
- can_continue_trial: `{result.get('can_continue_trial', True)}`
- summary: {result.get('summary', '')}

## Pipeline Status

- phase20_status: `{pipeline.get('phase20_status', 'UNKNOWN')}`
- phase19_status: `{pipeline.get('phase19_status', 'UNKNOWN')}`
- checklist_regression: `{pipeline.get('checklist_regression', 'UNKNOWN')}`
- failure_blockers: `{pipeline.get('failure_blockers', 0)}`
- failure_warnings: `{pipeline.get('failure_warnings', 0)}`

## Content Ops Snapshot

- queue_item_count: `{snapshot.get('queue_item_count', 0)}`
- today_count: `{snapshot.get('today_count', 0)}`
- this_week_count: `{snapshot.get('this_week_count', 0)}`
- blocked_count: `{snapshot.get('blocked_count', 0)}`
- planned_slots: `{snapshot.get('planned_slots', 0)}`
- ready_slots: `{snapshot.get('ready_slots', 0)}`

## Publishing Readiness

- manual_publish_recommended: `{readiness.get('manual_publish_recommended', False)}`
- reason: {readiness.get('reason', '')}

## Operator Actions

{actions}

## Issues

{issues}

Safety: no auto publish, no WeChat API, no auto image generation, live default disabled.
"""
