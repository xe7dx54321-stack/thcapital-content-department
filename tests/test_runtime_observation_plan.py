"""Phase36 tests: Runtime Observation Plan"""

import unittest
import sys
sys.path.insert(0, '/workspace/src')

from content_system.runtime_observation_plan import (
    build_runtime_observation_plan,
    RuntimeObservationPlanResult
)


class TestRuntimeObservationPlan(unittest.TestCase):

    def test_plan_generated(self):
        result = build_runtime_observation_plan()
        self.assertEqual(result.schema_version, "v1")
        self.assertEqual(result.status, "plan_generated")

    def test_no_mac_runtime_required_in_cloud(self):
        result = build_runtime_observation_plan()
        self.assertFalse(result.requires_mac_runtime)

    def test_cloud_mode_notes_exist(self):
        result = build_runtime_observation_plan()
        for check in result.runtime_checks:
            # Cloud mode notes should explain cloud compatibility
            if "launchd" in check.command or "launchctl" in check.command:
                self.assertTrue("云端不要求" in check.cloud_mode_note or "not_required" in check.cloud_mode_note)

    def test_observation_days_defined(self):
        result = build_runtime_observation_plan()
        self.assertTrue(result.observation_days >= 1)
        self.assertTrue(result.observation_days <= 7)

    def test_commands_reference_includes_pause_resume(self):
        result = build_runtime_observation_plan()
        self.assertTrue(any("pause" in cmd for cmd in result.commands_reference))
        self.assertTrue(any("resume" in cmd for cmd in result.commands_reference))

    def test_to_dict_serialization(self):
        result = build_runtime_observation_plan()
        data = result.to_dict()
        self.assertIn("requires_mac_runtime", data)
        self.assertIn("runtime_checks", data)


if __name__ == "__main__":
    unittest.main()