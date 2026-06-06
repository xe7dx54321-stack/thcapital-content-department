"""Build the stable daily ops baseline for Content Factory v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__stable-daily-ops-baseline.json",
        "dated_md": paths.logs_root / f"{run_date}__stable-daily-ops-baseline.md",
        "latest_json": paths.logs_root / "latest_stable_daily_ops_baseline.json",
        "latest_md": paths.logs_root / "latest_stable_daily_ops_baseline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__stable-daily-ops-baseline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_stable_daily_ops_baseline_board.md",
    }


def input_paths(paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    return {
        "phase24": paths.logs_root / "latest_phase24_daily_stable_trial_pipeline.json",
        "stable_ops_review": paths.logs_root / "latest_stable_ops_readiness_review.json",
        "quality_calibration": paths.logs_root / "latest_content_quality_calibration.json",
        "methodology_feedback": paths.logs_root / "latest_ops_to_methodology_feedback.json",
        "stable_trial_gate": paths.logs_root / "latest_stable_trial_readiness_gate.json",
        "phase23": paths.logs_root / "latest_phase23_daily_stability_pipeline.json",
        "queue_repair": paths.market_content_root / "07_publishing" / "latest_content_queue_readiness_repair.json",
        "calendar_calibration": paths.market_content_root / "07_publishing" / "latest_publishing_calendar_readiness_calibration.json",
        "hot_material_pool": paths.market_content_root / "03_topic_candidates" / "latest_daily_hot_material_pool.json",
        "hot_material_quality_gate": paths.logs_root / "latest_hot_material_quality_gate.json",
        "operator_runbook": repo_root / "docs" / "OPERATOR_RUNBOOK.md",
        "system_closeout": repo_root / "docs" / "PHASE0_19_SYSTEM_CLOSEOUT.md",
    }


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def build_recommended_flow() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "Run daily ops baseline",
            "command": "make stable-daily-ops",
            "expected_result": "SUCCESS or ACTIONABLE_WITH_WARNINGS",
            "operator_decision": "Continue unless blocker exists",
        },
        {
            "step": 2,
            "name": "Open stable workbench",
            "command": "open 同行资本市场内容系统/11_frontstage/latest_wechat_workbench.html",
            "expected_result": "Stable Daily Ops Baseline and Operator Acceptance panels are visible",
            "operator_decision": "Review manual required items before any publishing action",
        },
        {
            "step": 3,
            "name": "Inspect queue and publishing readiness",
            "command": "review workbench 今日运营 and 内容队列 sections",
            "expected_result": "Every non-ready item has a reason and next operator action",
            "operator_decision": "Pick review/visual/evidence actions; do not publish automatically",
        },
        {
            "step": 4,
            "name": "Handle content quality blockers",
            "command": "review Content Quality Calibration",
            "expected_result": "Blocking quality issues are explicit",
            "operator_decision": "Rewrite, collect evidence, or hold manually",
        },
        {
            "step": 5,
            "name": "Record manual outcomes",
            "command": "use existing publish session and metrics scripts only after manual action",
            "expected_result": "Manual publishing and metrics records stay operator-controlled",
            "operator_decision": "No WeChat API, no backend scraping, no image generation",
        },
    ]


def build_stable_daily_ops_baseline(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    inputs = input_paths(paths, repo_root)
    warnings = warning_for_missing(inputs)
    phase24 = read_json(inputs["phase24"])
    review = read_json(inputs["stable_ops_review"])
    quality = read_json(inputs["quality_calibration"])
    methodology = read_json(inputs["methodology_feedback"])
    gate = read_json(inputs["stable_trial_gate"])
    phase23 = read_json(inputs["phase23"])
    queue = read_json(inputs["queue_repair"])
    calendar = read_json(inputs["calendar_calibration"])
    hot_pool = read_json(inputs["hot_material_pool"])
    hot_gate = read_json(inputs["hot_material_quality_gate"])

    phase24_summary = phase24.get("summary") if isinstance(phase24.get("summary"), dict) else {}
    review_summary = review.get("summary") if isinstance(review.get("summary"), dict) else {}
    quality_summary = quality.get("summary") if isinstance(quality.get("summary"), dict) else {}
    methodology_summary = methodology.get("summary") if isinstance(methodology.get("summary"), dict) else {}
    gate_summary = gate.get("summary") if isinstance(gate.get("summary"), dict) else {}
    phase23_summary = phase23.get("summary") if isinstance(phase23.get("summary"), dict) else {}
    queue_summary = queue.get("summary") if isinstance(queue.get("summary"), dict) else {}
    calendar_summary = calendar.get("summary") if isinstance(calendar.get("summary"), dict) else {}
    hot_pool_summary = hot_pool.get("summary") if isinstance(hot_pool.get("summary"), dict) else {}
    hot_gate_summary = hot_gate.get("summary") if isinstance(hot_gate.get("summary"), dict) else {}

    safety = {
        "auto_publish": False,
        "wechat_api": False,
        "auto_image_generation": False,
        "auto_config_change": False,
    }
    blocking_issue_count = max(
        safe_int(review_summary.get("blocking_issues")),
        safe_int(phase24_summary.get("blocking_issues")),
        safe_int(gate_summary.get("blocking_failures")),
        safe_int(phase23_summary.get("blocking_failures")),
    )
    phase24_status = str(phase24.get("status") or "UNKNOWN")
    review_status = str(review.get("readiness_status") or "UNKNOWN")

    true_blockers: list[str] = []
    if phase24_status == "FAILED":
        true_blockers.append("Phase 24 daily stable trial pipeline failed.")
    if review_status == "BLOCKED":
        true_blockers.append("Stable ops readiness review is BLOCKED.")
    if blocking_issue_count:
        true_blockers.append(f"{blocking_issue_count} blocking issue(s) remain.")
    if not all(value is False for value in safety.values()):
        true_blockers.append("Safety boundary violation detected.")

    if true_blockers:
        baseline_status = "BLOCKED"
    elif review_status == "READY_FOR_DAILY_OPS" and phase24_status in {"SUCCESS", "ACTIONABLE"}:
        baseline_status = "READY_FOR_DAILY_OPS"
    elif review_status in {"ACTIONABLE_WITH_WARNINGS", "READY_FOR_DAILY_OPS"}:
        baseline_status = "ACTIONABLE_WITH_WARNINGS"
    else:
        baseline_status = "NEEDS_FIX"

    ready_to_publish = safe_int(queue_summary.get("ready_to_publish"))
    ready_for_review = safe_int(queue_summary.get("ready_for_review"))
    quality_issues = safe_int(quality_summary.get("quality_issue_count"))
    publish_blocking_quality = safe_int(quality_summary.get("publish_blocking_quality_issues"))
    manual_required = max(
        safe_int(review_summary.get("manual_required_items")),
        safe_int(queue_summary.get("needs_manual")),
        publish_blocking_quality,
    )
    acceptable_warnings = [
        "ready_to_publish=0 is acceptable when all content blockers have explicit next operator actions.",
        "Quality issues are content inventory state, not an engineering failure, when they are visible and actionable.",
        "Methodology feedback remains advisory until a human applies methodology/config changes.",
        "Manual visual review and publishing checklist warnings are expected before any real publication.",
    ]
    hot_gate_status = str(hot_gate.get("gate_status") or "UNKNOWN")
    weak_supply_reasons = hot_gate_summary.get("weak_supply_reasons") if isinstance(hot_gate_summary.get("weak_supply_reasons"), list) else []
    if hot_gate_status == "WEAK_SUPPLY":
        acceptable_warnings.append(
            "Upstream hot material supply can be WEAK_SUPPLY while daily ops remains usable; operator should run backfill tasks."
        )
    upstream_supply = {
        "hot_material_count": safe_int(hot_pool_summary.get("material_count")),
        "write_now": safe_int(hot_pool_summary.get("write_now")),
        "develop_topic": safe_int(hot_pool_summary.get("develop_topic")),
        "backfill_first": safe_int(hot_pool_summary.get("backfill_first")),
        "promote_to_topic_pipeline": safe_int(hot_gate_summary.get("promote_to_topic_pipeline")),
        "backfill_required": safe_int(hot_gate_summary.get("backfill_required")),
        "gate_status": hot_gate_status,
        "weak_supply_reasons": weak_supply_reasons,
        "interpretation": (
            "Upstream supply is weak; daily ops can continue, but operator should backfill verified sources before assuming the topic queue is exhausted."
            if hot_gate_status == "WEAK_SUPPLY"
            else "Upstream supply is available or actionable based on the latest hot material quality gate."
        ),
    }
    manual_required_items = [
        {
            "area": "content_quality",
            "count": publish_blocking_quality,
            "operator_action": "Review publish-blocking title/opening/evidence/visual issues before manual publishing.",
        },
        {
            "area": "queue",
            "count": safe_int(queue_summary.get("needs_manual")),
            "operator_action": "Use queue next actions to choose rewrite, evidence, visual, hold, or review.",
        },
        {
            "area": "methodology",
            "count": safe_int(methodology_summary.get("feedback_count")),
            "operator_action": "Treat ops-to-methodology feedback as suggestions; do not auto-apply config changes.",
        },
    ]
    content_quality_status = {
        "ready_to_publish": ready_to_publish,
        "ready_for_review": ready_for_review,
        "quality_issues": quality_issues,
        "publish_blocking_quality_issues": publish_blocking_quality,
        "interpretation": (
            "System is ready for daily ops, but content inventory still needs human quality work before publishing."
            if ready_to_publish == 0
            else "At least one queue item is ready to publish after human final checks."
        ),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "baseline_status": baseline_status,
        "daily_command": "make stable-daily-ops",
        "recommended_operator_flow": build_recommended_flow(),
        "acceptable_warnings": acceptable_warnings,
        "true_blockers": true_blockers,
        "manual_required_items": manual_required_items,
        "content_quality_status": content_quality_status,
        "upstream_supply": upstream_supply,
        "ops_status": {
            "phase24_status": phase24_status,
            "stable_ops_readiness_status": review_status,
            "phase23_status": phase23.get("status", "UNKNOWN"),
            "calendar_actionable_days": safe_int(calendar_summary.get("actionable_days")),
            "calendar_ready_days": safe_int(calendar_summary.get("ready_days")),
            "queue_ready_for_review": ready_for_review,
        },
        "safety_boundaries": safety,
        "summary": {
            "baseline_ready": baseline_status == "READY_FOR_DAILY_OPS",
            "can_run_daily": baseline_status in {"READY_FOR_DAILY_OPS", "ACTIONABLE_WITH_WARNINGS"},
            "requires_operator_review": True,
            "blocking_issue_count": len(true_blockers),
            "warnings": len(warnings),
            "upstream_gate_status": hot_gate_status,
        },
        "warnings": warnings,
        "notes": [
            "Daily ops readiness does not mean every article is ready to publish.",
            "ready_to_publish=0 remains acceptable when blockers are explicit and operator actions are available.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    quality = payload.get("content_quality_status") if isinstance(payload.get("content_quality_status"), dict) else {}
    upstream = payload.get("upstream_supply") if isinstance(payload.get("upstream_supply"), dict) else {}
    flow = "\n".join(
        f"{item.get('step')}. `{item.get('command')}` - {item.get('operator_decision')}"
        for item in payload.get("recommended_operator_flow", [])
    )
    warnings = "\n".join(f"- {item}" for item in payload.get("acceptable_warnings", []))
    blockers = "\n".join(f"- {item}" for item in payload.get("true_blockers", [])) or "- None."
    manual = "\n".join(
        f"- {item.get('area')}: {item.get('count')} - {item.get('operator_action')}"
        for item in payload.get("manual_required_items", [])
    )
    return f"""# Stable Daily Ops Baseline

