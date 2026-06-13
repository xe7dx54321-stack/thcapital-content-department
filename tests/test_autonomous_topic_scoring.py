import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import score_topic


class AutonomousTopicScoringTest(unittest.TestCase):
    def test_topic_score_dimensions_complete(self):
        weights = {
            "urgency": {"weight": 0.15},
            "reader_value": {"weight": 0.2},
            "evidence_strength": {"weight": 0.2},
            "narrative_potential": {"weight": 0.15},
            "investment_relevance": {"weight": 0.15},
            "differentiation": {"weight": 0.15},
        }
        scores = score_topic(
            {
                "title": "AI infra funding signal",
                "source_origin": "connector",
                "evidence_strength": "MEDIUM",
                "evidence_ids": ["e1", "e2"],
                "activation_status": "ACTIVATED",
            },
            weights,
        )
        self.assertEqual(set(scores) - {"total"}, set(weights))
        self.assertIn("total", scores)


if __name__ == "__main__":
    unittest.main()
