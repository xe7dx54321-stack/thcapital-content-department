#!/usr/bin/env python3
"""Build the stable daily ops baseline."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.stable_daily_ops_baseline import build_stable_daily_ops_baseline


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_stable_daily_ops_baseline(paths, ROOT)
    summary = payload.get("summary", {})
    print("Stable Daily Ops Baseline")
    print("=========================")
    print(f"baseline_status: {payload.get('baseline_status')}")
    print(f"can_run_daily: {summary.get('can_run_daily')}")
    print(f"blocking_issue_count: {summary.get('blocking_issue_count')}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
