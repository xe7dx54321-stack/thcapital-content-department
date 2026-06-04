#!/usr/bin/env python3
"""Run Phase 18 daily publishing pack pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import python_command, read_json, run_step, safe_int, today_token, utc_now, write_json_and_markdown  # noqa: E402


SCHEMA_VERSION = "v1"


def output_paths(run_date: str) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    return {
        "dated_json": paths.logs_root / f"{run_date}__phase18-daily-publishing-pack-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase18-daily-publishing-pack-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase18_daily_publishing_pack_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase18_daily_publishing_pack_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase18-daily-publishing-pack-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase18_daily_publishing_pack_pipeline_board.md",
    }


def latest_payloads(paths) -> dict[str, dict[str, Any]]:
    publishing_root = paths.market_content_root / "07_publishing"
    return {
        "phase17": read_json(paths.logs_root / "latest_phase17_daily_visual_production_pipeline.json"),
        "visual_candidates": read_json(publishing_root / "latest_visual_approved_final_candidates.json"),
        "copy_packs": read_json(publishing_root / "latest_wechat_copy_pack_with_images.json"),
        "visual_checklists": read_json(publishing_root / "latest_visual_publishing_checklist.json"),
        "visual_performance": read_json(publishing_root / "latest_post_publish_visual_performance.json"),
        "visual_feedback": read_json(paths.logs_root / "latest_visual_strategy_learning_feedback.json"),
    }


def build_summary(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    candidate_summary = payloads["visual_candidates"].get("summary") if isinstance(payloads["visual_candidates"].get("summary"), dict) else {}
    pack_summary = payloads["copy_packs"].get("summary") if isinstance(payloads["copy_packs"].get("summary"), dict) else {}
    checklist_summary = payloads["visual_checklists"].get("summary") if isinstance(payloads["visual_checklists"].get("summary"), dict) else {}
    performance_summary = payloads["visual_performance"].get("summary") if isinstance(payloads["visual_performance"].get("summary"), dict) else {}
    feedback_summary = payloads["visual_feedback"].get("summary") if isinstance(payloads["visual_feedback"].get("summary"), dict) else {}
    return {
        "phase17_status": payloads["phase17"].get("status") or "UNKNOWN",
        "visual_candidate_count": safe_int(candidate_summary.get("candidate_count")),
        "visual_ready": safe_int(candidate_summary.get("visual_ready")),
        "copy_pack_count": safe_int(pack_summary.get("pack_count")),
        "ready_for_manual_copy": safe_int(pack_summary.get("ready_for_manual_copy")),
        "visual_checklist_count": safe_int(checklist_summary.get("checklist_count")),
        "checklist_ready": safe_int(checklist_summary.get("ready")),
        "visual_performance_record_count": safe_int(performance_summary.get("record_count")),
        "visual_feedback_recommendation_count": safe_int(feedback_summary.get("recommendation_count")),
        "no_auto_publish": True,
        "no_wechat_api": True,
        "no_auto_image_generation": True,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(f"| {item.get('name')} | {item.get('status')} | {item.get('returncode')} |" for item in payload.get("steps", []))
    return f"""# Phase 18 Daily Publishing Pack Pipeline

## Summary

- status: `{payload.get('status')}`
- phase17_status: `{summary.get('phase17_status')}`
- visual_candidate_count: `{summary.get('visual_candidate_count')}`
- visual_ready: `{summary.get('visual_ready')}`
- copy_pack_count: `{summary.get('copy_pack_count')}`
- ready_for_manual_copy: `{summary.get('ready_for_manual_copy')}`
- visual_checklist_count: `{summary.get('visual_checklist_count')}`
- checklist_ready: `{summary.get('checklist_ready')}`
- visual_performance_record_count: `{summary.get('visual_performance_record_count')}`
- visual_feedback_recommendation_count: `{summary.get('visual_feedback_recommendation_count')}`
- no_auto_publish: `true`
- no_wechat_api: `true`
- no_auto_image_generation: `true`

## Steps

| Step | Status | Return code |
|---|---|---:|
{rows}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 18 daily publishing pack pipeline.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    run_date = today_token()
    commands = [
        ("phase17_daily", python_command("scripts/run_phase17_daily_visual_production_pipeline.py")),
        ("visual_approved_final_candidates", python_command("scripts/build_visual_approved_final_candidates.py")),
        ("wechat_copy_pack_with_images", python_command("scripts/build_wechat_copy_pack_with_images.py")),
        ("visual_publishing_checklist", python_command("scripts/build_visual_publishing_checklist.py")),
        ("post_publish_visual_performance_board", python_command("scripts/build_post_publish_visual_performance_board.py")),
        ("visual_strategy_learning_feedback", python_command("scripts/build_visual_strategy_learning_feedback.py")),
        ("wechat_workbench_data", python_command("scripts/build_wechat_workbench_data.py")),
        ("wechat_workbench_frontend", python_command("scripts/build_wechat_workbench_frontend.py")),
    ]
    steps = [run_step(name, command, REPO_ROOT) for name, command in commands]
    payloads = latest_payloads(paths)
    summary = build_summary(payloads)
    status = "SUCCESS" if all(step.returncode == 0 for step in steps) else "DEGRADED"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": status,
        "summary": summary,
        "steps": [asdict(step) for step in steps],
        "policy": {
            "manual_copy_pack_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_image_generation": True,
            "no_visual_methodology_auto_apply": True,
        },
    }
    outputs = output_paths(run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(value) for key, value in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Phase 18 Daily Publishing Pack Pipeline")
        print("=======================================")
        print(f"status: {status}")
        for key, value in summary.items():
            print(f"{key}: {value}")
        print("Steps:")
        for step in steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if all(step.returncode == 0 for step in steps) else 1


if __name__ == "__main__":
    raise SystemExit(main())
