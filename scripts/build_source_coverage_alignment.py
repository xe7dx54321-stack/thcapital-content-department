#!/usr/bin/env python3
"""Build Source Registry coverage alignment report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.source_coverage import (  # noqa: E402
    build_source_coverage_report,
    report_to_dict,
    write_source_coverage_report,
)
from content_system.sources import load_source_registry  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build source coverage alignment.")
    parser.add_argument("--date", dest="run_date", help="Run date in YYYYMMDD or YYYY-MM-DD format.")
    parser.add_argument("--json", action="store_true", help="Print JSON report to stdout.")
    args = parser.parse_args()

    paths = get_project_paths(REPO_ROOT)
    registry = load_source_registry(repo_root=paths.repo_root)
    report = build_source_coverage_report(registry, paths, run_date=args.run_date)
    outputs = write_source_coverage_report(report, paths)

    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
        return 0

    print("Source Coverage Alignment")
    print("=========================")
    print(f"run_date: {report.run_date}")
    print(f"registry_source_count: {report.registry_source_count}")
    print(f"runtime_source_count: {report.runtime_source_count}")
    print(f"covered_count: {report.covered_count}")
    print(f"registry_only_count: {report.registry_only_count}")
    print(f"runtime_only_count: {report.runtime_only_count}")
    print("\nReports:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
