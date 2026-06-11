from __future__ import annotations

import os
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.missed_run_recovery import compress_catchup_plan, detect_missed_runs
from content_system.paths import get_project_paths


class RuntimeMissedRunTests(unittest.TestCase):
    def test_catchup_compression(self) -> None:
        missed = [
            {"business_date": "2026-06-11", "schedule_slot": "morning_acquisition"},
            {"business_date": "2026-06-11", "schedule_slot": "afternoon_refresh"},
        ]
        plan = compress_catchup_plan(missed, datetime(2026, 6, 11, 19, 30))
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0]["action"], "RUN_EVENING_CONSOLIDATED")

    def test_detect_missed_runs(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            old = os.environ.get("THCAP_AUTONOMOUS_RUNTIME_DB")
            os.environ["THCAP_AUTONOMOUS_RUNTIME_DB"] = str(Path(tmp) / "runtime.sqlite")
            try:
                payload = detect_missed_runs(repo_root, get_project_paths(repo_root), datetime(2026, 6, 11, 19, 30))
            finally:
                if old is None:
                    os.environ.pop("THCAP_AUTONOMOUS_RUNTIME_DB", None)
                else:
                    os.environ["THCAP_AUTONOMOUS_RUNTIME_DB"] = old
            self.assertGreaterEqual(payload["summary"]["missed_count"], 1)


if __name__ == "__main__":
    unittest.main()
