"""Phase37A tests: Observation Pipeline"""
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.phase37a_observation_pipeline import run_phase37a_pipeline


class TestPhase37AObservationPipeline(unittest.TestCase):

    def test_dry_run_mode(self):
        result = run_phase37a_pipeline(dry_run=True)
        self.assertTrue(result.dry_run)
        self.assertTrue(result.cloud_mode)

    def test_total_steps(self):
        result = run_phase37a_pipeline()
        self.assertEqual(result.total_steps, 6)

    def test_no_real_rss_required(self):
        result = run_phase37a_pipeline()
        self.assertTrue(result.cloud_mode)

    def test_to_dict(self):
        result = run_phase37a_pipeline()
        data = result.to_dict()
        self.assertIn("steps", data)
        self.assertIn("overall_status", data)


if __name__ == "__main__":
    unittest.main()