## Summary

- baseline_status: `{payload.get('baseline_status')}`
- daily_command: `{payload.get('daily_command')}`
- can_run_daily: `{summary.get('can_run_daily')}`
- blocking_issue_count: `{summary.get('blocking_issue_count')}`
- requires_operator_review: `{summary.get('requires_operator_review')}`

## Content Quality Status

- ready_to_publish: `{quality.get('ready_to_publish', 0)}`
- ready_for_review: `{quality.get('ready_for_review', 0)}`
- quality_issues: `{quality.get('quality_issues', 0)}`
- publish_blocking_quality_issues: `{quality.get('publish_blocking_quality_issues', 0)}`
- interpretation: {quality.get('interpretation', '')}

## Upstream Supply

- hot_material_count: `{upstream.get('hot_material_count', 0)}`
- promote_to_topic_pipeline: `{upstream.get('promote_to_topic_pipeline', 0)}`
- backfill_required: `{upstream.get('backfill_required', 0)}`
- gate_status: `{upstream.get('gate_status', 'UNKNOWN')}`
- weak_supply_reasons: `{len(upstream.get('weak_supply_reasons', [])) if isinstance(upstream.get('weak_supply_reasons'), list) else 0}`
- interpretation: {upstream.get('interpretation', '')}

## Recommended Operator Flow

{flow}

## Acceptable Warnings

{warnings}

## True Blockers

{blockers}

## Manual Required Items

{manual}

## Safety Boundaries

- auto_publish: `false`
- wechat_api: `false`
- auto_image_generation: `false`
- auto_config_change: `false`
"""
