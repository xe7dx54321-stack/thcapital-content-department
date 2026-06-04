"""Build a daily manual content operations action list."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


VALID_MODES = {"dry_run", "manual_confirm"}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__daily-content-ops-runner.json",
        "dated_md": paths.logs_root / f"{run_date}__daily-content-ops-runner.md",
        "latest_json": paths.logs_root / "latest_daily_content_ops_runner.json",
        "latest_md": paths.logs_root / "latest_daily_content_ops_runner.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__daily-content-ops-runner-board.md",
        "board_latest_md": paths.frontstage_root / "latest_daily_content_ops_runner_board.md",
    }


def action_type(area: str, text: str) -> str:
    lowered = text.lower()
    if area == "visual" or "visual" in lowered or "asset" in lowered or "图片" in text:
        return "fix_visual_asset"
    if area == "publishing" or "publish" in lowered or "发布" in text:
        return "prepare_manual_publish"
    if area == "metrics" or "metrics" in lowered:
        return "record_metrics"
    if area == "draft" or "rewrite" in lowered:
        return "rewrite_or_review"
    if area == "topic":
        return "collect_evidence_or_reprioritize"
    return "review_ops_issue"


def build_daily_content_ops_runner(paths: ProjectPaths, repo_root: Path, mode: str = "dry_run") -> tuple[dict[str, Any], dict[str, Path]]:
    if mode not in VALID_MODES:
        raise ValueError(f"mode must be one of {sorted(VALID_MODES)}")
    run_date = today_token()
    fix_pack = read_json(paths.logs_root / "latest_content_ops_fix_pack.json")
    issue_tracker = read_json(paths.logs_root / "latest_recurring_issue_tracker.json")
    queue = read_json(paths.market_content_root / "07_publishing" / "latest_content_queue_priority.json")
    calendar = read_json(paths.market_content_root / "07_publishing" / "latest_weekly_publishing_calendar.json")
    phase21 = read_json(paths.logs_root / "latest_phase21_trial_pipeline.json")

    actions: list[dict[str, Any]] = []
    for fix in list_payload(fix_pack, "fixes")[:12]:
        area = str(fix.get("area") or "system")
        text = str(fix.get("action") or "")
        can_execute = fix.get("fix_type") in {"quick_fix", "manual_ops_note", "manual_intervention"}
        actions.append(
            {
                "daily_action_id": make_id("ops_action", run_date, fix.get("content_fix_id"), mode),
                "source_id": fix.get("content_fix_id", ""),
                "source_type": "content_ops_fix",
                "area": area,
                "priority": fix.get("priority") or "LOW",
                "urgency": fix.get("urgency") or "P2",
                "action_type": action_type(area, text),
                "instruction": text or "Review content ops fix.",
                "command_hint": fix.get("command_hint") or "make phase22-daily",
                "can_execute_now": can_execute,
                "blocked_by": [] if can_execute else ["future_phase_or_human_context"],
                "manual_required": True,
                "status": "READY" if can_execute else "HOLD",
            }
        )

    queue_items = list_payload(queue, "items")
    today_items = [item for item in queue_items if item.get("priority") == "TODAY"]
    if not today_items:
        actions.append(
            {
                "daily_action_id": make_id("ops_action", run_date, "no_today"),
                "source_id": "content_queue_priority",
                "source_type": "queue_summary",
                "area": "publishing",
                "priority": "MEDIUM",
                "urgency": "P1",
                "action_type": "schedule_or_hold_today",
                "instruction": "今日没有 TODAY 内容：从 THIS_WEEK 中挑选 ready 项，或明确今天不发布。",
                "command_hint": "make content-queue-priority && make weekly-publishing-calendar",
                "can_execute_now": True,
                "blocked_by": [],
                "manual_required": True,
                "status": "READY",
            }
        )
    calendar_summary = calendar.get("summary") if isinstance(calendar.get("summary"), dict) else {}
    if safe_int(calendar_summary.get("blocked_days")):
        actions.append(
            {
                "daily_action_id": make_id("ops_action", run_date, "calendar_blocked"),
                "source_id": "weekly_publishing_calendar",
                "source_type": "weekly_calendar",
                "area": "publishing",
                "priority": "MEDIUM",
                "urgency": "P1",
                "action_type": "repair_calendar_blocker",
                "instruction": "发布日历存在 blocked day：检查对应内容是否缺图、缺证据或缺 copy pack。",
                "command_hint": "make weekly-publishing-calendar && make content-fix-pack",
                "can_execute_now": True,
                "blocked_by": [],
                "manual_required": True,
                "status": "READY",
            }
        )
    if not actions:
        actions.append(
            {
                "daily_action_id": make_id("ops_action", run_date, "continue"),
                "source_id": "phase22",
                "source_type": "system",
                "area": "system",
                "priority": "LOW",
                "urgency": "P2",
                "action_type": "continue_trial",
                "instruction": "今日无必须修复项，继续按 runbook 人工运营并记录发布/metrics。",
                "command_hint": "make phase22-daily",
                "can_execute_now": True,
                "blocked_by": [],
                "manual_required": True,
                "status": "READY",
            }
        )
    deduped = []
    seen = set()
    for item in sorted(actions, key=lambda value: (str(value.get("urgency") or "P9"), str(value.get("priority") or "LOW"))):
        key = f"{item.get('area')}::{item.get('action_type')}::{item.get('instruction')}"
        if key in seen:
            continue
        seen.add(key)
        item["recommended_order"] = len(deduped) + 1
        deduped.append(item)
    issue_summary = issue_tracker.get("summary") if isinstance(issue_tracker.get("summary"), dict) else {}
    phase21_summary = phase21.get("summary") if isinstance(phase21.get("summary"), dict) else {}
    status = "DEGRADED" if any(item.get("status") == "HOLD" for item in deduped) or safe_int(issue_summary.get("high")) else "SUCCESS"
    summary = {
        "action_count": len(deduped),
        "ready_actions": sum(1 for item in deduped if item.get("status") == "READY"),
        "blocked_actions": sum(1 for item in deduped if item.get("status") == "HOLD"),
        "quick_fix_actions": sum(1 for item in deduped if item.get("source_type") == "content_ops_fix" and item.get("can_execute_now")),
        "high_priority_actions": sum(1 for item in deduped if item.get("priority") == "HIGH" or item.get("urgency") == "P0"),
        "mode": mode,
        "phase21_warn_days": phase21_summary.get("warn_days", 0),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "mode": mode,
        "status": status,
        "actions": deduped,
        "summary": summary,
        "safety": {
            "sidecar_only": True,
            "manual_confirm_mode": mode == "manual_confirm",
            "auto_publish": False,
            "wechat_api": False,
            "auto_image_generation": False,
            "overwrite_mainline": False,
            "auto_config_prompt_rule_changes": False,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| {item.get('recommended_order')} | `{item.get('urgency')}` | `{item.get('status')}` | {item.get('area')} | {item.get('instruction')} | `{item.get('command_hint')}` |"
        for item in list_payload(payload, "actions")
    ]
    return f"""# Daily Content Operations Runner

## Summary

- status: `{payload.get('status')}`
- mode: `{payload.get('mode')}`
- action_count: `{summary.get('action_count', 0)}`
- ready_actions: `{summary.get('ready_actions', 0)}`
- blocked_actions: `{summary.get('blocked_actions', 0)}`
- quick_fix_actions: `{summary.get('quick_fix_actions', 0)}`
- high_priority_actions: `{summary.get('high_priority_actions', 0)}`

| Order | Urgency | Status | Area | Instruction | Command hint |
|---:|---|---|---|---|---|
{chr(10).join(rows)}

Safety: sidecar-only, no WeChat API, no auto publish.
"""
