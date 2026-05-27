#!/usr/bin/env python3
"""Run the Chief Editor Agent in plan-only mode."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.chief_editor_agent import run_chief_editor_agent  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Chief Editor Agent.")
    parser.add_argument("--message", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = run_chief_editor_agent(get_project_paths(REPO_ROOT), REPO_ROOT, args.message)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Chief Editor Agent")
        print("==================")
        print(f"message_id: {result.message_id}")
        print(f"intent: {result.intent}")
        print(f"status: {payload.get('status')}")
        print(f"actions: {len(payload.get('required_actions') or [])}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
