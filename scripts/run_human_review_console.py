#!/usr/bin/env python3
"""Build the local human review console."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.human_review_console import build_human_review_console, report_to_dict, write_human_review_console  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build human review console.")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--list-candidates", action="store_true")
    parser.add_argument("--list-exceptions", action="store_true")
    parser.add_argument("--list-feedback", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_human_review_console(paths)
    write_human_review_console(report, paths, REPO_ROOT)
    payload = report_to_dict(report)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif args.list_candidates:
        for item in report.publishing_candidates:
            print(f"{item.get('publishing_candidate_id')}\t{item.get('publish_priority')}\t{item.get('title')}")
    elif args.list_exceptions:
        for item in report.human_exceptions:
            print(f"{item.get('exception_id')}\t{item.get('urgency')}\t{item.get('reason')}")
    elif args.list_feedback:
        for item in report.pending_feedback:
            print(f"{item.get('feedback_id')}\t{item.get('publishing_candidate_id')}\t{item.get('title')}")
    else:
        print("Human Review Console")
        print("====================")
        print(f"status: {report.status}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
