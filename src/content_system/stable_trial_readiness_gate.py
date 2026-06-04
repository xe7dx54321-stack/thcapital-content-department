"""Build the stable trial readiness gate for Phase 23."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__stable-trial-readiness-gate.json",
        "dated_md": paths.logs_root / f"{run_date}__stable-trial-readiness-gate.md",
        "latest_json": paths.logs_root / "latest_stable_trial_readiness_gate.json",
        "latest_md": paths.logs_root / "latest_stable_trial_readiness_gate.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__stable-trial-readiness-gate-board.md",
        "board_latest_md": paths.frontstage_root / "latest_stable_trial_readiness_gate_board.md",
    }


def criterion(criterion_id: str, status: str, message: str, blocking: bool = False) -> dict[str, Any]:
    return {
        "criterion_id": criterion_id,
        "status": status,
        "message": message,
        "blocking": blocking,
    }


def bool_from_payload(payload: dict[str, Any], key: str, default: bool = False) -> bool:
    value = payload.get(key, default)
    return bool(value)


def build_stable_trial_readiness_gate(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    verification = read_json(paths.logs_root / "latest_issue_resolution_verification.json")
    stabilizer = read_json(paths.logs_root / "latest_trial_day_status_stabilizer.json")
    regression = read_json(paths.logs_root / "latest_publishing_checklist_regression.json")
    phase22 = read_json(paths.logs_root / "latest_phase22_daily_ops_pipeline.json")
    queue_repair = read_json(paths.market_content_root / "07_publishing" / "latest_content_queue_readiness_repair.json")
    calendar = read_json(paths.market_content_root / "07_publishing" / "latest_publishing_calendar_readiness_calibration.json")

    verification_summary = verification.get("summary") if isinstance(verification.get("summary"), dict) else {}
    stable_summary = stabilizer.get("stabilization_summary") if isinstance(stabilizer.get("stabilization_summary"), dict) else {}
    regression_summary = regression.get("summary") if isinstance(regression.get("summary"), dict) else {}
    phase22_summary = phase22.get("summary") if isinstance(phase22.get("summary"), dict) else {}
    queue_summary = queue_repair.get("summary") if isinstance(queue_repair.get("summary"), dict) else {}
    calendar_summary = calendar.get("summary") if isinstance(calendar.get("summary"), dict) else {}

    blocker_count = int(stable_summary.get("blocker_count") or 0)
    can_continue = bool_from_payload(stable_summary, "can_continue", True)
    unresolved = int(verification_summary.get("unresolved") or 0)
    needs_manual = int(verification_summary.get("needs_manual") or 0)
    applied_or_partial = int(verification_summary.get("verified") or 0) + int(verification_summary.get("partial") or 0)
    regression_status = str(regression_summary.get("regression_status") or "UNKNOWN")
    queue_item_count = int(queue_summary.get("item_count") or 0)
    queue_items = list_payload(queue_repair, "items")
    queue_missing_actions = [
        item for item in queue_items if item.get("repaired_readiness_status") != "READY_TO_PUBLISH" and not item.get("next_operator_action")
    ]
    calendar_days = int(calendar_summary.get("calendar_days") or 0)
    actionable_days = int(calendar_summary.get("actionable_days") or 0)
    ready_days = int(calendar_summary.get("ready_days") or 0)
    phase22_status = str(phase22.get("status") or "UNKNOWN")

    gitignore_text = (repo_root / ".gitignore").read_text(encoding="utf-8") if (repo_root / ".gitignore").exists() else ""
    phase23_ignored = "Phase 23 generated artifacts" in gitignore_text and "stable-trial-readiness-gate" in gitignore_text

    criteria = [
        criterion(
            "no_blockers",
            "PASS" if blocker_count == 0 else "FAIL",
            f"trial stabilizer blocker_count={blocker_count}",
            blocking=blocker_count > 0,
        ),
        criterion(
            "publishing_checklist_regression_pass",
            "PASS" if regression_status == "PASS" else "WARN" if regression_status == "WARN" else "FAIL",
            f"publishing checklist regression status={regression_status}",
            blocking=regression_status == "FAIL",
        ),
        criterion(
            "trial_day_can_continue",
            "PASS" if can_continue else "FAIL",
            f"trial stabilizer can_continue={can_continue}; status_after={stabilizer.get('status_after', 'UNKNOWN')}",
            blocking=not can_continue,
        ),
        criterion(
            "quick_fixes_processed",
            "PASS" if applied_or_partial > 0 and unresolved == 0 else "WARN" if applied_or_partial > 0 else "FAIL",
            f"verified_or_partial={applied_or_partial}; unresolved={unresolved}; needs_manual={needs_manual}",
            blocking=unresolved > 0 and applied_or_partial == 0,
        ),
        criterion(
            "queue_items_have_next_actions",
            "PASS" if queue_item_count > 0 and not queue_missing_actions else "WARN" if queue_item_count > 0 else "FAIL",
            f"queue_items={queue_item_count}; missing_next_actions={len(queue_missing_actions)}",
            blocking=queue_item_count == 0,
        ),
        criterion(
            "calendar_days_have_actionable_status",
            "PASS" if ready_days > 0 else "WARN" if actionable_days > 0 else "FAIL",
            f"calendar_days={calendar_days}; ready_days={ready_days}; actionable_days={actionable_days}",
            blocking=calendar_days == 0,
        ),
        criterion(
            "phase22_pipeline_continues",
            "PASS" if phase22_status == "SUCCESS" else "WARN" if phase22_status == "DEGRADED" else "FAIL",
            f"phase22 status={phase22_status}; high_issues={phase22_summary.get('high_issues', 0)}",
            blocking=phase22_status == "FAILED",
        ),
        criterion("no_auto_publish_boundary", "PASS", "Phase 23 remains sidecar-only; no publish API call is invoked."),
        criterion("no_wechat_api_boundary", "PASS", "No WeChat API or draft-box operation is present in the Phase 23 pipeline."),
        criterion("no_auto_image_generation_boundary", "PASS", "No image generation model is invoked; image work remains manual-first."),
        criterion(
            "generated_artifacts_ignored",
            "PASS" if phase23_ignored else "WARN",
            "Phase 23 generated artifact patterns are present in .gitignore." if phase23_ignored else "Phase 23 .gitignore patterns are not fully present yet.",
        ),
    ]

    pass_count = sum(1 for item in criteria if item.get("status") == "PASS")
    warn_count = sum(1 for item in criteria if item.get("status") == "WARN")
    fail_count = sum(1 for item in criteria if item.get("status") == "FAIL")
    blocking_failures = sum(1 for item in criteria if item.get("status") == "FAIL" and item.get("blocking"))
    if blocking_failures:
        gate_status = "BLOCKED"
    elif fail_count:
        gate_status = "NOT_READY"
    elif warn_count:
        gate_status = "ACTIONABLE_WITH_WARNINGS"
    else:
        gate_status = "READY_FOR_STABLE_TRIAL"

    next_actions = []
    if needs_manual:
        next_actions.append(f"Close {needs_manual} manual issue(s) from the verification board before calling the trial stable.")
    if unresolved:
        next_actions.append(f"Investigate {unresolved} unresolved issue(s); do not downgrade them without evidence.")
    if actionable_days and not ready_days:
        next_actions.append("Use calendar ACTIONABLE days: complete listed operator action, then rerun calibration.")
    if queue_missing_actions:
        next_actions.append("Add next_operator_action for queue items that still lack an operator handoff.")
    if not next_actions:
        next_actions.append("Proceed to stable trial using manual publish boundaries and daily operator review.")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "gate_status": gate_status,
        "criteria": criteria,
        "summary": {
            "criteria_count": len(criteria),
            "pass": pass_count,
            "warn": warn_count,
            "fail": fail_count,
            "blocking_failures": blocking_failures,
        },
        "next_actions": next_actions,
        "policy": {
            "sidecar_only": True,
            "auto_publish": False,
            "wechat_api": False,
            "auto_image_generation": False,
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
        f"| `{item.get('status')}` | `{item.get('criterion_id')}` | {item.get('message')} |"
        for item in list_payload(payload, "criteria")
    ]
    next_actions = "\n".join(f"- {item}" for item in payload.get("next_actions", []))
    return f"""# Stable Trial Readiness Gate

## Summary

- gate_status: `{payload.get('gate_status')}`
- criteria_count: `{summary.get('criteria_count', 0)}`
- pass: `{summary.get('pass', 0)}`
- warn: `{summary.get('warn', 0)}`
- fail: `{summary.get('fail', 0)}`
- blocking_failures: `{summary.get('blocking_failures', 0)}`

| Status | Criterion | Message |
|---|---|---|
{chr(10).join(rows)}

## Next Actions

{next_actions}

Policy: sidecar-only, no auto publish, no WeChat API, no image generation, no config/prompt/rule changes.
"""
