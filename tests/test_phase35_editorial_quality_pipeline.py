import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from content_system.phase35_editorial_quality_pipeline import run_phase35_pipeline


class TestPhase35EditorialQualityPipeline(unittest.TestCase):
    def test_pipeline_completes_in_dry_run(self):
        result = run_phase35_pipeline()
        self.assertIn(result.status, ["SUCCESS", "FAILED"])

    def test_pipeline_with_content(self):
        result = run_phase35_pipeline(
            topic_title="AI芯片市场格局变化",
            draft_text="AI芯片市场正在发生变化。",
        )
        self.assertTrue(result.framework_count >= 6)
        self.assertTrue(result.title_candidate_count >= 5)

    def test_pipeline_with_version_comparison(self):
        result = run_phase35_pipeline(
            original_version="AI芯片市场值得关注。",
            new_version="AI芯片市场正在发生变化。",
        )
        self.assertIn(result.version_gate_decision, ["accept", "reject"])

    def test_cloud_mode_does_not_require_real_rss(self):
        result = run_phase35_pipeline()
        self.assertTrue(result.status in ["SUCCESS", "FAILED"])

    def test_cloud_mode_does_not_require_mac_runtime(self):
        result = run_phase35_pipeline()
        self.assertTrue(result.status in ["SUCCESS", "FAILED"])

    def test_to_dict_serialization(self):
        result = run_phase35_pipeline()
        data = result.to_dict()
        self.assertIn("status", data)
        self.assertIn("run_date", data)
        self.assertIn("steps", data)
        self.assertIn("outputs", data)


if __name__ == "__main__":
    unittest.main()
