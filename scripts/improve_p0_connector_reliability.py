#!/usr/bin/env python3
"""Build Phase 28 P0 connector reliability improvement report."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.connector_reliability_improvement import build_connector_reliability_improvement
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_connector_reliability_improvement(paths, ROOT)
    summary = payload.get("reliability_summary", {})
    print("P0 Connector Reliability Improvement")
    print("====================================")
    for key in ("issue_count", "high", "medium", "low", "safe_to_retry", "requires_manual"):
        print(f"{key}: {summary.get(key, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
