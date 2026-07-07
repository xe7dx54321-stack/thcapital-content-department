import unittest

from content_system.competitive_coverage_penalty import (
    CompetitiveCoveragePenaltyReport,
    CompetitivePenalty,
    apply_competitive_penalty,
    report_to_dict,
    classify_topic,
)


class TestCompetitiveCoveragePenalty(unittest.TestCase):
    def test_classify_topic_llm(self):
        topics = classify_topic("GPT-5技术架构解析")
        self.assertIn("LLM/大模型", topics)

    def test_classify_topic_infrastructure(self):
        topics = classify_topic("NVIDIA GPU算力分析")
        self.assertIn("AI基础设施", topics)

    def test_classify_topic_agent(self):
        topics = classify_topic("多智能体系统应用")
        self.assertIn("Agent/智能体", topics)

    def test_classify_topic_multiple(self):
        topics = classify_topic("大模型应用落地与安全问题")
        self.assertIn("LLM/大模型", topics)
        self.assertIn("AI应用", topics)
        self.assertIn("AI安全", topics)

    def test_high_coverage_penalty(self):
        candidates = [
            {
                "topic_id": "test_001",
                "title": "GPT-5发布深度解析",
                "angle_type": "technical",
            }
        ]
        coverage_report = {
            "analysis": {
                "topic_coverage": [
                    {
                        "topic_name": "LLM/大模型",
                        "source_count": 5,
                        "article_count": 10,
                        "coverage_score": 0.75,
                    }
                ]
            }
        }
        report = apply_competitive_penalty(candidates, coverage_report, run_date="20260707")
        self.assertEqual(report.total_penalties, 1)
        penalty = report.penalties[0]
        self.assertEqual(penalty.topic_id, "test_001")
        self.assertGreater(penalty.penalty, 0)

    def test_same_angle_risk(self):
        candidates = [
            {
                "topic_id": "test_001",
                "title": "GPT-5技术架构",
                "angle_type": "technical",
            }
        ]
        coverage_report = {
            "analysis": {
                "topic_coverage": [
                    {
                        "topic_name": "LLM/大模型",
                        "source_count": 5,
                        "article_count": 10,
                        "coverage_score": 0.75,
                    }
                ]
            }
        }
        report = apply_competitive_penalty(candidates, coverage_report, run_date="20260707")
        penalty = report.penalties[0]
        self.assertTrue(penalty.same_angle_risk)
        self.assertGreater(penalty.penalty, 0.14)

    def test_no_angle_risk_with_few_competitors(self):
        candidates = [
            {
                "topic_id": "test_001",
                "title": "GPT-5技术架构",
                "angle_type": "technical",
            }
        ]
        coverage_report = {
            "analysis": {
                "topic_coverage": [
                    {
                        "topic_name": "LLM/大模型",
                        "source_count": 2,
                        "article_count": 3,
                        "coverage_score": 0.55,
                    }
                ]
            }
        }
        report = apply_competitive_penalty(candidates, coverage_report, run_date="20260707")
        penalty = report.penalties[0]
        self.assertFalse(penalty.same_angle_risk)

    def test_low_coverage_no_penalty(self):
        candidates = [
            {
                "topic_id": "test_001",
                "title": "GPT-5技术架构",
            }
        ]
        coverage_report = {
            "analysis": {
                "topic_coverage": [
                    {
                        "topic_name": "LLM/大模型",
                        "source_count": 2,
                        "article_count": 3,
                        "coverage_score": 0.30,
                    }
                ]
            }
        }
        report = apply_competitive_penalty(candidates, coverage_report, run_date="20260707")
        self.assertEqual(report.total_penalties, 0)

    def test_no_coverage_report(self):
        candidates = [
            {"topic_id": "test_001", "title": "GPT-5技术架构"}
        ]
        report = apply_competitive_penalty(candidates, None, run_date="20260707")
        self.assertEqual(report.total_penalties, 0)

    def test_empty_input(self):
        report = apply_competitive_penalty([], run_date="20260707")
        self.assertEqual(report.total_penalties, 0)
        self.assertGreater(len(report.warnings), 0)

    def test_report_to_dict(self):
        candidates = [{"topic_id": "test", "title": "GPT-5"}]
        coverage_report = {
            "analysis": {
                "topic_coverage": [
                    {"topic_name": "LLM/大模型", "source_count": 5, "article_count": 10, "coverage_score": 0.75}
                ]
            }
        }
        report = apply_competitive_penalty(candidates, coverage_report, run_date="20260707")
        data = report_to_dict(report)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
