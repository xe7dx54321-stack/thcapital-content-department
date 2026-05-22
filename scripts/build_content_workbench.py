#!/usr/bin/env python3
"""Build the daily content workbench board."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.content_workbench import (  # noqa: E402
    build_content_workbench_report,
    report_to_dict,
    write_content_workbench_report,
)
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Content Workbench v1 board.")
    parser.add_argument("--date", dest="run_date", help="Run date in YYYYMMDD or YYYY-MM-DD format.")
    parser.add_argument("--json", action="store_true", help="Print report JSON to stdout.")
    args = parser.parse_args()

    paths = get_project_paths(REPO_ROOT)
    report = build_content_workbench_report(paths, run_date=args.run_date)
    outputs = write_content_workbench_report(report, paths)

    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
        return 0

    print("Content Workbench v1")
    print("====================")
    print(f"run_date: {report.run_date}")
    for key, value in report.summary.items():
        print(f"{key}: {value}")
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
