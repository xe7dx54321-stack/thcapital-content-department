from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.install_macos_runtime_launchd import render_plist


class RuntimeLaunchdRenderTests(unittest.TestCase):
    def test_launchd_render_has_no_secret_and_runs_runtime_only(self) -> None:
        plist = render_plist("/usr/bin/python3")
        self.assertIn("scripts/run_autonomous_runtime.py", plist)
        self.assertNotIn("sk-", plist)
        self.assertNotIn("API_KEY=", plist)
        self.assertNotIn("run_daily_end_to_end_pipeline.py", plist)


if __name__ == "__main__":
    unittest.main()
