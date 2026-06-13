import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase33_historical_replay import build_content_quality_calibration_proposals


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "scripts", market / "11_frontstage", market / "10_logs")


class ContentQualityCalibrationProposalsTest(unittest.TestCase):
    def test_calibration_proposals_never_auto_apply(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            paths.logs_root.mkdir(parents=True)
            (paths.logs_root / "latest_replay_topic_quality_diagnosis.json").write_text(json.dumps({"issues": [{"issue_id": "i1", "issue_type": "metadata_title_pollution", "severity": "HIGH"}]}), encoding="utf-8")
            payload, _ = build_content_quality_calibration_proposals(paths, ROOT)
            self.assertEqual(payload["summary"]["auto_apply"], 0)
            self.assertTrue(all(item["requires_human_approval"] for item in payload["proposals"]))


if __name__ == "__main__":
    unittest.main()
