#!/usr/bin/env python3
"""Run the Phase 27 selected source connector pipeline."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase27-daily-connector-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase27-daily-connector-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase27_daily_connector_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase27_daily_connector_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase27-daily-connector-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase27_daily_connector_pipeline_board.md",
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
    return f"""# Phase 27 Daily Connector Pipeline

## Summary

- status: `{payload.get('status')}`
- connector_gate_status: `{summary.get('connector_gate_status')}`
- selected_count: `{summary.get('selected_count')}`
- rss_item_count: `{summary.get('rss_item_count')}`
- research_item_count: `{summary.get('research_item_count')}`
- manual_ready_for_review: `{summary.get('manual_ready_for_review')}`
- normalized_item_count: `{summary.get('normalized_item_count')}`
- connector_promote_candidates: `{summary.get('connector_promote_candidates')}`
- hot_material_gate_status: `{summary.get('hot_material_gate_status')}`
- stable_daily_ops_status: `{summary.get('stable_daily_ops_status')}`

## Steps

{rows}

## Safety

- no_auto_publish: `true`
- no_wechat_api: `true`
- no_auto_image_generation: `true`
- no_login_or_paywall_bypass: `true`
- no_api_key: `true`
- no_full_text: `true`
- metadata_only: `true`
- no_sources_yaml_mutation: `true`
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [
        ("p0_source_connector_selection", python_command("scripts/build_p0_source_connector_selection.py")),
        ("rss_official_blog_connectors", python_command("scripts/run_rss_official_blog_connectors.py")),
        ("lightweight_research_connectors", python_command("scripts/run_lightweight_research_connectors.py")),
        ("manual_url_backfill_ingestion", python_command("scripts/run_manual_url_backfill_ingestion.py")),
        ("normalize_connector_outputs", python_command("scripts/normalize_connector_outputs.py")),
        ("connector_source_health_gate", python_command("scripts/run_connector_source_health_gate.py")),
        ("hot_signal_capture", python_command("scripts/build_hot_signal_capture.py")),
        ("daily_hot_material_pool", python_command("scripts/build_daily_hot_material_pool.py")),
        ("hot_material_quality_gate", python_command("scripts/run_hot_material_quality_gate.py")),
        ("stable_daily_ops", python_command("scripts/run_stable_daily_ops.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, ROOT) for name, command in commands]
    failed = [step for step in steps if step.returncode != 0]
    selection = read_json(paths.logs_root / "latest_p0_source_connector_selection.json")
    rss = read_json(paths.logs_root / "latest_rss_official_blog_connector_run.json")
    research = read_json(paths.logs_root / "latest_lightweight_research_connector_run.json")
    manual = read_json(paths.logs_root / "latest_manual_url_backfill_ingestion.json")
    normalized = read_json(paths.logs_root / "latest_normalized_upstream_items.json")
    connector_gate = read_json(paths.logs_root / "latest_connector_source_health_gate.json")
    pool = read_json(paths.market_content_root / "03_topic_candidates" / "latest_daily_hot_material_pool.json")
    hot_gate = read_json(paths.logs_root / "latest_hot_material_quality_gate.json")
    stable = read_json(paths.logs_root / "latest_stable_daily_ops.json")
    selection_summary = selection.get("summary") if isinstance(selection.get("summary"), dict) else {}
    rss_summary = rss.get("summary") if isinstance(rss.get("summary"), dict) else {}
    research_summary = research.get("summary") if isinstance(research.get("summary"), dict) else {}
    manual_summary = manual.get("summary") if isinstance(manual.get("summary"), dict) else {}
    normalized_summary = normalized.get("summary") if isinstance(normalized.get("summary"), dict) else {}
    connector_gate_summary = connector_gate.get("summary") if isinstance(connector_gate.get("summary"), dict) else {}
    pool_summary = pool.get("summary") if isinstance(pool.get("summary"), dict) else {}
    hot_gate_summary = hot_gate.get("summary") if isinstance(hot_gate.get("summary"), dict) else {}
    connector_gate_status = connector_gate.get("gate_status", "UNKNOWN")
    hot_gate_status = hot_gate.get("gate_status", "UNKNOWN")
    if failed:
        status = "FAILED"
    elif connector_gate_status == "BLOCKED" or hot_gate_status == "BLOCKED":
        status = "DEGRADED"
    elif connector_gate_status in {"DEGRADED", "ACTIONABLE"} or hot_gate_status in {"ACTIONABLE", "WEAK_SUPPLY"}:
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
            "selected_count": selection_summary.get("selected_count", 0),
            "rss_item_count": rss_summary.get("item_count", 0),
            "research_item_count": research_summary.get("item_count", 0),
            "manual_ready_for_review": manual_summary.get("ready_for_review", 0),
            "normalized_item_count": normalized_summary.get("item_count", 0),
            "connector_candidates": normalized_summary.get("candidate_for_hot_material_pool", 0),
            "connector_gate_status": connector_gate_status,
            "connector_gate_pass": connector_gate_summary.get("pass", 0),
            "connector_gate_warn": connector_gate_summary.get("warn", 0),
            "connector_gate_fail": connector_gate_summary.get("fail", 0),
            "healthy_connectors": connector_gate_summary.get("healthy_connectors", 0),
            "weak_connectors": connector_gate_summary.get("weak_connectors", 0),
            "failed_connectors": connector_gate_summary.get("failed_connectors", 0),
            "hot_material_count": pool_summary.get("material_count", 0),
            "connector_item_count": pool_summary.get("connector_item_count", 0),
            "connector_promote_candidates": pool_summary.get("connector_promote_candidates", 0),
            "hot_material_gate_status": hot_gate_status,
            "promote_to_topic_pipeline": hot_gate_summary.get("promote_to_topic_pipeline", 0),
            "backfill_required": hot_gate_summary.get("backfill_required", 0),
            "stable_daily_ops_status": stable.get("status", "UNKNOWN"),
            "sidecar_only": True,
            "metadata_only": True,
            "no_full_text": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_sources_yaml_mutation": True,
        },
        "notes": [
            "Phase 27 runs selected lightweight metadata connectors for P0 upstream sources.",
            "Connector failures are recorded in the health gate; no single public source failure crashes the content ops pipeline.",
            "The pipeline does not publish, call WeChat API, generate images, bypass login/paywalls, capture full text, or mutate config/sources.yaml.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 27 Daily Connector Pipeline")
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
