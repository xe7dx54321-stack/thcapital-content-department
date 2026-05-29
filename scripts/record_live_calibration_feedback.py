#!/usr/bin/env python3
"""Record human calibration feedback for a live comparison."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.live_calibration_feedback import build_live_calibration_board, update_feedback  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import list_payload  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Record live calibration feedback.")
    parser.add_argument("--list", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--accept")
    group.add_argument("--reject")
    group.add_argument("--merge")
    group.add_argument("--defer")
    parser.add_argument("--note", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    if args.accept:
        payload, outputs = update_feedback(paths, args.accept, "ACCEPT_LIVE", args.note)
    elif args.reject:
        payload, outputs = update_feedback(paths, args.reject, "REJECT_LIVE", args.note)
    elif args.merge:
        payload, outputs = update_feedback(paths, args.merge, "MERGE", args.note)
    elif args.defer:
        payload, outputs = update_feedback(paths, args.defer, "DEFER", args.note)
    else:
        payload, outputs = build_live_calibration_board(paths)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {k: str(v) for k, v in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Live Calibration Feedback")
        print("=========================")
        for item in list_payload(payload, "feedback"):
            print(f"{item.get('comparison_id')}: {item.get('decision')} {item.get('human_note') or ''}")
        for key, value in payload.get("summary", {}).items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
