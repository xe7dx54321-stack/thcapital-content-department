#!/usr/bin/env python3
"""Build the Phase 26 fallback search and backfill queue."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.fallback_backfill_queue import build_fallback_backfill_queue
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_fallback_backfill_queue(paths, ROOT)
    summary = payload.get("summary", {})
    print("Fallback Backfill Queue")
    print("=======================")
    for key in ("task_count", "high_priority", "requires_manual", "requires_api_key"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
