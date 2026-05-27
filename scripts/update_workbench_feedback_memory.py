#!/usr/bin/env python3
"""Update workbench feedback memory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.workbench_feedback_memory import update_workbench_feedback_memory  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Update workbench feedback memory.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    memory = update_workbench_feedback_memory(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps(memory, ensure_ascii=False, indent=2))
    else:
        print("Workbench Feedback Memory")
        print("=========================")
        print(f"preferences: {len(memory.get('preferences') or [])}")
        print(f"recent_feedback: {len(memory.get('recent_feedback') or [])}")
        print(f"rule_suggestion_inputs: {len(memory.get('rule_suggestion_inputs') or [])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
