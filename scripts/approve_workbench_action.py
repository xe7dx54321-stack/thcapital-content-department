#!/usr/bin/env python3
"""Approve, reject, defer, or list workbench actions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.workbench_action_approval import update_action_approval  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Approve/reject/defer workbench actions.")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--approve", default="")
    parser.add_argument("--reject", default="")
    parser.add_argument("--defer", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    action_id = args.approve or args.reject or args.defer or None
    status = "APPROVED" if args.approve else "REJECTED" if args.reject else "DEFERRED" if args.defer else None
    result, payload, changed = update_action_approval(get_project_paths(REPO_ROOT), REPO_ROOT, action_id, status, args.note)
    if args.json:
        print(json.dumps({"result": asdict(result), "changed": changed, "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Workbench Action Approval")
        print("=========================")
        print(f"actions: {result.action_count}")
        print(f"approved: {result.approved_count}")
        print(f"changed: {changed}")
        print(f"output: {result.output_path}")
        for action in payload.get("actions", []):
            print(f"- {action.get('action_id')} | {action.get('action_type')} | {action.get('approval_status')} | {action.get('description')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
