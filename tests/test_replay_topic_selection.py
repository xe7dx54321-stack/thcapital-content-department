import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.phase33_historical_replay import topic_key


class ReplayTopicSelectionTest(unittest.TestCase):
    def test_duplicate_topic_key_normalizes_titles(self):
        self.assertEqual(topic_key("AI Agent: funding!"), topic_key("AI Agent funding"))


if __name__ == "__main__":
    unittest.main()
