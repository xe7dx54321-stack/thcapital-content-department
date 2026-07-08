import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from content_system.version_comparison_gate import compare_versions


class TestVersionComparisonGate(unittest.TestCase):
    def test_metric_changes_calculated(self):
        result = compare_versions(
            "AI芯片市场值得关注。",
            "AI芯片市场正在发生变化。我们认为这有重大影响。",
        )
        self.assertTrue(result.improvement_score != 0)

    def test_accept_improvement(self):
        result = compare_versions(
            "AI芯片市场值得关注，未来可期。",
            "AI芯片市场正在发生变化。根据数据，NVIDIA发布新GPU，我们认为这重新定义了竞争格局。",
        )
        self.assertTrue(result.accept_rewrite)

    def test_reject_no_improvement(self):
        result = compare_versions(
            "AI芯片市场正在发生变化。",
            "AI芯片市场正在发生变化。",
        )
        self.assertFalse(result.accept_rewrite)

    def test_reject_regression_rewrite(self):
        result = compare_versions(
            "AI芯片市场正在发生变化。我们认为这有重大影响，需要注意供应链风险。",
            "AI芯片市场值得关注，未来可期。",
        )
        self.assertFalse(result.accept_rewrite)

    def test_partial_accept_with_minor_regression(self):
        result = compare_versions(
            "AI芯片市场值得关注。",
            "AI芯片市场正在发生变化。我们认为这有重大影响，需要注意供应链风险。",
        )
        self.assertTrue(result.accept_rewrite)

    def test_to_dict_serialization(self):
        result = compare_versions(
            "AI芯片市场值得关注。",
            "AI芯片市场正在发生变化。",
        )
        data = result.to_dict()
        self.assertIn("original_score", data)
        self.assertIn("rewritten_score", data)
        self.assertIn("improvement_score", data)
        self.assertIn("accept_rewrite", data)
        self.assertIn("reason", data)


if __name__ == "__main__":
    unittest.main()
