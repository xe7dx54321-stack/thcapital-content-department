import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import select_daily_main_topics


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "09_runbooks" / "scripts", market / "11_frontstage", market / "10_logs")


class AutonomousTopicSelectionTest(unittest.TestCase):
    def test_weak_evidence_topic_not_selected_main(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            topic_dir = paths.market_content_root / "03_topic_candidates"
            topic_dir.mkdir(parents=True)
            (topic_dir / "latest_autonomous_topic_scores.json").write_text(
                json.dumps(
                    {
                        "topics": [
                            {
                                "topic_id": "t1",
                                "title": "Weak community signal",
                                "score_total": 0.95,
                                "decision": "NEEDS_EVIDENCE",
                                "source_origin": "openclaw",
                                "recommended_angle": "",
                                "content_recipe": "",
                            }
                        ],
                        "summary": {},
                    }
                ),
                encoding="utf-8",
            )
            payload, _ = select_daily_main_topics(paths, ROOT)
            self.assertFalse(payload["summary"]["selected"])
            self.assertEqual(payload["status"], "NO_QUALIFIED_TOPIC")


if __name__ == "__main__":
    unittest.main()
