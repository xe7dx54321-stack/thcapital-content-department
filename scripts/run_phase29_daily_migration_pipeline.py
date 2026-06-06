#!/usr/bin/env python3
"""Run the Phase 29 OpenClaw source migration pipeline."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.phase7_report_utils import PipelineStep, python_command, read_json, repo_relative, run_step, today_token, utc_now, write_json_and_markdown


def output_paths(paths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__phase29-daily-migration-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase29-daily-migration-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase29_daily_migration_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase29_daily_migration_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase29-daily-migration-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase29_daily_migration_pipeline_board.md",
    }


def step_payload(step: PipelineStep) -> dict[str, Any]:
    return {
        "name": step.name,
        "command": step.command,
        "return_code": step.returncode,
        "status": step.status,
        "started_at": step.started_at,
        "finished_at": step.finished_at,
        "stdout_tail": step.stdout_tail,
        "stderr_tail": step.stderr_tail,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(f"- {step.get('name')}: {step.get('status')} ({step.get('return_code')})" for step in payload.get("steps", []))
    return f"""# Phase 29 Daily Migration Pipeline

## Summary

- status: `{payload.get('status')}`
- inventory_source_count: `{summary.get('inventory_source_count')}`
- migration_candidate_count: `{summary.get('migration_candidate_count')}`
- metadata_item_count: `{summary.get('metadata_item_count')}`
- weak_signal_item_count: `{summary.get('weak_signal_item_count')}`
- normalized_signal_count: `{summary.get('normalized_signal_count')}`
- openclaw_hot_material_count: `{summary.get('openclaw_hot_material_count')}`
- hard_evidence_allowed: `{summary.get('hard_evidence_allowed')}`
- stable_daily_ops_status: `{summary.get('stable_daily_ops_status')}`

## Steps

{rows}

## Safety

- no_auto_publish: `true`
- no_wechat_api: `true`
- no_auto_image_generation: `true`
- no_full_text: `true`
- no_login_or_paywall_bypass: `true`
- no_openclaw_gateway: `true`
- no_openclaw_cron_migration: `true`
- openclaw_signals_not_hard_evidence: `true`
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [
        ("openclaw_source_inventory", python_command("scripts/import_openclaw_source_inventory.py")),
        ("openclaw_source_risk_classification", python_command("scripts/classify_openclaw_source_risk.py")),
        ("openclaw_migration_plan", python_command("scripts/build_openclaw_migration_plan.py")),
        ("openclaw_metadata_connectors", python_command("scripts/run_openclaw_metadata_connectors.py")),
        ("weak_signal_safety_gate", python_command("scripts/run_weak_signal_safety_gate.py")),
        ("normalize_openclaw_signals", python_command("scripts/normalize_openclaw_signals.py")),
        ("daily_hot_material_pool", python_command("scripts/build_daily_hot_material_pool.py")),
        ("hot_material_quality_gate", python_command("scripts/run_hot_material_quality_gate.py")),
        ("stable_daily_ops", python_command("scripts/run_stable_daily_ops.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, ROOT) for name, command in commands]
    failed = [step for step in steps if step.returncode != 0]
    inventory = read_json(paths.logs_root / "latest_openclaw_source_inventory.json")
    risk = read_json(paths.logs_root / "latest_openclaw_source_risk_classification.json")
    plan = read_json(paths.logs_root / "latest_openclaw_migration_plan.json")
    connectors = read_json(paths.logs_root / "latest_openclaw_metadata_connector_run.json")
    weak_gate = read_json(paths.logs_root / "latest_weak_signal_safety_gate.json")
    normalized = read_json(paths.logs_root / "latest_normalized_openclaw_signals.json")
    pool = read_json(paths.market_content_root / "03_topic_candidates" / "latest_daily_hot_material_pool.json")
    stable = read_json(paths.logs_root / "latest_stable_daily_ops.json")
    inv_summary = inventory.get("summary") if isinstance(inventory.get("summary"), dict) else {}
    risk_summary = risk.get("summary") if isinstance(risk.get("summary"), dict) else {}
    plan_summary = plan.get("summary") if isinstance(plan.get("summary"), dict) else {}
    conn_summary = connectors.get("summary") if isinstance(connectors.get("summary"), dict) else {}
    weak_summary = weak_gate.get("summary") if isinstance(weak_gate.get("summary"), dict) else {}
    normalized_summary = normalized.get("summary") if isinstance(normalized.get("summary"), dict) else {}
    pool_summary = pool.get("summary") if isinstance(pool.get("summary"), dict) else {}
    hard_allowed = int(weak_summary.get("hard_evidence_allowed") or 0) + int(normalized_summary.get("hard_evidence_allowed") or 0)
    if failed:
        status = "FAILED"
    elif hard_allowed:
        status = "DEGRADED"
    elif weak_gate.get("gate_status") in {"ACTIONABLE", "WARN"} or int(risk_summary.get("blocked") or 0):
        status = "ACTIONABLE"
    elif stable.get("status") == "SUCCESS":
        status = "SUCCESS"
    else:
        status = "ACTIONABLE"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "steps": [step_payload(step) for step in steps],
        "summary": {
            "inventory_source_count": inv_summary.get("source_count", 0),
            "inventory_job_count": inv_summary.get("job_count", 0),
            "risk_blocked": risk_summary.get("blocked", 0),
            "migration_candidate_count": plan_summary.get("candidate_count", 0),
            "migration_p0": plan_summary.get("p0", 0),
            "migration_p1": plan_summary.get("p1", 0),
            "metadata_item_count": conn_summary.get("item_count", 0),
            "weak_signal_item_count": conn_summary.get("weak_signal_items", 0),
            "normalized_signal_count": normalized_summary.get("signal_count", 0),
            "openclaw_hot_material_count": pool_summary.get("openclaw_hot_material_count", 0),
            "hard_evidence_allowed": hard_allowed,
            "stable_daily_ops_status": stable.get("status", "UNKNOWN"),
            "sidecar_only": True,
        },
        "safety": {
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_full_text": True,
            "no_login_or_paywall_bypass": True,
            "no_openclaw_gateway": True,
            "no_openclaw_cron_migration": True,
            "no_config_prompt_rules_mutation": True,
            "openclaw_signals_not_hard_evidence": True,
        },
        "notes": [
            "Phase 29 imports OpenClaw source inventory and selected metadata/weak-signal sidecars.",
            "It does not migrate cron jobs, start the OpenClaw gateway, fetch full text, or publish.",
            "OpenClaw migrated signals default to weak/supporting use and require confirmation before content claims.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 29 Daily Migration Pipeline")
    print("=================================")
    print(f"status: {status}")
    for key, value in payload["summary"].items():
        print(f"{key}: {value}")
    print("Steps:")
    for step in steps:
        print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if status in {"SUCCESS", "ACTIONABLE", "DEGRADED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
