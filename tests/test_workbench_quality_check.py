import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from content_system.workbench_view_model import build_workbench_view_model_from_data
from workbench_vm_fixture import sample_workbench_data


class WorkbenchQualityCheckTest(unittest.TestCase):
    def test_quality_check_is_content_and_evidence_only(self):
        quality = build_workbench_view_model_from_data(sample_workbench_data(), {})["quality_check"]
        payload = json.dumps(quality, ensure_ascii=False)
        self.assertIn("checklist", quality)
        self.assertIn("evidence_summary", quality)
        self.assertIn("human_review_checklist", quality)
        self.assertNotIn("LaunchAgent", payload)
        self.assertNotIn("heartbeat", payload.lower())
        self.assertNotIn("runtime_pid", payload)

    def test_weak_signal_is_labeled_not_hard_evidence(self):
        evidence = build_workbench_view_model_from_data(sample_workbench_data(), {})["quality_check"]["evidence_summary"]
        self.assertEqual(evidence["weak_signal_count"], 1)
        self.assertIn("弱信号", evidence["note"])


if __name__ == "__main__":
    unittest.main()
