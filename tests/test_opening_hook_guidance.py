import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from content_system.opening_hook_guidance import generate_opening_hook, check_marketing_style


class TestOpeningHookGuidance(unittest.TestCase):
    def test_hook_types_generated(self):
        guidance = generate_opening_hook("AI芯片市场格局变化")
        self.assertTrue(guidance.hook_strategy)
        self.assertTrue(guidance.opening_question)
        self.assertTrue(guidance.first_paragraph_guidance)

    def test_opening_guidance_does_not_generate_marketing_style(self):
        guidance = generate_opening_hook("AI芯片市场格局变化")
        marketing_patterns = ["震惊", "你绝对想不到", "揭秘"]
        for pattern in marketing_patterns:
            self.assertNotIn(pattern, guidance.first_paragraph_guidance)

    def test_guidance_field_present(self):
        guidance = generate_opening_hook("AI芯片市场格局变化")
        self.assertIn("避免", guidance.first_paragraph_guidance)

    def test_marketing_patterns_detected_and_rewritten(self):
        result = check_marketing_style("震惊！AI芯片市场格局变化")
        self.assertTrue(result["has_marketing_style"])

    def test_to_dict_serialization(self):
        guidance = generate_opening_hook("AI芯片市场格局变化")
        data = guidance.to_dict()
        self.assertIn("hook_strategy", data)
        self.assertIn("opening_question", data)
        self.assertIn("first_paragraph_guidance", data)
        self.assertIn("avoid_opening_patterns", data)


if __name__ == "__main__":
    unittest.main()
