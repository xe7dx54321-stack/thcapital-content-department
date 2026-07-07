import unittest

from content_system.differentiated_angle_recommender import (
    AngleRecommendation,
    AngleReport,
    AngleRecommendationReport,
    recommend_angles,
    recommend_all_angles,
    DIFFERENTIATED_ANGLES,
)
from content_system.wechat_article_intelligence import ArticleIntelligence, IntelligenceEntity, IntelligenceAngle, IntelligenceClaim, IntelligencePattern


class TestRecommendAngles(unittest.TestCase):
    def test_recommend_angles_basic(self):
        intelligence = ArticleIntelligence(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            title="GPT-4技术架构深度解析",
            link="https://example.com/article",
            excerpt="GPT-4采用了全新的技术架构，性能大幅提升，市场反应积极。",
            entities=(IntelligenceEntity("company", "OpenAI", 0.9),),
            angles=(IntelligenceAngle("技术深度", 0.8),),
            claims=(IntelligenceClaim("性能大幅提升", "evidence", 0.7),),
            patterns=(),
            do_not_copy_text=True,
        )
        recommendations = recommend_angles(intelligence)
        self.assertGreater(len(recommendations), 0)
        self.assertTrue(all(isinstance(r, AngleRecommendation) for r in recommendations))

    def test_recommend_technical_angle(self):
        intelligence = ArticleIntelligence(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            title="技术实现分析",
            link="https://example.com/article",
            excerpt="深入分析技术实现细节和架构设计原理。",
            entities=(),
            angles=(),
            claims=(),
            patterns=(),
            do_not_copy_text=True,
        )
        recommendations = recommend_angles(intelligence)
        angle_names = [r.angle_name for r in recommendations]
        self.assertIn("技术实现角度", angle_names)

    def test_recommend_business_angle(self):
        intelligence = ArticleIntelligence(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            title="商业价值评估",
            link="https://example.com/article",
            excerpt="评估商业价值和市场潜力，分析商业模式和变现途径。",
            entities=(),
            angles=(),
            claims=(),
            patterns=(),
            do_not_copy_text=True,
        )
        recommendations = recommend_angles(intelligence)
        angle_names = [r.angle_name for r in recommendations]
        self.assertIn("商业价值角度", angle_names)

    def test_recommend_multiple_angles(self):
        intelligence = ArticleIntelligence(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            title="AI趋势分析",
            link="https://example.com/article",
            excerpt="分析行业发展趋势，对比竞品差异，展望未来前景。",
            entities=(),
            angles=(),
            claims=(),
            patterns=(),
            do_not_copy_text=True,
        )
        recommendations = recommend_angles(intelligence)
        angle_names = [r.angle_name for r in recommendations]
        self.assertIn("行业影响角度", angle_names)
        self.assertIn("对比分析角度", angle_names)
        self.assertIn("未来展望角度", angle_names)

    def test_at_least_11_angles_available(self):
        self.assertGreaterEqual(len(DIFFERENTIATED_ANGLES), 11)

    def test_15_angles_available(self):
        self.assertEqual(len(DIFFERENTIATED_ANGLES), 15)


class TestRecommendAllAngles(unittest.TestCase):
    def test_recommend_all_angles(self):
        intelligence_items = (
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry1",
                source_id="source1",
                title="Article 1",
                link="https://example.com/article1",
                excerpt="技术分析内容",
                entities=(),
                angles=(),
                claims=(),
                patterns=(),
                do_not_copy_text=True,
            ),
            ArticleIntelligence(
                schema_version="v1",
                entry_id="entry2",
                source_id="source2",
                title="Article 2",
                link="https://example.com/article2",
                excerpt="商业分析内容",
                entities=(),
                angles=(),
                claims=(),
                patterns=(),
                do_not_copy_text=True,
            ),
        )
        report = recommend_all_angles(intelligence_items)
        self.assertEqual(report.input_count, 2)
        self.assertEqual(len(report.reports), 2)

    def test_empty_input(self):
        report = recommend_all_angles(())
        self.assertEqual(report.input_count, 0)
        self.assertEqual(len(report.reports), 0)


if __name__ == "__main__":
    unittest.main()