#!/usr/bin/env python3
"""Build post-publish metrics board."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.post_publish_metrics import build_post_publish_metrics_board  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build post-publish metrics board.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = build_post_publish_metrics_board(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Post-publish Metrics Board")
        print("==========================")
        print(f"metrics: {result.metrics_count}")
        print(f"published_sessions: {result.published_session_count}")
        print(f"board: {result.board_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
