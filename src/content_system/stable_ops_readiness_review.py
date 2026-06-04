"""Review readiness for stable daily ops after Phase 24 trial."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__stable-ops-readiness-review.json",
        "dated_md": paths.logs_root / f"{run_date}__stable-ops-readiness-review.md",
        "latest_json": paths.logs_root / "latest_stable_ops_readiness_review.json",
        "latest_md": paths.logs_root / "latest_stable_ops_readiness_review.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__stable-ops-readiness-review-board.md",
        "board_latest_md": paths.frontstage_root / "latest_stable_ops_readiness_review_board.md",
    }


def criterion(criterion_id: str, status: str, message: str) -> dict[str, str]:
    return {"criterion_id": criterion_id, "status": status, "message": message}


def build_stable_ops_readiness_review(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    days = [read_json(paths.logs_root / f"latest_stable_trial_day_{day}.json") for day in range(1, 4)]
    calibration = read_json(paths.logs_root / "latest_content_quality_calibration.json")
    methodology = read_json(paths.logs_root / "latest_ops_to_methodology_feedback.json")
    gate = read_json(paths.logs_root / "latest_stable_trial_readiness_gate.json")
    verification = read_json(paths.logs_root / "latest_issue_resolution_verification.json")
    phase23 = read_json(paths.logs_root / "latest_phase23_daily_stability_pipeline.json")
    regression = read_json(paths.logs_root / "latest_publishing_checklist_regression.json")
    gitignore_text = (repo_root / ".gitignore").read_text(encoding="utf-8") if (repo_root / ".gitignore").exists() else ""
    phase24_ignored = "Phase 24 generated artifacts" in gitignore_text and "stable-ops-readiness-review" in gitignore_text

    day_results = [day.get("day_result") for day in days if isinstance(day.get("day_result"), dict)]
    day_snapshots = [day.get("ops_snapshot") for day in days if isinstance(day.get("ops_snapshot"), dict)]
    stable_trial_days = len(day_results)
    ready_days = sum(1 for result in day_results if result.get("day_status") == "READY")
    actionable_days = sum(1 for result in day_results if result.get("day_status") == "ACTIONABLE")
    blocked_days = sum(1 for result in day_results if result.get("day_status") == "BLOCKED")
    can_continue_days = sum(1 for result in day_results if result.get("can_continue"))
    blocking_issues = max([int(snapshot.get("blocker_count") or 0) for snapshot in day_snapshots] or [0])
    manual_required_items = sum(len(list_payload(day, "operator_actions")) for day in days if day)
    calibration_summary = calibration.get("summary") if isinstance(calibration.get("summary"), dict) else {}
    methodology_summary = methodology.get("summary") if isinstance(methodology.get("summary"), dict) else {}
    gate_summary = gate.get("summary") if isinstance(gate.get("summary"), dict) else {}
    verification_summary = verification.get("summary") if isinstance(verification.get("summary"), dict) else {}
    regression_summary = regression.get("summary") if isinstance(regression.get("summary"), dict) else {}

    criteria = [
        criterion(
            "stable_trial_no_blockers",
            "PASS" if stable_trial_days == 3 and blocked_days == 0 and can_continue_days == stable_trial_days else "FAIL",
            f"stable_trial_days={stable_trial_days}; blocked_days={blocked_days}; can_continue_days={can_continue_days}",
        ),
        criterion(
            "no_blocking_failures",
            "PASS" if int(gate_summary.get("blocking_failures") or 0) == 0 and blocking_issues == 0 else "FAIL",
            f"gate_blocking_failures={gate_summary.get('blocking_failures', 0)}; trial_blocking_issues={blocking_issues}",
        ),
        criterion(
            "publishing_checklist_regression_pass",
            "PASS" if regression_summary.get("regression_status") == "PASS" else "WARN",
            f"regression_status={regression_summary.get('regression_status', 'UNKNOWN')}",
        ),
        criterion(
            "queue_has_actionable_items",
            "PASS" if actionable_days or ready_days else "FAIL",
            f"ready_days={ready_days}; actionable_days={actionable_days}",
        ),
        criterion(
            "calendar_has_actionable_days",
            "PASS" if actionable_days or ready_days else "FAIL",
            f"stable trial actionable_days={actionable_days}; ready_days={ready_days}",
        ),
        criterion(
            "content_quality_issues_are_understood",
            "PASS" if int(calibration_summary.get("quality_issue_count") or 0) > 0 else "WARN",
            f"quality_issue_count={calibration_summary.get('quality_issue_count', 0)}; recommendations={calibration_summary.get('calibration_recommendation_count', 0)}",
        ),
        criterion(
            "visual_blockers_are_explicit",
            "PASS" if any(issue.get("area") == "visual" for issue in list_payload(calibration, "quality_issues")) else "WARN",
            "visual quality issues are explicitly represented in calibration." if any(issue.get("area") == "visual" for issue in list_payload(calibration, "quality_issues")) else "no visual issue found in calibration.",
        ),
        criterion(
            "manual_actions_are_clearly_listed",
            "PASS" if manual_required_items > 0 else "WARN",
            f"manual_required_items={manual_required_items}",
        ),
        criterion(
            "safety_boundaries_intact",
            "PASS"
            if all(not (day.get("safety") or {}).get(key) for day in days if day for key in ("auto_publish", "wechat_api", "auto_image_generation", "live_default_enabled"))
            else "FAIL",
            "no auto publish, no WeChat API, no image generation, no live default.",
        ),
        criterion(
            "generated_artifacts_ignored",
            "PASS" if phase24_ignored else "WARN",
            "Phase 24 generated artifact patterns are present in .gitignore." if phase24_ignored else "Phase 24 .gitignore patterns not fully present yet.",
        ),
    ]
    pass_count = sum(1 for item in criteria if item["status"] == "PASS")
    warn_count = sum(1 for item in criteria if item["status"] == "WARN")
    fail_count = sum(1 for item in criteria if item["status"] == "FAIL")
    if blocked_days or blocking_issues or fail_count >= 2:
        readiness_status = "BLOCKED" if blocking_issues else "NEEDS_FIX"
    elif fail_count:
        readiness_status = "NEEDS_FIX"
    elif warn_count:
        readiness_status = "ACTIONABLE_WITH_WARNINGS"
    else:
        readiness_status = "READY_FOR_DAILY_OPS"

    remaining_risks = []
    if int(verification_summary.get("needs_manual") or 0):
        remaining_risks.append(f"{verification_summary.get('needs_manual')} issue(s) still require manual verification.")
    if int(calibration_summary.get("publish_blocking_quality_issues") or 0):
        remaining_risks.append(f"{calibration_summary.get('publish_blocking_quality_issues')} quality issue(s) can block publishing.")
    if methodology_summary.get("feedback_count"):
        remaining_risks.append("Methodology feedback exists but is not auto-applied.")
    operator_commitments = [
        "Run the daily ops command before making any publishing decision.",
        "Close manual verification items before promoting ACTIONABLE to READY.",
        "Resolve visual asset and mobile readability warnings manually.",
        "Record post-publish metrics manually after any real publication.",
    ]
    next_phase = (
        "Phase 25：Stable Daily Ops Baseline & Operator Acceptance v1"
        if readiness_status in {"READY_FOR_DAILY_OPS", "ACTIONABLE_WITH_WARNINGS"}
        else "Continue Phase 24 fixes before operator acceptance."
    )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "readiness_status": readiness_status,
        "summary": {
            "stable_trial_days": stable_trial_days,
            "ready_days": ready_days,
            "actionable_days": actionable_days,
            "blocked_days": blocked_days,
            "blocking_issues": blocking_issues,
            "manual_required_items": manual_required_items,
            "criteria_pass": pass_count,
            "criteria_warn": warn_count,
            "criteria_fail": fail_count,
            "phase23_status": phase23.get("status", "UNKNOWN"),
        },
        "criteria": criteria,
        "remaining_risks": remaining_risks,
        "operator_commitments": operator_commitments,
        "next_phase_recommendation": next_phase,
        "policy": {"auto_publish": False, "wechat_api": False, "auto_image_generation": False, "auto_apply": False},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    criteria_rows = [
        f"| `{item.get('status')}` | `{item.get('criterion_id')}` | {item.get('message')} |"
        for item in list_payload(payload, "criteria")
    ]
    risks = "\n".join(f"- {item}" for item in payload.get("remaining_risks", [])) or "- None."
    commitments = "\n".join(f"- {item}" for item in payload.get("operator_commitments", []))
    return f"""# Stable Ops Readiness Review

## Summary

- readiness_status: `{payload.get('readiness_status')}`
- stable_trial_days: `{summary.get('stable_trial_days', 0)}`
- ready_days: `{summary.get('ready_days', 0)}`
- actionable_days: `{summary.get('actionable_days', 0)}`
- blocked_days: `{summary.get('blocked_days', 0)}`
- blocking_issues: `{summary.get('blocking_issues', 0)}`

| Status | Criterion | Message |
|---|---|---|
{chr(10).join(criteria_rows)}

## Remaining Risks

{risks}

## Operator Commitments

{commitments}

Next phase: {payload.get('next_phase_recommendation')}
"""
