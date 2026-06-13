import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import run_topic_to_article_pipeline


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "09_runbooks" / "scripts", market / "11_frontstage", market / "10_logs")


class AutonomousTopicToArticlePipelineTest(unittest.TestCase):
    def test_no_qualified_topic_is_success_empty_and_cost_guard_not_bypassed(self):
        with tempfile.TemporaryDirectory() as td:
            payload, _ = run_topic_to_article_pipeline(temp_paths(Path(td)), ROOT)
            self.assertEqual(payload["status"], "SUCCESS_EMPTY")
            self.assertTrue(payload["policy"]["cost_guard_not_bypassed"])


if __name__ == "__main__":
    unittest.main()
