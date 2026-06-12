from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.autonomous_acquisition_validation import run_autonomous_acquisition_dry_run
from content_system.paths import get_project_paths


class AutonomousAcquisitionDryRunTest(unittest.TestCase):
    def test_dry_run_end_to_end(self) -> None:
        payload, _ = run_autonomous_acquisition_dry_run(get_project_paths(ROOT), ROOT)
        summary = payload["summary"]
        self.assertEqual(payload["status"], "SUCCESS")
        self.assertGreater(summary["scheduled_lane_runs"], 0)
        self.assertGreater(summary["downstream_routes"], 0)
        self.assertEqual(summary["failures"], 0)
        self.assertTrue(payload["policy"]["no_openclaw_mutation"])


if __name__ == "__main__":
    unittest.main()
