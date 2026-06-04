#!/usr/bin/env python3
"""Build Phase 22 weekly publishing calendar."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.weekly_publishing_calendar_v2 import build_weekly_publishing_calendar


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a manual weekly publishing calendar.")
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()
    paths = get_project_paths(ROOT)
    payload, _ = build_weekly_publishing_calendar(paths, ROOT, max(1, args.days))
    summary = payload.get("summary", {})
    print("Weekly Publishing Calendar")
    print("==========================")
    print(f"calendar_days: {summary.get('calendar_days', 0)}")
    print(f"ready_days: {summary.get('ready_days', 0)}")
    print(f"hold_days: {summary.get('hold_days', 0)}")
    print(f"blocked_days: {summary.get('blocked_days', 0)}")
    print(f"open_days: {summary.get('open_days', 0)}")
    print(f"latest: {paths.market_content_root / '07_publishing/latest_weekly_publishing_calendar.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
