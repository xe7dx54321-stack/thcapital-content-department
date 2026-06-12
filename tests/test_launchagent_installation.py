from __future__ import annotations

import unittest
from pathlib import Path

from scripts.install_macos_runtime_launchd import LABEL, LAUNCH_AGENT, render_plist


class LaunchAgentInstallationTests(unittest.TestCase):
    def test_plist_user_level_and_secret_free(self) -> None:
        rendered = render_plist("/usr/bin/python3")
        self.assertIn("scripts/run_autonomous_runtime.py", rendered)
        self.assertIn(LABEL, rendered)
        self.assertNotIn("API_KEY", rendered)
        self.assertNotIn("sk-", rendered)
        self.assertIn(str(Path.home() / "Library" / "LaunchAgents"), str(LAUNCH_AGENT.parent))


if __name__ == "__main__":
    unittest.main()
