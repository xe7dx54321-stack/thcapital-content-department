"""Local path compatibility checks for Phase37A scripts."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class Phase37ALocalPathCompatibilityTest(unittest.TestCase):
    def test_phase37a_scripts_do_not_hardcode_workspace(self) -> None:
        paths = [
            REPO_ROOT / "scripts" / "build_production_observation_schema.py",
            REPO_ROOT / "scripts" / "capture_rss_smoke_result.py",
            REPO_ROOT / "scripts" / "capture_runtime_observation_result.py",
            REPO_ROOT / "scripts" / "build_manual_observation_log.py",
            REPO_ROOT / "scripts" / "build_production_observation_dashboard.py",
            REPO_ROOT / "scripts" / "import_local_observation_results.py",
            REPO_ROOT / "scripts" / "run_phase37a_observation_pipeline.py",
            REPO_ROOT / "src" / "content_system" / "phase37a_observation_pipeline.py",
        ]
        forbidden = "/" + "workspace"
        for path in paths:
            self.assertNotIn(forbidden, path.read_text(encoding="utf-8"), str(path))

    def test_script_from_other_cwd_writes_to_repo_logs(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(REPO_ROOT / "src")
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, str(REPO_ROOT / "scripts" / "build_production_observation_schema.py")],
                cwd=temp_dir,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(REPO_ROOT / "同行资本市场内容系统" / "10_logs"), result.stdout)


if __name__ == "__main__":
    unittest.main()
