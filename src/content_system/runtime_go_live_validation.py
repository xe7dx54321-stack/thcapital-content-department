"""Validate installed LaunchAgent runtime startup, heartbeat, and restart."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import today_token, utc_now, write_json_and_markdown
from content_system.runtime_heartbeat import build_runtime_health_summary, read_runtime_heartbeat


LABEL = "com.thcapital.content-factory-runtime"
LAUNCH_AGENT = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
SECRET_VALUE_RE = re.compile(r"sk-[A-Za-z0-9_-]{8,}")
SECRET_ENV_RE = re.compile(r"((?:MINIMAX|ANTHROPIC|OPENAI|API)_API_KEY\\s*=>\\s*)[^\\n]+")


def _sanitize(text: str | None) -> str:
    sanitized = SECRET_ENV_RE.sub(r"\\1<redacted>", text or "")
    return SECRET_VALUE_RE.sub("<redacted>", sanitized)


def _service_name() -> str:
    return f"gui/{os.getuid()}/{LABEL}"


def _run(command: list[str], repo_root: Path | None = None) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
    return {"returncode": completed.returncode, "stdout": _sanitize(completed.stdout)[-3000:], "stderr": _sanitize(completed.stderr)[-3000:], "command": " ".join(command)}


def runtime_pids() -> list[int]:
    completed = subprocess.run(["pgrep", "-fl", "scripts/run_autonomous_runtime.py"], text=True, capture_output=True, check=False)
    pids: list[int] = []
    for line in completed.stdout.splitlines():
        if "pgrep" in line:
            continue
        try:
            pid = int(line.split(maxsplit=1)[0])
        except (IndexError, ValueError):
            continue
        pids.append(pid)
    return pids


def _heartbeat_age_seconds(heartbeat: dict[str, Any]) -> int:
    text = str(heartbeat.get("last_heartbeat_at") or "")
    if not text:
        return 999999
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return 999999
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int((datetime.now(timezone.utc) - dt).total_seconds())


def _wait_for_pid_change(old_pid: int, timeout_seconds: int = 180) -> int:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        pids = [pid for pid in runtime_pids() if pid != old_pid]
        if pids:
            return pids[0]
        time.sleep(3)
    return 0


def _wait_for_active_heartbeat(paths: ProjectPaths, timeout_seconds: int = 60) -> dict[str, Any]:
    deadline = time.time() + timeout_seconds
    latest = read_runtime_heartbeat(paths)
    while time.time() < deadline:
        latest = read_runtime_heartbeat(paths)
        if latest.get("status") in {"IDLE", "RUNNING", "STARTING"} and _heartbeat_age_seconds(latest) < 30:
            return latest
        time.sleep(2)
    return latest


def validate_runtime_go_live(paths: ProjectPaths, repo_root: Path, restart: bool = True) -> tuple[dict[str, Any], dict[str, Path]]:
    launch_print = _run(["launchctl", "print", _service_name()])
    pids = runtime_pids()
    heartbeat = read_runtime_heartbeat(paths)
    build_runtime_health_summary(paths, repo_root)
    stdout_path = repo_root / "logs" / "autonomous-runtime" / "content-factory-runtime.runtime.log"
    stderr_path = repo_root / "logs" / "autonomous-runtime" / "content-factory-runtime.runtime.err"
    old_pid = pids[0] if pids else 0
    new_pid = 0
    restart_status = "SKIPPED"
    if restart and old_pid:
        _run([sys.executable, "scripts/runtime_control.py", "shutdown"], repo_root=repo_root)
        new_pid = _wait_for_pid_change(old_pid)
        restart_status = "PASS" if new_pid and new_pid != old_pid else "FAIL"
        heartbeat = _wait_for_active_heartbeat(paths)
    checks = [
        {"check_id": "launchagent_installed", "status": "PASS" if LAUNCH_AGENT.exists() else "FAIL", "message": str(LAUNCH_AGENT)},
        {"check_id": "launchagent_loaded", "status": "PASS" if launch_print["returncode"] == 0 else "FAIL", "message": launch_print["stderr"] or "loaded"},
        {"check_id": "runtime_pid_exists", "status": "PASS" if (new_pid or old_pid) else "FAIL", "message": f"old_pid={old_pid} new_pid={new_pid}"},
        {"check_id": "pid_matches_runtime_entry", "status": "PASS" if (new_pid or old_pid) else "FAIL", "message": "pgrep scripts/run_autonomous_runtime.py"},
        {"check_id": "heartbeat_recent", "status": "PASS" if _heartbeat_age_seconds(heartbeat) < 180 else "FAIL", "message": f"age={_heartbeat_age_seconds(heartbeat)}"},
        {"check_id": "runtime_status_valid", "status": "PASS" if heartbeat.get("status") in {"IDLE", "RUNNING", "STARTING"} else "WARN", "message": str(heartbeat.get("status"))},
        {"check_id": "logs_readable", "status": "PASS" if stdout_path.parent.exists() else "FAIL", "message": f"stdout={stdout_path.exists()} stderr={stderr_path.exists()}"},
        {"check_id": "graceful_restart", "status": restart_status if restart else "SKIPPED", "message": f"old_pid={old_pid} new_pid={new_pid}"},
    ]
    fail = sum(1 for item in checks if item["status"] == "FAIL")
    warn = sum(1 for item in checks if item["status"] == "WARN")
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "PASS" if fail == 0 else "BLOCKED",
        "checks": checks,
        "launchctl_print": launch_print,
        "runtime": {
            "pid": new_pid or old_pid,
            "old_pid": old_pid,
            "new_pid": new_pid,
            "runtime_instance_id": heartbeat.get("runtime_instance_id", ""),
            "status": heartbeat.get("status", ""),
            "heartbeat_age": _heartbeat_age_seconds(heartbeat),
            "next_scheduled_run": heartbeat.get("next_scheduled_run", ""),
            "relaunched_by_launchd": bool(new_pid and new_pid != old_pid),
        },
        "summary": {
            "check_count": len(checks),
            "pass": sum(1 for item in checks if item["status"] == "PASS"),
            "warn": warn,
            "fail": fail,
            "blocking_failures": fail,
        },
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_runtime_startup_heartbeat_restart_validation.json",
        "latest_md": paths.logs_root / "latest_runtime_startup_heartbeat_restart_validation.md",
    }
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    runtime = payload.get("runtime") if isinstance(payload.get("runtime"), dict) else {}
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Runtime Startup / Heartbeat / Restart Validation

- status: `{payload.get('status')}`
- pid: `{runtime.get('pid', 0)}`
- old_pid: `{runtime.get('old_pid', 0)}`
- new_pid: `{runtime.get('new_pid', 0)}`
- relaunched_by_launchd: `{runtime.get('relaunched_by_launchd')}`
- heartbeat_age: `{runtime.get('heartbeat_age')}`
- blocking_failures: `{summary.get('blocking_failures', 0)}`
"""
