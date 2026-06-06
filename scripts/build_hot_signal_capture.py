#!/usr/bin/env python3
"""Build the Phase 26 multi-lane hot signal capture report."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.hot_signal_capture import build_hot_signal_capture
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_hot_signal_capture(paths, ROOT)
    summary = payload.get("summary", {})
    print("Hot Signal Capture")
    print("==================")
    for key in ("lane_count", "active_lanes", "hot_signal_count", "candidate_for_topic_pool", "connector_item_count", "connector_signal_count"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
