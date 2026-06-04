#!/usr/bin/env python3
"""Run a Phase 24 stable trial day record."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.stable_trial_day import build_stable_trial_day


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a stable ops trial day record.")
    parser.add_argument("--day", type=int, choices=[1, 2, 3], required=True)
    args = parser.parse_args()
    paths = get_project_paths(ROOT)
    payload, _ = build_stable_trial_day(paths, ROOT, args.day)
    result = payload.get("day_result", {})
    ops = payload.get("ops_snapshot", {})
    print(f"Stable Trial Day {args.day}")
    print("==================")
    print(f"day_status: {result.get('day_status')}")
    print(f"can_continue: {result.get('can_continue')}")
    print(f"ready_to_publish: {ops.get('ready_to_publish', 0)}")
    print(f"actionable_warnings: {ops.get('actionable_warning_count', 0)}")
    print(f"latest: {paths.logs_root / f'latest_stable_trial_day_{args.day}.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
