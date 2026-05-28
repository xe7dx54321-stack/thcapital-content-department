#!/usr/bin/env python3
"""Execute approved rewrite actions into new versions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.rewrite_action_executor import execute_rewrite_actions  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute rewrite actions.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = execute_rewrite_actions(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Rewrite Action Executor")
        print("=======================")
        print(f"status: {result.status}")
        print(f"versions: {result.version_count}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
