from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.openclaw_conflict_resolution import apply_safe_conflict_resolution, rollback_latest_conflict_resolution, sha256_file
from content_system.paths import ProjectPaths


class OpenClawConflictRollbackTests(unittest.TestCase):
    def test_rollback_restores_exact_hash(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = ProjectPaths(repo, root, root / "legacy", root / "console", root / "scripts", root / "11_frontstage", root / "10_logs")
            paths.logs_root.mkdir(parents=True)
            jobs_path = root / "jobs.json"
            jobs_path.write_text(json.dumps({"jobs": [{"id": "safe-job", "enabled": True, "payload": "covered"}]}, indent=2), encoding="utf-8")
            original_hash = sha256_file(jobs_path)
            (paths.logs_root / "latest_openclaw_conflict_resolution_plan.json").write_text(
                json.dumps({"resolution_items": [{"openclaw_job_id": "safe-job", "safe_to_disable": True, "recommended_action": "DISABLE"}]}),
                encoding="utf-8",
            )
            applied, _ = apply_safe_conflict_resolution(paths, repo, jobs_path)
            self.assertEqual(applied["actually_disabled"], 1)
            rollback, _ = rollback_latest_conflict_resolution(paths, jobs_path)
        self.assertEqual(rollback["status"], "SUCCESS")
        self.assertEqual(rollback["restored_hash"], original_hash)


if __name__ == "__main__":
    unittest.main()
