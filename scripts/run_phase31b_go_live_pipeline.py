#!/usr/bin/env python3
"""Run Phase31B go-live pipeline with fail-closed ordering."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import today_token, utc_now, write_json_and_markdown  # noqa: E402


def run_step(name: str, command: list[str]) -> dict[str, object]:
    started_at = utc_now()
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    return {
        "name": name,
        "command": " ".join(command),
        "returncode": completed.returncode,
        "status": "OK" if completed.returncode == 0 else "FAILED",
        "started_at": started_at,
        "finished_at": utc_now(),
        "stdout_tail": completed.stdout[-3000:],
        "stderr_tail": completed.stderr[-3000:],
    }


def main() -> int:
    steps_def = [
        ("runtime_config_validate", [sys.executable, "scripts/validate_runtime_config.py"], True),
        ("runtime_go_live_preflight", [sys.executable, "scripts/run_runtime_go_live_preflight.py"], True),
        ("openclaw_coexistence", [sys.executable, "scripts/build_openclaw_schedule_coexistence_report.py"], True),
        ("openclaw_conflict_plan", [sys.executable, "scripts/build_openclaw_conflict_resolution_plan.py"], True),
        ("openclaw_safe_apply", [sys.executable, "scripts/apply_openclaw_conflict_resolution.py", "--apply-safe-only"], True),
        ("runtime_go_live_preflight_recheck", [sys.executable, "scripts/run_runtime_go_live_preflight.py"], True),
        ("launchagent_install", [sys.executable, "scripts/install_macos_runtime_launchd.py", "--install"], True),
        ("launchagent_check", [sys.executable, "scripts/check_macos_runtime_launchd.py"], True),
        ("runtime_startup_restart_validate", [sys.executable, "scripts/validate_runtime_go_live.py"], True),
        ("runtime_live_trigger_validate", [sys.executable, "scripts/run_runtime_live_trigger_validation.py"], True),
        ("missed_run_live_validate", [sys.executable, "scripts/run_missed_run_live_validation.py"], True),
        ("idempotency_live_validate", [sys.executable, "scripts/run_runtime_idempotency_live_validation.py"], True),
        ("workbench_build", [sys.executable, "scripts/build_wechat_workbench_data.py"], True),
        ("workbench_frontend", [sys.executable, "scripts/build_wechat_workbench_frontend.py"], True),
        ("runtime_go_live_observation", [sys.executable, "scripts/build_runtime_go_live_observation.py"], True),
        ("runtime_go_live_acceptance", [sys.executable, "scripts/run_runtime_go_live_acceptance_gate.py"], True),
    ]
    steps: list[dict[str, object]] = []
    for name, command, required in steps_def:
        step = run_step(name, command)
        steps.append(step)
        if required and step["returncode"] != 0:
            break
    failed = sum(1 for step in steps if step["returncode"] != 0)
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "SUCCESS" if failed == 0 else "ACTIONABLE",
        "steps": steps,
        "summary": {"step_count": len(steps), "ok": sum(1 for step in steps if step["returncode"] == 0), "failed": failed},
        "fail_closed": True,
    }
    paths = get_project_paths(ROOT)
    outputs = {
        "latest_json": paths.logs_root / "latest_phase31b_go_live_pipeline.json",
        "latest_md": paths.logs_root / "latest_phase31b_go_live_pipeline.md",
    }
    markdown = f"""# Phase31B Go-Live Pipeline

- status: `{payload['status']}`
- step_count: `{payload['summary']['step_count']}`
- ok: `{payload['summary']['ok']}`
- failed: `{payload['summary']['failed']}`
"""
    write_json_and_markdown(payload, markdown, outputs)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    print(f"status: {payload['status']}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
