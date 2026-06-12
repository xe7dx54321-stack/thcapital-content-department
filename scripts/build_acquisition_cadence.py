#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_cadence import build_acquisition_cadence_plan
from content_system.paths import get_project_paths


def main() -> int:
    payload, _ = build_acquisition_cadence_plan(get_project_paths(ROOT), ROOT)
    summary = payload.get("summary", {})
    print(
        "acquisition-cadence-build "
        f"lane_count={summary.get('lane_count', 0)} schedule_slot_count={summary.get('schedule_slot_count', 0)} "
        f"grouped_slots={summary.get('grouped_slots', 0)} shared_source_dedup_enabled={summary.get('shared_source_dedup_enabled', False)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
