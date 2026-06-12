from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.openclaw_conflict_resolution import apply_safe_conflict_resolution, build_conflict_resolution_plan
from content_system.paths import ProjectPaths


def temp_paths(root: Path, repo: Path) -> ProjectPaths:
    return ProjectPaths(
        repo_root=repo,
        market_content_root=root,
        legacy_content_root=root / "legacy",
        console_root=root / "console",
        scripts_root=root / "scripts",
        frontstage_root=root / "11_frontstage",
        logs_root=root / "10_logs",
    )


class OpenClawConflictResolutionTests(unittest.TestCase):
    def test_safe_only_apply_does_not_modify_non_safe_conflict(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = temp_paths(root, repo)
            paths.logs_root.mkdir(parents=True)
            jobs_path = root / "jobs.json"
            jobs_path.write_text(json.dumps({"jobs": [{"id": "legacy-publish", "enabled": True, "payload": {"message": "publish guard"}}]}), encoding="utf-8")
            (paths.logs_root / "latest_openclaw_schedule_coexistence_report.json").write_text(
                json.dumps(
                    {
                        "conflicts": [
                            {
                                "openclaw_job_id": "legacy-publish",
                                "conflict_type": "DUPLICATE_CONTENT_GENERATION",
                                "severity": "HIGH",
                                "runtime_job_id": "none",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            plan, _ = build_conflict_resolution_plan(paths, repo, jobs_path)
            applied, _ = apply_safe_conflict_resolution(paths, repo, jobs_path)
            jobs = json.loads(jobs_path.read_text(encoding="utf-8"))["jobs"]
        self.assertEqual(plan["summary"]["safe_to_disable"], 0)
        self.assertEqual(applied["actually_disabled"], 0)
        self.assertTrue(jobs[0]["enabled"])


if __name__ == "__main__":
    unittest.main()
