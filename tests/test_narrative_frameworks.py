import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from content_system.narrative_frameworks import (
    load_narrative_frameworks,
    validate_narrative_frameworks,
    get_framework_by_id,
    get_applicable_frameworks,
)


class TestNarrativeFrameworks(unittest.TestCase):
    def test_framework_count_at_least_six(self):
        frameworks = load_narrative_frameworks()
        self.assertTrue(len(frameworks) >= 6)

    def test_framework_basic_fields(self):
        frameworks = load_narrative_frameworks()
        for fw in frameworks:
            self.assertTrue(fw.framework_id)
            self.assertTrue(fw.name)
            self.assertTrue(fw.purpose)

    def test_each_framework_has_section_sequence(self):
        frameworks = load_narrative_frameworks()
        for fw in frameworks:
            self.assertTrue(len(fw.section_sequence) >= 3)

    def test_each_framework_has_strategy_fields(self):
        frameworks = load_narrative_frameworks()
        for fw in frameworks:
            self.assertTrue(fw.opening_strategy)
            self.assertTrue(fw.evidence_strategy)
            self.assertTrue(fw.counterargument_strategy)
            self.assertTrue(fw.closing_strategy)

    def test_get_framework_by_id(self):
        fw = get_framework_by_id("news_explainer")
        self.assertIsNotNone(fw)
        self.assertEqual(fw.name, "新闻解读框架")

    def test_get_applicable_frameworks(self):
        frameworks = get_applicable_frameworks("news_event")
        self.assertTrue(len(frameworks) >= 1)

    def test_to_dict_serialization(self):
        frameworks = load_narrative_frameworks()
        for fw in frameworks:
            result = fw.to_dict()
            self.assertIn("framework_id", result)
            self.assertIn("name", result)
            self.assertIn("section_sequence", result)


if __name__ == "__main__":
    unittest.main()
