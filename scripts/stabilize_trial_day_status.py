#!/usr/bin/env python3
"""Stabilize Phase 23 trial day status."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.trial_day_status_stabilizer import build_trial_day_status_stabilizer


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_trial_day_status_stabilizer(paths, ROOT)
    summary = payload.get("stabilization_summary", {})
    print("Trial Day Status Stabilizer")
    print("===========================")
    print(f"status_before: {payload.get('status_before')}")
    print(f"status_after: {payload.get('status_after')}")
    print(f"blocker_count: {summary.get('blocker_count', 0)}")
    print(f"actionable_warning_count: {summary.get('actionable_warning_count', 0)}")
    print(f"operator_note_count: {summary.get('operator_note_count', 0)}")
    print(f"can_continue: {summary.get('can_continue')}")
    print(f"latest: {paths.logs_root / 'latest_trial_day_status_stabilizer.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
