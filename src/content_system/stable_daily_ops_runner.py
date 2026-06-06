"""Run the simplified stable daily ops command."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.phase7_report_utils import PipelineStep, python_command, read_json, repo_relative, run_step, today_token, utc_now, write_json_and_markdown


def output_paths(logs_root: Path, frontstage_root: Path, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": logs_root / f"{run_date}__stable-daily-ops.json",
        "dated_md": logs_root / f"{run_date}__stable-daily-ops.md",
        "latest_json": logs_root / "latest_stable_daily_ops.json",
        "latest_md": logs_root / "latest_stable_daily_ops.md",
        "board_dated_md": frontstage_root / f"{run_date}__stable-daily-ops-board.md",
        "board_latest_md": frontstage_root / "latest_stable_daily_ops_board.md",
    }


def step_payload(step: PipelineStep) -> dict[str, Any]:
    return {
        "name": step.name,
        "command": step.command,
        "return_code": step.returncode,
        "status": step.status if step.returncode == 0 else "FAILED",
        "started_at": step.started_at,
        "finished_at": step.finished_at,
        "stdout_tail": step.stdout_tail,
        "stderr_tail": step.stderr_tail,
    }


def build_stable_daily_ops(repo_root: Path, logs_root: Path, frontstage_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    commands = [
        ("phase24_daily", python_command("scripts/run_phase24_daily_stable_trial_pipeline.py")),
        ("stable_daily_ops_baseline", python_command("scripts/build_stable_daily_ops_baseline.py")),
        ("operator_acceptance_checklist", python_command("scripts/build_operator_acceptance_checklist.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, repo_root) for name, command in commands]
    failed = [step for step in steps if step.returncode != 0]
    baseline = read_json(logs_root / "latest_stable_daily_ops_baseline.json")
    acceptance = read_json(logs_root / "latest_operator_acceptance_checklist.json")
    baseline_summary = baseline.get("summary") if isinstance(baseline.get("summary"), dict) else {}
    acceptance_summary = acceptance.get("operator_acceptance_summary") if isinstance(acceptance.get("operator_acceptance_summary"), dict) else {}
    baseline_upstream = baseline.get("upstream_supply") if isinstance(baseline.get("upstream_supply"), dict) else {}
    hot_gate = read_json(logs_root / "latest_hot_material_quality_gate.json")
    hot_pool = read_json(logs_root.parent / "03_topic_candidates" / "latest_daily_hot_material_pool.json")
    evidence = read_json(logs_root.parent / "03_topic_candidates" / "latest_connector_evidence_packets.json")
    promoted_topics = read_json(logs_root.parent / "03_topic_candidates" / "latest_connector_promoted_topic_candidates.json")
    acquisition_bridge = read_json(logs_root / "latest_acquisition_to_content_bridge.json")
    openclaw_inventory = read_json(logs_root / "latest_openclaw_source_inventory.json")
    openclaw_plan = read_json(logs_root / "latest_openclaw_migration_plan.json")
    openclaw_connectors = read_json(logs_root / "latest_openclaw_metadata_connector_run.json")
    weak_gate = read_json(logs_root / "latest_weak_signal_safety_gate.json")
    openclaw_signals = read_json(logs_root / "latest_normalized_openclaw_signals.json")
    hot_gate_summary = hot_gate.get("summary") if isinstance(hot_gate.get("summary"), dict) else {}
    hot_pool_summary = hot_pool.get("summary") if isinstance(hot_pool.get("summary"), dict) else {}
    evidence_summary = evidence.get("summary") if isinstance(evidence.get("summary"), dict) else {}
    promoted_summary = promoted_topics.get("summary") if isinstance(promoted_topics.get("summary"), dict) else {}
    bridge_summary = acquisition_bridge.get("summary") if isinstance(acquisition_bridge.get("summary"), dict) else {}
    inv_summary = openclaw_inventory.get("summary") if isinstance(openclaw_inventory.get("summary"), dict) else {}
    plan_summary = openclaw_plan.get("summary") if isinstance(openclaw_plan.get("summary"), dict) else {}
    conn_summary = openclaw_connectors.get("summary") if isinstance(openclaw_connectors.get("summary"), dict) else {}
    weak_summary = weak_gate.get("summary") if isinstance(weak_gate.get("summary"), dict) else {}
    signal_summary = openclaw_signals.get("summary") if isinstance(openclaw_signals.get("summary"), dict) else {}
    upstream_supply = {
        "hot_material_count": int(
            baseline_upstream.get("hot_material_count")
            if baseline_upstream.get("hot_material_count") is not None
            else hot_pool_summary.get("material_count") or 0
        ),
        "promote_to_topic_pipeline": int(
            baseline_upstream.get("promote_to_topic_pipeline")
            if baseline_upstream.get("promote_to_topic_pipeline") is not None
            else hot_gate_summary.get("promote_to_topic_pipeline") or 0
        ),
        "backfill_required": int(
            baseline_upstream.get("backfill_required")
            if baseline_upstream.get("backfill_required") is not None
            else hot_gate_summary.get("backfill_required") or 0
        ),
        "connector_item_count": int(
            baseline_upstream.get("connector_item_count")
            if baseline_upstream.get("connector_item_count") is not None
            else hot_pool_summary.get("connector_item_count") or 0
        ),
        "evidence_packet_count": int(
            baseline_upstream.get("evidence_packet_count")
            if baseline_upstream.get("evidence_packet_count") is not None
            else evidence_summary.get("packet_count") or 0
        ),
        "promoted_topic_count": int(
            baseline_upstream.get("promoted_topic_count")
            if baseline_upstream.get("promoted_topic_count") is not None
            else promoted_summary.get("promoted") or 0
        ),
        "ready_for_brief": int(
            baseline_upstream.get("ready_for_brief")
            if baseline_upstream.get("ready_for_brief") is not None
            else bridge_summary.get("ready_for_brief") or 0
        ),
        "needs_evidence": int(
            baseline_upstream.get("needs_evidence")
            if baseline_upstream.get("needs_evidence") is not None
            else bridge_summary.get("needs_evidence") or 0
        ),
        "gate_status": baseline_upstream.get("gate_status") or hot_gate.get("gate_status", "UNKNOWN"),
        "weak_supply_reasons": baseline_upstream.get("weak_supply_reasons")
        if isinstance(baseline_upstream.get("weak_supply_reasons"), list)
        else hot_gate_summary.get("weak_supply_reasons", []),
    }
    if upstream_supply["gate_status"] == "WEAK_SUPPLY":
        upstream_supply["status_label"] = "ACTIONABLE_WITH_UPSTREAM_WEAK_SUPPLY"
    elif upstream_supply["gate_status"] == "BLOCKED":
        upstream_supply["status_label"] = "UPSTREAM_BLOCKED"
    else:
        upstream_supply["status_label"] = upstream_supply["gate_status"]
    baseline_status = baseline.get("baseline_status", "UNKNOWN")
    acceptance_status = acceptance.get("acceptance_status", "UNKNOWN")
    baseline_acquisition = baseline.get("acquisition_to_content") if isinstance(baseline.get("acquisition_to_content"), dict) else {}
    acquisition_to_content = {
        "connector_topic_candidates": int(
            baseline_acquisition.get("connector_topic_candidates")
            if baseline_acquisition.get("connector_topic_candidates") is not None
            else promoted_summary.get("candidate_count") or 0
        ),
        "ready_for_brief": upstream_supply["ready_for_brief"],
        "needs_evidence": upstream_supply["needs_evidence"],
        "watch": int(
            baseline_acquisition.get("watch")
            if baseline_acquisition.get("watch") is not None
            else bridge_summary.get("watch") or 0
        ),
    }
    baseline_openclaw = baseline.get("openclaw_migration") if isinstance(baseline.get("openclaw_migration"), dict) else {}
    openclaw_migration = {
        "inventory_source_count": int(
            baseline_openclaw.get("inventory_source_count")
            if baseline_openclaw.get("inventory_source_count") is not None
            else inv_summary.get("source_count") or 0
        ),
        "migration_candidate_count": int(
            baseline_openclaw.get("migration_candidate_count")
            if baseline_openclaw.get("migration_candidate_count") is not None
            else plan_summary.get("candidate_count") or 0
        ),
        "metadata_item_count": int(
            baseline_openclaw.get("metadata_item_count")
            if baseline_openclaw.get("metadata_item_count") is not None
            else conn_summary.get("item_count") or 0
        ),
        "weak_signal_item_count": int(
            baseline_openclaw.get("weak_signal_item_count")
            if baseline_openclaw.get("weak_signal_item_count") is not None
            else conn_summary.get("weak_signal_items") or 0
        ),
        "openclaw_hot_material_count": int(
            baseline_openclaw.get("openclaw_hot_material_count")
            if baseline_openclaw.get("openclaw_hot_material_count") is not None
            else hot_pool_summary.get("openclaw_hot_material_count") or 0
        ),
        "blocked_source_count": int(
            baseline_openclaw.get("blocked_source_count")
            if baseline_openclaw.get("blocked_source_count") is not None
            else weak_summary.get("blocked") or 0
        ),
        "hard_evidence_allowed": int(
            baseline_openclaw.get("hard_evidence_allowed")
            if baseline_openclaw.get("hard_evidence_allowed") is not None
            else signal_summary.get("hard_evidence_allowed") or 0
        ),
    }
    blocking_issue_count = int(baseline_summary.get("blocking_issue_count") or 0)
    workbench_ready = (frontstage_root / "latest_wechat_workbench.html").exists()
    if failed:
        status = "FAILED"
    elif blocking_issue_count:
        status = "DEGRADED"
    elif upstream_supply["gate_status"] == "BLOCKED":
        status = "DEGRADED"
    elif upstream_supply["gate_status"] == "WEAK_SUPPLY":
        status = "ACTIONABLE"
    elif baseline_status == "READY_FOR_DAILY_OPS" and acceptance_status in {"ACCEPTABLE_FOR_DAILY_USE", "ACCEPTABLE_WITH_MANUAL_REVIEW"}:
        status = "SUCCESS"
    elif baseline_status in {"READY_FOR_DAILY_OPS", "ACTIONABLE_WITH_WARNINGS"}:
        status = "ACTIONABLE"
    else:
        status = "DEGRADED"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "steps": [step_payload(step) for step in steps],
        "daily_summary": {
            "baseline_status": baseline_status,
            "operator_acceptance_status": acceptance_status,
            "blocking_issue_count": blocking_issue_count,
            "manual_required": bool(acceptance_summary.get("manual_review_required", True)),
            "workbench_ready": workbench_ready,
            "acceptance_pass": acceptance_summary.get("pass", 0),
            "acceptance_warn": acceptance_summary.get("warn", 0),
            "acceptance_fail": acceptance_summary.get("fail", 0),
            "upstream_supply": upstream_supply,
            "acquisition_to_content": acquisition_to_content,
            "openclaw_migration": openclaw_migration,
        },
        "safety": {
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_auto_config_change": True,
            "no_mainline_overwrite": True,
        },
        "notes": [
            "stable-daily-ops is the simplified daily operator command.",
            "It does not publish, call WeChat API, generate images, mutate config, or overwrite mainline content.",
            "SUCCESS means the system baseline is usable; publishing still requires human review.",
            "Upstream WEAK_SUPPLY is actionable operator work, not an engineering failure.",
            "Connector evidence remains metadata-derived and requires human/source review before writing.",
            "OpenClaw migrated signals are weak/supporting signals by default and cannot be used as hard evidence.",
        ],
    }
    outputs = output_paths(logs_root, frontstage_root, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("daily_summary") if isinstance(payload.get("daily_summary"), dict) else {}
    upstream = summary.get("upstream_supply") if isinstance(summary.get("upstream_supply"), dict) else {}
    acquisition = summary.get("acquisition_to_content") if isinstance(summary.get("acquisition_to_content"), dict) else {}
    openclaw = summary.get("openclaw_migration") if isinstance(summary.get("openclaw_migration"), dict) else {}
    rows = "\n".join(
        f"- {step.get('name')}: {step.get('status')} ({step.get('return_code')})"
        for step in payload.get("steps", [])
    )
    return f"""# Stable Daily Ops

