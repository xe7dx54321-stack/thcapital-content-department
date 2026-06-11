from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.runtime_config import validate_runtime_config


class RuntimeConfigTests(unittest.TestCase):
    def test_repo_runtime_config_validates(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        payload = validate_runtime_config(repo_root)
        self.assertEqual(payload["status"], "PASS", payload.get("errors"))
        self.assertGreaterEqual(payload["summary"]["job_count"], 1)

    def test_invalid_schedule_rejected(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config").mkdir()
            shutil.copy(repo_root / "config" / "runtime_jobs.yaml", root / "config" / "runtime_jobs.yaml")
            shutil.copy(repo_root / "config" / "runtime_policies.yaml", root / "config" / "runtime_policies.yaml")
            (root / "config" / "runtime_schedule.yaml").write_text(
                """
schema_version: v1
runtime:
  enabled: true
  timezone: system_local
  scheduler_tick_seconds: 30
  heartbeat_seconds: 60
  max_parallel_jobs: 2
  catchup_max_age_hours: 24
daily_schedule:
  bad_slot:
    enabled: true
    time: "25:99"
    jobs: [missing_job]
""",
                encoding="utf-8",
            )
            payload = validate_runtime_config(root)
            self.assertEqual(payload["status"], "FAIL")
            self.assertTrue(any("HH:MM" in error for error in payload["errors"]))


if __name__ == "__main__":
    unittest.main()
