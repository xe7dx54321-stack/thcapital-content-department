#!/usr/bin/env python3
"""Run the Phase 26 daily upstream acquisition pipeline."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase26-daily-acquisition-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase26-daily-acquisition-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase26_daily_acquisition_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase26_daily_acquisition_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase26-daily-acquisition-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase26_daily_acquisition_pipeline_board.md",
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
    weak = "\n".join(f"- {item}" for item in summary.get("weak_supply_reasons", [])) or "- None."
    return f"""# Phase 26 Daily Acquisition Pipeline

## Summary

- status: `{payload.get('status')}`
- gate_status: `{summary.get('gate_status')}`
- hot_material_count: `{summary.get('hot_material_count')}`
- promote_to_topic_pipeline: `{summary.get('promote_to_topic_pipeline')}`
- backfill_required: `{summary.get('backfill_required')}`
- source_gap_count: `{summary.get('source_gap_count')}`
- stable_daily_ops_status: `{summary.get('stable_daily_ops_status')}`

## Weak Supply Reasons

{weak}

## Steps

{rows}

## Safety

- no_auto_publish: `true`
- no_wechat_api: `true`
- no_auto_image_generation: `true`
- no_external_login_or_paid_bypass: `true`
- no_sources_yaml_mutation: `true`
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [
        ("source_coverage_gap_audit", python_command("scripts/build_source_coverage_gap_audit.py")),
        ("high_value_source_expansion_plan", python_command("scripts/build_high_value_source_expansion_plan.py")),
        ("hot_signal_capture", python_command("scripts/build_hot_signal_capture.py")),
        ("fallback_backfill_queue", python_command("scripts/build_fallback_backfill_queue.py")),
        ("daily_hot_material_pool", python_command("scripts/build_daily_hot_material_pool.py")),
        ("hot_material_quality_gate", python_command("scripts/run_hot_material_quality_gate.py")),
        ("stable_daily_ops", python_command("scripts/run_stable_daily_ops.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, ROOT) for name, command in commands]
    failed = [step for step in steps if step.returncode != 0]
    audit = read_json(paths.logs_root / "latest_source_coverage_gap_audit.json")
    pool = read_json(paths.market_content_root / "03_topic_candidates" / "latest_daily_hot_material_pool.json")
    gate = read_json(paths.logs_root / "latest_hot_material_quality_gate.json")
    stable = read_json(paths.logs_root / "latest_stable_daily_ops.json")
    audit_summary = audit.get("summary") if isinstance(audit.get("summary"), dict) else {}
    pool_summary = pool.get("summary") if isinstance(pool.get("summary"), dict) else {}
    gate_summary = gate.get("summary") if isinstance(gate.get("summary"), dict) else {}
    gate_status = gate.get("gate_status", "UNKNOWN")
    if failed:
        status = "FAILED"
    elif gate_status == "BLOCKED":
        status = "DEGRADED"
    elif gate_status == "WEAK_SUPPLY":
        status = "WEAK_SUPPLY"
    elif gate_status in {"PASS", "ACTIONABLE"}:
        status = "SUCCESS" if stable.get("status") == "SUCCESS" and gate_status == "PASS" else "ACTIONABLE"
    else:
        status = "ACTIONABLE"
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "steps": [step_payload(step) for step in steps],
        "summary": {
            "source_gap_count": audit_summary.get("gap_count", 0),
            "source_gap_high_severity": audit_summary.get("high_severity", 0),
            "hot_material_count": pool_summary.get("material_count", 0),
            "write_now": pool_summary.get("write_now", 0),
            "develop_topic": pool_summary.get("develop_topic", 0),
            "backfill_first": pool_summary.get("backfill_first", 0),
            "gate_status": gate_status,
            "promote_to_topic_pipeline": gate_summary.get("promote_to_topic_pipeline", 0),
            "watch": gate_summary.get("watch", 0),
            "backfill_required": gate_summary.get("backfill_required", 0),
            "reject": gate_summary.get("reject", 0),
            "weak_supply_reasons": gate_summary.get("weak_supply_reasons", []),
            "stable_daily_ops_status": stable.get("status", "UNKNOWN"),
            "sidecar_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_sources_yaml_mutation": True,
        },
        "notes": [
            "Phase 26 reinforces upstream intelligence acquisition as diagnosis and scheduling.",
            "The pipeline does not fetch paid/login sources, mutate config/sources.yaml, publish, or generate images.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 26 Daily Acquisition Pipeline")
    print("===================================")
    print(f"status: {status}")
    for key, value in payload["summary"].items():
        print(f"{key}: {value}")
    print("Steps:")
    for step in steps:
        print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if status in {"SUCCESS", "ACTIONABLE", "WEAK_SUPPLY", "DEGRADED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