## Daily Summary

- status: `{payload.get('status')}`
- baseline_status: `{summary.get('baseline_status')}`
- operator_acceptance_status: `{summary.get('operator_acceptance_status')}`
- blocking_issue_count: `{summary.get('blocking_issue_count')}`
- manual_required: `{summary.get('manual_required')}`
- workbench_ready: `{summary.get('workbench_ready')}`
- upstream_gate_status: `{upstream.get('gate_status', 'UNKNOWN')}`
- upstream_status_label: `{upstream.get('status_label', 'UNKNOWN')}`
- hot_material_count: `{upstream.get('hot_material_count', 0)}`
- connector_item_count: `{upstream.get('connector_item_count', 0)}`
- evidence_packet_count: `{upstream.get('evidence_packet_count', 0)}`
- promoted_topic_count: `{upstream.get('promoted_topic_count', 0)}`
- ready_for_brief: `{upstream.get('ready_for_brief', 0)}`
- needs_evidence: `{upstream.get('needs_evidence', 0)}`
- promote_to_topic_pipeline: `{upstream.get('promote_to_topic_pipeline', 0)}`
- backfill_required: `{upstream.get('backfill_required', 0)}`

## Acquisition to Content

- connector_topic_candidates: `{acquisition.get('connector_topic_candidates', 0)}`
- ready_for_brief: `{acquisition.get('ready_for_brief', 0)}`
- needs_evidence: `{acquisition.get('needs_evidence', 0)}`
- watch: `{acquisition.get('watch', 0)}`

## OpenClaw Migration

- inventory_source_count: `{openclaw.get('inventory_source_count', 0)}`
- migration_candidate_count: `{openclaw.get('migration_candidate_count', 0)}`
- metadata_item_count: `{openclaw.get('metadata_item_count', 0)}`
- weak_signal_item_count: `{openclaw.get('weak_signal_item_count', 0)}`
- openclaw_hot_material_count: `{openclaw.get('openclaw_hot_material_count', 0)}`
- blocked_source_count: `{openclaw.get('blocked_source_count', 0)}`
- hard_evidence_allowed: `{openclaw.get('hard_evidence_allowed', 0)}`

## Steps

{rows}

## Safety

- no_auto_publish: `true`
- no_wechat_api: `true`
- no_auto_image_generation: `true`
- no_auto_config_change: `true`
- no_mainline_overwrite: `true`
"""
