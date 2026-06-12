#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_downstream_router import load_downstream_routes, summarize_downstream_routes
from content_system.acquisition_playbook_common import basic_markdown, write_latest_report
from content_system.paths import get_project_paths


def main() -> int:
    routes = load_downstream_routes(ROOT)
    summary = summarize_downstream_routes(routes)
    payload = {"schema_version": "v1", "routes": routes, "summary": summary}
    write_latest_report(get_project_paths(ROOT), ROOT, "acquisition_downstream_routes", payload, basic_markdown("Acquisition Downstream Routes", summary))
    print(
        "acquisition-downstream-routes-build "
        f"route_count={summary.get('route_count', 0)} topic_scoring_routes={summary.get('topic_scoring_routes', 0)} "
        f"evidence_backfill_routes={summary.get('evidence_backfill_routes', 0)} watch_routes={summary.get('watch_routes', 0)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
