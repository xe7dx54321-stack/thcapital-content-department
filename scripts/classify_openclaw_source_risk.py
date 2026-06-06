#!/usr/bin/env python3
"""Classify OpenClaw source migration risk."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_source_risk_classifier import build_openclaw_source_risk_classification
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_openclaw_source_risk_classification(paths, ROOT)
    summary = payload.get("summary", {})
    print("OpenClaw Source Risk Classification")
    print("===================================")
    for key in ("source_count", "p0", "p1", "p2", "p3", "do_not_migrate", "metadata_connector", "manual_backfill", "weak_signal", "blocked"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
