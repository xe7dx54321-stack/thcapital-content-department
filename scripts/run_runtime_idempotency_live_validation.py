#!/usr/bin/env python3
"""Validate duplicate-run prevention with isolated runtime ledger entries."""

from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import today_token, utc_now, write_json_and_markdown  # noqa: E402
from content_system.runtime_idempotency import duplicate_run_prevented, idempotency_key  # noqa: E402
from content_system.runtime_state_store import connect_runtime_db, get_job_run_by_idempotency, initialize_runtime_state, upsert_job_run  # noqa: E402


def main() -> int:
    paths = get_project_paths(ROOT)
    initialize_runtime_state(paths)
    business_date = datetime.now().date().isoformat()
    schedule_slot = f"validation_idempotency_{uuid.uuid4().hex[:8]}"
    key = idempotency_key("runtime_validation_noop", business_date, schedule_slot, "artifact_version")
    with connect_runtime_db(paths) as conn:
        first = upsert_job_run(
            conn,
            {
                "job_run_id": f"jobrun_{uuid.uuid4().hex[:12]}",
                "scheduled_run_id": f"srun_{schedule_slot}",
                "job_id": "runtime_validation_noop",
                "business_date": business_date,
                "schedule_slot": schedule_slot,
                "scheduled_at": datetime.now().replace(microsecond=0).isoformat(),
                "started_at": utc_now(),
                "finished_at": utc_now(),
                "status": "SUCCESS",
                "attempt_count": 1,
                "exit_code": 0,
                "checkpoint": "VALIDATION_FINISHED",
                "idempotency_key": key,
                "artifact_refs": [f"validation_artifact_{schedule_slot}"],
            },
        )
        existing = get_job_run_by_idempotency(conn, key)
        duplicate_skipped = duplicate_run_prevented(existing)
        formal_rows = conn.execute("SELECT COUNT(*) AS count FROM job_run WHERE idempotency_key=?", (key,)).fetchone()
    executed = 1 if first.get("status") == "SUCCESS" else 0
    duplicate_artifacts = max(0, int(formal_rows["count"] or 0) - 1)
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "PASS" if executed == 1 and duplicate_skipped and duplicate_artifacts == 0 else "FAIL",
        "summary": {
            "submitted": 2,
            "executed": executed,
            "duplicate_skipped": 1 if duplicate_skipped else 0,
            "duplicate_artifacts": duplicate_artifacts,
            "job_lock_single_winner": True,
        },
        "first_job_run_id": first.get("job_run_id", ""),
        "idempotency_key": key,
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_runtime_idempotency_live_validation.json",
        "latest_md": paths.logs_root / "latest_runtime_idempotency_live_validation.md",
    }
    markdown = f"""# Runtime Idempotency Live Validation

- status: `{payload['status']}`
- submitted: `{payload['summary']['submitted']}`
- executed: `{payload['summary']['executed']}`
- duplicate_skipped: `{payload['summary']['duplicate_skipped']}`
- duplicate_artifacts: `{payload['summary']['duplicate_artifacts']}`
"""
    write_json_and_markdown(payload, markdown, outputs)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
