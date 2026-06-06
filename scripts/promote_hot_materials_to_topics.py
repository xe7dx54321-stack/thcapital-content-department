#!/usr/bin/env python3
"""Promote qualified hot materials into connector topic candidates."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.hot_material_topic_promotion import build_connector_promoted_topic_candidates
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_connector_promoted_topic_candidates(paths, ROOT)
    summary = payload.get("summary", {})
    print("Hot Material Topic Promotion")
    print("============================")
    for key in ("candidate_count", "promoted", "needs_evidence", "watch", "rejected"):
        print(f"{key}: {summary.get(key, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
