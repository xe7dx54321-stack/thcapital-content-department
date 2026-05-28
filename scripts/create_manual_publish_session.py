#!/usr/bin/env python3
"""Create or update manual publish sessions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.manual_publish_session import build_publish_session_board, update_manual_publish_session  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Track manual publish sessions.")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--create", default="")
    parser.add_argument("--mark-published", default="")
    parser.add_argument("--cancel", default="")
    parser.add_argument("--defer", default="")
    parser.add_argument("--url", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--planned-publish-at", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    if args.create or args.mark_published or args.cancel or args.defer:
        session_id = args.mark_published or args.cancel or args.defer
        status = "MANUALLY_PUBLISHED" if args.mark_published else "CANCELLED" if args.cancel else "DEFERRED" if args.defer else ""
        result, payload, changed = update_manual_publish_session(paths, REPO_ROOT, args.create, session_id, status, args.url, args.note, args.planned_publish_at)
    else:
        result, payload = build_publish_session_board(paths, REPO_ROOT)
        changed = False
    if args.json:
        print(json.dumps({"result": asdict(result), "changed": changed, "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Manual Publish Sessions")
        print("=======================")
        print(f"sessions: {result.session_count}")
        print(f"planned: {result.planned}")
        print(f"published: {result.published}")
        print(f"cancelled: {result.cancelled}")
        print(f"deferred: {result.deferred}")
        print(f"changed: {changed}")
        print(f"board: {result.board_path}")
        for item in payload.get("sessions", []):
            print(f"- {item.get('publish_session_id')} | {item.get('final_candidate_id')} | {item.get('publish_status')} | {item.get('published_url')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
