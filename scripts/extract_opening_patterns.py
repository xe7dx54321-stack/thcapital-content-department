#!/usr/bin/env python3
"""Extract opening patterns from current content assets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.opening_pattern import build_opening_pattern_report, report_to_dict, write_opening_pattern_report  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract Opening Patterns v1.")
    parser.add_argument("--json", action="store_true", help="Print report JSON.")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_opening_pattern_report(paths)
    outputs = write_opening_pattern_report(report, paths)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
        return 0
    print("Opening Patterns v1")
    print("===================")
    print(f"run_date: {report.run_date}")
    print(f"pattern_count: {report.pattern_count}")
    print(f"type_distribution: {report.type_distribution}")
    print("\nReports:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
