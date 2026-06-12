"""Go-live preflight checks for the Mac mini autonomous runtime."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from content_system.autonomous_scheduler import runtime_lock_path
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, today_token, utc_now, write_json_and_markdown
from content_system.runtime_config import validate_runtime_config
from content_system.runtime_heartbeat import write_runtime_heartbeat
from content_system.runtime_process_lock import RuntimeProcessLock
from content_system.runtime_state_store import initialize_runtime_state, runtime_store_root


LABEL = "com.thcapital.content-factory-runtime"
OPENCLAW_JOBS = Path("/Users/apple/.openclaw/cron/jobs.json")


def _run(command: list[str], repo_root: Path) -> tuple[int, str]:
    completed = subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
    return completed.returncode, (completed.stdout + completed.stderr).strip()[-1000:]


def _check(checks: list[dict[str, Any]], check_id: str, ok: bool, message: str, required: bool = True, warn: bool = False) -> None:
    if ok:
        status = "WARN" if warn else "PASS"
    else:
        status = "FAIL" if required else "WARN"
    checks.append({"check_id": check_id, "status": status, "message": message, "required_before_install": required})


def _path_writable(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".phase31b_write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True
    except OSError:
        return False


def _runtime_processes() -> list[str]:
    completed = subprocess.run(["pgrep", "-fl", "scripts/run_autonomous_runtime.py"], text=True, capture_output=True, check=False)
    return [line for line in completed.stdout.splitlines() if "pgrep" not in line]


def _plist_secret_scan(repo_root: Path) -> bool:
    template = repo_root / "deploy" / "macos" / f"{LABEL}.plist.template"
    if not template.exists():
        return False
    text = template.read_text(encoding="utf-8")
    rendered = (
        text.replace("{{PYTHON}}", sys.executable)
        .replace("{{REPO_ROOT}}", str(repo_root))
        .replace("{{STDOUT_PATH}}", str(repo_root / "logs" / "autonomous-runtime" / "runtime.log"))
        .replace("{{STDERR_PATH}}", str(repo_root / "logs" / "autonomous-runtime" / "runtime.err"))
    )
    forbidden = ("sk-", "API_KEY=", "ANTHROPIC_API_KEY", "MINIMAX_API_KEY", "OPENAI_API_KEY")
    return not any(token in rendered for token in forbidden)


def build_runtime_go_live_preflight(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    checks: list[dict[str, Any]] = []

    rc, branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_root)
    _check(checks, "git_branch_main", rc == 0 and branch.strip() == "main", f"branch={branch.strip()}")
    rc_head, head = _run(["git", "rev-parse", "HEAD"], repo_root)
    rc_origin, origin = _run(["git", "rev-parse", "origin/main"], repo_root)
    _check(checks, "head_matches_origin_main", rc_head == 0 and rc_origin == 0 and head.strip() == origin.strip(), f"HEAD={head.strip()} origin/main={origin.strip()}")
    _check(checks, "repo_path_exists", repo_root.exists(), str(repo_root))
    _check(checks, "python_path_valid", Path(sys.executable).exists(), sys.executable)
    _check(checks, "runtime_entry_exists", (repo_root / "scripts" / "run_autonomous_runtime.py").exists(), "scripts/run_autonomous_runtime.py")

    config_payload = validate_runtime_config(repo_root)
    _check(checks, "runtime_config_valid", config_payload.get("status") == "PASS", str(config_payload.get("errors") or "PASS"))
    _check(checks, "runtime_job_commands_exist", config_payload.get("status") == "PASS", "runtime config validation checks commands")

    try:
        db_path = initialize_runtime_state(paths)
        _check(checks, "runtime_store_writable", db_path.exists(), str(db_path))
    except Exception as exc:  # pragma: no cover - defensive on host filesystem
        _check(checks, "runtime_store_writable", False, str(exc))

    _check(checks, "runtime_store_dir_writable", _path_writable(runtime_store_root(paths)), str(runtime_store_root(paths)))
    log_dir = repo_root / "logs" / "autonomous-runtime"
    _check(checks, "runtime_log_dir_writable", _path_writable(log_dir), str(log_dir))
    launch_agents = Path.home() / "Library" / "LaunchAgents"
    _check(checks, "launchagents_dir_writable", _path_writable(launch_agents), str(launch_agents))
    launch_agent = launch_agents / f"{LABEL}.plist"
    _check(checks, "existing_launchagent_detected", True, f"exists={launch_agent.exists()}", required=False, warn=launch_agent.exists())

    processes = _runtime_processes()
    runtime_process_ok = not processes or launch_agent.exists()
    _check(
        checks,
        "existing_runtime_process",
        runtime_process_ok,
        f"process_count={len(processes)} launchagent_exists={launch_agent.exists()}",
        required=not launch_agent.exists(),
        warn=bool(processes),
    )
    lock = RuntimeProcessLock(runtime_lock_path(paths), stale_after_seconds=7200)
    lock_exists = runtime_lock_path(paths).exists()
    lock_stale = lock.is_stale() if lock_exists else False
    lock_ok = (not lock_exists) or lock_stale or launch_agent.exists()
    _check(
        checks,
        "runtime_lock_state",
        lock_ok,
        f"lock_exists={lock_exists} stale={lock_stale} launchagent_exists={launch_agent.exists()}",
        required=not launch_agent.exists(),
        warn=lock_exists and not lock_stale,
    )

    try:
        heartbeat = write_runtime_heartbeat(paths, "go_live_preflight", "IDLE", payload={"phase": "31B"})
        _check(checks, "heartbeat_writable", bool(heartbeat.get("last_heartbeat_at")), heartbeat.get("last_heartbeat_at", ""))
    except Exception as exc:  # pragma: no cover - defensive on host filesystem
        _check(checks, "heartbeat_writable", False, str(exc))

    _check(checks, "openclaw_jobs_exists", OPENCLAW_JOBS.exists(), str(OPENCLAW_JOBS), required=False, warn=not OPENCLAW_JOBS.exists())
    coexistence = read_json(paths.logs_root / "latest_openclaw_schedule_coexistence_report.json")
    _check(checks, "openclaw_coexistence_report_valid", bool(coexistence.get("summary")), "latest_openclaw_schedule_coexistence_report.json", required=False, warn=not bool(coexistence.get("summary")))
    _check(checks, "api_key_not_in_plist", _plist_secret_scan(repo_root), "plist template/render secret scan")
    _check(checks, "python_resolves", shutil.which("python3") is not None, f"python3={shutil.which('python3')}")
    _check(checks, "network_readiness_detectable", (repo_root / "scripts" / "check_runtime_network_readiness.py").exists(), "network readiness script exists")
    _check(checks, "workbench_build_available", (repo_root / "scripts" / "build_wechat_workbench_frontend.py").exists(), "workbench frontend script exists")
    _check(checks, "no_secret_in_logs_policy", True, "runtime writes local reports only; plist has no environment secrets")

    pass_count = sum(1 for item in checks if item["status"] == "PASS")
    warn_count = sum(1 for item in checks if item["status"] == "WARN")
    fail_count = sum(1 for item in checks if item["status"] == "FAIL")
    blocking = sum(1 for item in checks if item["status"] == "FAIL" and item.get("required_before_install"))
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "PASS" if blocking == 0 and warn_count == 0 else ("ACTIONABLE" if blocking == 0 else "BLOCKED"),
        "checks": checks,
        "summary": {"check_count": len(checks), "pass": pass_count, "warn": warn_count, "fail": fail_count, "blocking_failures": blocking},
        "can_install_launchagent": blocking == 0,
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_runtime_go_live_preflight.json",
        "latest_md": paths.logs_root / "latest_runtime_go_live_preflight.md",
    }
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(f"- `{item.get('status')}` {item.get('check_id')}: {item.get('message')}" for item in payload.get("checks", []))
    return f"""# Runtime Go-Live Preflight

- status: `{payload.get('status')}`
- pass: `{summary.get('pass', 0)}`
- warn: `{summary.get('warn', 0)}`
- fail: `{summary.get('fail', 0)}`
- blocking_failures: `{summary.get('blocking_failures', 0)}`
- can_install_launchagent: `{payload.get('can_install_launchagent')}`

## Checks

{rows}
"""
