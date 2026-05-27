#!/usr/bin/env python3
"""Build retry/fallback plan from runtime health and failure reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.retry_fallback_runner import build_retry_fallback_runner_report, report_to_dict, write_retry_fallback_runner_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build retry/fallback runner report.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_retry_fallback_runner_report(paths, REPO_ROOT)
    outputs = write_retry_fallback_runner_report(report, paths, REPO_ROOT)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        print("Retry / Fallback Runner")
        print("=======================")
        print(f"status: {report.status}")
        print(f"retry_plan: {len(report.retry_plan)}")
        print(f"fallback_candidates: {len(report.fallback_candidates)}")
        for key, path in outputs.items():
            print(f"  {key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
