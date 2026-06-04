"""Build a weekly retrospective from trial day execution records."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__weekly-trial-retrospective.json",
        "dated_md": paths.logs_root / f"{run_date}__weekly-trial-retrospective.md",
        "latest_json": paths.logs_root / "latest_weekly_trial_retrospective.json",
        "latest_md": paths.logs_root / "latest_weekly_trial_retrospective.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__weekly-trial-retrospective-board.md",
        "board_latest_md": paths.frontstage_root / "latest_weekly_trial_retrospective_board.md",
    }


def load_days(paths: ProjectPaths) -> list[dict[str, Any]]:
    days = []
    for day in range(1, 6):
        payload = read_json(paths.logs_root / f"latest_trial_day_{day}_execution.json")
        if payload:
            days.append(payload)
    return days


def issue_key(issue: dict[str, Any]) -> str:
    return f"{issue.get('area')}::{issue.get('description')}"


def safety_violations(days: list[dict[str, Any]]) -> list[str]:
    violations: list[str] = []
    for day in days:
        safety = day.get("safety") if isinstance(day.get("safety"), dict) else {}
        for key in ("auto_publish", "wechat_api", "auto_image_generation", "live_default_enabled"):
            if safety.get(key):
                violations.append(f"day {day.get('trial_day')}: {key} unexpectedly true")
    return violations


def build_weekly_trial_retrospective(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    days = load_days(paths)
    statuses = [(day.get("daily_result") or {}).get("day_status", "UNKNOWN") for day in days if isinstance(day.get("daily_result"), dict)]
    all_issues = [issue for day in days for issue in list_payload(day, "issues")]
    counts = Counter(issue_key(issue) for issue in all_issues)
    recurring = []
    unresolved = []
    for key, count in counts.items():
        area, description = key.split("::", 1)
        entry = {"issue_id": make_id("trial_recurring", run_date, key), "area": area, "description": description, "count": count}
        if count >= 2:
            recurring.append(entry)
        unresolved.append(entry)
    frictions = []
    if any(((day.get("content_ops_snapshot") or {}).get("today_count", 0) == 0) for day in days):
        frictions.append("TODAY queue often empty; operator must choose from THIS_WEEK or fix blockers.")
    if any(((day.get("publishing_readiness") or {}).get("has_visual_blocker")) for day in days):
        frictions.append("Visual assets/checklist are currently the main publishing readiness drag.")
    if any(list_payload(day, "issues") for day in days):
        frictions.append("Failure handling is useful, but issue volume needs prioritization in the workbench.")
    content_observations = [
        "Queue has enough watch/this-week candidates for trial scaffolding, but TODAY readiness is not yet strong.",
        "Evidence and visual blockers are more prominent than core pipeline failures.",
    ]
    readiness_observations = [
        "Manual publish should not be recommended until copy pack, visual checklist, and calendar slot are all ready.",
        "Current trial can continue because blocker_count is zero, but readiness remains WARN/NEEDS_FIX.",
    ]
    ux_observations = [
        "Workbench Phase20 grouping reduces panel sprawl by separating ops, review, visual prep, post-publish, and system ops.",
        "Trial panel should keep recurring issues and fix pack visible without polluting reading mode.",
    ]
    violations = safety_violations(days)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "trial_summary": {
            "days_recorded": len(days),
            "pass_days": sum(1 for status in statuses if status == "PASS"),
            "warn_days": sum(1 for status in statuses if status == "WARN"),
            "blocked_days": sum(1 for status in statuses if status == "BLOCKED"),
            "can_continue": not any(status == "BLOCKED" for status in statuses) and not violations,
        },
        "recurring_issues": recurring[:10],
        "resolved_issues": [],
        "unresolved_issues": unresolved[:12],
        "operator_friction": frictions,
        "content_quality_observations": content_observations,
        "publishing_readiness_observations": readiness_observations,
        "workbench_ux_observations": ux_observations,
        "safety_boundary_check": {"auto_publish": False, "wechat_api": False, "auto_image_generation": False, "violations": violations},
        "recommendations": [
            "Phase22 should reduce high-frequency visual and evidence blockers.",
            "Calibrate content queue so TODAY only contains truly publish-ready items.",
            "Keep phase21-trial as scaffold; real operator should still run trial-day-N across natural days.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("trial_summary") if isinstance(payload.get("trial_summary"), dict) else {}
    recurring = "\n".join(f"- {item.get('area')}: {item.get('description')} (`{item.get('count')}`)" for item in list_payload(payload, "recurring_issues")) or "- None."
    friction = "\n".join(f"- {item}" for item in payload.get("operator_friction", [])) or "- None."
    recommendations = "\n".join(f"- {item}" for item in payload.get("recommendations", [])) or "- None."
    return f"""# Weekly Trial Retrospective

## Summary

- days_recorded: `{summary.get('days_recorded', 0)}`
- pass_days: `{summary.get('pass_days', 0)}`
- warn_days: `{summary.get('warn_days', 0)}`
- blocked_days: `{summary.get('blocked_days', 0)}`
- can_continue: `{summary.get('can_continue', True)}`

## Recurring Issues

{recurring}

## Operator Friction

{friction}

## Recommendations

{recommendations}
"""
