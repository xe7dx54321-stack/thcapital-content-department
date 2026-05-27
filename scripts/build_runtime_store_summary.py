#!/usr/bin/env python3
"""Build runtime store summary report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_store import default_db_path, runtime_store_summary, write_runtime_store_summary  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build runtime store summary.")
    parser.add_argument("--db-path", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    db_path = Path(args.db_path).expanduser().resolve() if args.db_path else default_db_path(paths)
    summary = runtime_store_summary(paths, db_path)
    outputs = write_runtime_store_summary(paths, summary)
    if args.json:
        print(json.dumps({"schema_version": "v1", "summary": summary}, ensure_ascii=False, indent=2))
    else:
        print("Runtime Store Summary")
        print("=====================")
        for key in ("pipeline_runs", "agent_runs", "content_artifacts", "publishing_candidates", "human_feedback_records", "system_events"):
            print(f"{key}: {summary.get(key)}")
        print(f"agent_failed_count: {summary.get('agent_failed_count')}")
        print(f"estimated_cost_usd: {summary.get('estimated_cost_usd')}")
        print("\nReports:")
        for key, path in outputs.items():
            print(f"  {key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
