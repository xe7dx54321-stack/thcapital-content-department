#!/usr/bin/env python3
"""Build Phase 23 high-priority issue resolution plan."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.high_priority_issue_resolution import build_high_priority_issue_resolution_plan
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_high_priority_issue_resolution_plan(paths, ROOT)
    summary = payload.get("summary", {})
    print("High-priority Issue Resolution Plan")
    print("===================================")
    print(f"issue_count: {summary.get('issue_count', 0)}")
    print(f"high_priority: {summary.get('high_priority', 0)}")
    print(f"quick_fix: {summary.get('quick_fix', 0)}")
    print(f"manual_intervention: {summary.get('manual_intervention', 0)}")
    print(f"next_phase: {summary.get('next_phase', 0)}")
    print(f"monitor_only: {summary.get('monitor_only', 0)}")
    print(f"latest: {paths.logs_root / 'latest_high_priority_issue_resolution_plan.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
