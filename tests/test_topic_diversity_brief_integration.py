import unittest

from content_system.topic_diversity_brief_integration import (
    BriefIntegrationReport,
    DiversityInsight,
    build_diversity_insights,
    generate_brief_update,
    report_to_dict,
)


class TestTopicDiversityBriefIntegration(unittest.TestCase):
    def test_build_diversity_insights_basic(self):
        candidates = [
            {"topic_id": "test_001", "title": "Test Topic"}
        ]
        report = build_diversity_insights(candidates, run_date="20260707")
        self.assertIsInstance(report, BriefIntegrationReport)
        self.assertEqual(report.total_topics, 1)
        self.assertEqual(report.topics_with_angle, 0)
        self.assertEqual(report.topics_with_risk, 0)

    def test_build_diversity_insights_with_angle(self):
        candidates = [
            {"topic_id": "test_001", "title": "Test Topic"}
        ]
        angle_report = {
            "boosts": [
                {
                    "topic_id": "test_001",
                    "boost_type": "strong_differentiated_angle",
                    "boost_value": 0.12,
                    "angle_name": "技术实现角度",
                    "confidence": 0.85,
                    "description": "深入分析技术实现细节",
                }
            ]
        }
        report = build_diversity_insights(candidates, angle_report=angle_report, run_date="20260707")
        self.assertEqual(report.topics_with_angle, 1)
        insight = report.insights[0]
        self.assertEqual(insight.recommended_angle, "技术实现角度")
        self.assertEqual(insight.angle_description, "深入分析技术实现细节")
        self.assertEqual(insight.angle_confidence, 0.85)

    def test_build_diversity_insights_with_similarity(self):
        candidates = [
            {"topic_id": "test_001", "title": "Test Topic"}
        ]
        similarity_report = {
            "similarity_matches": [
                {
                    "topic_id": "test_001",
                    "similar_to_title": "Similar Topic",
                    "similar_to_date": "20260706",
                    "combined_score": 0.80,
                    "is_hard_duplicate": False,
                }
            ]
        }
        report = build_diversity_insights(candidates, similarity_report=similarity_report, run_date="20260707")
        self.assertEqual(report.topics_with_risk, 1)
        insight = report.insights[0]
        self.assertEqual(insight.duplication_risk_level, "MEDIUM")
        self.assertIn("相似选题", insight.duplication_risk_details)

    def test_build_diversity_insights_with_hard_duplicate(self):
        candidates = [
            {"topic_id": "test_001", "title": "Test Topic"}
        ]
        similarity_report = {
            "similarity_matches": [
                {
                    "topic_id": "test_001",
                    "similar_to_title": "Test Topic",
                    "similar_to_date": "20260706",
                    "combined_score": 0.95,
                    "is_hard_duplicate": True,
                }
            ]
        }
        report = build_diversity_insights(candidates, similarity_report=similarity_report, run_date="20260707")
        insight = report.insights[0]
        self.assertEqual(insight.duplication_risk_level, "HIGH")
        self.assertIn("硬重复", insight.duplication_risk_details)

    def test_build_diversity_insights_with_diversity_score(self):
        candidates = [
            {"topic_id": "test_001", "title": "Test Topic"}
        ]
        diversity_report = {
            "diversity_scores": [
                {"topic_id": "test_001", "diversity_adjusted_score": 0.85, "diversity_status": "BOOSTED"}
            ]
        }
        report = build_diversity_insights(candidates, diversity_report=diversity_report, run_date="20260707")
        insight = report.insights[0]
        self.assertEqual(insight.diversity_score, 0.85)
        self.assertEqual(insight.diversity_status, "BOOSTED")

    def test_generate_brief_update_with_angle(self):
        insight = DiversityInsight(
            topic_id="test_001",
            recommended_angle="技术实现角度",
            angle_description="深入分析技术实现细节",
            angle_confidence=0.85,
            duplication_risk_level="LOW",
            duplication_risk_details="无重复风险",
            diversity_score=0.85,
            diversity_status="BOOSTED",
        )
        update = generate_brief_update(insight)
        self.assertEqual(update["diversity_recommended_angle"], "技术实现角度")
        self.assertEqual(update["diversity_angle_description"], "深入分析技术实现细节")
        self.assertEqual(update["diversity_angle_confidence"], 0.85)
        self.assertEqual(update["diversity_duplication_risk_level"], "LOW")
        self.assertEqual(update["diversity_score"], 0.85)
        self.assertEqual(update["diversity_status"], "BOOSTED")

    def test_generate_brief_update_with_original_brief(self):
        insight = DiversityInsight(
            topic_id="test_001",
            recommended_angle=None,
            angle_description=None,
            angle_confidence=0.0,
            duplication_risk_level="LOW",
            duplication_risk_details="无重复风险",
            diversity_score=0.80,
            diversity_status="NEUTRAL",
        )
        original_brief = {"title": "Original Brief", "content": "Some content"}
        update = generate_brief_update(insight, original_brief)
        self.assertEqual(update["title"], "Original Brief")
        self.assertEqual(update["content"], "Some content")
        self.assertIn("diversity_duplication_risk_level", update)

    def test_empty_input(self):
        report = build_diversity_insights([], run_date="20260707")
        self.assertEqual(report.total_topics, 0)
        self.assertGreater(len(report.warnings), 0)

    def test_report_to_dict(self):
        candidates = [{"topic_id": "test", "title": "Test"}]
        report = build_diversity_insights(candidates, run_date="20260707")
        data = report_to_dict(report)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
