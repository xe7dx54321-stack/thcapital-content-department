#!/usr/bin/env python3
"""Build Source Health v1 reports from config/sources.yaml.

This P0-006 command is intentionally static: it validates and summarizes the
source registry, then writes JSON/Markdown reports. It does not fetch remote
sources, retry failures, or alter existing ingestion outputs.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.source_health import build_source_health_report, write_default_reports  # noqa: E402
from content_system.sources import SourceRegistryError, load_source_registry  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Source Health v1 reports.")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y%m%d"),
        help="Report date in YYYYMMDD format. Defaults to today.",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=None,
        help="Optional path to sources.yaml. Defaults to config/sources.yaml.",
    )
    parser.add_argument(
        "--max-md-items",
        type=int,
        default=200,
        help="Maximum records to render in Markdown tables. JSON keeps all records.",
    )
    return parser.parse_args()


def print_summary(report, written_paths: dict[str, Path]) -> None:
    print("Source Health v1")
    print("================")
    print(f"schema_version: {report.schema_version}")
    print(f"registry_schema_version: {report.registry_schema_version}")
    print(f"sources: {report.source_count}")
    print(f"enabled: {report.enabled_count}")
    print(f"disabled: {report.disabled_count}")
    print(f"validation ERROR: {report.issue_summary.get('ERROR', 0)}")
    print(f"validation WARN: {report.issue_summary.get('WARN', 0)}")

    print("\nTier distribution:")
    for tier, count in report.tier_distribution.items():
        print(f"  {tier}: {count}")

    print("\nCategory distribution:")
    for category, count in report.category_distribution.items():
        print(f"  {category}: {count}")

    print("\nReports written:")
    for label, path in written_paths.items():
        print(f"  {label}: {path}")


def main() -> int:
    args = parse_args()
    paths = get_project_paths(REPO_ROOT)

    try:
        registry = load_source_registry(path=args.registry, repo_root=REPO_ROOT)
    except (OSError, SourceRegistryError) as exc:
        print(f"ERROR: failed to load source registry: {exc}")
        return 1

    report = build_source_health_report(registry)
    written_paths = write_default_reports(
        report,
        paths=paths,
        run_date=args.date,
        max_records=args.max_md_items,
    )

    print_summary(report, written_paths)

    if report.issue_summary.get("ERROR", 0):
        print("\nFAILED: source registry has validation errors.")
        return 1

    print("\nOK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
