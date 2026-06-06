#!/usr/bin/env python3
"""Build the Phase 26 high-value source expansion plan."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.high_value_source_expansion import build_high_value_source_expansion_plan
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_high_value_source_expansion_plan(paths, ROOT)
    summary = payload.get("summary", {})
    print("High-value Source Expansion Plan")
    print("================================")
    for key in ("candidate_count", "p0", "p1", "p2", "p3", "api_required", "no_api_required"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
