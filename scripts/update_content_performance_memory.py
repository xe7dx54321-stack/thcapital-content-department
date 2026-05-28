#!/usr/bin/env python3
"""Update content performance memory."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.content_performance_memory import update_content_performance_memory  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Update content performance memory.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = update_content_performance_memory(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Content Performance Memory")
        print("==========================")
        print(f"records: {result.record_count}")
        print(f"high_or_excellent: {result.high_or_excellent_count}")
        print(f"low: {result.low_count}")
        print(f"average_views: {result.average_views}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
