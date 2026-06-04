#!/usr/bin/env python3
"""Build Phase 21 weekly trial retrospective."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.weekly_trial_retrospective import build_weekly_trial_retrospective


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_weekly_trial_retrospective(paths, ROOT)
    summary = payload.get("trial_summary", {})
    print("Weekly Trial Retrospective")
    print("==========================")
    for key in ("days_recorded", "pass_days", "warn_days", "blocked_days", "can_continue"):
        print(f"{key}: {summary.get(key)}")
    print(f"recurring_issues_count: {len(payload.get('recurring_issues', []))}")
    print(f"latest: {paths.logs_root / 'latest_weekly_trial_retrospective.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
