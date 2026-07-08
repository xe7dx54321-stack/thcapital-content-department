"""Phase36 tests: Real Data Calibration Checklist"""

import unittest
import sys
sys.path.insert(0, '/workspace/src')

from content_system.real_data_calibration_checklist import (
    build_real_data_calibration_checklist,
    CalibrationChecklistResult
)


class TestRealDataCalibrationChecklist(unittest.TestCase):

    def test_checklist_generated(self):
        result = build_real_data_calibration_checklist()
        self.assertEqual(result.schema_version, "v1")
        self.assertEqual(result.status, "checklist_generated")

    def test_rss_items_exist(self):
        result = build_real_data_calibration_checklist()
        self.assertTrue(len(result.rss_items) >= 4)

    def test_topic_items_exist(self):
        result = build_real_data_calibration_checklist()
        self.assertTrue(len(result.topic_items) >= 2)

    def test_editorial_items_exist(self):
        result = build_real_data_calibration_checklist()
        self.assertTrue(len(result.editorial_items) >= 4)

    def test_workbench_items_exist(self):
        result = build_real_data_calibration_checklist()
        self.assertTrue(len(result.workbench_items) >= 2)

    def test_each_item_has_pass_criteria(self):
        result = build_real_data_calibration_checklist()
        for item in result.checklist_items:
            self.assertTrue(len(item.pass_criteria) > 0)
            self.assertTrue(len(item.fail_indication) > 0)
            self.assertTrue(len(item.record_field) > 0)

    def test_calibration_notes_for_adjustments(self):
        result = build_real_data_calibration_checklist()
        items_with_notes = [i for i in result.checklist_items if i.calibration_notes]
        self.assertTrue(len(items_with_notes) > 0)

    def test_to_dict_serialization(self):
        result = build_real_data_calibration_checklist()
        data = result.to_dict()
        self.assertIn("rss_items", data)
        self.assertIn("topic_items", data)
        self.assertIn("editorial_items", data)
        self.assertIn("workbench_items", data)


if __name__ == "__main__":
    unittest.main()