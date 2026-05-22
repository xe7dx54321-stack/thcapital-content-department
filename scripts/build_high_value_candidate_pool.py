#!/usr/bin/env python3
"""Build the daily high-value candidate pool."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.high_value_candidates import (  # noqa: E402
    build_high_value_candidate_report,
    report_to_dict,
    write_high_value_candidate_report,
)
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Daily High-Value Candidate Pool v1.")
    parser.add_argument("--date", dest="run_date", help="Run date in YYYYMMDD or YYYY-MM-DD format.")
    parser.add_argument("--json", action="store_true", help="Print report JSON to stdout.")
    args = parser.parse_args()

    paths = get_project_paths(REPO_ROOT)
    report = build_high_value_candidate_report(paths, run_date=args.run_date)
    outputs = write_high_value_candidate_report(report, paths)

    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
        return 0

    print("Daily High-Value Candidates")
    print("===========================")
    print(f"run_date: {report.run_date}")
    print(f"candidate_count: {report.candidate_count}")
    print(f"A_band: {report.band_counts.get('A', 0)}")
    print(f"B_band: {report.band_counts.get('B', 0)}")
    if report.warnings:
        print("warnings:")
        for warning in report.warnings:
            print(f"  - {warning}")
    print("\nReports:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
