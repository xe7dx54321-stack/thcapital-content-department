#!/usr/bin/env python3
"""Execute approved topic replacement actions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.topic_replacement_executor import execute_topic_replacement_actions  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute topic replacement actions.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = execute_topic_replacement_actions(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Topic Replacement Executor")
        print("==========================")
        print(f"status: {result.status}")
        print(f"replacements: {result.replacement_count}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
