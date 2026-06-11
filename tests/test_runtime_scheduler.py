from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.autonomous_scheduler import run_scheduler_once
from content_system.paths import get_project_paths
from content_system.runtime_process_lock import RuntimeLockError, RuntimeProcessLock


class RuntimeSchedulerTests(unittest.TestCase):
    def test_single_instance_lock_and_stale_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lock_path = Path(tmp) / "runtime.lock"
            lock = RuntimeProcessLock(lock_path, stale_after_seconds=3600)
            lock.acquire()
            with self.assertRaises(RuntimeLockError):
                RuntimeProcessLock(lock_path, stale_after_seconds=3600).acquire()
            lock.release()
            lock_path.write_text("999999\n", encoding="utf-8")
            recovered = RuntimeProcessLock(lock_path, stale_after_seconds=3600)
            recovered.acquire()
            recovered.release()
            self.assertFalse(lock_path.exists())

    def test_scheduler_once_dry_run(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            old = os.environ.get("THCAP_AUTONOMOUS_RUNTIME_DB")
            os.environ["THCAP_AUTONOMOUS_RUNTIME_DB"] = str(Path(tmp) / "runtime.sqlite")
            try:
                payload, _ = run_scheduler_once(repo_root, execute=False, force_slot="workbench_finalize")
            finally:
                if old is None:
                    os.environ.pop("THCAP_AUTONOMOUS_RUNTIME_DB", None)
                else:
                    os.environ["THCAP_AUTONOMOUS_RUNTIME_DB"] = old
            self.assertIn(payload["status"], {"SUCCESS", "ACTIONABLE"})
            self.assertGreaterEqual(payload["summary"]["skipped_count"], 1)


if __name__ == "__main__":
    unittest.main()
