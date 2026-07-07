import unittest

from content_system.wechat_intelligence_integration import (
    WechatTopicScore,
    WechatTopicScoringReport,
    WechatContentBrief,
    WechatBriefReport,
    make_topic_id,
    score_band_for,
    editorial_priority_for,
    score_topics,
    build_briefs,
)
from content_system.wechat_article_intelligence import (
    IntelligenceReport,
    ArticleIntelligence,
    IntelligenceEntity,
    IntelligenceAngle,
    IntelligenceClaim,
    IntelligencePattern,
)
from content_system.wechat_evidence_support import (
    EvidenceSupportReport,
    EvidenceSupport,
)
from content_system.differentiated_angle_recommender import (
    AngleRecommendationReport,
    AngleReport,
    AngleRecommendation,
)


class TestMakeTopicId(unittest.TestCase):
    def test_make_topic_id(self):
        topic_id = make_topic_id("Test Article Title")
        self.assertIsInstance(topic_id, str)
        self.assertTrue(topic_id.startswith("topic_"))
        self.assertEqual(len(topic_id), len("topic_") + 12)

    def test_topic_id_consistency(self):
        id1 = make_topic_id("Test Article Title")
        id2 = make_topic_id("Test Article Title")
        self.assertEqual(id1, id2)


class TestScoreBandFor(unittest.TestCase):
    def test_score_band_a(self):
        band = score_band_for(85)
        self.assertEqual(band, "A")

    def test_score_band_b(self):
        band = score_band_for(70)
        self.assertEqual(band, "B")

    def test_score_band_c(self):
        band = score_band_for(55)
        self.assertEqual(band, "C")

    def test_score_band_d(self):
        band = score_band_for(45)
        self.assertEqual(band, "D")


class TestEditorialPriorityFor(unittest.TestCase):
    def test_priority_high(self):
        priority = editorial_priority_for("A")
        self.assertEqual(priority, "HIGH")

    def test_priority_medium(self):
        priority = editorial_priority_for("B")
        self.assertEqual(priority, "MEDIUM")

    def test_priority_low(self):
        priority = editorial_priority_for("C")
        self.assertEqual(priority, "LOW")

    def test_priority_low_for_d(self):
        priority = editorial_priority_for("D")
        self.assertEqual(priority, "LOW")


class TestScoreTopics(unittest.TestCase):
    def test_score_topics_basic(self):
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="source1",
                title="GPT-4 Release",
                link="https://example.com/article1",
                excerpt="OpenAI releases GPT-4 with improved performance.",
                entities=(IntelligenceEntity("company", "OpenAI", 0.9),),
                angles=(IntelligenceAngle("技术深度", 0.8),),
                claims=(IntelligenceClaim("improved performance", "evidence", 0.7),),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        intelligence_report = IntelligenceReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=1,
            output_count=1,
            items=intelligence_items,
            warnings=(),
        )
        evidence_items = (
            EvidenceSupport(
                evidence_id="entry1",
                source_id="source1",
                is_official=False,
                is_hard_evidence=False,
                evidence_strength="SOFT",
                support_score=0.3,
                reliability_reason="Media source",
                caveats=(),
            ),
        )
        evidence_report = EvidenceSupportReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=1,
            hard_evidence_count=0,
            soft_evidence_count=1,
            unsupported_count=0,
            evidence_items=evidence_items,
            warnings=(),
        )
        scoring_report = score_topics(intelligence_report, evidence_report)
        self.assertEqual(scoring_report.topic_count, 1)
        self.assertEqual(scoring_report.topics[0].title, "GPT-4 Release")
        self.assertGreater(scoring_report.topics[0].total_score, 0)

    def test_score_topics_with_hard_evidence(self):
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="openai",
                title="GPT-4 Release",
                link="https://example.com/article1",
                excerpt="OpenAI officially releases GPT-4.",
                entities=(IntelligenceEntity("company", "OpenAI", 0.9),),
                angles=(IntelligenceAngle("技术深度", 0.8),),
                claims=(IntelligenceClaim("officially releases", "evidence", 0.7),),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        intelligence_report = IntelligenceReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=1,
            output_count=1,
            items=intelligence_items,
            warnings=(),
        )
        evidence_items = (
            EvidenceSupport(
                evidence_id="entry1",
                source_id="openai",
                is_official=True,
                is_hard_evidence=True,
                evidence_strength="HARD",
                support_score=0.9,
                reliability_reason="Official source",
                caveats=(),
            ),
        )
        evidence_report = EvidenceSupportReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=1,
            hard_evidence_count=1,
            soft_evidence_count=0,
            unsupported_count=0,
            evidence_items=evidence_items,
            warnings=(),
        )
        scoring_report = score_topics(intelligence_report, evidence_report)
        self.assertEqual(scoring_report.topics[0].hard_evidence_count, 1)
        self.assertGreater(scoring_report.topics[0].evidence_score, 30)

    def test_do_not_copy_text_preserved(self):
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="source1",
                title="Test Topic",
                link="https://example.com/article1",
                excerpt="Test content",
                entities=(),
                angles=(),
                claims=(),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        intelligence_report = IntelligenceReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=1,
            output_count=1,
            items=intelligence_items,
            warnings=(),
        )
        evidence_items = (
            EvidenceSupport(
                evidence_id="entry1",
                source_id="source1",
                is_official=False,
                is_hard_evidence=False,
                evidence_strength="SOFT",
                support_score=0.3,
                reliability_reason="Media source",
                caveats=(),
            ),
        )
        evidence_report = EvidenceSupportReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=1,
            hard_evidence_count=0,
            soft_evidence_count=1,
            unsupported_count=0,
            evidence_items=evidence_items,
            warnings=(),
        )
        scoring_report = score_topics(intelligence_report, evidence_report)
        self.assertTrue(scoring_report.topics[0].do_not_copy_text)


