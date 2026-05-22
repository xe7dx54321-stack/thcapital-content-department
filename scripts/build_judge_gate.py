#!/usr/bin/env python3
"""Build Judge Agent Gate v1 decisions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.judge_gate import build_judge_gate_report, report_to_dict, write_judge_gate_report  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Judge Gate v1.")
    parser.add_argument("--json", action="store_true", help="Print report JSON to stdout.")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_judge_gate_report(paths)
    outputs = write_judge_gate_report(report, paths)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
        return 0
    print("Judge Gate v1")
    print("=============")
    print(f"run_date: {report.run_date}")
    print(f"decision_count: {report.decision_count}")
    print(f"decision_distribution: {report.decision_distribution}")
    print("\nReports:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
