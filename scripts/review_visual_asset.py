#!/usr/bin/env python3
"""Approve, reject, or request revision for visual assets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.final_visual_review import build_final_visual_review, update_review  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import list_payload  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Review a visual asset.")
    parser.add_argument("--list", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--approve")
    group.add_argument("--reject")
    group.add_argument("--needs-revision")
    group.add_argument("--defer")
    parser.add_argument("--note", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    if args.approve:
        payload, outputs = update_review(paths, REPO_ROOT, args.approve, "APPROVED", args.note)
    elif args.reject:
        payload, outputs = update_review(paths, REPO_ROOT, args.reject, "REJECTED", args.note)
    elif args.needs_revision:
        payload, outputs = update_review(paths, REPO_ROOT, args.needs_revision, "NEEDS_REVISION", args.note)
    elif args.defer:
        payload, outputs = update_review(paths, REPO_ROOT, args.defer, "DEFERRED", args.note)
    else:
        payload, outputs = build_final_visual_review(paths, REPO_ROOT)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(value) for key, value in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Visual Asset Reviews")
        print("====================")
        for review in list_payload(payload, "reviews"):
            print(f"{review.get('asset_id')}: {review.get('review_status')} wechat_ready={review.get('wechat_ready')}")
        for key, value in payload.get("summary", {}).items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
