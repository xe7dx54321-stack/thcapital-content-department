#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.autonomous_acquisition_validation import run_autonomous_acquisition_dry_run
from content_system.paths import get_project_paths


def main() -> int:
    payload, _ = run_autonomous_acquisition_dry_run(get_project_paths(ROOT), ROOT)
    summary = payload.get("summary", {})
    print(
        "autonomous-acquisition-dry-run "
        f"status={payload.get('status')} lane_count={summary.get('lane_count', 0)} "
        f"scheduled_lane_runs={summary.get('scheduled_lane_runs', 0)} connector_runs={summary.get('connector_runs', 0)} "
        f"item_count={summary.get('item_count', 0)} warnings={summary.get('warnings', 0)} failures={summary.get('failures', 0)}"
    )
    return 0 if payload.get("status") in {"SUCCESS", "ACTIONABLE"} and int(summary.get("failures", 0) or 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
