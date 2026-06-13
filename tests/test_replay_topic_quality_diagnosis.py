import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase33_historical_replay import diagnose_replay_topic_quality


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "scripts", market / "11_frontstage", market / "10_logs")


class ReplayTopicQualityDiagnosisTest(unittest.TestCase):
    def test_duplicate_topic_detection_summary(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            paths.logs_root.mkdir(parents=True)
            (paths.logs_root / "latest_7day_topic_selection_replay.json").write_text(json.dumps({"days": [{"business_date": "d1", "status": "SELECTED", "duplicate_topic": True, "main_topic": {"title": "A"}}, {"business_date": "d2", "status": "SELECTED", "duplicate_topic": False, "main_topic": {"title": "B"}}]}), encoding="utf-8")
            (paths.logs_root / "latest_7day_quality_regression.json").write_text(json.dumps({"days": []}), encoding="utf-8")
            payload, _ = diagnose_replay_topic_quality(paths, ROOT)
            self.assertGreater(payload["summary"]["duplicate_topic_ratio"], 0)


if __name__ == "__main__":
    unittest.main()
