#!/usr/bin/env python3
"""Repair Phase 23 content queue readiness as a sidecar artifact."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.content_queue_readiness_repair import build_content_queue_readiness_repair
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_content_queue_readiness_repair(paths, ROOT)
    summary = payload.get("summary", {})
    print("Content Queue Readiness Repair")
    print("==============================")
    print(f"item_count: {summary.get('item_count', 0)}")
    print(f"improved: {summary.get('improved', 0)}")
    print(f"still_blocked: {summary.get('still_blocked', 0)}")
    print(f"ready_for_review: {summary.get('ready_for_review', 0)}")
    print(f"ready_to_publish: {summary.get('ready_to_publish', 0)}")
    print(f"needs_manual: {summary.get('needs_manual', 0)}")
    print(f"latest: {paths.market_content_root / '07_publishing/latest_content_queue_readiness_repair.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
