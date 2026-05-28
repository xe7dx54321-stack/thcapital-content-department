#!/usr/bin/env python3
"""Build manual publish session board."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.manual_publish_session import build_publish_session_board  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build publish session board.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = build_publish_session_board(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Manual Publish Session Board")
        print("============================")
        print(f"sessions: {result.session_count}")
        print(f"planned: {result.planned}")
        print(f"published: {result.published}")
        print(f"board: {result.board_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
