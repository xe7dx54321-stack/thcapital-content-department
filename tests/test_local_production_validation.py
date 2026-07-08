"""Phase36 tests: Local Production Validation"""

import unittest
import sys
sys.path.insert(0, '/workspace/src')

from content_system.local_production_validation import (
    build_local_production_validation_plan,
    ValidationPlanResult
)


class TestLocalProductionValidation(unittest.TestCase):

    def test_plan_generated(self):
        result = build_local_production_validation_plan()
        self.assertEqual(result.schema_version, "v1")
        self.assertEqual(result.status, "generated")

    def test_cloud_mode_no_real_rss_required(self):
        result = build_local_production_validation_plan()
        self.assertEqual(result.mode, "cloud_development")
        # Cloud mode should not require real RSS
        local_only_count = sum(1 for s in result.validation_sequence if s.local_only)
        self.assertTrue(local_only_count > 0)
        # But cloud_safe items should exist
        self.assertTrue(result.cloud_safe_items > 0)

    def test_cloud_capabilities_listed(self):
        result = build_local_production_validation_plan()
        self.assertTrue(len(result.cloud_completed_capabilities) >= 4)

    def test_validation_sequence_exists(self):
        result = build_local_production_validation_plan()
        self.assertTrue(result.checklist_count >= 5)

    def test_pass_criteria_defined(self):
        result = build_local_production_validation_plan()
        self.assertTrue(len(result.pass_criteria) >= 4)
        self.assertTrue(len(result.block_criteria) >= 3)

    def test_to_dict_serialization(self):
        result = build_local_production_validation_plan()
        data = result.to_dict()
        self.assertIn("schema_version", data)
        self.assertIn("mode", data)
        self.assertIn("cloud_completed_capabilities", data)
        self.assertIn("validation_sequence", data)


if __name__ == "__main__":
    unittest.main()