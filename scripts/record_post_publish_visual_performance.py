#!/usr/bin/env python3
"""Record manual post-publish visual performance observations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import list_payload, read_json  # noqa: E402
from content_system.post_publish_visual_performance import build_post_publish_visual_performance_board, record_visual_performance  # noqa: E402


def list_sessions(paths) -> None:
    sessions_payload = read_json(paths.market_content_root / "07_publishing" / "latest_manual_publish_sessions.json")
    print("Manual Publish Sessions")
    print("=======================")
    for item in list_payload(sessions_payload, "sessions"):
        print(f"{item.get('publish_session_id')}: {item.get('publish_status')} final_candidate={item.get('final_candidate_id')}")
    if not list_payload(sessions_payload, "sessions"):
        print("No manual publish sessions found.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Record post-publish visual performance.")
    parser.add_argument("--list-sessions", action="store_true")
    parser.add_argument("--session", default="")
    parser.add_argument("--rating", default="UNKNOWN")
    parser.add_argument("--note", default="")
    parser.add_argument("--asset", default="")
    parser.add_argument("--effect", default="UNKNOWN")
    parser.add_argument("--asset-note", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    if args.list_sessions or not args.session:
        list_sessions(paths)
        payload, outputs = build_post_publish_visual_performance_board(paths, REPO_ROOT)
    else:
        payload, outputs = record_visual_performance(
            paths,
            REPO_ROOT,
            session_id=args.session,
            rating=args.rating,
            note=args.note,
            asset_id=args.asset,
            effect=args.effect,
            asset_note=args.asset_note,
        )
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(value) for key, value in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Post-publish Visual Performance")
        print("===============================")
        for key, value in payload.get("summary", {}).items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
