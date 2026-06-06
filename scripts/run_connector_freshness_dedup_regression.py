#!/usr/bin/env python3
"""Run connector freshness and dedupe regression."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.connector_freshness_dedup_regression import build_connector_freshness_dedup_regression
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_connector_freshness_dedup_regression(paths, ROOT)
    freshness = payload.get("freshness_summary", {})
    dedup = payload.get("dedup_summary", {})
    print("Connector Freshness and Dedup Regression")
    print("========================================")
    print(f"regression_status: {payload.get('regression_status')}")
    for key in ("today", "this_week", "stale", "unknown"):
        print(f"{key}: {freshness.get(key, 0)}")
    print(f"duplicate_ratio: {dedup.get('duplicate_ratio', 0.0)}")
    return 0 if payload.get("regression_status") in {"PASS", "WARN", "FAIL"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
