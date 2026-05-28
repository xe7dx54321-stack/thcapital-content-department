#!/usr/bin/env python3
"""Build the version review board without changing decisions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.version_acceptance import build_version_review_board  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build version review board.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = build_version_review_board(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Version Review Board")
        print("====================")
        print(f"decisions: {result.decision_count}")
        print(f"accepted: {result.accepted_count}")
        print(f"rejected: {result.rejected_count}")
        print(f"board: {result.board_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
