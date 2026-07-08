"""Phase37A tests: Runtime Observation Result Capture"""
import unittest
import sys
sys.path.insert(0, '/workspace/src')
from content_system.runtime_observation_result_capture import build_runtime_observation_result


class TestRuntimeObservationResultCapture(unittest.TestCase):

    def test_cloud_mode_pending(self):
        result = build_runtime_observation_result(cloud_mode=True)
        self.assertEqual(result.status, "PENDING_LOCAL_EXECUTION")
        self.assertFalse(result.requires_mac_runtime)
        self.assertEqual(result.blocking_failures, 0)

    def test_cloud_mode_no_launchd_required(self):
        result = build_runtime_observation_result(cloud_mode=True)
        self.assertEqual(result.launchagent_status, "PENDING_LOCAL")
        self.assertEqual(result.runtime_status, "PENDING_LOCAL")

    def test_observation_days_zero_in_cloud(self):
        result = build_runtime_observation_result(cloud_mode=True)
        self.assertEqual(result.observation_days, 0)

    def test_observation_checks_defined(self):
        result = build_runtime_observation_result()
        self.assertTrue(len(result.observation_checks) >= 5)
        self.assertIn("runtime_status_check", result.observation_checks)
        self.assertIn("workbench_check", result.observation_checks)

    def test_to_dict(self):
        result = build_runtime_observation_result()
        data = result.to_dict()
        self.assertIn("status", data)
        self.assertIn("observation_days", data)
        self.assertIn("observation_checks", data)


if __name__ == "__main__":
    unittest.main()