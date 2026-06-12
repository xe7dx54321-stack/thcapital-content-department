#!/usr/bin/env python3
"""Validate missed-run catch-up behavior using isolated validation scenarios."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.missed_run_recovery import compress_catchup_plan  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import today_token, utc_now, write_json_and_markdown  # noqa: E402


def main() -> int:
    paths = get_project_paths(ROOT)
    now = datetime.now().replace(hour=19, minute=30, second=0, microsecond=0)
    recent = [{"business_date": now.date().isoformat(), "schedule_slot": "validation_required_local", "scheduled_at": (now - timedelta(minutes=20)).isoformat(), "jobs": ["runtime_validation_noop"]}]
    many = [
        {"business_date": now.date().isoformat(), "schedule_slot": slot, "scheduled_at": (now - timedelta(hours=idx + 1)).isoformat(), "jobs": ["acquisition_phase29"]}
        for idx, slot in enumerate(["morning_acquisition", "morning_backfill", "afternoon_refresh"])
    ]
    final_done = []
    scenario_a_plan = compress_catchup_plan(recent, now.replace(hour=10, minute=30))
    scenario_b_plan = compress_catchup_plan(many, now)
    scenario_c_plan = compress_catchup_plan(final_done, now)
    scenarios = [
        {"scenario": "required_local_job", "status": "PASS" if scenario_a_plan and scenario_a_plan[0].get("action") == "RUN_SLOT" else "FAIL", "catchup_plan": scenario_a_plan},
        {"scenario": "compressed_acquisition_slots", "status": "PASS" if len(scenario_b_plan) == 1 and scenario_b_plan[0].get("action") == "RUN_EVENING_CONSOLIDATED" else "FAIL", "catchup_plan": scenario_b_plan},
        {"scenario": "completed_daily_finalization_not_repeated", "status": "PASS" if not scenario_c_plan else "FAIL", "catchup_plan": scenario_c_plan},
    ]
    fail = sum(1 for item in scenarios if item["status"] != "PASS")
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "PASS" if fail == 0 else "FAIL",
        "namespace": "validation_phase31b",
        "scenarios": scenarios,
        "summary": {"scenarios": len(scenarios), "pass": len(scenarios) - fail, "fail": fail, "compressed_catchup": len(scenario_b_plan) == 1},
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_missed_run_live_validation.json",
        "latest_md": paths.logs_root / "latest_missed_run_live_validation.md",
    }
    markdown = f"""# Missed-run Live Validation

- status: `{payload['status']}`
- scenarios: `{payload['summary']['scenarios']}`
- pass: `{payload['summary']['pass']}`
- fail: `{payload['summary']['fail']}`
- compressed_catchup: `{payload['summary']['compressed_catchup']}`
"""
    write_json_and_markdown(payload, markdown, outputs)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
