#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_playbook_regression import run_acquisition_playbook_regression
from content_system.paths import get_project_paths


def main() -> int:
    payload, _ = run_acquisition_playbook_regression(get_project_paths(ROOT), ROOT)
    coverage = payload.get("coverage", {})
    duplicates = payload.get("duplicates", {})
    summary = payload.get("summary", {})
    print(
        "acquisition-playbook-regression "
        f"status={payload.get('status')} coverage_ratio={coverage.get('coverage_ratio', 0)} "
        f"duplicate_source_slots={duplicates.get('duplicate_source_slots', 0)} "
        f"duplicate_connector_runs={duplicates.get('duplicate_connector_runs', 0)} "
        f"blocking_failures={summary.get('blocking_failures', 0)}"
    )
    return 0 if payload.get("status") in {"PASS", "ACTIONABLE"} and int(summary.get("blocking_failures", 0) or 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
