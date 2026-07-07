import unittest

from content_system.wechat_rss_usage_boundary_gate import (
    BoundaryCheckResult,
    BoundaryGateReport,
    check_no_full_text,
    check_do_not_copy_text,
    check_rate_limit,
    check_no_hard_evidence_from_media,
    check_dry_run_safety,
    run_boundary_check,
    assert_boundaries,
    BOUNDARY_RULES,
)


class TestCheckNoFullText(unittest.TestCase):
    def test_all_excerpts_within_limit(self):
        articles = [
            {"excerpt": "Short excerpt" * 10},
            {"excerpt": "Another short excerpt" * 5},
        ]
        result = check_no_full_text(articles)
        self.assertTrue(result.passed)

    def test_exceeding_limit_fails(self):
        long_excerpt = "x" * 600
        articles = [
            {"excerpt": long_excerpt},
        ]
        result = check_no_full_text(articles)
        self.assertFalse(result.passed)
        self.assertIn("full text", result.message)

    def test_empty_articles(self):
        result = check_no_full_text([])
        self.assertTrue(result.passed)


class TestCheckDoNotCopyText(unittest.TestCase):
    def test_all_have_do_not_copy_text(self):
        articles = [
            {"do_not_copy_text": True},
            {"do_not_copy_text": True},
        ]
        result = check_do_not_copy_text(articles)
        self.assertTrue(result.passed)

    def test_missing_do_not_copy_text_fails(self):
        articles = [
            {"do_not_copy_text": True},
            {"do_not_copy_text": False},
        ]
        result = check_do_not_copy_text(articles)
        self.assertFalse(result.passed)

    def test_default_false_fails(self):
        articles = [
            {"title": "Article 1"},
        ]
        result = check_do_not_copy_text(articles)
        self.assertFalse(result.passed)


class TestCheckRateLimit(unittest.TestCase):
    def test_within_limit(self):
        articles = [{} for _ in range(50)]
        result = check_rate_limit(articles)
        self.assertTrue(result.passed)

    def test_exceeds_limit(self):
        articles = [{} for _ in range(150)]
        result = check_rate_limit(articles)
        self.assertFalse(result.passed)
        self.assertIn("exceeds limit", result.message)

    def test_at_limit(self):
        articles = [{} for _ in range(100)]
        result = check_rate_limit(articles)
        self.assertTrue(result.passed)


class TestCheckNoHardEvidenceFromMedia(unittest.TestCase):
    def test_no_media_as_hard_evidence(self):
        evidence_items = [
            {"is_hard_evidence": True, "source_id": "openai"},
            {"is_hard_evidence": False, "source_id": "jiqizhixin"},
        ]
        result = check_no_hard_evidence_from_media(evidence_items)
        self.assertTrue(result.passed)

    def test_media_marked_as_hard_evidence_fails(self):
        evidence_items = [
            {"is_hard_evidence": True, "source_id": "tech_news_公众号"},
        ]
        result = check_no_hard_evidence_from_media(evidence_items)
        self.assertFalse(result.passed)
        self.assertIn("media source", result.message)


class TestCheckDryRunSafety(unittest.TestCase):
    def test_dry_run_mode(self):
        result = check_dry_run_safety(True)
        self.assertTrue(result.passed)
        self.assertIn("Dry-run mode", result.message)

    def test_live_mode(self):
        result = check_dry_run_safety(False)
        self.assertTrue(result.passed)
        self.assertIn("Live mode", result.message)


class TestRunBoundaryCheck(unittest.TestCase):
    def test_all_checks_pass(self):
        articles = [
            {"excerpt": "Short excerpt", "do_not_copy_text": True},
            {"excerpt": "Another excerpt", "do_not_copy_text": True},
        ]
        evidence_items = [
            {"is_hard_evidence": True, "source_id": "openai"},
            {"is_hard_evidence": False, "source_id": "media"},
        ]
        report = run_boundary_check(articles=articles, evidence_items=evidence_items, dry_run=True)
        self.assertTrue(report.all_passed)
        self.assertEqual(len(report.check_results), 5)

    def test_some_checks_fail(self):
        articles = [
            {"excerpt": "x" * 600, "do_not_copy_text": False},
        ]
        report = run_boundary_check(articles=articles, dry_run=True)
        self.assertFalse(report.all_passed)
        self.assertGreater(len(report.warnings), 0)

    def test_direct_republication_intercepted(self):
        articles = [
            {"excerpt": "x" * 600, "do_not_copy_text": False},
        ]
        report = run_boundary_check(articles=articles, dry_run=True)
        self.assertFalse(report.all_passed)
        no_full_text_result = next(r for r in report.check_results if r.rule_id == "no_full_text")
        do_not_copy_result = next(r for r in report.check_results if r.rule_id == "do_not_copy_text")
        self.assertFalse(no_full_text_result.passed)
        self.assertFalse(do_not_copy_result.passed)

    def test_long_quote_not_allowed(self):
        articles = [
            {"excerpt": '引用："' + "x" * 600 + '"', "do_not_copy_text": True},
        ]
        report = run_boundary_check(articles=articles, dry_run=True)
        no_full_text_result = next(r for r in report.check_results if r.rule_id == "no_full_text")
        self.assertFalse(no_full_text_result.passed)


class TestAssertBoundaries(unittest.TestCase):
    def test_assert_boundaries_pass(self):
        report = BoundaryGateReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            dry_run=True,
            all_passed=True,
            check_results=(),
            warnings=(),
        )
        assert_boundaries(report)

    def test_assert_boundaries_fail(self):
        report = BoundaryGateReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            dry_run=True,
            all_passed=False,
            check_results=(
                BoundaryCheckResult("test_rule", False, "Test failure", {}),
            ),
            warnings=(),
        )
        with self.assertRaises(RuntimeError):
            assert_boundaries(report)


class TestBoundaryRules(unittest.TestCase):
    def test_no_full_text_rule_exists(self):
        self.assertIn("no_full_text", BOUNDARY_RULES)

    def test_do_not_copy_text_rule_exists(self):
        self.assertIn("do_not_copy_text", BOUNDARY_RULES)

    def test_no_hard_evidence_from_media_rule_exists(self):
        self.assertIn("no_hard_evidence_from_media", BOUNDARY_RULES)

    def test_rate_limit_rule_exists(self):
        self.assertIn("rate_limit", BOUNDARY_RULES)


if __name__ == "__main__":
    unittest.main()