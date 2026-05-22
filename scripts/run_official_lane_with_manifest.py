#!/usr/bin/env python3
"""Run the official update lane and write a P0-008 runtime manifest.

This is the P0-010 pilot integration. It wraps the existing official-lane
script instead of modifying the fetcher itself, so the legacy output contract
remains unchanged while we start producing a structured runtime manifest.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.runtime_manifest_official_lane import build_official_lane_manifest  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run official lane and write runtime manifest")
    parser.add_argument("--date", default=None, help="Run date in YYYY-MM-DD format. Defaults to today.")
    parser.add_argument("--source-id", action="append", default=[], help="Forward one source id to official lane. Repeatable.")
    parser.add_argument("--skip-run", action="store_true", help="Do not run fetcher; only translate existing packet JSON.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable result summary.")
    parser.add_argument(
        "--official-arg",
        action="append",
        default=[],
        help="Extra argument forwarded to market_official_update_lane.py. Repeatable.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = build_official_lane_manifest(
        repo_root=REPO_ROOT,
        run_date=args.date,
        source_ids=args.source_id,
        extra_args=args.official_arg,
        skip_run=args.skip_run,
    )

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2, default=str))
    else:
        print("Official Lane Runtime Manifest")
        print("================================")
        print(f"status: {result.status}")
        print(f"source_count: {result.source_count}")
        print(f"total_items_found: {result.total_items_found}")
        print(f"command_returncode: {result.command_returncode}")
        print(f"manifest: {result.manifest_path}")
        print(f"latest: {result.latest_manifest_path}")
        if result.packet_path:
            print(f"packet: {result.packet_path}")
        else:
            print("packet: not found")

    return 0 if result.status in {"SUCCESS", "PARTIAL", "UNKNOWN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
