import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.phase33_historical_replay import normalize_title_for_topic


class HumanReviewChecklistBuilderTest(unittest.TestCase):
    def test_metadata_title_gets_rewrite_suggestion(self):
        title = normalize_title_for_topic("OpenClaw source metadata: Finsmes Ai Gnews")
        self.assertIn("需要提炼", title)


if __name__ == "__main__":
    unittest.main()
