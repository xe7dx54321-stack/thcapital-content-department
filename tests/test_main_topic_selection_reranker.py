import unittest

from content_system.main_topic_selection_reranker import (
    TopicRerankingReport,
    RerankedTopic,
    rerank_topics,
    report_to_dict,
)


class TestMainTopicSelectionReranker(unittest.TestCase):
    def test_rerank_topics_basic(self):
        candidates = [
            {"topic_id": "t1", "title": "Topic 1", "score": 0.90},
            {"topic_id": "t2", "title": "Topic 2", "score": 0.85},
            {"topic_id": "t3", "title": "Topic 3", "score": 0.80},
        ]
        report = rerank_topics(candidates, run_date="20260707")
        self.assertIsInstance(report, TopicRerankingReport)
        self.assertEqual(report.total_candidates, 3)
        self.assertEqual(report.rank_changed_count, 0)

    def test_rerank_topics_with_diversity_scores(self):
        candidates = [
            {"topic_id": "t1", "title": "Topic 1", "score": 0.90},
            {"topic_id": "t2", "title": "Topic 2", "score": 0.85},
            {"topic_id": "t3", "title": "Topic 3", "score": 0.80},
        ]
        diversity_report = {
            "diversity_scores": [
                {"topic_id": "t1", "diversity_adjusted_score": 0.70},
                {"topic_id": "t2", "diversity_adjusted_score": 0.95},
                {"topic_id": "t3", "diversity_adjusted_score": 0.85},
            ]
        }
        report = rerank_topics(candidates, diversity_report, run_date="20260707")
        self.assertGreater(report.rank_changed_count, 0)
        self.assertEqual(report.reranked_topics[0].topic_id, "t2")
        self.assertEqual(report.reranked_topics[1].topic_id, "t1")
        self.assertEqual(report.reranked_topics[2].topic_id, "t3")

    def test_final_score_calculation(self):
        candidates = [
            {"topic_id": "t1", "title": "Topic 1", "score": 0.80},
        ]
        diversity_report = {
            "diversity_scores": [
                {"topic_id": "t1", "diversity_adjusted_score": 0.90},
            ]
        }
        report = rerank_topics(
            candidates,
            diversity_report,
            run_date="20260707",
            original_score_weight=0.6,
            diversity_score_weight=0.4,
        )
        topic = report.reranked_topics[0]
        expected_final = 0.80 * 0.6 + 0.90 * 0.4
        self.assertEqual(topic.original_score, 0.80)
        self.assertEqual(topic.diversity_adjusted_score, 0.90)

    def test_rank_up(self):
        candidates = [
            {"topic_id": "t1", "title": "Topic 1", "score": 0.90},
            {"topic_id": "t2", "title": "Topic 2", "score": 0.85},
        ]
        diversity_report = {
            "diversity_scores": [
                {"topic_id": "t1", "diversity_adjusted_score": 0.60},
                {"topic_id": "t2", "diversity_adjusted_score": 0.95},
            ]
        }
        report = rerank_topics(candidates, diversity_report, run_date="20260707")
        t2 = report.reranked_topics[0]
        self.assertEqual(t2.topic_id, "t2")
        self.assertEqual(t2.status, "UP")
        self.assertEqual(t2.rank_change, 1)

    def test_rank_down(self):
        candidates = [
            {"topic_id": "t1", "title": "Topic 1", "score": 0.90},
            {"topic_id": "t2", "title": "Topic 2", "score": 0.85},
        ]
        diversity_report = {
            "diversity_scores": [
                {"topic_id": "t1", "diversity_adjusted_score": 0.60},
                {"topic_id": "t2", "diversity_adjusted_score": 0.95},
            ]
        }
        report = rerank_topics(candidates, diversity_report, run_date="20260707")
        t1 = report.reranked_topics[1]
        self.assertEqual(t1.topic_id, "t1")
        self.assertEqual(t1.status, "DOWN")
        self.assertEqual(t1.rank_change, -1)

    def test_rank_same(self):
        candidates = [
            {"topic_id": "t1", "title": "Topic 1", "score": 0.90},
            {"topic_id": "t2", "title": "Topic 2", "score": 0.85},
        ]
        diversity_report = {
            "diversity_scores": [
                {"topic_id": "t1", "diversity_adjusted_score": 0.90},
                {"topic_id": "t2", "diversity_adjusted_score": 0.85},
            ]
        }
        report = rerank_topics(candidates, diversity_report, run_date="20260707")
        self.assertEqual(report.rank_changed_count, 0)

    def test_empty_input(self):
        report = rerank_topics([], run_date="20260707")
        self.assertEqual(report.total_candidates, 0)
        self.assertGreater(len(report.warnings), 0)

    def test_no_diversity_report(self):
        candidates = [
            {"topic_id": "t1", "title": "Topic 1", "score": 0.90},
            {"topic_id": "t2", "title": "Topic 2", "score": 0.85},
        ]
        report = rerank_topics(candidates, None, run_date="20260707")
        self.assertEqual(report.total_candidates, 2)
        self.assertEqual(report.rank_changed_count, 0)

    def test_report_to_dict(self):
        candidates = [{"topic_id": "test", "title": "Test", "score": 0.85}]
        report = rerank_topics(candidates, run_date="20260707")
        data = report_to_dict(report)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
