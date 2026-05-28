#!/usr/bin/env python3
"""Update article version memory."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.article_version_memory import update_article_version_memory  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Update article version memory.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = update_article_version_memory(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Article Version Memory")
        print("======================")
        print(f"versions: {result.version_count}")
        print(f"accepted: {result.accepted_count}")
        print(f"rejected: {result.rejected_count}")
        print(f"average_score_delta: {result.average_score_delta}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
