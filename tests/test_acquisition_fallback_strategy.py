from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.acquisition_fallback_strategy import load_fallback_strategies, validate_fallback_strategies


class AcquisitionFallbackStrategyTest(unittest.TestCase):
    def test_fallback_routes_and_weak_boundaries(self) -> None:
        payload = validate_fallback_strategies(ROOT)
        self.assertEqual(payload["status"], "PASS")
        strategies = load_fallback_strategies(ROOT)
        self.assertFalse(strategies["reddit_llm_discussion"]["hard_evidence_allowed"])
        self.assertFalse(strategies["wechat_metadata"]["full_text_fetch"])


if __name__ == "__main__":
    unittest.main()
