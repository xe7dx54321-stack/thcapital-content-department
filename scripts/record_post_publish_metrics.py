#!/usr/bin/env python3
"""Record manually entered post-publish metrics."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import list_payload, read_json  # noqa: E402
from content_system.post_publish_metrics import build_post_publish_metrics_board, record_post_publish_metrics  # noqa: E402


def optional_int(value: str) -> int | None:
    return None if value == "" else int(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="Record post-publish manual metrics.")
    parser.add_argument("--list-sessions", action="store_true")
    parser.add_argument("--session", default="")
    parser.add_argument("--views", default="")
    parser.add_argument("--likes", default="")
    parser.add_argument("--wows", default="")
    parser.add_argument("--shares", default="")
    parser.add_argument("--saves", default="")
    parser.add_argument("--comments", default="")
    parser.add_argument("--new-followers", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--metric-time", default="")
    parser.add_argument("--hours-after-publish", type=float, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    sessions_payload = read_json(paths.market_content_root / "07_publishing" / "latest_manual_publish_sessions.json")
    sessions = list_payload(sessions_payload, "sessions")
    if args.session:
        result, payload, changed = record_post_publish_metrics(
            paths,
            REPO_ROOT,
            args.session,
            optional_int(args.views),
            optional_int(args.likes),
            optional_int(args.wows),
            optional_int(args.shares),
            optional_int(args.saves),
            optional_int(args.comments),
            optional_int(args.new_followers),
            args.note,
            args.metric_time,
            args.hours_after_publish,
        )
    else:
        result, payload = build_post_publish_metrics_board(paths, REPO_ROOT)
        changed = False
    if args.json:
        print(json.dumps({"result": asdict(result), "changed": changed, "payload": payload, "sessions": sessions if args.list_sessions else []}, ensure_ascii=False, indent=2))
    else:
        print("Post-publish Metrics")
        print("====================")
        print(f"metrics: {result.metrics_count}")
        print(f"published_sessions: {result.published_session_count}")
        print(f"average_views: {result.average_views}")
        print(f"average_likes: {result.average_likes}")
        print(f"changed: {changed}")
        print(f"board: {result.board_path}")
        if args.list_sessions:
            print("\nManual publish sessions:")
            if sessions:
                for item in sessions:
                    print(f"- {item.get('publish_session_id')} | {item.get('final_candidate_id')} | {item.get('publish_status')} | {item.get('published_url') or ''}")
            else:
                print("- No manual publish sessions recorded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
