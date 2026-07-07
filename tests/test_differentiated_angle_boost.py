import unittest

from content_system.differentiated_angle_boost import (
    DifferentiatedAngleBoostReport,
    AngleBoost,
    apply_angle_boosts,
    recommend_angles_for_candidate,
    report_to_dict,
    DIFFERENTIATED_ANGLES,
)


class TestDifferentiatedAngleBoost(unittest.TestCase):
    def test_recommend_angles_for_candidate_technical(self):
        candidate = {
            "title": "GPT-5技术架构深度解析",
            "summary": "深入分析技术实现细节和架构设计原理",
        }
        angles = recommend_angles_for_candidate(candidate)
        self.assertGreater(len(angles), 0)
        angle_names = [a["angle_name"] for a in angles]
        self.assertIn("技术实现角度", angle_names)

    def test_recommend_angles_for_candidate_business(self):
        candidate = {
            "title": "AI创业公司商业价值评估",
            "summary": "评估商业价值和市场潜力，分析商业模式",
        }
        angles = recommend_angles_for_candidate(candidate)
        angle_names = [a["angle_name"] for a in angles]
        self.assertIn("商业价值角度", angle_names)

    def test_recommend_angles_for_candidate_comparison(self):
        candidate = {
            "title": "GPT-5 vs Claude性能对比分析",
            "summary": "与竞品进行深度对比分析",
        }
        angles = recommend_angles_for_candidate(candidate)
        angle_names = [a["angle_name"] for a in angles]
        self.assertIn("对比分析角度", angle_names)

    def test_strong_differentiated_angle_boost(self):
        candidates = [
            {
                "topic_id": "test_001",
                "title": "GPT-5技术架构深度解析原理实现细节",
                "summary": "深入分析技术实现细节和架构设计原理",
            }
        ]
        report = apply_angle_boosts(candidates, run_date="20260707")
        boosts = [b for b in report.boosts if b.boost_type == "strong_differentiated_angle"]
        self.assertGreater(len(boosts), 0)
        self.assertGreater(boosts[0].boost_value, 0)

    def test_fresh_undercovered_angle_boost(self):
        candidates = [
            {
                "topic_id": "test_001",
                "title": "AI应用案例",
                "summary": "探讨应用案例",
            }
        ]
        report = apply_angle_boosts(candidates, run_date="20260707")
        boosts = [b for b in report.boosts if b.boost_type == "fresh_undercovered_angle"]
        self.assertGreater(len(boosts), 0)

    def test_multi_source_support_boost(self):
        candidates = [
            {
                "topic_id": "test_001",
                "title": "Multi-source supported topic",
                "source_count": 3,
            }
        ]
        report = apply_angle_boosts(candidates, run_date="20260707")
        boosts = [b for b in report.boosts if b.boost_type == "multi_source_support"]
        self.assertEqual(len(boosts), 1)
        self.assertGreater(boosts[0].boost_value, 0)

    def test_weak_differentiation_penalty(self):
        candidates = [
            {
                "topic_id": "test_001",
                "title": "应用",
                "summary": "应用相关",
            }
        ]
        report = apply_angle_boosts(
            candidates,
            run_date="20260707",
            fresh_angle_threshold=0.43,
            weak_differentiation_threshold=0.42,
        )
        penalties = [b for b in report.boosts if b.boost_type == "weak_differentiation"]
        self.assertGreater(len(penalties), 0)
        self.assertLess(penalties[0].boost_value, 0)

    def test_empty_input(self):
        report = apply_angle_boosts([], run_date="20260707")
        self.assertEqual(report.total_boosts, 0)
        self.assertGreater(len(report.warnings), 0)

    def test_angle_report_from_external_source(self):
        candidates = [
            {"topic_id": "test_001", "title": "Test", "entry_id": "entry_001"}
        ]
        angle_report = {
            "reports": [
                {
                    "entry_id": "entry_001",
                    "recommended_angles": [
                        {"angle_name": "技术实现角度", "confidence": 0.85, "description": "技术分析"}
                    ]
                }
            ]
        }
        report = apply_angle_boosts(candidates, angle_report, run_date="20260707")
        boosts = [b for b in report.boosts if b.topic_id == "test_001"]
        self.assertGreater(len(boosts), 0)

    def test_15_angles_available(self):
        self.assertEqual(len(DIFFERENTIATED_ANGLES), 15)

    def test_report_to_dict(self):
        candidates = [{"topic_id": "test", "title": "Technical analysis"}]
        report = apply_angle_boosts(candidates, run_date="20260707")
        data = report_to_dict(report)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
