#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_playbook_runtime import build_runtime_acquisition_plan
from content_system.paths import get_project_paths


def main() -> int:
    payload, _ = build_runtime_acquisition_plan(get_project_paths(ROOT), ROOT)
    summary = payload.get("summary", {})
    print(
        "runtime-acquisition-plan "
        f"lane_runs={summary.get('lane_runs', 0)} grouped_runs={summary.get('grouped_runs', 0)} "
        f"connector_runs={summary.get('connector_runs', 0)} shared_source_dedup_count={summary.get('shared_source_dedup_count', 0)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
