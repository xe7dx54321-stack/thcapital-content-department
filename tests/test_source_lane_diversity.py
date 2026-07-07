import unittest

from content_system.source_lane_diversity import (
    SourceLaneDiversityReport,
    SourceLaneInfo,
    analyze_source_lane_diversity,
    report_to_dict,
)


class TestSourceLaneDiversity(unittest.TestCase):
    def test_analyze_source_lane_diversity_basic(self):
        historical_topics = [
            {
                "topic_id": "hist_001",
                "source_id": "source_a",
                "lane": "tech",
                "run_date": "20260706",
            },
            {
                "topic_id": "hist_002",
                "source_id": "source_a",
                "lane": "tech",
                "run_date": "20260705",
            },
        ]
        report = analyze_source_lane_diversity(historical_topics, run_date="20260707")
        self.assertIsInstance(report, SourceLaneDiversityReport)
        self.assertEqual(report.total_sources, 1)
        self.assertEqual(report.total_lanes, 1)

    def test_source_consecutive_days_penalty(self):
        historical_topics = [
            {"topic_id": "t1", "source_id": "source_a", "lane": "tech", "run_date": "20260706"},
            {"topic_id": "t2", "source_id": "source_a", "lane": "tech", "run_date": "20260705"},
            {"topic_id": "t3", "source_id": "source_a", "lane": "tech", "run_date": "20260704"},
        ]
        report = analyze_source_lane_diversity(historical_topics, run_date="20260707")
        source_info = [s for s in report.source_lane_info if s.source_id == "source_a"]
        self.assertEqual(len(source_info), 1)
        self.assertEqual(source_info[0].days_consecutive, 3)
        self.assertTrue(source_info[0].is_over_concentrated)

    def test_lane_consecutive_days_penalty(self):
        historical_topics = [
            {"topic_id": "t1", "source_id": "source_a", "lane": "tech", "run_date": "20260706"},
            {"topic_id": "t2", "source_id": "source_b", "lane": "tech", "run_date": "20260705"},
            {"topic_id": "t3", "source_id": "source_c", "lane": "tech", "run_date": "20260704"},
        ]
        report = analyze_source_lane_diversity(historical_topics, run_date="20260707")
        lane_info = [s for s in report.source_lane_info if s.lane == "tech"]
        self.assertEqual(len(lane_info), 1)
        self.assertTrue(lane_info[0].is_over_concentrated)

    def test_7_day_count_penalty(self):
        historical_topics = [
            {"topic_id": f"t{i}", "source_id": "source_a", "lane": "tech", "run_date": "20260706"}
            for i in range(5)
        ]
        report = analyze_source_lane_diversity(historical_topics, run_date="20260707")
        source_info = [s for s in report.source_lane_info if s.source_id == "source_a"]
        self.assertEqual(source_info[0].topic_count_7d, 5)
        self.assertTrue(source_info[0].is_over_concentrated)

    def test_no_over_concentration(self):
        historical_topics = [
            {"topic_id": "t1", "source_id": "source_a", "lane": "tech", "run_date": "20260706"},
            {"topic_id": "t2", "source_id": "source_b", "lane": "business", "run_date": "20260705"},
        ]
        report = analyze_source_lane_diversity(historical_topics, run_date="20260707")
        self.assertEqual(report.over_concentrated_count, 0)

    def test_mixed_sources_and_lanes(self):
        historical_topics = [
            {"topic_id": "t1", "source_id": "source_a", "lane": "tech", "run_date": "20260706"},
            {"topic_id": "t2", "source_id": "source_a", "lane": "tech", "run_date": "20260705"},
            {"topic_id": "t3", "source_id": "source_b", "lane": "business", "run_date": "20260706"},
        ]
        report = analyze_source_lane_diversity(historical_topics, run_date="20260707")
        self.assertEqual(report.total_sources, 2)
        self.assertEqual(report.total_lanes, 2)

    def test_empty_input(self):
        report = analyze_source_lane_diversity([], run_date="20260707")
        self.assertEqual(report.total_sources, 0)
        self.assertEqual(report.total_lanes, 0)
        self.assertGreater(len(report.warnings), 0)

    def test_report_to_dict(self):
        historical_topics = [
            {"topic_id": "t1", "source_id": "source_a", "lane": "tech", "run_date": "20260706"}
        ]
        report = analyze_source_lane_diversity(historical_topics, run_date="20260707")
        data = report_to_dict(report)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
