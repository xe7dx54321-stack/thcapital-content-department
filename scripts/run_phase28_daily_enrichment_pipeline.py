#!/usr/bin/env python3
"""Run the Phase 28 source enrichment and acquisition-to-content pipeline."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase28-daily-enrichment-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase28-daily-enrichment-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase28_daily_enrichment_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase28_daily_enrichment_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase28-daily-enrichment-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase28_daily_enrichment_pipeline_board.md",
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
    return f"""# Phase 28 Daily Enrichment Pipeline

## Summary

- status: `{payload.get('status')}`
- reliability_issues: `{summary.get('reliability_issues')}`
- evidence_packet_count: `{summary.get('evidence_packet_count')}`
- eligible_for_topic_promotion: `{summary.get('eligible_for_topic_promotion')}`
- promoted_topic_count: `{summary.get('promoted_topic_count')}`
- needs_evidence: `{summary.get('needs_evidence')}`
- regression_status: `{summary.get('regression_status')}`
- ready_for_brief: `{summary.get('ready_for_brief')}`
- stable_daily_ops_status: `{summary.get('stable_daily_ops_status')}`

## Steps

{rows}

## Safety

- no_auto_publish: `true`
- no_wechat_api: `true`
- no_auto_image_generation: `true`
- no_full_text: `true`
- no_login_or_paywall_bypass: `true`
- no_config_prompt_rules_mutation: `true`
- no_openclaw_migration: `true`
"""


def main() -> int:
    paths = get_project_paths(ROOT)
    run_date = today_token()
    commands = [
        ("phase27_daily_connector_pipeline", python_command("scripts/run_phase27_daily_connector_pipeline.py")),
        ("connector_reliability_improvement", python_command("scripts/improve_p0_connector_reliability.py")),
        ("connector_evidence_enrichment", python_command("scripts/enrich_evidence_from_connector_items.py")),
        ("promote_hot_materials_to_topics", python_command("scripts/promote_hot_materials_to_topics.py")),
        ("connector_freshness_dedup_regression", python_command("scripts/run_connector_freshness_dedup_regression.py")),
        ("acquisition_to_content_bridge", python_command("scripts/build_acquisition_to_content_bridge.py")),
        ("stable_daily_ops", python_command("scripts/run_stable_daily_ops.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, ROOT) for name, command in commands]
    failed = [step for step in steps if step.returncode != 0]

    reliability = read_json(paths.logs_root / "latest_connector_reliability_improvement.json")
    evidence = read_json(paths.market_content_root / "03_topic_candidates" / "latest_connector_evidence_packets.json")
    promoted = read_json(paths.market_content_root / "03_topic_candidates" / "latest_connector_promoted_topic_candidates.json")
    regression = read_json(paths.logs_root / "latest_connector_freshness_dedup_regression.json")
    bridge = read_json(paths.logs_root / "latest_acquisition_to_content_bridge.json")
    stable = read_json(paths.logs_root / "latest_stable_daily_ops.json")

    reliability_summary = reliability.get("reliability_summary") if isinstance(reliability.get("reliability_summary"), dict) else {}
    evidence_summary = evidence.get("summary") if isinstance(evidence.get("summary"), dict) else {}
    promoted_summary = promoted.get("summary") if isinstance(promoted.get("summary"), dict) else {}
    bridge_summary = bridge.get("summary") if isinstance(bridge.get("summary"), dict) else {}
    regression_status = regression.get("regression_status", "UNKNOWN")
    issue_count = int(reliability_summary.get("issue_count") or 0)
    needs_evidence = int(promoted_summary.get("needs_evidence") or 0)
    ready_for_brief = int(bridge_summary.get("ready_for_brief") or 0)
    if failed:
        status = "FAILED"
    elif regression_status == "FAIL":
        status = "DEGRADED"
    elif issue_count or needs_evidence or regression_status == "WARN":
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
            "reliability_issues": issue_count,
            "reliability_high": reliability_summary.get("high", 0),
            "reliability_requires_manual": reliability_summary.get("requires_manual", 0),
            "evidence_packet_count": evidence_summary.get("packet_count", 0),
            "eligible_for_topic_promotion": evidence_summary.get("eligible_for_topic_promotion", 0),
            "promoted_topic_count": promoted_summary.get("promoted", 0),
            "needs_evidence": needs_evidence,
            "watch": promoted_summary.get("watch", 0),
            "regression_status": regression_status,
            "ready_for_brief": ready_for_brief,
            "bridge_item_count": bridge_summary.get("bridge_item_count", 0),
            "stable_daily_ops_status": stable.get("status", "UNKNOWN"),
            "sidecar_only": True,
            "metadata_derived_evidence_only": True,
            "no_openclaw_migration": True,
        },
        "safety": {
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_full_text": True,
            "no_login_or_paywall_bypass": True,
            "no_config_prompt_rules_mutation": True,
            "no_openclaw_migration": True,
        },
        "notes": [
            "Phase 28 enriches Phase 27 connector metadata into evidence packets and promoted topic candidates.",
            "Evidence remains metadata-derived; this pipeline does not fetch full text or perform automatic fact verification.",
            "OpenClaw source migration is intentionally deferred to Phase 29.",
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, ROOT) for key, path in outputs.items()}
    print("Phase 28 Daily Enrichment Pipeline")
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
