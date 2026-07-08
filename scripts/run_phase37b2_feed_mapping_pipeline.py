#!/usr/bin/env python3
"""Run Phase37B2 feed discovery and competitor mapping pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.phase37b2_feed_mapping_pipeline import run_phase37b2_pipeline  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase37B2 feed mapping pipeline")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    payload, outputs = run_phase37b2_pipeline(limit=args.limit)
    print("Phase37B2 Feed Mapping Pipeline")
    print("=" * 40)
    print(f"status: {payload.get('status')}")
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False, indent=2))
    print(f"latest_json: {outputs['latest_json']}")
    print(f"latest_md: {outputs['latest_md']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
