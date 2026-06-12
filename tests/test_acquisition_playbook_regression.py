from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.acquisition_playbook_regression import run_acquisition_playbook_regression
from content_system.paths import get_project_paths


class AcquisitionPlaybookRegressionTest(unittest.TestCase):
    def test_regression_gate_passes_without_blockers(self) -> None:
        payload, _ = run_acquisition_playbook_regression(get_project_paths(ROOT), ROOT)
        self.assertEqual(payload["status"], "PASS")
        self.assertGreaterEqual(payload["coverage"]["coverage_ratio"], 0.8)
        self.assertEqual(payload["summary"]["blocking_failures"], 0)
        self.assertEqual(payload["duplicates"]["duplicate_connector_runs"], 0)


if __name__ == "__main__":
    unittest.main()
