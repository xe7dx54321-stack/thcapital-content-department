import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import build_autonomous_briefs


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "09_runbooks" / "scripts", market / "11_frontstage", market / "10_logs")


class AutonomousBriefBuilderTest(unittest.TestCase):
    def test_no_qualified_topic_does_not_create_ready_brief(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            topic_dir = paths.market_content_root / "03_topic_candidates"
            topic_dir.mkdir(parents=True)
            (topic_dir / "latest_daily_main_topic_selection.json").write_text(json.dumps({"summary": {"selected": False}}), encoding="utf-8")
            payload, _ = build_autonomous_briefs(paths, ROOT)
            self.assertEqual(payload["summary"]["ready_for_outline"], 0)


if __name__ == "__main__":
    unittest.main()
