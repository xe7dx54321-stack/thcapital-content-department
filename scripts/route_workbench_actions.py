#!/usr/bin/env python3
"""Route Chief Editor Agent actions into the pending queue."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.workbench_action_router import route_workbench_actions  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Route workbench actions.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = route_workbench_actions(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Workbench Action Router")
        print("=======================")
        print(f"actions: {result.action_count}")
        print(f"all_do_not_auto_execute: {result.all_do_not_auto_execute}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
