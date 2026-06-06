#!/usr/bin/env python3
"""Build the Content Factory v1 closeout report."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.content_factory_v1_closeout import build_content_factory_v1_closeout
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_content_factory_v1_closeout(paths, ROOT)
    daily = payload.get("daily_use", {})
    print("Content Factory v1 Closeout")
    print("===========================")
    print(f"v1_status: {payload.get('v1_status')}")
    print(f"recommended_command: {daily.get('recommended_command')}")
    print(f"operator_review_required: {daily.get('operator_review_required')}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
