import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from content_system.draft_style_quality_scorer import score_draft_quality


class TestDraftStyleQualityScorer(unittest.TestCase):
    def test_overall_score_in_range(self):
        result = score_draft_quality("AI芯片市场正在发生变化。")
        self.assertTrue(0 <= result.overall_style_score <= 1)

    def test_breakdown_has_seven_dimensions(self):
        result = score_draft_quality("AI芯片市场正在发生变化。")
        self.assertTrue(len(result.dimension_scores) >= 7)

    def test_all_dimensions_in_range(self):
        result = score_draft_quality("AI芯片市场正在发生变化。")
        for dim in result.dimension_scores:
            self.assertTrue(0 <= dim.score <= 1)

    def test_seven_dimensions_output(self):
        result = score_draft_quality("AI芯片市场正在发生变化。")
        dimensions = [d.dimension for d in result.dimension_scores]
        self.assertIn("判断强度", dimensions)
        self.assertIn("证据密度", dimensions)
        self.assertIn("叙事流畅度", dimensions)

    def test_suggestions_generated(self):
        result = score_draft_quality("值得关注的是，未来可期。")
        self.assertTrue(len(result.revision_suggestions) > 0)

    def test_to_dict_serialization(self):
        result = score_draft_quality("AI芯片市场正在发生变化。")
        data = result.to_dict()
        self.assertIn("overall_style_score", data)
        self.assertIn("grade", data)
        self.assertIn("dimension_scores", data)
        self.assertIn("blocking_issues", data)
        self.assertIn("revision_suggestions", data)


if __name__ == "__main__":
    unittest.main()
