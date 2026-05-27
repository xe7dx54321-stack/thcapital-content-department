#!/usr/bin/env python3
"""Run the local daily scheduler wrapper."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.daily_scheduler import build_daily_scheduler_report, report_to_dict, write_daily_scheduler_report  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local daily scheduler wrapper.")
    parser.add_argument("--dry-run", action="store_true", help="Record the planned run without executing the pipeline.")
    parser.add_argument("--pipeline", choices=("learning-daily", "phase6-daily"), default="learning-daily")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_daily_scheduler_report(paths, REPO_ROOT, args.pipeline, args.dry_run)
    outputs = write_daily_scheduler_report(report, paths, REPO_ROOT)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        print("Daily Scheduler")
        print("===============")
        print(f"status: {report.status}")
        print(f"pipeline: {report.pipeline}")
        print(f"dry_run: {report.dry_run}")
        for key, path in outputs.items():
            print(f"  {key}: {path}")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
