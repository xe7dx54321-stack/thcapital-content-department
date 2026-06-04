#!/usr/bin/env python3
"""Run a single Phase 21 trial day record."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.trial_day_execution import build_trial_day_execution


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a trial day execution record.")
    parser.add_argument("--day", type=int, required=True, choices=range(1, 6), help="Trial day number, 1-5.")
    parser.add_argument("--skip-phase20", action="store_true", help="Use existing Phase20 artifacts without rerunning the hardening pipeline.")
    return parser.parse_args()


def run_phase20() -> int:
    completed = subprocess.run([sys.executable, "scripts/run_phase20_daily_hardening_pipeline.py"], cwd=ROOT, text=True, check=False)
    return completed.returncode


def main() -> int:
    args = parse_args()
    if not args.skip_phase20:
        code = run_phase20()
        if code != 0:
            print(f"phase20 prerequisite returned {code}; continuing to record trial day status from latest artifacts.")
    paths = get_project_paths(ROOT)
    payload, _ = build_trial_day_execution(paths, ROOT, args.day)
    result = payload.get("daily_result", {})
    print(f"Trial Day {args.day} Execution")
    print("=====================")
    print(f"day_status: {result.get('day_status', 'UNKNOWN')}")
    print(f"issue_count: {len(payload.get('issues', []))}")
    print(f"action_count: {len(payload.get('operator_actions', []))}")
    print(f"can_continue_trial: {result.get('can_continue_trial', True)}")
    print(f"latest: {paths.logs_root / f'latest_trial_day_{args.day}_execution.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
