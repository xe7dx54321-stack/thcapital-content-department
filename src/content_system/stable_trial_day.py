"""Build stable ops trial day records for Phase 24."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str, day: int) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__stable-trial-day-{day}.json",
        "dated_md": paths.logs_root / f"{run_date}__stable-trial-day-{day}.md",
        "latest_json": paths.logs_root / f"latest_stable_trial_day_{day}.json",
        "latest_md": paths.logs_root / f"latest_stable_trial_day_{day}.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__stable-trial-day-{day}-board.md",
        "board_latest_md": paths.frontstage_root / f"latest_stable_trial_day_{day}_board.md",
    }


def common_quality_issues(article_reviews: list[dict[str, Any]]) -> list[str]:
    counts: dict[str, int] = {}
    for article in article_reviews:
        for weakness in article.get("weaknesses") or []:
            text = str(weakness)
            counts[text] = counts.get(text, 0) + 1
        scores = article.get("scores") if isinstance(article.get("scores"), dict) else {}
        for key, value in scores.items():
            try:
                score = float(value)
            except (TypeError, ValueError):
                continue
            if score < 6:
                label = f"{key} below 6"
                counts[label] = counts.get(label, 0) + 1
    return [f"{key} ({value})" for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:8]]


def action_from_calendar(day_index: int, calendar_days: list[dict[str, Any]]) -> dict[str, Any]:
    selected = calendar_days[(day_index - 1) % len(calendar_days)] if calendar_days else {}
    status = str(selected.get("calibrated_status") or "OPEN")
    priority = "HIGH" if status == "ACTIONABLE" else "MEDIUM" if status in {"OPEN", "NEEDS_REVIEW"} else "LOW"
    action = selected.get("required_operator_action") or selected.get("readiness_reason") or "Review today's content queue and decide whether to hold."
    return {
        "action_id": make_id("stable_action", day_index, selected.get("date"), selected.get("recommended_queue_item_id")),
        "area": "publishing",
        "action": action,
        "priority": priority,
        "manual_required": True,
        "status": "OPEN",
    }


def build_stable_trial_day(paths: ProjectPaths, repo_root: Path, day: int) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing = paths.market_content_root / "07_publishing"
    inputs = {
        "phase23": paths.logs_root / "latest_phase23_daily_stability_pipeline.json",
        "gate": paths.logs_root / "latest_stable_trial_readiness_gate.json",
        "stabilizer": paths.logs_root / "latest_trial_day_status_stabilizer.json",
        "verification": paths.logs_root / "latest_issue_resolution_verification.json",
        "queue_repair": publishing / "latest_content_queue_readiness_repair.json",
        "calendar_calibration": publishing / "latest_publishing_calendar_readiness_calibration.json",
        "queue_priority": publishing / "latest_content_queue_priority.json",
        "weekly_calendar": publishing / "latest_weekly_publishing_calendar.json",
        "closeout": paths.logs_root / "latest_content_ops_closeout.json",
        "article_review": paths.market_content_root / "05_draft_packs" / "latest_methodology_article_review.json",
    }
    payloads = {key: read_json(path) for key, path in inputs.items()}
    warnings = [f"Missing input: {key}" for key, value in payloads.items() if not value]

    gate = payloads["gate"]
    gate_summary = gate.get("summary") if isinstance(gate.get("summary"), dict) else {}
    stabilizer = payloads["stabilizer"]
    stable_summary = stabilizer.get("stabilization_summary") if isinstance(stabilizer.get("stabilization_summary"), dict) else {}
    queue_repair = payloads["queue_repair"]
    queue_summary = queue_repair.get("summary") if isinstance(queue_repair.get("summary"), dict) else {}
    calendar = payloads["calendar_calibration"]
    calendar_summary = calendar.get("summary") if isinstance(calendar.get("summary"), dict) else {}
    article_review = payloads["article_review"]
    article_summary = article_review.get("summary") if isinstance(article_review.get("summary"), dict) else {}
    articles = list_payload(article_review, "articles")
    calendar_days = list_payload(calendar, "days")
    verification_summary = payloads["verification"].get("summary") if isinstance(payloads["verification"].get("summary"), dict) else {}

    actions = [action_from_calendar(day, calendar_days)]
    if int(verification_summary.get("needs_manual") or 0):
        actions.append(
            {
                "action_id": make_id("stable_action", day, "manual_verification"),
                "area": "system",
                "action": f"Review {verification_summary.get('needs_manual')} issue(s) marked NEEDS_MANUAL in issue resolution verification.",
                "priority": "HIGH",
                "manual_required": True,
                "status": "OPEN",
            }
        )
    if int(article_summary.get("revise") or 0):
        actions.append(
            {
                "action_id": make_id("stable_action", day, "quality_review"),
                "area": "draft",
                "action": "Prioritize one methodology-reviewed draft for title/opening/core-judgment calibration before publishing.",
                "priority": "MEDIUM",
                "manual_required": True,
                "status": "OPEN",
            }
        )

    blocker_count = int(stable_summary.get("blocker_count") or 0) + int(gate_summary.get("blocking_failures") or 0)
    can_continue = bool(stable_summary.get("can_continue", True)) and blocker_count == 0
    ready_to_publish = int(queue_summary.get("ready_to_publish") or 0)
    actionable_days = int(calendar_summary.get("actionable_days") or 0)
    if not can_continue:
        day_status = "BLOCKED"
    elif ready_to_publish > 0:
        day_status = "READY"
    elif actionable_days > 0:
        day_status = "ACTIONABLE"
    else:
        day_status = "WARN"

    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "stable_trial_day": day,
        "trial_mode": "manual_ops_only",
        "readiness_gate": {
            "gate_status": gate.get("gate_status", "UNKNOWN"),
            "blocking_failures": int(gate_summary.get("blocking_failures") or 0),
        },
        "ops_snapshot": {
            "queue_items": int(queue_summary.get("item_count") or 0),
            "ready_for_review": int(queue_summary.get("ready_for_review") or 0),
            "ready_to_publish": ready_to_publish,
            "needs_manual": int(queue_summary.get("needs_manual") or 0),
            "calendar_ready_days": int(calendar_summary.get("ready_days") or 0),
            "calendar_actionable_days": actionable_days,
            "blocker_count": blocker_count,
            "actionable_warning_count": int(stable_summary.get("actionable_warning_count") or 0),
        },
        "content_quality_snapshot": {
            "articles_reviewed": int(article_summary.get("article_count") or len(articles)),
            "ready_articles": int(article_summary.get("ready") or 0),
            "needs_revision": int(article_summary.get("revise") or 0),
            "common_quality_issues": common_quality_issues(articles),
        },
        "operator_actions": actions,
        "day_result": {
            "day_status": day_status,
            "can_continue": can_continue,
            "summary": f"Stable trial day {day}: gate={gate.get('gate_status', 'UNKNOWN')}; calendar actionable={actionable_days}; ready_to_publish={ready_to_publish}.",
        },
        "safety": {
            "auto_publish": False,
            "wechat_api": False,
            "auto_image_generation": False,
            "live_default_enabled": False,
        },
        "warnings": warnings,
    }
    outputs = output_paths(paths, run_date, day)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    result = payload.get("day_result") if isinstance(payload.get("day_result"), dict) else {}
    ops = payload.get("ops_snapshot") if isinstance(payload.get("ops_snapshot"), dict) else {}
    quality = payload.get("content_quality_snapshot") if isinstance(payload.get("content_quality_snapshot"), dict) else {}
    actions = "\n".join(
        f"- `{item.get('priority')}` {item.get('area')}: {item.get('action')}" for item in list_payload(payload, "operator_actions")
    )
    issues = "\n".join(f"- {item}" for item in quality.get("common_quality_issues", [])) or "- None."
    return f"""# Stable Trial Day {payload.get('stable_trial_day')}

## Result

- day_status: `{result.get('day_status')}`
- can_continue: `{result.get('can_continue')}`
- ready_to_publish: `{ops.get('ready_to_publish', 0)}`
- actionable_warnings: `{ops.get('actionable_warning_count', 0)}`
- calendar_actionable_days: `{ops.get('calendar_actionable_days', 0)}`

## Content Quality Snapshot

- articles_reviewed: `{quality.get('articles_reviewed', 0)}`
- ready_articles: `{quality.get('ready_articles', 0)}`
- needs_revision: `{quality.get('needs_revision', 0)}`

## Common Quality Issues

{issues}

## Operator Actions

{actions}

Safety: no auto publish, no WeChat API, no image generation, no live default.
"""
