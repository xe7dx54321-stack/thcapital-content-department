#!/usr/bin/env python3
"""Build recurring issue tracker and board."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.recurring_issue_tracker import build_recurring_issue_tracker


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_recurring_issue_tracker(paths, ROOT)
    summary = payload.get("summary", {})
    print("Recurring Issue Tracker")
    print("=======================")
    print(f"issue_count: {summary.get('issue_count', 0)}")
    print(f"high: {summary.get('high', 0)}")
    print(f"medium: {summary.get('medium', 0)}")
    print(f"low: {summary.get('low', 0)}")
    print(f"quick_fix_candidates: {summary.get('quick_fix_candidates', 0)}")
    print(f"latest: {paths.logs_root / 'latest_recurring_issue_tracker.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
