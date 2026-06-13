import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase33_historical_replay import run_phase33_historical_replay_pipeline


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "scripts", market / "11_frontstage", market / "10_logs")


class Phase33HistoricalReplayPipelineTest(unittest.TestCase):
    def test_pipeline_uses_replay_namespace_policy(self):
        with tempfile.TemporaryDirectory() as td:
            payload, _ = run_phase33_historical_replay_pipeline(temp_paths(Path(td)), ROOT)
            self.assertIn(payload["status"], {"SUCCESS", "ACTIONABLE"})
            self.assertTrue(payload["policy"]["replay_namespace_only"])
            self.assertFalse(payload["policy"]["calibration_auto_apply"])


if __name__ == "__main__":
    unittest.main()
