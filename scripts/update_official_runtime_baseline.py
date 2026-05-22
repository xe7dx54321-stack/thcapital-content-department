#!/usr/bin/env python3
"""Update the official lane runtime baseline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_baseline import (  # noqa: E402
    baseline_to_dict,
    update_runtime_baseline,
    write_runtime_baseline,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Update official runtime baseline.")
    parser.add_argument("--date", dest="run_date", help="Override run date in YYYYMMDD or YYYY-MM-DD format.")
    parser.add_argument("--json", action="store_true", help="Print baseline JSON to stdout.")
    args = parser.parse_args()

    paths = get_project_paths(REPO_ROOT)
    baseline = update_runtime_baseline(paths, run_date=args.run_date)
    outputs = write_runtime_baseline(baseline, paths)

    if args.json:
        print(json.dumps(baseline_to_dict(baseline), ensure_ascii=False, indent=2))
        return 0

    latest = baseline.records[-1] if baseline.records else None
    print("Official Runtime Baseline")
    print("=========================")
    print(f"records: {baseline.summary['record_count']}")
    if latest:
        print(f"latest_run_date: {latest.run_date}")
        print(f"latest_status: {latest.status}")
        print(f"quality_gate_status: {latest.quality_gate_status}")
        print(f"total_items_found: {latest.total_items_found}")
    print("\nReports:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
