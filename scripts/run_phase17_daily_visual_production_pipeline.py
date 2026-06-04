#!/usr/bin/env python3
"""Run Phase 17 daily visual production pipeline."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase17-daily-visual-production-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase17-daily-visual-production-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase17_daily_visual_production_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase17_daily_visual_production_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase17-daily-visual-production-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase17_daily_visual_production_pipeline_board.md",
    }


def latest_payloads(paths) -> dict[str, dict[str, Any]]:
    draft_root = paths.market_content_root / "05_draft_packs"
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    assets_root = paths.market_content_root / "08_assets"
    return {
        "phase16": read_json(paths.logs_root / "latest_phase16_daily_live_pilot_pipeline.json"),
        "live_content_promotions": read_json(draft_root / "latest_promoted_live_content_candidates.json"),
        "live_rewrite_promotions": read_json(versions_root / "latest_promoted_live_rewrite_versions.json"),
        "image_tasks": read_json(assets_root / "latest_manual_image_generation_tasks.json"),
        "image_library": read_json(assets_root / "image_asset_library.json"),
        "article_with_images": read_json(paths.logs_root / "latest_article_with_images_preview.json"),
        "visual_review": read_json(assets_root / "latest_final_visual_review.json"),
    }


def build_summary(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    content_summary = payloads["live_content_promotions"].get("summary") if isinstance(payloads["live_content_promotions"].get("summary"), dict) else {}
    rewrite_summary = payloads["live_rewrite_promotions"].get("summary") if isinstance(payloads["live_rewrite_promotions"].get("summary"), dict) else {}
    task_summary = payloads["image_tasks"].get("summary") if isinstance(payloads["image_tasks"].get("summary"), dict) else {}
    asset_summary = payloads["image_library"].get("summary") if isinstance(payloads["image_library"].get("summary"), dict) else {}
    preview_summary = payloads["article_with_images"].get("summary") if isinstance(payloads["article_with_images"].get("summary"), dict) else {}
    review_summary = payloads["visual_review"].get("summary") if isinstance(payloads["visual_review"].get("summary"), dict) else {}
    return {
        "phase16_status": payloads["phase16"].get("status") or "UNKNOWN",
        "promoted_live_candidate_count": safe_int(content_summary.get("candidate_count")),
        "promoted_live_rewrite_count": safe_int(rewrite_summary.get("promoted")),
        "manual_image_task_count": safe_int(task_summary.get("task_count")),
        "image_asset_count": safe_int(asset_summary.get("asset_count")),
        "image_asset_available": safe_int(asset_summary.get("available")),
        "article_visual_slot_count": safe_int(preview_summary.get("visual_slot_count")),
        "visual_review_count": safe_int(review_summary.get("review_count")),
        "visual_wechat_ready": safe_int(review_summary.get("wechat_ready")),
        "no_auto_image_generation": True,
        "no_auto_publish": True,
        "sidecar_only": True,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    step_rows = "\n".join(f"| {item.get('name')} | {item.get('status')} | {item.get('returncode')} |" for item in payload.get("steps", []))
    return f"""# Phase 17 Daily Visual Production Pipeline

## Summary

- status: `{payload.get('status')}`
- phase16_status: `{summary.get('phase16_status')}`
- promoted_live_candidate_count: `{summary.get('promoted_live_candidate_count')}`
- promoted_live_rewrite_count: `{summary.get('promoted_live_rewrite_count')}`
- manual_image_task_count: `{summary.get('manual_image_task_count')}`
- image_asset_count: `{summary.get('image_asset_count')}`
- image_asset_available: `{summary.get('image_asset_available')}`
- article_visual_slot_count: `{summary.get('article_visual_slot_count')}`
- visual_review_count: `{summary.get('visual_review_count')}`
- visual_wechat_ready: `{summary.get('visual_wechat_ready')}`
- no_auto_image_generation: `true`
- no_auto_publish: `true`
- sidecar_only: `true`

## Steps

| Step | Status | Return code |
|---|---|---:|
{step_rows}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 17 daily visual production pipeline.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    run_date = today_token()
    commands = [
        ("phase16_daily", python_command("scripts/run_phase16_daily_live_pilot_pipeline.py")),
        ("promote_approved_live_outputs", python_command("scripts/promote_approved_live_outputs.py")),
        ("promote_live_rewrite_versions", python_command("scripts/promote_live_rewrite_versions.py")),
        ("manual_image_generation_tasks", python_command("scripts/build_manual_image_generation_tasks.py")),
        ("image_asset_library", python_command("scripts/update_image_asset_library.py")),
        ("image_asset_library_board", python_command("scripts/build_image_asset_library_board.py")),
        ("article_with_images_preview", python_command("scripts/build_article_with_images_preview.py")),
        ("final_visual_review", python_command("scripts/build_final_visual_review.py")),
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
            "no_auto_image_generation": True,
            "no_image_model_called": True,
            "no_auto_publish": True,
            "sidecar_only": True,
            "no_mainline_replacement": True,
        },
    }
    outputs = output_paths(run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(value) for key, value in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Phase 17 Daily Visual Production Pipeline")
        print("=========================================")
        print(f"status: {status}")
        for key, value in summary.items():
            print(f"{key}: {value}")
        print("Steps:")
        for step in steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if all(step.returncode == 0 for step in steps) else 1


if __name__ == "__main__":
    raise SystemExit(main())
