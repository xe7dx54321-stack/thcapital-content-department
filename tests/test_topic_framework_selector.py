import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from content_system.topic_framework_selector import select_topic_framework


class TestTopicFrameworkSelector(unittest.TestCase):
    def test_selector_selects_applicable_framework(self):
        result = select_topic_framework(
            topic_id="test_001",
            topic_type="news_event",
        )
        self.assertIsNotNone(result.selected_framework)

    def test_selector_with_angle_type(self):
        result = select_topic_framework(
            topic_id="test_002",
            topic_type="product_launch",
            angle_type="产品策略",
        )
        self.assertTrue(result.confidence > 0.5)

    def test_selector_with_event_type(self):
        result = select_topic_framework(
            topic_id="test_003",
            topic_type="news_event",
            event_type="launch",
        )
        self.assertIsNotNone(result.selected_framework)

    def test_selector_has_fallback_for_unknown_topic_type(self):
        result = select_topic_framework(
            topic_id="test_004",
            topic_type="unknown_type",
        )
        self.assertTrue(result.fallback_used)
        self.assertIsNotNone(result.selected_framework)

    def test_selection_result_fields(self):
        result = select_topic_framework(
            topic_id="test_005",
            topic_type="news_event",
        )
        self.assertEqual(result.topic_id, "test_005")
        self.assertTrue(result.reason)
        self.assertTrue(0 <= result.confidence <= 1)
        self.assertIsInstance(result.fallback_used, bool)

    def test_to_dict_serialization(self):
        result = select_topic_framework(
            topic_id="test_006",
            topic_type="news_event",
        )
        data = result.to_dict()
        self.assertIn("topic_id", data)
        self.assertIn("selected_framework", data)
        self.assertIn("reason", data)
        self.assertIn("confidence", data)
        self.assertIn("fallback_used", data)


if __name__ == "__main__":
    unittest.main()
