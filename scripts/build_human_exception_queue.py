#!/usr/bin/env python3
"""Build the sparse human exception queue from agent review outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.human_exception_queue import (  # noqa: E402
    build_human_exception_queue_report,
    report_to_dict,
    write_human_exception_queue_report,
)
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Human Exception Queue v1.")
    parser.add_argument("--json", action="store_true", help="Print report JSON to stdout.")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_human_exception_queue_report(paths)
    outputs = write_human_exception_queue_report(report, paths)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
        return 0
    print("Human Exception Queue v1")
    print("========================")
    print(f"run_date: {report.run_date}")
    print(f"exception_count: {report.exception_count}")
    print(f"estimated_review_minutes: {report.total_estimated_review_minutes}")
    print("\nReports:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
