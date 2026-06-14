import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from content_system.workbench_view_model import build_workbench_view_model_from_data
from workbench_vm_fixture import sample_workbench_data


class WorkbenchViewModelTest(unittest.TestCase):
    def test_schema_has_five_operator_views(self):
        vm = build_workbench_view_model_from_data(sample_workbench_data(), {"gate_status": "GO_LIVE_WITH_WARNINGS", "summary": {"blocking_failures": 0}})
        self.assertEqual(
            set(vm.keys()),
            {"schema_version", "generated_at", "run_date", "today_overview", "today_article", "quality_check", "replay_dashboard", "system_ops"},
        )

    def test_source_metadata_warning_appears_in_alerts(self):
        vm = build_workbench_view_model_from_data(sample_workbench_data("OpenClaw source metadata: Finsmes Ai Gnews"), {})
        alerts = " ".join(item["message"] for item in vm["today_overview"]["alerts"])
        self.assertIn("source metadata", alerts.lower())
        self.assertNotIn("OpenClaw source metadata:", vm["today_overview"]["recommended_title"])


if __name__ == "__main__":
    unittest.main()
