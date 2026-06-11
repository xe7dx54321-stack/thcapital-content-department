#!/usr/bin/env python3
"""Render or install the macOS LaunchAgent for autonomous runtime."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LABEL = "com.thcapital.content-factory-runtime"
TEMPLATE = ROOT / "deploy" / "macos" / f"{LABEL}.plist.template"
LAUNCH_AGENT = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
LOG_DIR = ROOT / "logs" / "autonomous-runtime"


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
    forbidden = ("sk-", "API_KEY=", "ANTHROPIC_API_KEY", "MINIMAX_API_KEY")
    if any(token in text for token in forbidden):
        raise RuntimeError("Rendered plist appears to contain a secret-like token.")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Content Factory Runtime LaunchAgent.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()
    rendered = render_plist(args.python)
    if args.dry_run:
        dry_path = LOG_DIR / f"{LABEL}.plist.dry-run"
        dry_path.write_text(rendered, encoding="utf-8")
        print(f"dry_run_rendered_path: {dry_path}")
        print(f"target_launch_agent: {LAUNCH_AGENT}")
        print("installed: false")
        return 0
    LAUNCH_AGENT.parent.mkdir(parents=True, exist_ok=True)
    if LAUNCH_AGENT.exists():
        backup = LAUNCH_AGENT.with_suffix(".plist.bak")
        shutil.copy2(LAUNCH_AGENT, backup)
        print(f"backup: {backup}")
    LAUNCH_AGENT.write_text(rendered, encoding="utf-8")
    subprocess.run(["launchctl", "unload", str(LAUNCH_AGENT)], check=False)
    completed = subprocess.run(["launchctl", "load", str(LAUNCH_AGENT)], check=False)
    print(f"installed: {completed.returncode == 0}")
    print(f"launch_agent: {LAUNCH_AGENT}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
