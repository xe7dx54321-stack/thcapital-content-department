#!/usr/bin/env python3
"""Run Phase 27 RSS / official blog metadata connectors."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.rss_official_blog_connector import build_rss_official_blog_connector_run


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_rss_official_blog_connector_run(paths, ROOT)
    summary = payload.get("summary", {})
    print("RSS / Official Blog Connector Run")
    print("=================================")
    for key in ("source_count", "success_sources", "failed_sources", "empty_sources", "item_count"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
