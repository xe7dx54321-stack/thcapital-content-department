import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import run_quality_regression


def temp_paths(root: Path) -> ProjectPaths:
    market = root / "market"
    return ProjectPaths(root, market, root / "legacy", root / "console", market / "09_runbooks" / "scripts", market / "11_frontstage", market / "10_logs")


class LegacyVsNewQualityRegressionTest(unittest.TestCase):
    def test_quality_regression_blocks_target_price_and_fake_citation(self):
        with tempfile.TemporaryDirectory() as td:
            paths = temp_paths(Path(td))
            final_dir = paths.market_content_root / "08_final_candidates"
            final_dir.mkdir(parents=True)
            (final_dir / "latest_autonomous_final_candidates.json").write_text(
                json.dumps({"final_candidates": [{"title": "Test title", "article_markdown": "据某媒体，匿名人士称 target price 上调。"}]}),
                encoding="utf-8",
            )
            payload, _ = run_quality_regression(paths, ROOT)
            failed = {item["check_id"] for item in payload["checks"] if item["status"] == "FAIL"}
            self.assertIn("no_target_price", failed)
            self.assertIn("no_fake_citations", failed)


if __name__ == "__main__":
    unittest.main()
