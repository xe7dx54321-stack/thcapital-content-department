import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from content_system.workbench_view_model import build_workbench_view_model_from_data
from workbench_vm_fixture import sample_workbench_data


class WorkbenchSystemOpsTest(unittest.TestCase):
    def test_system_ops_contains_runtime_launchagent_openclaw(self):
        ops = build_workbench_view_model_from_data(sample_workbench_data(), {})["system_ops"]
        self.assertIn("runtime", ops)
        self.assertIn("launchagent", ops)
        self.assertIn("openclaw", ops)
        self.assertEqual(ops["runtime"]["pid"], 12345)

    def test_debug_actions_are_only_in_system_ops(self):
        vm = build_workbench_view_model_from_data(sample_workbench_data(), {})
        self.assertIn("debug_actions", vm["system_ops"])
        self.assertNotIn("debug_actions", vm["today_overview"])
        self.assertNotIn("debug_actions", vm["today_article"])
        self.assertNotIn("debug_actions", vm["quality_check"])


if __name__ == "__main__":
    unittest.main()
