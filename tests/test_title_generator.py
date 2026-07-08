import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from content_system.title_generator import generate_title_candidates


class TestTitleGenerator(unittest.TestCase):
    def test_generate_at_least_five_titles(self):
        result = generate_title_candidates("AI芯片市场格局变化")
        self.assertTrue(len(result.candidates) >= 5)

    def test_title_length_compliance(self):
        result = generate_title_candidates("AI芯片市场格局变化")
        for candidate in result.candidates:
            self.assertTrue(len(candidate.title) >= 10)

    def test_scores_in_range(self):
        result = generate_title_candidates("AI芯片市场格局变化")
        for candidate in result.candidates:
            self.assertTrue(0 <= candidate.score <= 1)

    def test_forbidden_pattern_intercepted(self):
        result = generate_title_candidates("震惊！AI芯片市场格局变化")
        hit_count = sum(1 for c in result.candidates if c.forbidden_pattern_hit)
        self.assertTrue(hit_count > 0)

    def test_candidates_are_compliant(self):
        result = generate_title_candidates("AI芯片市场格局变化")
        self.assertTrue(result.compliant_count >= 3)

    def test_to_dict_serialization(self):
        result = generate_title_candidates("AI芯片市场格局变化")
        data = result.to_dict()
        self.assertIn("candidates", data)
        self.assertIn("compliant_count", data)
        self.assertIn("recommended_count", data)


if __name__ == "__main__":
    unittest.main()
