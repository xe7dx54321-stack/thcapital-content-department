#!/usr/bin/env python3
"""Run Phase 16 daily live pilot pipeline."""

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
from content_system.phase7_report_utils import list_payload, python_command, read_json, run_step, safe_int, today_token, utc_now, write_json_and_markdown  # noqa: E402


SCHEMA_VERSION = "v1"


def output_paths(run_date: str) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    return {
        "dated_json": paths.logs_root / f"{run_date}__phase16-daily-live-pilot-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase16-daily-live-pilot-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase16_daily_live_pilot_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase16_daily_live_pilot_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase16-daily-live-pilot-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase16_daily_live_pilot_pipeline_board.md",
    }


def latest_payloads(paths) -> dict[str, dict[str, Any]]:
    return {
        "brief": read_json(paths.market_content_root / "05_draft_packs" / "latest_live_methodology_brief_pilot.json"),
        "draft": read_json(paths.market_content_root / "05_draft_packs" / "latest_live_methodology_draft_pilot.json"),
        "rewrite": read_json(paths.market_content_root / "09_workbench_actions" / "versions" / "latest_live_methodology_rewrite_pilot.json"),
        "visual": read_json(paths.market_content_root / "05_draft_packs" / "latest_live_visual_prompt_pilot.json"),
        "comparison": read_json(paths.logs_root / "latest_live_output_quality_comparison.json"),
        "calibration": read_json(paths.logs_root / "latest_live_calibration_feedback.json"),
        "approval": read_json(paths.market_content_root / "05_draft_packs" / "latest_image_generation_approval_queue.json"),
        "phase15": read_json(paths.logs_root / "latest_phase15_daily_generation_pipeline.json"),
    }


def build_summary(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    comparison_summary = payloads["comparison"].get("summary") if isinstance(payloads["comparison"].get("summary"), dict) else {}
    approval_summary = payloads["approval"].get("summary") if isinstance(payloads["approval"].get("summary"), dict) else {}
    calibration_summary = payloads["calibration"].get("summary") if isinstance(payloads["calibration"].get("summary"), dict) else {}
    return {
        "phase15_status": payloads["phase15"].get("status") or payloads["phase15"].get("summary", {}).get("status") or "UNKNOWN",
        "live_brief_count": safe_int((payloads["brief"].get("summary") or {}).get("brief_count")) if isinstance(payloads["brief"].get("summary"), dict) else 0,
        "live_draft_count": safe_int((payloads["draft"].get("summary") or {}).get("draft_count")) if isinstance(payloads["draft"].get("summary"), dict) else 0,
        "live_rewrite_count": safe_int((payloads["rewrite"].get("summary") or {}).get("rewrite_count")) if isinstance(payloads["rewrite"].get("summary"), dict) else 0,
        "live_visual_prompt_count": safe_int((payloads["visual"].get("summary") or {}).get("visual_prompt_count")) if isinstance(payloads["visual"].get("summary"), dict) else 0,
        "comparison_count": safe_int(comparison_summary.get("comparison_count")),
        "live_calibration_feedback_count": safe_int(calibration_summary.get("feedback_count")),
        "image_approval_request_count": safe_int(approval_summary.get("request_count")),
        "image_approval_pending": safe_int(approval_summary.get("pending")),
        "live_attempted_count": sum(1 for key in ("brief", "draft", "rewrite", "visual") if (payloads[key].get("summary") or {}).get("live_attempted")),
        "live_succeeded_count": sum(1 for key in ("brief", "draft", "rewrite", "visual") if (payloads[key].get("summary") or {}).get("live_succeeded")),
        "do_not_auto_generate_images": True,
        "do_not_auto_publish": True,
        "sidecar_only": True,
        "auto_apply": False,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    step_rows = "\n".join(
        f"| {item.get('name')} | {item.get('status')} | {item.get('returncode')} |"
        for item in payload.get("steps", [])
    )
    return f"""# Phase 16 Daily Live Pilot Pipeline

## Summary

- status: `{payload.get('status')}`
- phase15_status: `{summary.get('phase15_status')}`
- live_brief_count: `{summary.get('live_brief_count')}`
- live_draft_count: `{summary.get('live_draft_count')}`
- live_rewrite_count: `{summary.get('live_rewrite_count')}`
- live_visual_prompt_count: `{summary.get('live_visual_prompt_count')}`
- comparison_count: `{summary.get('comparison_count')}`
- image_approval_request_count: `{summary.get('image_approval_request_count')}`
- live_attempted_count: `{summary.get('live_attempted_count')}`
- live_succeeded_count: `{summary.get('live_succeeded_count')}`
- do_not_auto_generate_images: `true`
- do_not_auto_publish: `true`
- sidecar_only: `true`

## Steps

| Step | Status | Return code |
|---|---|---:|
{step_rows}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 16 daily live pilot pipeline.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    run_date = today_token()
    commands = [
        ("phase15_daily", python_command("scripts/run_phase15_daily_generation_pipeline.py")),
        ("live_methodology_brief", python_command("scripts/run_live_methodology_brief_pilot.py", "--limit", "1")),
        ("live_methodology_draft", python_command("scripts/run_live_methodology_draft_pilot.py", "--limit", "1")),
        ("live_methodology_rewrite", python_command("scripts/run_live_methodology_rewrite_pilot.py", "--limit", "1")),
        ("live_visual_prompt", python_command("scripts/run_live_visual_prompt_pilot.py", "--limit", "3")),
        ("live_output_comparison", python_command("scripts/compare_live_outputs.py")),
        ("live_calibration_board", python_command("scripts/build_live_calibration_board.py")),
        ("image_generation_approval_queue", python_command("scripts/build_image_generation_approval_queue.py")),
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
        "policy": {"dry_run_default": True, "sidecar_only": True, "no_auto_publish": True, "no_auto_image_generation": True, "auto_apply": False},
    }
    outputs = output_paths(run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {k: str(v) for k, v in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Phase 16 Daily Live Pilot Pipeline")
        print("==================================")
        print(f"status: {status}")
        for key, value in summary.items():
            print(f"{key}: {value}")
        print("Steps:")
        for step in steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if all(step.returncode == 0 for step in steps) else 1


if __name__ == "__main__":
    raise SystemExit(main())
