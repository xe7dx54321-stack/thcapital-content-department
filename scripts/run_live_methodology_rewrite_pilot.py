#!/usr/bin/env python3
"""Run Phase 16 live methodology rewrite pilot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.live_methodology_rewrite_agent import run_live_methodology_rewrite_pilot  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run live methodology rewrite pilot.")
    parser.add_argument("--mode", choices=("dry_run", "live"), default="dry_run")
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload, outputs = run_live_methodology_rewrite_pilot(get_project_paths(REPO_ROOT), REPO_ROOT, mode=args.mode, limit=args.limit)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {k: str(v) for k, v in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Live Methodology Rewrite Pilot")
        print("===============================")
        print(f"status: {payload.get('status')}")
        for key, value in payload.get("summary", {}).items():
            print(f"{key}: {value}")
        print(f"latest: {outputs['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
