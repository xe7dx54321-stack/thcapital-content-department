#!/usr/bin/env python3
"""Build the Agent Review Dashboard v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.agent_review_dashboard import (  # noqa: E402
    build_agent_review_dashboard_report,
    report_to_dict,
    write_agent_review_dashboard_report,
)
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Agent Review Dashboard v1.")
    parser.add_argument("--json", action="store_true", help="Print report JSON to stdout.")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_agent_review_dashboard_report(paths)
    outputs = write_agent_review_dashboard_report(report, paths)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
        return 0
    print("Agent Review Dashboard v1")
    print("=========================")
    print(f"run_date: {report.run_date}")
    for key, value in report.summary.items():
        print(f"{key}: {value}")
    print("\nReports:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
