#!/usr/bin/env python3
"""Run the Phase 22 daily content ops runner."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.daily_content_ops_runner import VALID_MODES, build_daily_content_ops_runner
from content_system.paths import get_project_paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a manual daily content ops action list.")
    parser.add_argument("--mode", choices=sorted(VALID_MODES), default="dry_run")
    args = parser.parse_args()
    paths = get_project_paths(ROOT)
    payload, _ = build_daily_content_ops_runner(paths, ROOT, args.mode)
    summary = payload.get("summary", {})
    print("Daily Content Ops Runner")
    print("========================")
    print(f"status: {payload.get('status')}")
    print(f"mode: {payload.get('mode')}")
    print(f"action_count: {summary.get('action_count', 0)}")
    print(f"ready_actions: {summary.get('ready_actions', 0)}")
    print(f"blocked_actions: {summary.get('blocked_actions', 0)}")
    print(f"quick_fix_actions: {summary.get('quick_fix_actions', 0)}")
    print(f"latest: {paths.logs_root / 'latest_daily_content_ops_runner.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
