import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import run_article_review_pipeline


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "09_runbooks" / "scripts", market / "11_frontstage", market / "10_logs")


class AutonomousArticleReviewPipelineTest(unittest.TestCase):
    def test_rewrite_creates_new_version_without_overwriting_draft(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            draft_dir = paths.market_content_root / "07_drafts"
            draft_dir.mkdir(parents=True)
            draft = {"draft_id": "d1", "topic_id": "t1", "title": "Title", "article_markdown": "## 为什么现在\ncontent", "known_weaknesses": ["needs polish"], "status": "READY_FOR_REVIEW"}
            (draft_dir / "latest_autonomous_drafts.json").write_text(json.dumps({"drafts": [draft]}), encoding="utf-8")
            payload, _ = run_article_review_pipeline(paths, ROOT)
            rewrite_id = payload["reviews"][0]["rewrite"]["rewrite_version_id"]
            self.assertTrue(rewrite_id.startswith("autorewrite_"))
            self.assertNotEqual(rewrite_id, draft["draft_id"])
            stored = json.loads((draft_dir / "latest_autonomous_drafts.json").read_text(encoding="utf-8"))
            self.assertEqual(stored["drafts"][0]["article_markdown"], draft["article_markdown"])


if __name__ == "__main__":
    unittest.main()
