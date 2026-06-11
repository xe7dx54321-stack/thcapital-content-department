#!/usr/bin/env python3
"""Run the Phase 30 OpenClaw activation pipeline."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase30-daily-activation-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase30-daily-activation-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase30_daily_activation_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase30_daily_activation_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase30-daily-activation-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase30_daily_activation_pipeline_board.md",
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
    return f"""# Phase 30 Daily Activation Pipeline

## Summary

- status: `{payload.get('status')}`
- backfill_count: `{summary.get('backfill_count')}`
- ready_for_confirmation: `{summary.get('ready_for_confirmation')}`
- needs_primary_source: `{summary.get('needs_primary_source')}`
- needs_second_source: `{summary.get('needs_second_source')}`
- manual_review: `{summary.get('manual_review')}`
- activated_topic_count: `{summary.get('activated_topic_count')}`
- can_enter_brief_pipeline: `{summary.get('can_enter_brief_pipeline')}`
- regression_gate_status: `{summary.get('regression_gate_status')}`
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
- no_sources_yaml_mutation: `true`
- weak_signals_not_hard_evidence: `true`
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [
        ("phase29_daily", python_command("scripts/run_phase29_daily_migration_pipeline.py")),
        ("openclaw_signal_evidence_backfill", python_command("scripts/backfill_openclaw_signal_evidence.py")),
        ("weak_signal_confirmation_workflow", python_command("scripts/build_weak_signal_confirmation_workflow.py")),
        ("openclaw_topic_activation", python_command("scripts/activate_openclaw_migrated_topics.py")),
        ("openclaw_to_content_regression_gate", python_command("scripts/run_openclaw_to_content_regression_gate.py")),
        ("openclaw_source_registry_proposal", python_command("scripts/build_openclaw_source_registry_proposal.py")),
        ("stable_daily_ops", python_command("scripts/run_stable_daily_ops.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, ROOT) for name, command in commands]
    failed = [step for step in steps if step.returncode != 0]
    topic_root = paths.market_content_root / "03_topic_candidates"
    backfill = read_json(topic_root / "latest_openclaw_signal_evidence_backfill.json")
    workflow = read_json(paths.logs_root / "latest_weak_signal_confirmation_workflow.json")
    activation = read_json(topic_root / "latest_openclaw_activated_topic_candidates.json")
    regression = read_json(paths.logs_root / "latest_openclaw_to_content_regression_gate.json")
    proposal = read_json(paths.logs_root / "latest_openclaw_source_registry_proposal.json")
    stable = read_json(paths.logs_root / "latest_stable_daily_ops.json")
    backfill_summary = backfill.get("summary") if isinstance(backfill.get("summary"), dict) else {}
    workflow_summary = workflow.get("summary") if isinstance(workflow.get("summary"), dict) else {}
    activation_summary = activation.get("summary") if isinstance(activation.get("summary"), dict) else {}
    regression_summary = regression.get("summary") if isinstance(regression.get("summary"), dict) else {}
    proposal_summary = proposal.get("summary") if isinstance(proposal.get("summary"), dict) else {}
    if failed:
        status = "FAILED"
    elif regression.get("gate_status") == "BLOCKED":
        status = "DEGRADED"
    elif int(workflow_summary.get("needs_primary_source") or 0) or int(workflow_summary.get("needs_second_source") or 0) or int(workflow_summary.get("manual_review") or 0):
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
            "backfill_count": backfill_summary.get("backfill_count", 0),
            "ready_for_confirmation": backfill_summary.get("ready_for_confirmation", 0),
            "needs_primary_source": workflow_summary.get("needs_primary_source", 0),
            "needs_second_source": workflow_summary.get("needs_second_source", 0),
            "manual_review": workflow_summary.get("manual_review", 0),
            "activated_topic_count": activation_summary.get("activated", 0),
            "can_enter_brief_pipeline": activation_summary.get("can_enter_brief_pipeline", 0),
            "regression_gate_status": regression.get("gate_status", "UNKNOWN"),
            "regression_blocking_failures": regression_summary.get("blocking_failures", 0),
            "registry_proposal_count": proposal_summary.get("proposal_count", 0),
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
            "no_sources_yaml_mutation": True,
            "no_config_prompt_rules_mutation": True,
            "weak_signals_not_hard_evidence": True,
        },
        "notes": [
            "Phase 30 backfills confirmation tasks from OpenClaw migrated metadata.",
            "It does not fetch full text, use OpenClaw gateway, migrate cron jobs, or modify config/sources.yaml.",
            "Weak signals remain weak/supporting until confirmed by stronger evidence.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 30 Daily Activation Pipeline")
    print("==================================")
    print(f"status: {status}")
    for key, value in payload["summary"].items():
        print(f"{key}: {value}")
    print("Steps:")
    for step in steps:
        print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if status in {"SUCCESS", "ACTIONABLE", "DEGRADED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
