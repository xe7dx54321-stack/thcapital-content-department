"""Phase36 tests: Production Readiness Gate"""

import unittest
import sys
sys.path.insert(0, '/workspace/src')

from content_system.production_readiness_gate import (
    run_production_readiness_gate,
    ProductionReadinessGateResult
)


class TestProductionReadinessGate(unittest.TestCase):

    def test_all_pass_in_cloud_mode(self):
        result = run_production_readiness_gate(
            phase35_pass=True,
            phase34b_pass=True,
            phase34a_pass=True,
            phase33b_pass=True,
            usage_boundary_pass=True,
            no_secret_leak=True,
            no_openclaw_mod=True,
            auto_publish_disabled=True,
            workbench_ok=True,
            local_rss_smoke_done=False,  # pending
            runtime_observation_done=False,  # pending
            cloud_mode=True
        )
        # Should be ACTIONABLE (not FAIL) because local items pending but not blocking
        self.assertEqual(result.overall_status, "ACTIONABLE")
        self.assertTrue(result.ready_for_observation)
        # pending items should be WARN, not FAIL
        self.assertTrue(result.warn_count >= 2)

    def test_pending_local_items_not_fail_in_cloud_mode(self):
        result = run_production_readiness_gate(
            cloud_mode=True,
            local_rss_smoke_done=False,
            runtime_observation_done=False
        )
        # Check that pending items are WARN, not FAIL
        for check in result.gate_checks:
            if check.cloud_mode_warn_only:
                if check.actual == "pending":
                    self.assertEqual(check.status, "WARN")
                    self.assertFalse(check.is_blocking)

    def test_auto_publish_enabled_causes_fail(self):
        result = run_production_readiness_gate(
            auto_publish_disabled=False,
            cloud_mode=True
        )
        self.assertEqual(result.overall_status, "FAIL")
        self.assertTrue(result.blocking_failures > 0)
        self.assertFalse(result.ready_for_observation)

    def test_secret_leak_causes_fail(self):
        result = run_production_readiness_gate(
            no_secret_leak=False,
            cloud_mode=True
        )
        self.assertEqual(result.overall_status, "FAIL")
        self.assertTrue(result.blocking_failures > 0)

    def test_pipeline_fail_causes_fail(self):
        result = run_production_readiness_gate(
            phase35_pass=False,
            cloud_mode=True
        )
        self.assertEqual(result.overall_status, "FAIL")

    def test_all_pass_with_local_done_gives_pass(self):
        result = run_production_readiness_gate(
            local_rss_smoke_done=True,
            runtime_observation_done=True,
            cloud_mode=True
        )
        self.assertEqual(result.overall_status, "PASS")
        self.assertEqual(result.warn_count, 0)

    def test_to_dict_serialization(self):
        result = run_production_readiness_gate()
        data = result.to_dict()
        self.assertIn("overall_status", data)
        self.assertIn("gate_checks", data)
        self.assertIn("next_steps", data)


if __name__ == "__main__":
    unittest.main()