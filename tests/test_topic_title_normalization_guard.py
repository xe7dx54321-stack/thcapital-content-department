import unittest

from content_system.topic_title_normalization_guard import (
    TitleNormalizationReport,
    TitleGuard,
    apply_title_guard,
    is_raw_metadata,
    is_human_readable,
    normalize_title,
    report_to_dict,
)


class TestTopicTitleNormalizationGuard(unittest.TestCase):
    def test_is_raw_metadata_url(self):
        self.assertTrue(is_raw_metadata("https://example.com/article"))
        self.assertTrue(is_raw_metadata("http://test.com"))

    def test_is_raw_metadata_email(self):
        self.assertTrue(is_raw_metadata("test@example.com"))

    def test_is_raw_metadata_date(self):
        self.assertTrue(is_raw_metadata("2024-01-15"))
        self.assertTrue(is_raw_metadata("01/15/2024"))

    def test_is_raw_metadata_hash(self):
        self.assertTrue(is_raw_metadata("a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"))
        self.assertTrue(is_raw_metadata("a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6a7b8c9d0e1f2a3b4c5d6a7b8c9d0e1f2"))

    def test_is_raw_metadata_domain(self):
        self.assertTrue(is_raw_metadata("example.com"))

    def test_is_raw_metadata_empty(self):
        self.assertTrue(is_raw_metadata(""))
        self.assertTrue(is_raw_metadata("   "))

    def test_is_raw_metadata_placeholder(self):
        self.assertTrue(is_raw_metadata("Untitled"))
        self.assertTrue(is_raw_metadata("No title"))
        self.assertTrue(is_raw_metadata("Title"))

    def test_is_not_raw_metadata(self):
        self.assertFalse(is_raw_metadata("GPT-5技术架构深度解析"))
        self.assertFalse(is_raw_metadata("AI创业公司融资新闻"))

    def test_is_human_readable_valid(self):
        self.assertTrue(is_human_readable("GPT-5技术架构深度解析"))
        self.assertTrue(is_human_readable("AI创业公司获千万融资"))

    def test_is_human_readable_too_short(self):
        self.assertFalse(is_human_readable("AI"))
        self.assertFalse(is_human_readable("Hi"))

    def test_is_human_readable_low_text_ratio(self):
        self.assertFalse(is_human_readable("1234567890"))
        self.assertFalse(is_human_readable("!!!@@@###"))

    def test_is_human_readable_low_quality_indicators(self):
        self.assertFalse(is_human_readable("Read more about AI"))
        self.assertFalse(is_human_readable("Click here for details"))
        self.assertFalse(is_human_readable("Learn more now"))

    def test_normalize_title(self):
        title = "  GPT-5 | 技术架构深度解析  "
        normalized = normalize_title(title)
        self.assertEqual(normalized, "GPT-5 | 技术架构深度解析")

        title = "<html><title>Test</title></html>"
        normalized = normalize_title(title)
        self.assertEqual(normalized, "Test")

    def test_apply_title_guard_raw_metadata(self):
        candidates = [
            {"topic_id": "test_001", "title": "https://example.com/article"}
        ]
        report = apply_title_guard(candidates, run_date="20260707")
        self.assertEqual(report.raw_metadata_count, 1)
        guard = report.guards[0]
        self.assertTrue(guard.is_raw_metadata_title)

    def test_apply_title_guard_non_human_readable(self):
        candidates = [
            {"topic_id": "test_001", "title": "AI"},
            {"topic_id": "test_002", "title": "Read more"},
        ]
        report = apply_title_guard(candidates, run_date="20260707")
        self.assertEqual(report.non_human_readable_count, 2)

    def test_apply_title_guard_valid_titles(self):
        candidates = [
            {"topic_id": "test_001", "title": "GPT-5技术架构深度解析"},
            {"topic_id": "test_002", "title": "AI创业公司获千万融资"},
        ]
        report = apply_title_guard(candidates, run_date="20260707")
        self.assertEqual(report.raw_metadata_count, 0)
        self.assertEqual(report.non_human_readable_count, 0)

    def test_normalized_title_generated(self):
        candidates = [
            {"topic_id": "test_001", "title": "  GPT-5 | 技术架构深度解析  "}
        ]
        report = apply_title_guard(candidates, run_date="20260707")
        guard = report.guards[0]
        self.assertEqual(guard.normalized_title, "GPT-5 | 技术架构深度解析")

    def test_empty_input(self):
        report = apply_title_guard([], run_date="20260707")
        self.assertEqual(report.total_candidates, 0)
        self.assertGreater(len(report.warnings), 0)

    def test_report_to_dict(self):
        candidates = [{"topic_id": "test", "title": "Valid Title"}]
        report = apply_title_guard(candidates, run_date="20260707")
        data = report_to_dict(report)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
