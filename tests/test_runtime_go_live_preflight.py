from __future__ import annotations

import tempfile
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.paths import get_project_paths
from content_system.runtime_go_live_preflight import build_runtime_go_live_preflight


class RuntimeGoLivePreflightTests(unittest.TestCase):
    def test_preflight_builds_schema_and_can_block_install(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = get_project_paths(repo)
            # Use real repo checks but redirect report outputs away from tracked files.
            paths = paths.__class__(
                repo_root=paths.repo_root,
                market_content_root=root,
                legacy_content_root=paths.legacy_content_root,
                console_root=paths.console_root,
                scripts_root=root / "09_runbooks" / "scripts",
                frontstage_root=root / "11_frontstage",
                logs_root=root / "10_logs",
            )
            payload, _ = build_runtime_go_live_preflight(paths, repo)
        self.assertEqual(payload["schema_version"], "v1")
        self.assertIn(payload["status"], {"PASS", "ACTIONABLE", "BLOCKED"})
        self.assertIn("blocking_failures", payload["summary"])


if __name__ == "__main__":
    unittest.main()
