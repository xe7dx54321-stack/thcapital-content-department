import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from content_system.editorial_prompt_builder import build_editorial_prompt, build_review_prompt


class TestEditorialPromptBuilder(unittest.TestCase):
    def test_injects_style_guide(self):
        result = build_editorial_prompt("写一篇文章")
        self.assertTrue(result.style_guide_injected)
        self.assertIn("写作原则", result.prompt)

    def test_injects_framework(self):
        result = build_editorial_prompt("写一篇文章", framework_id="news_explainer")
        self.assertTrue(result.framework_injected)
        self.assertIn("新闻解读框架", result.prompt)

    def test_injects_title_policy(self):
        result = build_editorial_prompt("写一篇文章")
        self.assertTrue(result.title_policy_injected)
        self.assertIn("标题", result.prompt)

    def test_injects_ai_taste_guard(self):
        result = build_editorial_prompt("写一篇文章")
        self.assertTrue(result.ai_taste_guard_injected)
        self.assertIn("AI味", result.prompt)

    def test_prompt_has_all_required_sections(self):
        result = build_editorial_prompt("写一篇文章", framework_id="news_explainer")
        self.assertIn("编辑风格指南", result.prompt)
        self.assertIn("叙事框架", result.prompt)
        self.assertIn("标题生成策略", result.prompt)
        self.assertIn("AI味表达拦截", result.prompt)

    def test_to_dict_serialization(self):
        result = build_editorial_prompt("写一篇文章")
        data = result.to_dict()
        self.assertIn("prompt", data)
        self.assertIn("style_guide_injected", data)
        self.assertIn("framework_injected", data)


if __name__ == "__main__":
    unittest.main()
