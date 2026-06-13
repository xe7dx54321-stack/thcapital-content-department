import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import write_autonomous_drafts


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "09_runbooks" / "scripts", market / "11_frontstage", market / "10_logs")


class AutonomousDraftWriterTest(unittest.TestCase):
    def test_draft_is_do_not_publish(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            brief_dir = paths.market_content_root / "05_briefs"
            outline_dir = paths.market_content_root / "06_outlines"
            brief_dir.mkdir(parents=True)
            outline_dir.mkdir(parents=True)
            (brief_dir / "latest_autonomous_briefs.json").write_text(json.dumps({"briefs": [{"brief_id": "b1", "topic_id": "t1", "title": "Title", "one_sentence_thesis": "thesis", "why_now": "now", "evidence_inventory": [{"evidence_id": "e1"}], "counterarguments": [], "writing_risks": []}]}), encoding="utf-8")
            (outline_dir / "latest_autonomous_outlines.json").write_text(json.dumps({"outlines": [{"outline_id": "o1", "brief_id": "b1", "topic_id": "t1", "title_options": ["A specific AI infrastructure shift"], "status": "READY_FOR_DRAFT", "sections": [{"heading": "Section", "purpose": "Explain", "key_points": ["point"], "evidence_ids": ["e1"], "risk": ""}]}]}), encoding="utf-8")
            payload, _ = write_autonomous_drafts(paths, ROOT)
            self.assertTrue(all(item["do_not_publish"] for item in payload["drafts"]))
            self.assertNotIn("target price", payload["drafts"][0]["article_markdown"].lower())


if __name__ == "__main__":
    unittest.main()
