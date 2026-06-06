#!/usr/bin/env python3
"""Run the simplified stable daily ops command."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.stable_daily_ops_runner import build_stable_daily_ops


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_stable_daily_ops(ROOT, paths.logs_root, paths.frontstage_root)
    summary = payload.get("daily_summary", {})
    print("Stable Daily Ops")
    print("================")
    print(f"status: {payload.get('status')}")
    print(f"baseline_status: {summary.get('baseline_status')}")
    print(f"operator_acceptance_status: {summary.get('operator_acceptance_status')}")
    print(f"blocking_issue_count: {summary.get('blocking_issue_count')}")
    print(f"workbench_ready: {summary.get('workbench_ready')}")
    print("Safety:")
    for key, value in payload.get("safety", {}).items():
        print(f"  {key}: {value}")
    print("Steps:")
    for step in payload.get("steps", []):
        print(f"  {step.get('name')}: {step.get('status')} ({step.get('return_code')})")
    return 0 if payload.get("status") in {"SUCCESS", "ACTIONABLE", "DEGRADED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
