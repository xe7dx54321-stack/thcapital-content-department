"""Phase37A tests: Manual Observation Log"""
import unittest
import sys
sys.path.insert(0, '/workspace/src')
from content_system.manual_observation_log import build_manual_observation_log


class TestManualObservationLog(unittest.TestCase):

    def test_day_slots_default(self):
        result = build_manual_observation_log(day_slots=2)
        self.assertEqual(result.day_slots, 2)
        self.assertEqual(len(result.day_records), 2)

    def test_each_day_has_required_fields(self):
        result = build_manual_observation_log(day_slots=2)
        for record in result.day_records:
            self.assertTrue(hasattr(record, "date"))
            self.assertTrue(hasattr(record, "workbench_openable"))
            self.assertTrue(hasattr(record, "main_issues"))
            self.assertTrue(hasattr(record, "calibration_items"))

    def test_checklist_count(self):
        result = build_manual_observation_log(day_slots=2)
        self.assertTrue(result.checklist_count > 0)

    def test_day_records_have_dates(self):
        result = build_manual_observation_log(day_slots=2)
        dates = [r.date for r in result.day_records]
        self.assertEqual(len(dates), 2)
        self.assertNotEqual(dates[0], dates[1])

    def test_to_dict(self):
        result = build_manual_observation_log()
        data = result.to_dict()
        self.assertIn("day_slots", data)
        self.assertIn("day_records", data)
        self.assertIn("checklist_count", data)


if __name__ == "__main__":
    unittest.main()