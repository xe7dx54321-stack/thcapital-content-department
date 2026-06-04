#!/usr/bin/env python3
"""Run Phase 19 daily content ops pipeline."""

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
        "dated_json": paths.logs_root / f"{run_date}__phase19-daily-ops-pipeline.json",
        "dated_md": paths.logs_root / f"{run_date}__phase19-daily-ops-pipeline.md",
        "latest_json": paths.logs_root / "latest_phase19_daily_ops_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase19_daily_ops_pipeline.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__phase19-daily-ops-pipeline-board.md",
        "board_latest_md": paths.frontstage_root / "latest_phase19_daily_ops_pipeline_board.md",
    }


def latest_payloads(paths) -> dict[str, dict[str, Any]]:
    publishing_root = paths.market_content_root / "07_publishing"
    return {
        "phase18": read_json(paths.logs_root / "latest_phase18_daily_publishing_pack_pipeline.json"),
        "calendar": read_json(publishing_root / "latest_publishing_session_calendar.json"),
        "queue": read_json(publishing_root / "latest_content_queue_priority.json"),
        "rhythm": read_json(publishing_root / "latest_weekly_publishing_rhythm.json"),
        "archive": read_json(publishing_root / "published_article_archive.json"),
        "metrics_review": read_json(paths.logs_root / "latest_post_publish_metrics_review.json"),
        "closeout": read_json(paths.logs_root / "latest_content_ops_closeout.json"),
    }


def build_summary(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    calendar = payloads["calendar"].get("summary") if isinstance(payloads["calendar"].get("summary"), dict) else {}
    queue = payloads["queue"].get("summary") if isinstance(payloads["queue"].get("summary"), dict) else {}
    rhythm = payloads["rhythm"].get("summary") if isinstance(payloads["rhythm"].get("summary"), dict) else {}
    archive = payloads["archive"].get("summary") if isinstance(payloads["archive"].get("summary"), dict) else {}
    closeout = payloads["closeout"].get("summary") if isinstance(payloads["closeout"].get("summary"), dict) else {}
    return {
        "phase18_status": payloads["phase18"].get("status") or "UNKNOWN",
        "calendar_days": safe_int(calendar.get("calendar_days")),
        "planned_slots": safe_int(calendar.get("planned_slots")),
        "queue_items": safe_int(queue.get("item_count")),
        "queue_today": safe_int(queue.get("today")),
        "rhythm_ready_days": safe_int(rhythm.get("ready_days")),
        "published_article_count": safe_int(archive.get("published_count")),
        "ready_next_week_count": safe_int(closeout.get("ready_next_week_count")),
        "blocked_count": safe_int(closeout.get("blocked_count")),
        "no_auto_publish": True,
        "no_wechat_api": True,
        "manual_ops_only": True,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(f"| {item.get('name')} | {item.get('status')} | {item.get('returncode')} |" for item in payload.get("steps", []))
    return f"""# Phase 19 Daily Ops Pipeline

## Summary

- status: `{payload.get('status')}`
- phase18_status: `{summary.get('phase18_status')}`
- calendar_days: `{summary.get('calendar_days')}`
- planned_slots: `{summary.get('planned_slots')}`
- queue_items: `{summary.get('queue_items')}`
- queue_today: `{summary.get('queue_today')}`
- rhythm_ready_days: `{summary.get('rhythm_ready_days')}`
- published_article_count: `{summary.get('published_article_count')}`
- ready_next_week_count: `{summary.get('ready_next_week_count')}`
- blocked_count: `{summary.get('blocked_count')}`
- no_auto_publish: `true`
- no_wechat_api: `true`

## Steps

| Step | Status | Return code |
|---|---|---:|
{rows}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 19 daily ops pipeline.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    run_date = today_token()
    commands = [
        ("phase18_daily", python_command("scripts/run_phase18_daily_publishing_pack_pipeline.py")),
        ("publishing_session_calendar", python_command("scripts/build_publishing_session_calendar.py")),
        ("content_queue_priority", python_command("scripts/build_content_queue_priority_board.py")),
        ("weekly_publishing_rhythm", python_command("scripts/build_weekly_publishing_rhythm.py")),
        ("published_article_archive", python_command("scripts/update_published_article_archive.py")),
        ("published_article_archive_board", python_command("scripts/build_published_article_archive_board.py")),
        ("post_publish_metrics_review", python_command("scripts/build_post_publish_metrics_review_board.py")),
        ("content_ops_closeout", python_command("scripts/build_content_ops_closeout.py")),
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
            "manual_ops_only": True,
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_auto_session_creation": True,
            "no_auto_metrics_input": True,
            "no_strategy_auto_apply": True,
        },
    }
    outputs = output_paths(run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(value) for key, value in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Phase 19 Daily Ops Pipeline")
        print("===========================")
        print(f"status: {status}")
        for key, value in summary.items():
            print(f"{key}: {value}")
        print("Steps:")
        for step in steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
    return 0 if all(step.returncode == 0 for step in steps) else 1


if __name__ == "__main__":
    raise SystemExit(main())
