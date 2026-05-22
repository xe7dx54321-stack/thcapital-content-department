#!/usr/bin/env python3
"""Build Source Runtime Health v1 reports.

This P0-007 command aligns config/sources.yaml with existing runtime artifacts
such as manifests, source packets, and logs. It intentionally does not fetch
remote sources, retry failed fetches, alter fetcher behavior, or create a DB.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.source_runtime_health import (  # noqa: E402
    build_source_runtime_health_report,
    write_default_runtime_reports,
)
from content_system.sources import load_source_registry, validate_registry  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Source Runtime Health v1 reports.")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y%m%d"),
        help="Run date in YYYYMMDD format. Default: today.",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=200,
        help="Maximum records/evidence rows to show in markdown reports.",
    )
    parser.add_argument(
        "--fail-on-missing",
        action="store_true",
        help="Exit with 1 if enabled daily/hourly sources have no runtime evidence.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = get_project_paths(REPO_ROOT)
    registry = load_source_registry(repo_root=REPO_ROOT)
    validation_issues = validate_registry(registry)
    errors = [issue for issue in validation_issues if issue.severity == "ERROR"]

    if errors:
        print("Source registry has validation errors; aborting runtime health build.")
        for issue in errors[:20]:
            print(f"ERROR {issue.source_id or '-'} {issue.field or '-'}: {issue.message}")
        return 1

    report = build_source_runtime_health_report(registry=registry, paths=paths, run_date=args.date)
    output_paths = write_default_runtime_reports(
        report=report,
        paths=paths,
        run_date=args.date,
        max_records=args.max_records,
    )

    print("Source Runtime Health v1")
    print("========================")
    print(f"run_date: {report.run_date}")
    print(f"sources: {report.source_count}")
    print(f"enabled: {report.enabled_count}")
    print(f"observed: {report.observed_count}")
    print(f"missing_expected: {report.missing_expected_count}")
    print("")
    print("Status distribution:")
    for status, count in report.status_distribution.items():
        print(f"  {status}: {count}")
    print("")
    print("Reports:")
    for name, path in output_paths.items():
        print(f"  {name}: {path}")

    if args.fail_on_missing and report.missing_expected_count:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
