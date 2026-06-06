#!/usr/bin/env python3
"""Build the Phase 26 daily hot material pool."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.daily_hot_material_pool import build_daily_hot_material_pool
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_daily_hot_material_pool(paths, ROOT)
    summary = payload.get("summary", {})
    print("Daily Hot Material Pool")
    print("=======================")
    for key in ("material_count", "write_now", "develop_topic", "watch", "backfill_first", "hold"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
