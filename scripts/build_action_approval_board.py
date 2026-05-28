#!/usr/bin/env python3
"""Build the action approval board."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.workbench_action_approval import build_action_approval_board  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build action approval board.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = build_action_approval_board(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Action Approval Board")
        print("=====================")
        print(f"actions: {result.action_count}")
        print(f"approved: {result.approved_count}")
        print(f"output: {result.output_path}")
        print(f"board: {result.board_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
