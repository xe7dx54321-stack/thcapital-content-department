import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.phase33_historical_replay import score_replay_topic


class ReplayTopicScoringTest(unittest.TestCase):
    def test_source_metadata_title_warning(self):
        score = score_replay_topic({"title": "OpenClaw source metadata: Finsmes Ai Gnews", "evidence_strength": "MEDIUM"})
        self.assertTrue(score["metadata_title"])
        self.assertIn("TITLE_NORMALIZATION_REQUIRED", score["flags"])


if __name__ == "__main__":
    unittest.main()
