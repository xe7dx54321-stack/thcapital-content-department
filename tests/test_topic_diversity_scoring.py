import unittest

from content_system.topic_diversity_scoring import (
    TopicDiversityReport,
    DiversityScoreBreakdown,
    build_topic_diversity_report,
    calculate_diversity_score,
    report_to_dict,
)


class TestTopicDiversityScoring(unittest.TestCase):
    def test_build_diversity_report_basic(self):
        candidates = [
            {"topic_id": "test_001", "title": "Test Topic", "score": 0.85}
        ]
        report = build_topic_diversity_report(candidates, run_date="20260707")
        self.assertIsInstance(report, TopicDiversityReport)
        self.assertEqual(report.candidate_count, 1)
        self.assertEqual(report.penalty_count, 0)
        self.assertEqual(report.boost_count, 0)
        self.assertEqual(report.neutral_count, 1)

    def test_calculate_diversity_score_with_penalties(self):
        candidate = {
            "topic_id": "test_001",
            "title": "Test Topic",
            "score": 0.85,
            "source_id": "source_a",
            "lane": "tech",
        }
        similarity_report = {
            "similarity_matches": [
                {"topic_id": "test_001", "is_similar": True, "is_hard_duplicate": False}
            ]
        }
        score = calculate_diversity_score(
            candidate,
            similarity_report=similarity_report,
        )
        self.assertIsInstance(score, DiversityScoreBreakdown)
        self.assertGreater(score.recent_topic_duplicate_penalty, 0)
        self.assertEqual(score.diversity_status, "PENALIZED")

    def test_hard_duplicate_increases_penalty(self):
        candidate = {"topic_id": "test_001", "title": "Test", "score": 0.85}
        similarity_report_soft = {
            "similarity_matches": [
                {"topic_id": "test_001", "is_similar": True, "is_hard_duplicate": False}
            ]
        }
        similarity_report_hard = {
            "similarity_matches": [
                {"topic_id": "test_001", "is_similar": True, "is_hard_duplicate": True}
            ]
        }
        score_soft = calculate_diversity_score(candidate, similarity_report=similarity_report_soft)
        score_hard = calculate_diversity_score(candidate, similarity_report=similarity_report_hard)
        self.assertGreater(score_hard.recent_topic_duplicate_penalty, score_soft.recent_topic_duplicate_penalty)

    def test_source_lane_penalty(self):
        candidate = {"topic_id": "test_001", "title": "Test", "score": 0.85, "source_id": "source_a", "lane": "tech"}
        source_lane_report = {
            "source_lane_info": {
                "source_a": {"recent_repetition": 2},
                "tech": {"recent_repetition": 2},
            }
        }
        score = calculate_diversity_score(candidate, source_lane_report=source_lane_report)
        self.assertGreater(score.same_source_repetition_penalty, 0)
        self.assertGreater(score.same_lane_repetition_penalty, 0)

    def test_competitive_penalty(self):
        candidate = {"topic_id": "test_001", "title": "Test", "score": 0.85}
        competitive_report = {
            "penalties": [
                {"topic_id": "test_001", "penalty": 0.14}
            ]
        }
        score = calculate_diversity_score(candidate, competitive_penalty_report=competitive_report)
        self.assertGreater(score.high_competitive_same_angle_penalty, 0)

    def test_metadata_title_penalty(self):
        candidate = {"topic_id": "test_001", "title": "Test", "score": 0.85}
        title_guard_report = {
            "guards": [
                {"topic_id": "test_001", "is_raw_metadata_title": True}
            ]
        }
        score = calculate_diversity_score(candidate, title_guard_report=title_guard_report)
        self.assertGreater(score.metadata_title_penalty, 0)

    def test_angle_boost(self):
        candidate = {"topic_id": "test_001", "title": "Test", "score": 0.85}
        angle_boost_report = {
            "boosts": [
                {"topic_id": "test_001", "boost_type": "strong_differentiated_angle"}
            ]
        }
        score = calculate_diversity_score(candidate, angle_boost_report=angle_boost_report)
        self.assertGreater(score.strong_differentiated_angle_boost, 0)
        self.assertEqual(score.diversity_status, "BOOSTED")

    def test_multi_source_boost(self):
        candidate = {"topic_id": "test_001", "title": "Test", "score": 0.85}
        angle_boost_report = {
            "boosts": [
                {"topic_id": "test_001", "boost_type": "multi_source_support"}
            ]
        }
        score = calculate_diversity_score(candidate, angle_boost_report=angle_boost_report)
        self.assertGreater(score.multi_source_support_boost, 0)

    def test_soft_differentiation_penalty(self):
        candidate = {"topic_id": "test_001", "title": "Test", "score": 0.85}
        angle_boost_report = {
            "boosts": [
                {"topic_id": "test_001", "boost_type": "weak_differentiation"}
            ]
        }
        score = calculate_diversity_score(candidate, angle_boost_report=angle_boost_report)
        self.assertGreater(score.weak_differentiation_penalty, 0)

    def test_score_clamping(self):
        candidate = {"topic_id": "test_001", "title": "Test", "score": 0.95}
        similarity_report = {
            "similarity_matches": [
                {"topic_id": "test_001", "is_similar": True, "is_hard_duplicate": True}
            ]
        }
        score = calculate_diversity_score(
            candidate,
            similarity_report=similarity_report,
            policy={
                "penalties": {"recent_topic_duplicate": 1.0},
                "boosts": {},
            },
        )
        self.assertGreaterEqual(score.diversity_adjusted_score, 0.0)
        self.assertLessEqual(score.diversity_adjusted_score, 1.0)

    def test_report_to_dict(self):
        candidates = [{"topic_id": "test", "title": "Test", "score": 0.85}]
        report = build_topic_diversity_report(candidates, run_date="20260707")
        data = report_to_dict(report)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
