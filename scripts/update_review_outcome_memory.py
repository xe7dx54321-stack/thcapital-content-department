#!/usr/bin/env python3
"""Update Review Outcome Memory v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.review_outcome_memory import (  # noqa: E402
    build_review_outcome_memory,
    memory_to_dict,
    write_review_outcome_memory,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Update Review Outcome Memory v1.")
    parser.add_argument("--json", action="store_true", help="Print memory JSON to stdout.")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    memory = build_review_outcome_memory(paths)
    outputs = write_review_outcome_memory(memory, paths)
    if args.json:
        print(json.dumps(memory_to_dict(memory), ensure_ascii=False, indent=2))
        return 0
    print("Review Outcome Memory v1")
    print("========================")
    for key, value in memory.summary.items():
        print(f"{key}: {value}")
    print("\nReports:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
