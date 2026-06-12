from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.autonomous_scheduler import run_scheduler_once
from content_system.paths import get_project_paths
from content_system.runtime_live_trigger_validation import create_live_validation_slot, wait_for_validation_slot


class RuntimeLiveTriggerValidationTests(unittest.TestCase):
    def test_scheduler_validation_slot_auto_trigger(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            old = os.environ.get("THCAP_AUTONOMOUS_RUNTIME_DB")
            os.environ["THCAP_AUTONOMOUS_RUNTIME_DB"] = str(Path(tmp) / "runtime.sqlite")
            try:
                paths = get_project_paths(repo)
                slot = create_live_validation_slot(paths, delay_seconds=-1)
                run_scheduler_once(repo, execute=True)
                observed = wait_for_validation_slot(paths, slot["validation_slot_id"], timeout_seconds=1)
            finally:
                if old is None:
                    os.environ.pop("THCAP_AUTONOMOUS_RUNTIME_DB", None)
                else:
                    os.environ["THCAP_AUTONOMOUS_RUNTIME_DB"] = old
        self.assertEqual(observed.get("trigger_source"), "AUTONOMOUS_SCHEDULER")
        self.assertEqual(observed.get("status"), "SUCCESS")


if __name__ == "__main__":
    unittest.main()
