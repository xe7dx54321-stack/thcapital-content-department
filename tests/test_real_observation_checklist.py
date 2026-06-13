import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase33_historical_replay import build_real_observation_checklist


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "scripts", market / "11_frontstage", market / "10_logs")


class RealObservationChecklistTest(unittest.TestCase):
    def test_observation_checklist_generation(self):
        with tempfile.TemporaryDirectory() as td:
            payload, _ = build_real_observation_checklist(temp_paths(Path(td)), ROOT)
            self.assertGreaterEqual(payload["summary"]["check_count"], 15)
            self.assertEqual(payload["summary"]["recommended_observation_days"], 2)


if __name__ == "__main__":
    unittest.main()
