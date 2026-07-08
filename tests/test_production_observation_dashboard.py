"""Phase37A tests: Production Observation Dashboard"""
import unittest
import sys
sys.path.insert(0, '/workspace/src')
from content_system.production_observation_dashboard import build_production_observation_dashboard


class TestProductionObservationDashboard(unittest.TestCase):

    def test_cloud_mode_actionable_not_fail(self):
        result = build_production_observation_dashboard(mode="CLOUD_DEVELOPMENT")
        self.assertEqual(result.readiness_status, "ACTIONABLE")
        self.assertNotEqual(result.readiness_status, "FAIL")

    def test_auto_publish_true_causes_fail(self):
        result = build_production_observation_dashboard(auto_publish_enabled=True)
        self.assertEqual(result.readiness_status, "FAIL")
        self.assertTrue(len(result.blocking_issues) > 0)

    def test_secret_leak_causes_fail(self):
        result = build_production_observation_dashboard(secret_leak_detected=True)
        self.assertEqual(result.readiness_status, "FAIL")

    def test_openclaw_modified_causes_fail(self):
        result = build_production_observation_dashboard(openclaw_modified=True)
        self.assertEqual(result.readiness_status, "FAIL")

    def test_fulltext_committed_causes_fail(self):
        result = build_production_observation_dashboard(fulltext_committed=True)
        self.assertEqual(result.readiness_status, "FAIL")

    def test_cloud_mode_rss_pending(self):
        result = build_production_observation_dashboard(mode="CLOUD_DEVELOPMENT")
        self.assertEqual(result.rss_status, "PENDING_LOCAL_EXECUTION")
        self.assertEqual(result.runtime_status, "PENDING_LOCAL_EXECUTION")

    def test_warning_issues_in_cloud(self):
        result = build_production_observation_dashboard(mode="CLOUD_DEVELOPMENT")
        self.assertTrue(len(result.warning_issues) >= 2)

    def test_next_action_defined(self):
        result = build_production_observation_dashboard()
        self.assertTrue(len(result.next_action) > 0)

    def test_to_dict(self):
        result = build_production_observation_dashboard()
        data = result.to_dict()
        self.assertIn("readiness_status", data)
        self.assertIn("blocking_issues", data)
        self.assertIn("next_action", data)


if __name__ == "__main__":
    unittest.main()