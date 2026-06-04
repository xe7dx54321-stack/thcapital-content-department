#!/usr/bin/env python3
"""Calibrate Phase 23 publishing calendar readiness."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.publishing_calendar_readiness_calibration import build_publishing_calendar_readiness_calibration


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_publishing_calendar_readiness_calibration(paths, ROOT)
    summary = payload.get("summary", {})
    print("Publishing Calendar Readiness Calibration")
    print("=========================================")
    print(f"calendar_days: {summary.get('calendar_days', 0)}")
    print(f"ready_days: {summary.get('ready_days', 0)}")
    print(f"actionable_days: {summary.get('actionable_days', 0)}")
    print(f"hold_days: {summary.get('hold_days', 0)}")
    print(f"open_days: {summary.get('open_days', 0)}")
    print(f"blocked_days: {summary.get('blocked_days', 0)}")
    print(f"latest: {paths.market_content_root / '07_publishing/latest_publishing_calendar_readiness_calibration.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
