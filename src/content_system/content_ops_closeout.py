"""Build content operations closeout and next actions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__content-ops-closeout.json",
        "dated_md": paths.logs_root / f"{run_date}__content-ops-closeout.md",
        "latest_json": paths.logs_root / "latest_content_ops_closeout.json",
        "latest_md": paths.logs_root / "latest_content_ops_closeout.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__content-ops-closeout-board.md",
        "board_latest_md": paths.frontstage_root / "latest_content_ops_closeout_board.md",
    }


def build_content_ops_closeout(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing_root = paths.market_content_root / "07_publishing"
    calendar_payload = read_json(publishing_root / "latest_publishing_session_calendar.json")
    queue_payload = read_json(publishing_root / "latest_content_queue_priority.json")
    rhythm_payload = read_json(publishing_root / "latest_weekly_publishing_rhythm.json")
    archive_payload = read_json(publishing_root / "published_article_archive.json")
    metrics_review_payload = read_json(paths.logs_root / "latest_post_publish_metrics_review.json")
    visual_feedback_payload = read_json(paths.logs_root / "latest_visual_strategy_learning_feedback.json")
    slots = [slot for day in list_payload(calendar_payload, "calendar") for slot in day.get("slots", []) if isinstance(slot, dict)]
    queue_items = list_payload(queue_payload, "items")
    articles = list_payload(archive_payload, "articles")
    published = [item for item in articles if item.get("status") == "published"]
    deferred_slots = [item for item in slots if item.get("status") == "DEFERRED"]
    blocked_items = [item for item in queue_items if item.get("readiness_status") in {"BLOCKED", "NEEDS_VISUAL_ASSET", "NEEDS_EVIDENCE"}]
    ready_next_week = [item for item in queue_items if item.get("priority") in {"TODAY", "THIS_WEEK"} and item.get("readiness_status") in {"READY_TO_PUBLISH", "READY_FOR_REVIEW"}]
    operator_actions = []
    if ready_next_week:
        operator_actions.append(f"今天可发：{ready_next_week[0].get('title') or ready_next_week[0].get('queue_item_id')}")
    for item in blocked_items[:4]:
        action = item.get("recommended_next_action")
        operator_actions.append(f"{item.get('title') or item.get('queue_item_id')}：{action}")
    if not operator_actions:
        operator_actions.append("先录入发布后 metrics，并补齐 copy pack / visual checklist。")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "summary": {
            "planned_count": len(slots),
            "published_count": len(published),
            "deferred_count": len(deferred_slots),
            "ready_next_week_count": len(ready_next_week),
            "blocked_count": len(blocked_items),
        },
        "what_was_published": published[:6],
        "what_was_not_published": [slot for slot in slots if slot.get("status") not in {"PUBLISHED"}][:8],
        "why_not_published": [f"{item.get('title') or item.get('source_id')}: {', '.join(item.get('blockers') or []) or item.get('readiness_status')}" for item in blocked_items[:8]],
        "best_performing_content": list_payload(metrics_review_payload, "top_articles")[:5],
        "weakest_content": list_payload(metrics_review_payload, "underperforming_articles")[:5],
        "queue_changes": queue_items[:8],
        "next_week_plan": list_payload(rhythm_payload, "rhythm_plan"),
        "operator_actions": operator_actions,
        "visual_strategy_notes": list_payload(visual_feedback_payload, "recommendations")[:4],
        "policy": {"advisory_only": True, "no_auto_publish": True, "no_auto_strategy_changes": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    actions = "\n".join(f"- {item}" for item in payload.get("operator_actions", [])) or "- No operator actions."
    plan = "\n".join(f"- {item.get('date')} {item.get('weekday')}: {item.get('status')} {item.get('title') or item.get('reason')}" for item in list_payload(payload, "next_week_plan")) or "- No weekly plan."
    return f"""# Content Ops Closeout

## Summary

- planned_count: `{summary.get('planned_count', 0)}`
- published_count: `{summary.get('published_count', 0)}`
- deferred_count: `{summary.get('deferred_count', 0)}`
- ready_next_week_count: `{summary.get('ready_next_week_count', 0)}`
- blocked_count: `{summary.get('blocked_count', 0)}`

## Operator Actions

{actions}

## Next Week Plan

{plan}
"""
