#!/usr/bin/env python3
"""List or record final review status actions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.final_review_actions import record_final_review_action  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Record local final review actions.")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--mark-ready", default="")
    parser.add_argument("--mark-needs-edit", default="")
    parser.add_argument("--mark-hold", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    final_candidate_id = args.mark_ready or args.mark_needs_edit or args.mark_hold
    action = "MARK_READY" if args.mark_ready else "MARK_NEEDS_EDIT" if args.mark_needs_edit else "MARK_HOLD" if args.mark_hold else ""
    result, payload, changed = record_final_review_action(get_project_paths(REPO_ROOT), REPO_ROOT, final_candidate_id, action, args.note)
    if args.json:
        print(json.dumps({"result": asdict(result), "changed": changed, "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Final Review Actions")
        print("====================")
        print(f"actions: {result.action_count}")
        print(f"ready: {result.ready_count}")
        print(f"needs_edit: {result.needs_edit_count}")
        print(f"hold: {result.hold_count}")
        print(f"changed: {changed}")
        print(f"output: {result.output_path}")
        for item in payload.get("actions", []):
            print(f"- {item.get('final_candidate_id')} | {item.get('action')} | {item.get('human_note')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
