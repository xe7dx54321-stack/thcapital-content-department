import unittest

from content_system.wechat_evidence_support import (
    EvidenceSupport,
    EvidenceSupportReport,
    is_official_source,
    is_media_source,
    evaluate_evidence,
    evaluate_all_evidence,
    get_hard_evidence,
    get_soft_evidence,
    HARD_EVIDENCE_SOURCES,
)
from content_system.wechat_article_intelligence import ArticleIntelligence, IntelligenceEntity, IntelligenceAngle, IntelligenceClaim, IntelligencePattern


class TestIsOfficialSource(unittest.TestCase):
    def test_openai_is_official(self):
        self.assertTrue(is_official_source("openai", "OpenAI Official"))

    def test_anthropic_is_official(self):
        self.assertTrue(is_official_source("anthropic", "Anthropic Blog"))

    def test_google_is_official(self):
        self.assertTrue(is_official_source("google", "Google AI"))

    def test_arxiv_is_official(self):
        self.assertTrue(is_official_source("arxiv", "arXiv Papers"))

    def test_media_is_not_official(self):
        self.assertFalse(is_official_source("jiqizhixin", "机器之心"))


class TestIsMediaSource(unittest.TestCase):
    def test_tech_media(self):
        self.assertTrue(is_media_source("techweb", "TechWeb"))

    def test_news_source(self):
        self.assertTrue(is_media_source("news", "News Portal"))

    def test_公众号(self):
        self.assertTrue(is_media_source("some_public_account", "公众号名称"))

    def test_资讯_source(self):
        self.assertTrue(is_media_source("资讯网站", "资讯网站"))

    def test_official_not_media(self):
        self.assertFalse(is_media_source("openai", "OpenAI"))


class TestEvaluateEvidence(unittest.TestCase):
    def test_media_source_not_hard_evidence(self):
        intelligence = ArticleIntelligence(
            schema_version="v1",
            entry_id="test_entry",
            source_id="jiqizhixin_资讯",
            title="Test Article",
            link="https://example.com/article",
            excerpt="普通媒体报道的内容。",
            entities=(IntelligenceEntity("company", "OpenAI", 0.9),),
            angles=(IntelligenceAngle("技术深度", 0.8),),
            claims=(IntelligenceClaim("some claim", "evidence", 0.7),),
            patterns=(),
            do_not_copy_text=True,
        )
        evidence = evaluate_evidence(intelligence)
        self.assertFalse(evidence.is_hard_evidence)
        self.assertEqual(evidence.evidence_strength, "SOFT")
        self.assertIn("cannot be used as hard evidence", evidence.reliability_reason)

    def test_official_source_is_hard_evidence(self):
        intelligence = ArticleIntelligence(
            schema_version="v1",
            entry_id="test_entry",
            source_id="openai",
            title="Test Article",
            link="https://example.com/article",
            excerpt="OpenAI官方发布的内容。",
            entities=(IntelligenceEntity("company", "OpenAI", 0.9),),
            angles=(IntelligenceAngle("技术深度", 0.8),),
            claims=(IntelligenceClaim("some claim", "evidence", 0.7),),
            patterns=(),
            do_not_copy_text=True,
        )
        evidence = evaluate_evidence(intelligence)
        self.assertTrue(evidence.is_hard_evidence)
        self.assertEqual(evidence.evidence_strength, "HARD")

    def test_unknown_source_is_weak(self):
        intelligence = ArticleIntelligence(
            schema_version="v1",
            entry_id="test_entry",
            source_id="unknown_source",
            title="Test Article",
            link="https://example.com/article",
            excerpt="未知来源的内容。",
            entities=(),
            angles=(),
            claims=(),
            patterns=(),
            do_not_copy_text=True,
        )
        evidence = evaluate_evidence(intelligence)
        self.assertFalse(evidence.is_hard_evidence)
        self.assertEqual(evidence.evidence_strength, "WEAK")

    def test_official_configurable(self):
        intelligence = ArticleIntelligence(
            schema_version="v1",
            entry_id="test_entry",
            source_id="openai",
            title="Test Article",
            link="https://example.com/article",
            excerpt="内容。",
            entities=(),
            angles=(),
            claims=(),
            patterns=(),
            do_not_copy_text=True,
        )
        evidence = evaluate_evidence(intelligence)
        self.assertTrue(evidence.is_hard_evidence)
        self.assertEqual(evidence.evidence_strength, "HARD")


class TestEvaluateAllEvidence(unittest.TestCase):
    def test_evaluate_all_evidence(self):
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="openai",
                title="Official Article",
                link="https://example.com/article1",
                excerpt="OpenAI官方内容。",
                entities=(IntelligenceEntity("company", "OpenAI", 0.9),),
                angles=(),
                claims=(IntelligenceClaim("claim", "evidence", 0.7),),
                patterns=(),
                do_not_copy_text=True,
            ),
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry2",
                source_id="jiqizhixin_资讯",
                title="Media Article",
                link="https://example.com/article2",
                excerpt="媒体报道内容。",
                entities=(),
                angles=(),
                claims=(),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        report = evaluate_all_evidence(intelligence_items)
        self.assertEqual(report.input_count, 2)
        self.assertEqual(report.hard_evidence_count, 1)
        self.assertEqual(report.soft_evidence_count, 1)

    def test_empty_input(self):
        report = evaluate_all_evidence(())
        self.assertEqual(report.input_count, 0)
        self.assertEqual(report.hard_evidence_count, 0)


class TestGetHardAndSoftEvidence(unittest.TestCase):
    def test_get_hard_evidence(self):
        evidence_items = (
            EvidenceSupport(
                evidence_id="id1",
                source_id="openai",
                is_official=True,
                is_hard_evidence=True,
                evidence_strength="HARD",
                support_score=0.9,
                reliability_reason="Official",
                caveats=(),
            ),
            EvidenceSupport(
                evidence_id="id2",
                source_id="media",
                is_official=False,
                is_hard_evidence=False,
                evidence_strength="SOFT",
                support_score=0.3,
                reliability_reason="Media",
                caveats=(),
            ),
        )
        report = EvidenceSupportReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=2,
            hard_evidence_count=1,
            soft_evidence_count=1,
            unsupported_count=0,
            evidence_items=evidence_items,
            warnings=(),
        )
        hard = get_hard_evidence(report)
        self.assertEqual(len(hard), 1)
        self.assertEqual(hard[0].source_id, "openai")

    def test_get_soft_evidence(self):
        evidence_items = (
            EvidenceSupport(
                evidence_id="id1",
                source_id="openai",
                is_official=True,
                is_hard_evidence=True,
                evidence_strength="HARD",
                support_score=0.9,
                reliability_reason="Official",
                caveats=(),
            ),
            EvidenceSupport(
                evidence_id="id2",
                source_id="media",
                is_official=False,
                is_hard_evidence=False,
                evidence_strength="SOFT",
                support_score=0.3,
                reliability_reason="Media",
                caveats=(),
            ),
        )
        report = EvidenceSupportReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=2,
            hard_evidence_count=1,
            soft_evidence_count=1,
            unsupported_count=0,
            evidence_items=evidence_items,
            warnings=(),
        )
        soft = get_soft_evidence(report)
        self.assertEqual(len(soft), 1)
        self.assertEqual(soft[0].source_id, "media")


if __name__ == "__main__":
    unittest.main()