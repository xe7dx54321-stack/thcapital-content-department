from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.acquisition_playbook_runtime import build_runtime_acquisition_plan
from content_system.paths import get_project_paths


class AcquisitionPlaybookRuntimeTest(unittest.TestCase):
    def test_runtime_plan_and_offline_route_shape(self) -> None:
        payload, _ = build_runtime_acquisition_plan(get_project_paths(ROOT), ROOT)
        summary = payload["summary"]
        self.assertGreater(summary["lane_runs"], 0)
        self.assertGreater(summary["connector_runs"], 0)
        self.assertTrue(payload["policy"]["shared_connector_fetch_once"])


if __name__ == "__main__":
    unittest.main()
