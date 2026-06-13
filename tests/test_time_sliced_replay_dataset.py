import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase33_historical_replay import build_time_sliced_replay_dataset, replay_days


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "scripts", market / "11_frontstage", market / "10_logs")


class TimeSlicedReplayDatasetTest(unittest.TestCase):
    def test_future_data_does_not_enter_past_replay_day(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = temp_paths(root)
            paths.logs_root.mkdir(parents=True)
            (paths.logs_root / "20260607__topic.json").write_text(json.dumps({"topics": [{"title": "past topic"}]}), encoding="utf-8")
            (paths.logs_root / "20260614__topic.json").write_text(json.dumps({"topics": [{"title": "future topic"}]}), encoding="utf-8")
            build_time_sliced_replay_dataset(paths, ROOT)
            day = replay_days(date(2026, 6, 13) if False else None)[0]
            dataset_files = list((paths.market_content_root / "13_replay").glob("replay_*/dataset_summary.json"))
            self.assertEqual(len(dataset_files), 7)
            text = "\n".join(path.read_text(encoding="utf-8") for path in dataset_files)
            self.assertNotIn("future topic", text)

    def test_cutoff_and_namespace_written(self):
        days = replay_days()
        self.assertTrue(days[0].cutoff_at.endswith("23:59:59"))
        self.assertRegex(days[0].namespace, r"^replay_20\d{6}$")


if __name__ == "__main__":
    unittest.main()
