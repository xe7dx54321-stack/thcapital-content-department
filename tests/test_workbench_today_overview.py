import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from content_system.workbench_view_model import build_workbench_view_model_from_data
from workbench_vm_fixture import sample_workbench_data


class WorkbenchTodayOverviewTest(unittest.TestCase):
    def test_ready_to_review_when_candidate_and_quality_pass(self):
        vm = build_workbench_view_model_from_data(sample_workbench_data(), {"gate_status": "GO_LIVE_WITH_WARNINGS", "summary": {"blocking_failures": 0}})
        overview = vm["today_overview"]
        self.assertEqual(overview["overall_status"], "READY_TO_REVIEW")
        self.assertEqual(overview["candidate_status"], "READY")
        self.assertEqual(overview["quality_status"], "PASS")

    def test_no_candidate_is_clear(self):
        data = sample_workbench_data()
        data["autonomous_content_production_panel"]["selected_final_candidate"] = {}
        vm = build_workbench_view_model_from_data(data, {})
        self.assertEqual(vm["today_overview"]["overall_status"], "NO_CANDIDATE")

    def test_system_issue_when_gate_blocks(self):
        vm = build_workbench_view_model_from_data(sample_workbench_data(), {"gate_status": "BLOCKED", "summary": {"blocking_failures": 1}})
        self.assertEqual(vm["today_overview"]["overall_status"], "SYSTEM_ISSUE")

    def test_overview_has_no_debug_fields(self):
        overview = build_workbench_view_model_from_data(sample_workbench_data(), {})["today_overview"]
        self.assertNotIn("runtime_pid", overview)
        self.assertNotIn("path_audit", overview)
        self.assertNotIn("debug_actions", overview)


if __name__ == "__main__":
    unittest.main()
