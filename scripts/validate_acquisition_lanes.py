#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_lane_registry import render_lane_validation, validate_acquisition_lanes
from content_system.acquisition_playbook_common import write_latest_report
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload = validate_acquisition_lanes(ROOT)
    write_latest_report(paths, ROOT, "acquisition_lane_taxonomy_validation", payload, render_lane_validation(payload))
    print(
        "acquisition-lanes-validate "
        f"status={payload.get('status')} lane_count={payload.get('lane_count', 0)} "
        f"active_lane_count={payload.get('active_lane_count', 0)} weak_signal_lane_count={payload.get('weak_signal_lane_count', 0)}"
    )
    return 0 if payload.get("status") in {"PASS", "ACTIONABLE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
