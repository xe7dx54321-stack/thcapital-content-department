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
    upstream = summary.get("upstream_supply") if isinstance(summary.get("upstream_supply"), dict) else {}
    print("Upstream supply:")
    print(f"  gate_status: {upstream.get('gate_status', 'UNKNOWN')}")
    print(f"  status_label: {upstream.get('status_label', 'UNKNOWN')}")
    print(f"  hot_material_count: {upstream.get('hot_material_count', 0)}")
    print(f"  promote_to_topic_pipeline: {upstream.get('promote_to_topic_pipeline', 0)}")
    print(f"  backfill_required: {upstream.get('backfill_required', 0)}")
    print(f"  weak_supply_reasons: {upstream.get('weak_supply_reasons', [])}")
    print("Safety:")
    for key, value in payload.get("safety", {}).items():
        print(f"  {key}: {value}")
    print("Steps:")
    for step in payload.get("steps", []):
        print(f"  {step.get('name')}: {step.get('status')} ({step.get('return_code')})")
    return 0 if payload.get("status") in {"SUCCESS", "ACTIONABLE", "DEGRADED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
