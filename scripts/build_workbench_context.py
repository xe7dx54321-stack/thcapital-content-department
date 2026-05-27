#!/usr/bin/env python3
"""Build Chief Editor Agent context."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.workbench_context import build_and_write_workbench_context  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build workbench context.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = build_and_write_workbench_context(get_project_paths(REPO_ROOT), REPO_ROOT)
    payload = asdict(result)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Workbench Context")
        print("=================")
        print(f"selected_article_id: {result.selected_article_id}")
        for key, value in result.outputs.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
