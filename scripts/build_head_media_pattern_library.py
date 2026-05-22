#!/usr/bin/env python3
"""Build Head Media Pattern Library v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.head_media_pattern import build_head_media_pattern_library, library_to_dict, write_head_media_pattern_library  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Head Media Pattern Library v1.")
    parser.add_argument("--json", action="store_true", help="Print library JSON.")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    library = build_head_media_pattern_library(paths)
    outputs = write_head_media_pattern_library(library, paths)
    if args.json:
        print(json.dumps(library_to_dict(library), ensure_ascii=False, indent=2))
        return 0
    print("Head Media Pattern Library v1")
    print("=============================")
    for key, value in library.summary.items():
        print(f"{key}: {value}")
    print("\nReports:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
