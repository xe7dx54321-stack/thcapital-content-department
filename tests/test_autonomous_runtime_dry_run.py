from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.autonomous_runtime_validation import run_autonomous_runtime_dry_run
from content_system.paths import get_project_paths


class AutonomousRuntimeDryRunTests(unittest.TestCase):
    def test_autonomous_runtime_dry_run(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            old_db = os.environ.get("THCAP_AUTONOMOUS_RUNTIME_DB")
            old_network = os.environ.get("THCAP_RUNTIME_NETWORK_MODE")
            os.environ["THCAP_AUTONOMOUS_RUNTIME_DB"] = str(Path(tmp) / "runtime.sqlite")
            os.environ["THCAP_RUNTIME_NETWORK_MODE"] = "FULL"
            try:
                payload, _ = run_autonomous_runtime_dry_run(get_project_paths(repo_root), repo_root)
            finally:
                if old_db is None:
                    os.environ.pop("THCAP_AUTONOMOUS_RUNTIME_DB", None)
                else:
                    os.environ["THCAP_AUTONOMOUS_RUNTIME_DB"] = old_db
                if old_network is None:
                    os.environ.pop("THCAP_RUNTIME_NETWORK_MODE", None)
                else:
                    os.environ["THCAP_RUNTIME_NETWORK_MODE"] = old_network
            self.assertIn(payload["status"], {"SUCCESS", "ACTIONABLE"})
            self.assertGreaterEqual(payload["summary"]["step_count"], 10)
            self.assertTrue(payload["boundaries"]["no_auto_publish"])


if __name__ == "__main__":
    unittest.main()
