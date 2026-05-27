#!/usr/bin/env python3
"""Build weekly content retro report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.weekly_content_retro import build_weekly_content_retro_report, report_to_dict, write_weekly_content_retro_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build weekly content retro.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_weekly_content_retro_report(paths)
    outputs = write_weekly_content_retro_report(report, paths, REPO_ROOT)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        print("Weekly Content Retro")
        print("====================")
        print(f"status: {report.status}")
        print(f"high_value_candidates: {report.summary.get('high_value_candidate_count')}")
        print(f"publishing_queue: {report.summary.get('publishing_queue_count')}")
        for key, path in outputs.items():
            print(f"  {key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
