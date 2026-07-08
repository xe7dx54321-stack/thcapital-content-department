import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from content_system.ai_taste_guard import detect_ai_taste, get_ai_taste_rule_count


class TestAITasteGuard(unittest.TestCase):
    def test_at_least_fifty_rules(self):
        rule_count = get_ai_taste_rule_count()
        self.assertTrue(rule_count >= 50)

    def test_discouraged_phrase_detected(self):
        result = detect_ai_taste("AI芯片市场值得关注，未来可期。")
        self.assertTrue(result.hit_count > 0)

    def test_empty_expressions_detected(self):
        result = detect_ai_taste("这非常重要，极具价值。")
        self.assertTrue(result.hit_count > 0)

    def test_marketing_expressions_detected(self):
        result = detect_ai_taste("限时优惠，抢购爆款！")
        self.assertTrue(result.hit_count > 0)

    def test_ai_taste_score_calculated(self):
        result = detect_ai_taste("AI芯片市场值得关注。")
        self.assertTrue(0 <= result.ai_taste_score <= 1)

    def test_ai_taste_score_drops_with_violations(self):
        clean = detect_ai_taste("AI芯片市场正在发生变化。")
        dirty = detect_ai_taste("AI芯片市场值得关注，未来可期，赋能产业。")
        self.assertTrue(dirty.ai_taste_score < clean.ai_taste_score)

    def test_severity_level_assigned(self):
        result = detect_ai_taste("AI芯片市场值得关注。")
        for violation in result.violations:
            self.assertIn(violation.severity, ["high", "medium", "low"])

    def test_to_dict_serialization(self):
        result = detect_ai_taste("AI芯片市场值得关注。")
        data = result.to_dict()
        self.assertIn("hit_count", data)
        self.assertIn("high_severity_count", data)
        self.assertIn("violations", data)
        self.assertIn("ai_taste_score", data)


if __name__ == "__main__":
    unittest.main()
