import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.phase33_historical_replay import quality_checks_for_day, ReplayDay


class ReplayQualityRegressionTest(unittest.TestCase):
    def test_target_price_and_fake_citation_blocked(self):
        day = ReplayDay("2026-06-12", "20260612", "replay_20260612", "2026-06-12T23:59:59", "2026-06-12T00:00:00")
        status, checks, _ = quality_checks_for_day(day, [{"article_markdown": "据某媒体，匿名人士称 target price 上调。"}], {"main_topic": {"title": "topic"}})
        failed = {item["check_id"] for item in checks if item["status"] == "FAIL"}
        self.assertEqual(status, "FAIL")
        self.assertIn("no_target_price", failed)
        self.assertIn("no_fake_citation", failed)


if __name__ == "__main__":
    unittest.main()
