from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.acquisition_query_strategy import load_query_strategies, validate_query_strategies


class AcquisitionQueryStrategyTest(unittest.TestCase):
    def test_keywords_and_lookback(self) -> None:
        payload = validate_query_strategies(ROOT)
        self.assertEqual(payload["status"], "PASS")
        self.assertGreater(payload["keyword_count"], 0)
        for strategy in load_query_strategies(ROOT).values():
            self.assertGreater(int(strategy["lookback_hours"]), 0)
            self.assertGreater(int(strategy["max_items_per_source"]), 0)


if __name__ == "__main__":
    unittest.main()
