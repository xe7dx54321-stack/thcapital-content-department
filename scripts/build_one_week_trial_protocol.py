#!/usr/bin/env python3
"""Build the Phase 20 one-week trial protocol."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.trial_run_protocol import build_one_week_trial_protocol


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_one_week_trial_protocol(paths, ROOT)
    print("One-week Trial Run Protocol")
    print("===========================")
    print(f"days: {payload.get('trial_period', {}).get('days', 0)}")
    print(f"daily_checklist_count: {len(payload.get('daily_checklist', []))}")
    print(f"success_criteria_count: {len(payload.get('success_criteria', []))}")
    print(f"latest: {paths.logs_root / 'latest_one_week_trial_run_protocol.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
