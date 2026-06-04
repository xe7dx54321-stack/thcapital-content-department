#!/usr/bin/env python3
"""Build manual publishing session calendar."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.publishing_session_calendar import build_publishing_session_calendar  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build publishing session calendar.")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload, outputs = build_publishing_session_calendar(get_project_paths(REPO_ROOT), REPO_ROOT, days=args.days)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(value) for key, value in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Publishing Session Calendar")
        print("===========================")
        for key, value in payload.get("summary", {}).items():
            print(f"{key}: {value}")
        print(f"latest: {outputs['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
