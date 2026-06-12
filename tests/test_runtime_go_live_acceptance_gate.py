from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.paths import ProjectPaths
from content_system.runtime_go_live_acceptance_gate import run_go_live_acceptance_gate


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


class RuntimeGoLiveAcceptanceGateTests(unittest.TestCase):
    def test_auto_publish_attempt_blocks_gate(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = ProjectPaths(repo, root, root / "legacy", root / "console", root / "scripts", root / "11_frontstage", root / "10_logs")
            write_json(paths.logs_root / "latest_runtime_go_live_preflight.json", {"summary": {"blocking_failures": 0}})
            write_json(paths.logs_root / "latest_openclaw_conflict_resolution_plan.json", {"summary": {"manual_review": 0}})
            write_json(paths.logs_root / "latest_openclaw_conflict_resolution_apply.json", {"status": "SUCCESS", "safe_to_disable": 0, "actually_disabled": 0})
            write_json(paths.logs_root / "latest_macos_runtime_launchagent_installation.json", {"summary": {"installed": True, "loaded": True}})
            write_json(paths.logs_root / "latest_runtime_startup_heartbeat_restart_validation.json", {"status": "PASS", "runtime": {"relaunched_by_launchd": True}})
            write_json(paths.logs_root / "latest_runtime_live_trigger_validation.json", {"status": "SUCCESS", "trigger_source": "AUTONOMOUS_SCHEDULER"})
            write_json(paths.logs_root / "latest_missed_run_live_validation.json", {"status": "PASS", "summary": {}})
            write_json(paths.logs_root / "latest_runtime_idempotency_live_validation.json", {"status": "PASS", "summary": {}})
            write_json(paths.logs_root / "latest_runtime_go_live_observation.json", {"status": "BLOCKED", "summary": {"auto_publish_attempts": 1, "wechat_api_attempts": 0, "image_generation_attempts": 0, "secret_exposure_count": 0, "duplicate_content_generation_count": 0}})
            write_json(paths.logs_root / "latest_autonomous_runtime_dry_run.json", {"status": "SUCCESS", "summary": {}})
            write_json(paths.frontstage_root / "latest_wechat_workbench_data.json", {"runtime_control_center_panel": {"runtime_status": "IDLE"}})
            payload, _ = run_go_live_acceptance_gate(paths, repo)
        self.assertEqual(payload["gate_status"], "BLOCKED")
        self.assertGreater(payload["summary"]["blocking_failures"], 0)


if __name__ == "__main__":
    unittest.main()
