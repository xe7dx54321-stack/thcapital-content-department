#!/usr/bin/env python3
"""Build Phase 24 stable ops readiness review."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.stable_ops_readiness_review import build_stable_ops_readiness_review


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_stable_ops_readiness_review(paths, ROOT)
    summary = payload.get("summary", {})
    print("Stable Ops Readiness Review")
    print("===========================")
    print(f"readiness_status: {payload.get('readiness_status')}")
    print(f"stable_trial_days: {summary.get('stable_trial_days', 0)}")
    print(f"ready_days: {summary.get('ready_days', 0)}")
    print(f"actionable_days: {summary.get('actionable_days', 0)}")
    print(f"blocked_days: {summary.get('blocked_days', 0)}")
    print(f"blocking_issues: {summary.get('blocking_issues', 0)}")
    print(f"latest: {paths.logs_root / 'latest_stable_ops_readiness_review.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
