import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.phase33_historical_replay import replay_days


class HistoricalDataAvailabilityAuditTest(unittest.TestCase):
    def test_past_seven_replay_days(self):
        days = replay_days(date(2026, 6, 13))
        self.assertEqual([day.business_date for day in days], ["2026-06-06", "2026-06-07", "2026-06-08", "2026-06-09", "2026-06-10", "2026-06-11", "2026-06-12"])
        self.assertTrue(all(day.namespace.startswith("replay_") for day in days))


if __name__ == "__main__":
    unittest.main()