class TestBuildBriefs(unittest.TestCase):
    def test_build_briefs_basic(self):
        topics = (
            WechatTopicScore(
                topic_id="topic_test123",
                title="GPT-4 Release",
                source_count=2,
                evidence_count=2,
                hard_evidence_count=1,
                entity_count=2,
                angle_count=3,
                claim_count=2,
                intelligence_score=50.0,
                evidence_score=60.0,
                freshness_score=80.0,
                total_score=62.0,
                score_band="B",
                do_not_copy_text=True,
            ),
        )
        scoring_report = WechatTopicScoringReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            topic_count=1,
            topics=topics,
            warnings=(),
        )
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="source1",
                title="GPT-4 Release",
                link="https://example.com/article1",
                excerpt="OpenAI releases GPT-4.",
                entities=(IntelligenceEntity("company", "OpenAI", 0.9),),
                angles=(),
                claims=(IntelligenceClaim("releases GPT-4", "evidence", 0.7),),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        intelligence_report = IntelligenceReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=1,
            output_count=1,
            items=intelligence_items,
            warnings=(),
        )
        angle_reports = (
            AngleReport(
                schema_version="v1",
                run_date="20240115",
                entry_id="entry1",
                title="GPT-4 Release",
                recommended_angles=(
                    AngleRecommendation("技术深度", 0.8, "Technical analysis", ("技术",)),
                ),
                top_angle="技术深度",
            ),
        )
        angle_report = AngleRecommendationReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=1,
            reports=angle_reports,
            warnings=(),
        )
        brief_report = build_briefs(scoring_report, intelligence_report, angle_report)
        self.assertEqual(brief_report.brief_count, 1)
        self.assertEqual(brief_report.briefs[0].title, "GPT-4 Release")
        self.assertEqual(brief_report.briefs[0].score_band, "B")

    def test_build_briefs_skips_d_band(self):
        topics = (
            WechatTopicScore(
                topic_id="topic_test123",
                title="Low Quality Topic",
                source_count=1,
                evidence_count=1,
                hard_evidence_count=0,
                entity_count=0,
                angle_count=0,
                claim_count=0,
                intelligence_score=20.0,
                evidence_score=20.0,
                freshness_score=80.0,
                total_score=32.0,
                score_band="D",
                do_not_copy_text=True,
            ),
        )
        scoring_report = WechatTopicScoringReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            topic_count=1,
            topics=topics,
            warnings=(),
        )
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="source1",
                title="Low Quality Topic",
                link="https://example.com/article1",
                excerpt="Low quality content.",
                entities=(),
                angles=(),
                claims=(),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        intelligence_report = IntelligenceReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=1,
            output_count=1,
            items=intelligence_items,
            warnings=(),
        )
        angle_report = AngleRecommendationReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=0,
            reports=(),
            warnings=(),
        )
        brief_report = build_briefs(scoring_report, intelligence_report, angle_report)
        self.assertEqual(brief_report.brief_count, 0)

    def test_do_not_copy_text_preserved_in_briefs(self):
        topics = (
            WechatTopicScore(
                topic_id="topic_test123",
                title="Test Topic",
                source_count=1,
                evidence_count=1,
                hard_evidence_count=0,
                entity_count=1,
                angle_count=1,
                claim_count=1,
                intelligence_score=40.0,
                evidence_score=40.0,
                freshness_score=80.0,
                total_score=48.0,
                score_band="C",
                do_not_copy_text=True,
            ),
        )
        scoring_report = WechatTopicScoringReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            topic_count=1,
            topics=topics,
            warnings=(),
        )
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="source1",
                title="Test Topic",
                link="https://example.com/article1",
                excerpt="Test content.",
                entities=(IntelligenceEntity("company", "OpenAI", 0.9),),
                angles=(),
                claims=(IntelligenceClaim("test claim", "evidence", 0.7),),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        intelligence_report = IntelligenceReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=1,
            output_count=1,
            items=intelligence_items,
            warnings=(),
        )
        angle_report = AngleRecommendationReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=0,
            reports=(),
            warnings=(),
        )
        brief_report = build_briefs(scoring_report, intelligence_report, angle_report)
        self.assertTrue(brief_report.briefs[0].do_not_copy_text)


if __name__ == "__main__":
    unittest.main()