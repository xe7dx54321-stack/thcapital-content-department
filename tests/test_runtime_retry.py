from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.runtime_retry_manager import can_retry, classify_error


class RuntimeRetryTests(unittest.TestCase):
    def test_retry_classification_and_max_retry(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        self.assertEqual(classify_error("cost guard budget blocked"), "LLM_COST_BLOCK")
        allowed, error_class, reason = can_retry({"job_id": "content_generation_daily", "attempt_count": 1, "error_message": "rate limit 429"}, repo_root)
        self.assertTrue(allowed)
        self.assertEqual(error_class, "LLM_RATE_LIMIT")
        allowed, error_class, reason = can_retry({"job_id": "content_generation_daily", "attempt_count": 5, "error_message": "rate limit 429"}, repo_root)
        self.assertFalse(allowed)
        self.assertEqual(reason, "max_attempts_reached")
        allowed, error_class, reason = can_retry({"job_id": "content_generation_daily", "attempt_count": 1, "error_message": "safety gate blocked by gate"}, repo_root)
        self.assertFalse(allowed)
        self.assertEqual(error_class, "SAFETY_GATE_BLOCK")


if __name__ == "__main__":
    unittest.main()
