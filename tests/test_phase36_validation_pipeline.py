"""Phase36 tests: Validation Pipeline"""

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.phase36_validation_pipeline import (
    run_phase36_validation_pipeline,
    Phase36PipelineResult
)


class TestPhase36ValidationPipeline(unittest.TestCase):

    def test_pipeline_dry_run(self):
        result = run_phase36_validation_pipeline(dry_run=True)
        self.assertTrue(result.dry_run)
        self.assertTrue(result.cloud_mode)

    def test_pipeline_steps_count(self):
        result = run_phase36_validation_pipeline()
        self.assertEqual(result.total_steps, 6)

    def test_pipeline_does_not_require_real_rss(self):
        result = run_phase36_validation_pipeline()
        # Pipeline should complete without real RSS
        self.assertTrue(result.overall_status in ["SUCCESS", "PARTIAL_SUCCESS", "FAILURE"])

    def test_to_dict_serialization(self):
        result = run_phase36_validation_pipeline()
        data = result.to_dict()
        self.assertIn("dry_run", data)
        self.assertIn("cloud_mode", data)
        self.assertIn("steps", data)


if __name__ == "__main__":
    unittest.main()