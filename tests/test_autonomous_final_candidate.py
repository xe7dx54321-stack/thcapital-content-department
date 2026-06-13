import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import build_final_candidates


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "09_runbooks" / "scripts", market / "11_frontstage", market / "10_logs")


class AutonomousFinalCandidateTest(unittest.TestCase):
    def test_final_candidate_requires_manual_review(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            draft_dir = paths.market_content_root / "07_drafts"
            draft_dir.mkdir(parents=True)
            (draft_dir / "latest_autonomous_article_reviews.json").write_text(json.dumps({"reviews": [{"draft_id": "d1", "topic_id": "t1", "status": "REVISED", "rewrite": {"rewrite_version_id": "r1"}, "judge": {"quality_score": 0.7, "reason": "ok"}}]}), encoding="utf-8")
            (draft_dir / "latest_autonomous_article_rewrite_versions.json").write_text(json.dumps({"rewrite_versions": [{"rewrite_version_id": "r1", "draft_id": "d1", "topic_id": "t1", "title": "Title", "article_markdown": "content"}]}), encoding="utf-8")
            payload, _ = build_final_candidates(paths, ROOT)
            self.assertTrue(payload["final_candidates"][0]["manual_review_required"])
            self.assertTrue(payload["final_candidates"][0]["do_not_publish"])


if __name__ == "__main__":
    unittest.main()
