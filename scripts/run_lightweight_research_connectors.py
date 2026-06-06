#!/usr/bin/env python3
"""Run Phase 27 lightweight GitHub / HuggingFace / arXiv connectors."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.lightweight_research_connectors import build_lightweight_research_connector_run
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_lightweight_research_connector_run(paths, ROOT)
    summary = payload.get("summary", {})
    print("Lightweight Research Connector Run")
    print("==================================")
    for key in ("connector_count", "success_connectors", "failed_connectors", "item_count"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
