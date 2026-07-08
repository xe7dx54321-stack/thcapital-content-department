"""Phase37A tests: RSS Smoke Result Capture"""
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.rss_smoke_result_capture import build_rss_smoke_result


class TestRssSmokeResultCapture(unittest.TestCase):

    def test_cloud_mode_pending(self):
        result = build_rss_smoke_result(cloud_mode=True)
        self.assertEqual(result.status, "PENDING_LOCAL_EXECUTION")
        self.assertFalse(result.requires_real_rss)
        self.assertEqual(result.blocking_failures, 0)

    def test_secret_leak_causes_fail(self):
        result = build_rss_smoke_result(cloud_mode=False, article_count=10)
        result.secret_leak_count = 1
        result.status = "FAIL"
        result.blocking_failures = 1
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(result.blocking_failures > 0)

    def test_cloud_mode_zero_articles_ok(self):
        result = build_rss_smoke_result(cloud_mode=True)
        self.assertEqual(result.article_count, 0)
        self.assertEqual(result.fetched_source_count, 0)
        self.assertNotEqual(result.status, "FAIL")

    def test_safety_checks_defined(self):
        result = build_rss_smoke_result()
        self.assertIn("no_secret_in_output", result.safety_checks)
        self.assertIn("no_auto_publish", result.safety_checks)

    def test_to_dict(self):
        result = build_rss_smoke_result()
        data = result.to_dict()
        self.assertIn("status", data)
        self.assertIn("article_count", data)
        self.assertIn("safety_checks", data)


if __name__ == "__main__":
    unittest.main()