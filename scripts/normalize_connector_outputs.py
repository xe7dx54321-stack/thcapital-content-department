#!/usr/bin/env python3
"""Normalize Phase 27 connector outputs into shared upstream items."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.connector_output_normalizer import build_normalized_upstream_items
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_normalized_upstream_items(paths, ROOT)
    summary = payload.get("summary", {})
    print("Normalized Upstream Items")
    print("=========================")
    for key in ("item_count", "deduped_count", "candidate_for_hot_material_pool"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
