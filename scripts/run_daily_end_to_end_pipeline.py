#!/usr/bin/env python3
"""Run or dry-run the end-to-end daily pipeline graph."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.daily_pipeline_graph import run_daily_end_to_end  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run daily end-to-end pipeline.")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--execute-safe-nodes", action="store_true")
    args = parser.parse_args()
    payload, _ = run_daily_end_to_end(get_project_paths(ROOT), ROOT, execute=args.execute_safe_nodes)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"status: {payload.get('status')}")
    return 0 if payload.get("status") in {"SUCCESS", "ACTIONABLE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
