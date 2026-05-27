#!/usr/bin/env python3
"""Sync generated JSON artifacts into the SQLite runtime store."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_store import default_db_path, report_to_dict, sync_runtime_store  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync runtime store.")
    parser.add_argument("--db-path", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    db_path = Path(args.db_path).expanduser().resolve() if args.db_path else default_db_path(paths)
    report = sync_runtime_store(paths, REPO_ROOT, db_path)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        print("Runtime Store Sync")
        print("==================")
        print(f"status: {report.status}")
        print(f"db_path: {report.db_path}")
        for key, value in report.summary.items():
            print(f"{key}: {value}")
        if report.warnings:
            print("\nWarnings:")
            for item in report.warnings:
                print(f"  - {item}")
    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
