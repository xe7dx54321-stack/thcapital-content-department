#!/usr/bin/env python3
"""Run publishing API dry-run validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.publishing_dry_run import build_publishing_dry_run_report, report_to_dict, write_publishing_dry_run_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run publishing dry-run checks.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_publishing_dry_run_report(paths)
    write_publishing_dry_run_report(report, paths, REPO_ROOT)
    payload = report_to_dict(report)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Publishing API Dry-run")
        print("======================")
        print(f"status: {report.status}")
        print(f"ready_count: {report.summary.get('ready_count')}")
        print(f"not_ready_count: {report.summary.get('not_ready_count')}")
        print(f"hold_count: {report.summary.get('hold_count')}")
        print("would_publish_all_false: true")
    return 0 if report.status in {"SUCCESS", "DEGRADED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
