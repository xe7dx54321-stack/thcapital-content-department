import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase33_historical_replay import replay_days, replay_root, run_replay_content_generation


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "scripts", market / "11_frontstage", market / "10_logs")


class ReplayContentGenerationTest(unittest.TestCase):
    def test_draft_do_not_publish_true(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            day = replay_days()[0]
            root = replay_root(paths, day)
            root.mkdir(parents=True)
            (root / "main_topic_selection.json").write_text(json.dumps({"main_topic": {"topic_id": "t1", "title": "A real topic", "scores": {"evidence_strength": 0.7}}, "status": "SELECTED"}), encoding="utf-8")
            run_replay_content_generation(paths, ROOT)
            draft = json.loads((root / "drafts.json").read_text(encoding="utf-8"))["drafts"][0]
            self.assertTrue(draft["do_not_publish"])
            self.assertIn("为什么现在", draft["article_markdown"])


if __name__ == "__main__":
    unittest.main()
