from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.runtime_idempotency import duplicate_run_prevented, idempotency_key


class RuntimeIdempotencyTests(unittest.TestCase):
    def test_daily_slot_key_and_duplicate_prevention(self) -> None:
        key = idempotency_key("acquisition_phase29", "2026-06-11", "morning_acquisition", "daily_slot")
        self.assertEqual(key, "acquisition_phase29:2026-06-11:morning_acquisition")
        self.assertTrue(duplicate_run_prevented({"status": "SUCCESS"}))
        self.assertTrue(duplicate_run_prevented({"status": "RUNNING"}))
        self.assertFalse(duplicate_run_prevented({"status": "FAILED"}))


if __name__ == "__main__":
    unittest.main()
