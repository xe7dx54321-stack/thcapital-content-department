from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.acquisition_cadence import validate_acquisition_cadence
from content_system.acquisition_playbook_common import grouped_slot_key, parse_minutes


class AcquisitionCadenceTest(unittest.TestCase):
    def test_cadence_validation_and_timezone(self) -> None:
        payload = validate_acquisition_cadence(ROOT)
        self.assertEqual(payload["status"], "PASS")
        self.assertGreater(payload["schedule_slot_count"], 0)

    def test_invalid_cron_time_rejected(self) -> None:
        with self.assertRaises(ValueError):
            parse_minutes("25:99")

    def test_grouped_slot_key(self) -> None:
        self.assertEqual(grouped_slot_key("09:15", 20), "09:00")


if __name__ == "__main__":
    unittest.main()
