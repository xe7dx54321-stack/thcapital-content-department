#!/usr/bin/env python3
"""Build Phase 27 P0 source connector selection."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.p0_source_connector_selection import build_p0_source_connector_selection
from content_system.paths import get_project_paths


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_p0_source_connector_selection(paths, ROOT)
    summary = payload.get("summary", {})
    print("P0 Source Connector Selection")
    print("=============================")
    for key in ("selected_count", "rss_official_blog", "github_repo", "huggingface_feed", "arxiv_keyword", "manual_url_backfill"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
