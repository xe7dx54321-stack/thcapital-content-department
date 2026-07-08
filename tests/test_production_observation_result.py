"""Phase37A tests: Production Observation Result"""
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.production_observation_result import build_production_observation_schema


class TestProductionObservationResult(unittest.TestCase):

    def test_cloud_mode_default(self):
        result = build_production_observation_schema(mode="CLOUD_DEVELOPMENT")
        self.assertEqual(result.mode, "CLOUD_DEVELOPMENT")
        self.assertEqual(result.status, "generated")

    def test_cloud_mode_no_real_rss_required(self):
        result = build_production_observation_schema(mode="CLOUD_DEVELOPMENT")
        self.assertFalse(result.rss_smoke.get("requires_real_rss", True))
        self.assertFalse(result.runtime_observation.get("requires_mac_runtime", True))

    def test_cloud_mode_pending_not_fail(self):
        result = build_production_observation_schema(mode="CLOUD_DEVELOPMENT")
        rss_status = result.rss_smoke.get("status", "FAIL")
        rt_status = result.runtime_observation.get("status", "FAIL")
        self.assertIn(rss_status, ["PENDING_LOCAL_EXECUTION", "PASS", "ACTIONABLE"])
        self.assertIn(rt_status, ["PENDING_LOCAL_EXECUTION", "PASS", "ACTIONABLE"])

    def test_sections_count(self):
        result = build_production_observation_schema()
        self.assertTrue(result.section_count >= 5)

    def test_safety_boundary_fields(self):
        result = build_production_observation_schema()
        self.assertIn("auto_publish_allowed", result.safety_boundary)
        self.assertIn("no_secret_in_git", result.safety_boundary)
        self.assertFalse(result.safety_boundary["auto_publish_allowed"])
        self.assertTrue(result.safety_boundary["no_secret_in_git"])

    def test_to_dict(self):
        result = build_production_observation_schema()
        data = result.to_dict()
        self.assertIn("rss_smoke", data)
        self.assertIn("runtime_observation", data)
        self.assertIn("safety_boundary", data)


if __name__ == "__main__":
    unittest.main()