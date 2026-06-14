import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from content_system.workbench_view_model import build_workbench_view_model_from_data
from workbench_vm_fixture import sample_workbench_data


class WorkbenchReplayDashboardTest(unittest.TestCase):
    def test_replay_does_not_pollute_today_article(self):
        vm = build_workbench_view_model_from_data(sample_workbench_data(), {})
        self.assertIn("days", vm["replay_dashboard"])
        self.assertNotIn("days", vm["today_article"])
        self.assertTrue(vm["replay_dashboard"]["policy"]["replay_is_not_production"])

    def test_calibration_proposals_never_auto_apply(self):
        proposals = build_workbench_view_model_from_data(sample_workbench_data(), {})["replay_dashboard"]["calibration_proposals"]
        self.assertTrue(proposals)
        self.assertTrue(all(item["auto_apply"] is False for item in proposals))
        self.assertTrue(all(item["requires_human_approval"] is True for item in proposals))


if __name__ == "__main__":
    unittest.main()
