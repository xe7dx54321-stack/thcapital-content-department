import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase33_historical_replay import replay_days, replay_root, run_replay_article_review


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "scripts", market / "11_frontstage", market / "10_logs")


class ReplayArticleReviewTest(unittest.TestCase):
    def test_final_candidate_manual_review_required(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            day = replay_days()[0]
            root = replay_root(paths, day)
            root.mkdir(parents=True)
            (root / "drafts.json").write_text(json.dumps({"drafts": [{"draft_id": "d1", "topic_id": "t1", "title": "Title", "article_markdown": "content", "status": "READY_FOR_REVIEW", "known_weaknesses": []}]}), encoding="utf-8")
            run_replay_article_review(paths, ROOT)
            final = json.loads((root / "final_candidates.json").read_text(encoding="utf-8"))["final_candidates"][0]
            self.assertTrue(final["manual_review_required"])
            self.assertTrue(final["do_not_publish"])


if __name__ == "__main__":
    unittest.main()
