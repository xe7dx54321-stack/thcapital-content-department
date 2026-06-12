from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


class MissedRunLiveValidationTests(unittest.TestCase):
    def test_catchup_compressed(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        completed = subprocess.run([sys.executable, "scripts/run_missed_run_live_validation.py"], cwd=repo, text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout.splitlines()[0])
        self.assertTrue(summary["compressed_catchup"])
        self.assertEqual(summary["fail"], 0)


if __name__ == "__main__":
    unittest.main()
