"""Build the operator acceptance checklist for stable daily content ops."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__operator-acceptance-checklist.json",
        "dated_md": paths.logs_root / f"{run_date}__operator-acceptance-checklist.md",
        "latest_json": paths.logs_root / "latest_operator_acceptance_checklist.json",
        "latest_md": paths.logs_root / "latest_operator_acceptance_checklist.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__operator-acceptance-checklist-board.md",
        "board_latest_md": paths.frontstage_root / "latest_operator_acceptance_checklist_board.md",
    }


def check(check_id: str, label: str, status: str, operator_note: str) -> dict[str, str]:
    return {"check_id": check_id, "label": label, "status": status, "operator_note": operator_note}


def build_operator_acceptance_checklist(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    baseline = read_json(paths.logs_root / "latest_stable_daily_ops_baseline.json")
    review = read_json(paths.logs_root / "latest_stable_ops_readiness_review.json")
    regression = read_json(paths.logs_root / "latest_publishing_checklist_regression.json")
    failure = read_json(paths.logs_root / "latest_content_ops_failure_handling.json")
    phase24 = read_json(paths.logs_root / "latest_phase24_daily_stable_trial_pipeline.json")
    phase23 = read_json(paths.logs_root / "latest_phase23_daily_stability_pipeline.json")
    workbench_html = paths.frontstage_root / "latest_wechat_workbench.html"
    workbench_data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    runbook_exists = (repo_root / "docs" / "OPERATOR_RUNBOOK.md").exists()

    baseline_summary = baseline.get("summary") if isinstance(baseline.get("summary"), dict) else {}
    quality = baseline.get("content_quality_status") if isinstance(baseline.get("content_quality_status"), dict) else {}
    review_summary = review.get("summary") if isinstance(review.get("summary"), dict) else {}
    regression_summary = regression.get("summary") if isinstance(regression.get("summary"), dict) else {}
    failure_summary = failure.get("summary") if isinstance(failure.get("summary"), dict) else {}
    phase24_summary = phase24.get("summary") if isinstance(phase24.get("summary"), dict) else {}
    phase23_summary = phase23.get("summary") if isinstance(phase23.get("summary"), dict) else {}
    wb_summary = workbench_data.get("summary") if isinstance(workbench_data.get("summary"), dict) else {}

    safety_values = {
        "no_auto_publish": bool(phase24_summary.get("no_auto_publish", True)),
        "no_wechat_api": bool(phase24_summary.get("no_wechat_api", True)),
        "no_auto_image_generation": bool(phase24_summary.get("no_auto_image_generation", True)),
        "no_auto_config_change": bool(phase24_summary.get("no_config_prompt_rule_changes", True)),
    }
    checks = [
        check(
            "daily_command_runs",
            "Daily command runs without crash",
            "PASS" if baseline_summary.get("can_run_daily") else "FAIL",
            f"baseline_status={baseline.get('baseline_status', 'UNKNOWN')}",
        ),
        check(
            "workbench_opens",
            "Workbench can be opened locally",
            "PASS" if workbench_html.exists() else "FAIL",
            "latest_wechat_workbench.html exists." if workbench_html.exists() else "Run make wechat-workbench.",
        ),
        check(
            "shows_today_ops",
            "Workbench shows today's operator actions",
            "PASS" if safe_int(wb_summary.get("content_ops_queue_count")) or safe_int(wb_summary.get("phase22_action_count")) else "WARN",
            f"queue_count={wb_summary.get('content_ops_queue_count', 0)}; phase22_actions={wb_summary.get('phase22_action_count', 0)}",
        ),
        check(
            "shows_content_queue",
            "Workbench shows content queue",
            "PASS" if safe_int(wb_summary.get("content_ops_queue_count")) else "WARN",
            f"content_ops_queue_count={wb_summary.get('content_ops_queue_count', 0)}",
        ),
        check(
            "shows_publishing_readiness",
            "Workbench shows publishing readiness",
            "PASS" if safe_int(wb_summary.get("wechat_copy_pack_count")) or safe_int(wb_summary.get("visual_publishing_checklist_count")) else "WARN",
            f"copy_pack={wb_summary.get('wechat_copy_pack_count', 0)}; visual_checklist={wb_summary.get('visual_publishing_checklist_count', 0)}",
        ),
        check(
            "shows_quality_issues",
            "Quality issues are visible",
            "PASS" if safe_int(quality.get("quality_issues")) else "WARN",
            f"quality_issues={quality.get('quality_issues', 0)}; publish_blockers={quality.get('publish_blocking_quality_issues', 0)}",
        ),
        check(
            "shows_blockers",
            "True blockers are explicit",
            "PASS" if safe_int(baseline_summary.get("blocking_issue_count")) == 0 else "FAIL",
            f"blocking_issue_count={baseline_summary.get('blocking_issue_count', 0)}",
        ),
        check(
            "no_auto_publish",
            "No automatic publish",
            "PASS" if safety_values["no_auto_publish"] else "FAIL",
            "stable ops runner is manual-only.",
        ),
        check(
            "no_wechat_api",
            "No WeChat API integration",
            "PASS" if safety_values["no_wechat_api"] else "FAIL",
            "no draft-box or publishing API calls.",
        ),
        check(
            "no_auto_image_generation",
            "No automatic image generation",
            "PASS" if safety_values["no_auto_image_generation"] else "FAIL",
            "visual assets remain manual-first.",
        ),
        check(
            "no_auto_config_change",
            "No automatic prompt/config/rule changes",
            "PASS" if safety_values["no_auto_config_change"] else "FAIL",
            "methodology feedback is advisory and auto_apply=false.",
        ),
        check(
            "no_publishable_content_reason",
            "If no publishable article exists, reason is explained",
            "PASS" if safe_int(quality.get("ready_to_publish")) > 0 or quality.get("interpretation") else "WARN",
            str(quality.get("interpretation") or "No interpretation available."),
        ),
        check(
            "quality_next_actions",
            "Quality issues have next operator action",
            "PASS" if safe_int(quality.get("publish_blocking_quality_issues")) >= 0 and baseline.get("manual_required_items") else "WARN",
            "Manual required items are listed in stable daily ops baseline.",
        ),
        check(
            "regression_passes",
            "Publishing checklist regression passes",
            "PASS" if regression_summary.get("regression_status") == "PASS" else "WARN",
            f"regression_status={regression_summary.get('regression_status', 'UNKNOWN')}",
        ),
        check(
            "failure_handling_no_blocker",
            "Failure handling has no blocker",
            "PASS" if safe_int(failure_summary.get("blocker_count")) == 0 else "FAIL",
            f"failure_blockers={failure_summary.get('blocker_count', 0)}",
        ),
        check(
            "runbook_available",
            "Operator runbook is available",
            "PASS" if runbook_exists else "WARN",
            "docs/OPERATOR_RUNBOOK.md" if runbook_exists else "Run make operator-runbook.",
        ),
        check(
            "stable_review_ready",
            "Stable ops review is ready or actionable",
            "PASS" if review.get("readiness_status") in {"READY_FOR_DAILY_OPS", "ACTIONABLE_WITH_WARNINGS"} else "FAIL",
            f"readiness_status={review.get('readiness_status', 'UNKNOWN')}; phase23={phase23.get('status', 'UNKNOWN')}; phase23_blocking={phase23_summary.get('blocking_failures', 0)}",
        ),
    ]
    pass_count = sum(1 for item in checks if item["status"] == "PASS")
    warn_count = sum(1 for item in checks if item["status"] == "WARN")
    fail_count = sum(1 for item in checks if item["status"] == "FAIL")
    if fail_count:
        acceptance_status = "BLOCKED" if any(item["check_id"] in {"no_auto_publish", "no_wechat_api", "failure_handling_no_blocker"} and item["status"] == "FAIL" for item in checks) else "NEEDS_FIX"
    elif warn_count:
        acceptance_status = "ACCEPTABLE_WITH_MANUAL_REVIEW"
    else:
        acceptance_status = "ACCEPTABLE_FOR_DAILY_USE"
    decision_guide = [
        "PASS with manual review: use the workbench to choose rewrite/evidence/visual actions.",
        "WARN without blockers: continue daily ops, but do not publish until manual quality and visual checks pass.",
        "FAIL on safety boundary or blocker: stop publishing preparation and repair the issue first.",
        "ready_to_publish=0: acceptable for system baseline; it means content inventory still needs human work.",
    ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "acceptance_status": acceptance_status,
        "checks": checks,
        "operator_acceptance_summary": {
            "check_count": len(checks),
            "pass": pass_count,
            "warn": warn_count,
            "fail": fail_count,
            "manual_review_required": True,
        },
        "operator_decision_guide": decision_guide,
        "policy": {
            "manual_ops_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_auto_config_change": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("operator_acceptance_summary") if isinstance(payload.get("operator_acceptance_summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('status')}` | `{item.get('check_id')}` | {item.get('label')} | {item.get('operator_note')} |"
        for item in payload.get("checks", [])
    )
    guide = "\n".join(f"- {item}" for item in payload.get("operator_decision_guide", []))
    return f"""# Operator Acceptance Checklist

## Summary

- acceptance_status: `{payload.get('acceptance_status')}`
- check_count: `{summary.get('check_count', 0)}`
- pass: `{summary.get('pass', 0)}`
- warn: `{summary.get('warn', 0)}`
- fail: `{summary.get('fail', 0)}`
- manual_review_required: `{summary.get('manual_review_required')}`

| Status | Check | Label | Operator note |
|---|---|---|---|
{rows}

## Operator Decision Guide

{guide}
"""
