from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class RuntimeIdempotencyLiveValidationTests(unittest.TestCase):
    def test_duplicate_run_blocked(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["THCAP_AUTONOMOUS_RUNTIME_DB"] = str(Path(tmp) / "runtime.sqlite")
            completed = subprocess.run([sys.executable, "scripts/run_runtime_idempotency_live_validation.py"], cwd=repo, env=env, text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout.splitlines()[0])
        self.assertEqual(summary["submitted"], 2)
        self.assertEqual(summary["executed"], 1)
        self.assertEqual(summary["duplicate_skipped"], 1)
        self.assertEqual(summary["duplicate_artifacts"], 0)


if __name__ == "__main__":
    unittest.main()
