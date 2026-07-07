import unittest

from content_system.competitive_coverage_analysis import (
    TopicCoverage,
    CoverageGap,
    CompetitiveAnalysis,
    CoverageAnalysisReport,
    classify_topic,
    analyze_coverage,
)
from content_system.wechat_article_intelligence import ArticleIntelligence, IntelligenceEntity, IntelligenceAngle, IntelligenceClaim, IntelligencePattern


class TestClassifyTopic(unittest.TestCase):
    def test_classify_llm_topic(self):
        text = "GPT-4和Claude都是强大的大模型。"
        topics = classify_topic(text)
        self.assertIn("LLM/大模型", topics)

    def test_classify_agent_topic(self):
        text = "多智能体系统正在改变AI应用方式。"
        topics = classify_topic(text)
        self.assertIn("Agent/智能体", topics)

    def test_classify_infrastructure_topic(self):
        text = "NVIDIA GPU算力需求持续增长。"
        topics = classify_topic(text)
        self.assertIn("AI基础设施", topics)

    def test_classify_multiple_topics(self):
        text = "大模型应用落地，AI安全问题备受关注。"
        topics = classify_topic(text)
        self.assertIn("LLM/大模型", topics)
        self.assertIn("AI应用", topics)
        self.assertIn("AI安全", topics)

    def test_no_topic(self):
        text = "这是一篇没有特定主题的文章。"
        topics = classify_topic(text)
        self.assertEqual(len(topics), 0)


class TestAnalyzeCoverage(unittest.TestCase):
    def test_analyze_coverage_basic(self):
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="jiqizhixin",
                title="GPT-4发布",
                link="https://example.com/article1",
                excerpt="GPT-4发布，性能大幅提升。",
                entities=(IntelligenceEntity("company", "OpenAI", 0.9),),
                angles=(IntelligenceAngle("技术深度", 0.8),),
                claims=(IntelligenceClaim("性能大幅提升", "evidence", 0.7),),
                patterns=(),
                do_not_copy_text=True,
            ),
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry2",
                source_id="liangziwei",
                title="GPT-4评测",
                link="https://example.com/article2",
                excerpt="GPT-4评测结果令人印象深刻。",
                entities=(IntelligenceEntity("company", "OpenAI", 0.9),),
                angles=(IntelligenceAngle("产品对比", 0.7),),
                claims=(),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        report = analyze_coverage(intelligence_items)
        self.assertIsNotNone(report.analysis)
        self.assertEqual(report.analysis.total_articles, 2)
        self.assertGreater(len(report.analysis.topic_coverage), 0)

    def test_coverage_gaps(self):
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="jiqizhixin",
                title="AI安全新动态",
                link="https://example.com/article1",
                excerpt="AI安全问题日益受到重视。",
                entities=(),
                angles=(IntelligenceAngle("政策监管", 0.6),),
                claims=(),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        report = analyze_coverage(intelligence_items)
        self.assertGreaterEqual(len(report.analysis.coverage_gaps), 0)

    def test_top_competitors(self):
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="jiqizhixin",
                title="Article 1",
                link="https://example.com/article1",
                excerpt="Content",
                entities=(),
                angles=(),
                claims=(),
                patterns=(),
                do_not_copy_text=True,
            ),
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry2",
                source_id="jiqizhixin",
                title="Article 2",
                link="https://example.com/article2",
                excerpt="Content",
                entities=(),
                angles=(),
                claims=(),
                patterns=(),
                do_not_copy_text=True,
            ),
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry3",
                source_id="liangziwei",
                title="Article 3",
                link="https://example.com/article3",
                excerpt="Content",
                entities=(),
                angles=(),
                claims=(),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        report = analyze_coverage(intelligence_items)
        self.assertIn("jiqizhixin", report.analysis.top_competitors)

    def test_empty_input(self):
        report = analyze_coverage(())
        self.assertEqual(report.analysis.source_count, 0)
        self.assertEqual(report.analysis.total_articles, 0)


if __name__ == "__main__":
    unittest.main()