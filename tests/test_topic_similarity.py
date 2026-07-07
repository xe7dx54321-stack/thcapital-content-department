import unittest

from content_system.topic_similarity import (
    TopicSimilarityReport,
    SimilarityMatch,
    analyze_topic_similarity,
    report_to_dict,
    write_report,
    load_report,
    title_similarity_score,
    normalized_title_similarity,
    jaccard_similarity,
)


class TestTopicSimilarity(unittest.TestCase):
    def test_hard_duplicate_detection(self):
        candidates = [
            {
                "topic_id": "candidate_001",
                "title": "OpenAI发布GPT-5技术细节分析",
                "companies": ["OpenAI"],
                "products": ["GPT-5"],
                "event_type": "model_release",
                "normalized_title": "openai 发布 gpt-5 技术细节分析",
            }
        ]
        historical_topics = [
            {
                "topic_id": "history_001",
                "title": "OpenAI发布GPT-5技术细节分析",
                "run_date": "20260706",
                "companies": ["OpenAI"],
                "products": ["GPT-5"],
                "event_type": "model_release",
                "normalized_title": "openai 发布 gpt-5 技术细节分析",
            }
        ]
        report = analyze_topic_similarity(candidates, historical_topics, run_date="20260707")
        self.assertEqual(report.hard_duplicate_count, 1)
        self.assertEqual(report.similar_count, 1)
        self.assertTrue(report.similarity_matches[0].is_hard_duplicate)
        self.assertTrue(report.similarity_matches[0].is_similar)

    def test_similar_topics_with_different_angle(self):
        candidates = [
            {
                "topic_id": "candidate_002",
                "title": "GPT-5性能评测与竞品对比",
                "companies": ["OpenAI"],
                "products": ["GPT-5"],
                "event_type": "model_release",
                "angle_type": "comparison",
                "normalized_title": "gpt-5 性能评测 与 竞品对比",
            }
        ]
        historical_topics = [
            {
                "topic_id": "history_002",
                "title": "OpenAI发布GPT-5技术细节分析",
                "run_date": "20260706",
                "companies": ["OpenAI"],
                "products": ["GPT-5"],
                "event_type": "model_release",
                "angle_type": "technical",
                "normalized_title": "openai 发布 gpt-5 技术细节分析",
            }
        ]
        report = analyze_topic_similarity(candidates, historical_topics, run_date="20260707")
        self.assertEqual(report.hard_duplicate_count, 0)
        self.assertEqual(report.similar_count, 1)
        self.assertFalse(report.similarity_matches[0].is_hard_duplicate)
        self.assertTrue(report.similarity_matches[0].is_similar)

    def test_reuires_new_angle_scenario(self):
        candidates = [
            {
                "topic_id": "candidate_new_angle",
                "title": "GPT-5企业级应用落地挑战与解决方案",
                "companies": ["OpenAI"],
                "products": ["GPT-5"],
                "event_type": "model_release",
                "angle_type": "enterprise",
                "normalized_title": "gpt-5 企业级 应用 落地 挑战 与 解决方案",
            }
        ]
        historical_topics = [
            {
                "topic_id": "history_old_angle",
                "title": "OpenAI发布GPT-5技术架构深度解析",
                "run_date": "20260706",
                "companies": ["OpenAI"],
                "products": ["GPT-5"],
                "event_type": "model_release",
                "angle_type": "technical",
                "normalized_title": "openai 发布 gpt-5 技术 架构 深度 解析",
            }
        ]
        report = analyze_topic_similarity(candidates, historical_topics, run_date="20260707")
        self.assertGreater(report.similar_count, 0)
        match = report.similarity_matches[0]
        self.assertFalse(match.is_hard_duplicate)
        self.assertTrue(match.is_similar)
        self.assertNotEqual(match.angle_type_match, True)

    def test_no_similar_topics(self):
        candidates = [
            {
                "topic_id": "candidate_unique",
                "title": "全新AI创业公司获千万融资",
                "companies": ["NewAI"],
                "products": ["AIProduct"],
                "event_type": "funding",
            }
        ]
        historical_topics = [
            {
                "topic_id": "history_unrelated",
                "title": "GPT-5技术架构深度解析",
                "run_date": "20260706",
                "companies": ["OpenAI"],
                "products": ["GPT-5"],
                "event_type": "model_release",
            }
        ]
        report = analyze_topic_similarity(candidates, historical_topics, run_date="20260707")
        self.assertEqual(report.similar_count, 0)
        self.assertEqual(report.hard_duplicate_count, 0)

    def test_title_similarity_score(self):
        score = title_similarity_score("GPT-5发布", "GPT-5技术发布")
        self.assertGreater(score, 0.5)
        score = title_similarity_score("GPT-5发布", "NVIDIA新GPU")
        self.assertLess(score, 0.3)

    def test_normalized_title_similarity(self):
        score = normalized_title_similarity("GPT-5发布", "GPT-5技术发布")
        self.assertGreater(score, 0.7)

    def test_jaccard_similarity(self):
        score = jaccard_similarity({"a", "b", "c"}, {"a", "b", "d"})
        self.assertEqual(score, 0.5)

    def test_report_to_dict(self):
        candidates = [{"topic_id": "test", "title": "Test"}]
        historical = [{"topic_id": "hist", "title": "Test", "run_date": "20260706"}]
        report = analyze_topic_similarity(candidates, historical, run_date="20260707")
        data = report_to_dict(report)
        self.assertIsInstance(data, dict)

    def test_empty_inputs(self):
        report = analyze_topic_similarity([], [], run_date="20260707")
        self.assertEqual(report.candidate_count, 0)
        self.assertEqual(report.historical_topic_count, 0)
        self.assertGreater(len(report.warnings), 0)


if __name__ == "__main__":
    unittest.main()
