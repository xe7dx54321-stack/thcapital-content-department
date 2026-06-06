#!/usr/bin/env python3
"""Run Phase 27 manual URL backfill metadata ingestion."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.manual_url_backfill_ingestion import build_manual_url_backfill_ingestion
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_manual_url_backfill_ingestion(paths, ROOT)
    summary = payload.get("summary", {})
    print("Manual URL Backfill Ingestion")
    print("=============================")
    for key in ("manual_item_count", "ready_for_review", "needs_fetch", "invalid", "duplicate"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
