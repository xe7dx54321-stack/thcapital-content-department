#!/usr/bin/env python3
"""Run the Phase 26 hot material quality gate."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.hot_material_quality_gate import build_hot_material_quality_gate
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_hot_material_quality_gate(paths, ROOT)
    summary = payload.get("summary", {})
    print("Hot Material Quality Gate")
    print("=========================")
    print(f"gate_status: {payload.get('gate_status')}")
    for key in ("promote_to_topic_pipeline", "watch", "backfill_required", "reject"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
