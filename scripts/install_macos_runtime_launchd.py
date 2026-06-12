#!/usr/bin/env python3
"""Render or install the macOS LaunchAgent for autonomous runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import read_json, today_token, utc_now, write_json_and_markdown  # noqa: E402


LABEL = "com.thcapital.content-factory-runtime"
TEMPLATE = ROOT / "deploy" / "macos" / f"{LABEL}.plist.template"
LAUNCH_AGENT = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
LOG_DIR = ROOT / "logs" / "autonomous-runtime"


SECRET_VALUE_RE = re.compile(r"sk-[A-Za-z0-9_-]{8,}")
SECRET_ENV_RE = re.compile(r"\b(?:MINIMAX|ANTHROPIC|OPENAI|API)_API_KEY\s*=>\s*[^\n]+")


def _sanitize(text: str | None) -> str:
    sanitized = SECRET_ENV_RE.sub("<secret-env> => <redacted>", text or "")
    return SECRET_VALUE_RE.sub("<redacted>", sanitized)


def render_plist(python_path: str | None = None) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    python = python_path or sys.executable
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    replacements = {
        "{{PYTHON}}": python,
        "{{REPO_ROOT}}": str(ROOT),
        "{{STDOUT_PATH}}": str(LOG_DIR / "content-factory-runtime.runtime.log"),
        "{{STDERR_PATH}}": str(LOG_DIR / "content-factory-runtime.runtime.err"),
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    forbidden = ("sk-", "API_KEY=", "ANTHROPIC_API_KEY", "MINIMAX_API_KEY", "OPENAI_API_KEY")
    if any(token in text for token in forbidden):
        raise RuntimeError("Rendered plist appears to contain a secret-like token.")
    return text


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _run(command: list[str], timeout_seconds: int = 30) -> dict[str, Any]:
    try:
        completed = subprocess.run(command, text=True, capture_output=True, check=False, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        return {
            "command": " ".join(command),
            "returncode": 124,
            "stdout_tail": _sanitize(exc.stdout)[-2000:],
            "stderr_tail": _sanitize(((exc.stderr or "") + "\ncommand timed out").strip())[-2000:],
        }
    return {
        "command": " ".join(command),
        "returncode": completed.returncode,
        "stdout_tail": _sanitize(completed.stdout)[-2000:],
        "stderr_tail": _sanitize(completed.stderr)[-2000:],
    }


def _service_name() -> str:
    return f"gui/{os.getuid()}/{LABEL}"


def _launch_domain() -> str:
    return f"gui/{os.getuid()}"


def _check_loaded() -> dict[str, Any]:
    result = _run(["launchctl", "print", _service_name()])
    return {"loaded": result["returncode"] == 0, "print": result}


def _preflight_allows_install() -> tuple[bool, str]:
    paths = get_project_paths(ROOT)
    payload = read_json(paths.logs_root / "latest_runtime_go_live_preflight.json")
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    if not payload:
        return False, "Missing latest_runtime_go_live_preflight.json."
    if int(summary.get("blocking_failures") or 0) > 0:
        return False, "Preflight has blocking failures."
    if payload.get("can_install_launchagent") is not True:
        return False, "Preflight did not approve LaunchAgent installation."
    return True, "Preflight allows installation."


def _write_report(payload: dict[str, Any]) -> None:
    paths = get_project_paths(ROOT)
    outputs = {
        "latest_json": paths.logs_root / "latest_macos_runtime_launchagent_installation.json",
        "latest_md": paths.logs_root / "latest_macos_runtime_launchagent_installation.md",
    }
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    markdown = f"""# macOS Runtime LaunchAgent Installation

- installed: `{summary.get('installed')}`
- loaded: `{summary.get('loaded')}`
- enabled: `{summary.get('enabled')}`
- plist_path: `{payload.get('plist_path')}`
- label: `{LABEL}`
- dry_run: `{payload.get('dry_run')}`
"""
    write_json_and_markdown(payload, markdown, outputs)


def install(rendered: str) -> dict[str, Any]:
    allowed, reason = _preflight_allows_install()
    if not allowed:
        payload = {
            "schema_version": "v1",
            "generated_at": utc_now(),
            "run_date": today_token(),
            "status": "BLOCKED",
            "dry_run": False,
            "label": LABEL,
            "plist_path": str(LAUNCH_AGENT),
            "reason": reason,
            "steps": [],
            "summary": {"installed": False, "loaded": False, "enabled": False},
        }
        _write_report(payload)
        return payload

    LAUNCH_AGENT.parent.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    steps: list[dict[str, Any]] = []
    backup_path = ""
    if LAUNCH_AGENT.exists():
        backup = LAUNCH_AGENT.with_suffix(f".plist.{today_token()}.phase31b-backup")
        shutil.copy2(LAUNCH_AGENT, backup)
        backup_path = str(backup)
        steps.append({"step": "backup_existing_plist", "status": "OK", "backup_path": backup_path})
        steps.append({"step": "bootout_existing", **_run(["launchctl", "bootout", _launch_domain(), str(LAUNCH_AGENT)])})

    LAUNCH_AGENT.write_text(rendered, encoding="utf-8")
    steps.append({"step": "write_plist", "status": "OK", "sha256": _sha256_text(rendered)})
    bootstrap = _run(["launchctl", "bootstrap", _launch_domain(), str(LAUNCH_AGENT)])
    steps.append({"step": "launchctl_bootstrap", **bootstrap})
    enable = _run(["launchctl", "enable", _service_name()])
    steps.append({"step": "launchctl_enable", **enable})
    kickstart = _run(["launchctl", "kickstart", "-k", _service_name()], timeout_seconds=15)
    steps.append({"step": "launchctl_kickstart", **kickstart})
    loaded = _check_loaded()
    installed = LAUNCH_AGENT.exists()
    enabled = enable["returncode"] == 0
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "SUCCESS" if installed and loaded["loaded"] else "FAILED",
        "dry_run": False,
        "label": LABEL,
        "plist_path": str(LAUNCH_AGENT),
        "backup_path": backup_path,
        "steps": steps,
        "launchctl_print": loaded["print"],
        "summary": {"installed": installed, "loaded": loaded["loaded"], "enabled": enabled},
        "security": {"secret_scan_pass": True, "user_level_launch_agent": True, "no_business_schedule_in_plist": True},
    }
    _write_report(payload)
    return payload


def dry_run(rendered: str) -> dict[str, Any]:
    dry_path = LOG_DIR / f"{LABEL}.plist.dry-run"
    dry_path.parent.mkdir(parents=True, exist_ok=True)
    dry_path.write_text(rendered, encoding="utf-8")
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "DRY_RUN",
        "dry_run": True,
        "label": LABEL,
        "plist_path": str(LAUNCH_AGENT),
        "dry_run_rendered_path": str(dry_path),
        "summary": {"installed": False, "loaded": False, "enabled": False},
        "security": {"secret_scan_pass": True, "user_level_launch_agent": True, "no_business_schedule_in_plist": True},
    }
    print(f"dry_run_rendered_path: {dry_path}")
    print(f"target_launch_agent: {LAUNCH_AGENT}")
    print("installed: false")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Content Factory Runtime LaunchAgent.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--install", action="store_true")
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()
    rendered = render_plist(args.python)
    payload = dry_run(rendered) if args.dry_run else install(rendered)
    if not args.dry_run:
        print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    return 0 if payload.get("status") in {"SUCCESS", "DRY_RUN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
