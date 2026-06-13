import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import build_autonomous_outlines


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "09_runbooks" / "scripts", market / "11_frontstage", market / "10_logs")


class AutonomousOutlineBuilderTest(unittest.TestCase):
    def test_outline_sections_have_purpose(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            brief_dir = paths.market_content_root / "05_briefs"
            brief_dir.mkdir(parents=True)
            (brief_dir / "latest_autonomous_briefs.json").write_text(
                json.dumps(
                    {
                        "briefs": [
                            {
                                "brief_id": "b1",
                                "topic_id": "t1",
                                "title": "AI infra shift",
                                "status": "READY_FOR_OUTLINE",
                                "evidence_inventory": [{"evidence_id": "e1"}],
                                "narrative_angle": "why it matters",
                                "one_sentence_thesis": "test thesis",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            payload, _ = build_autonomous_outlines(paths, ROOT)
            self.assertTrue(all(section.get("purpose") for section in payload["outlines"][0]["sections"]))


if __name__ == "__main__":
    unittest.main()
