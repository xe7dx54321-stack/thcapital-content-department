#!/usr/bin/env python3
"""Discover grouping keys from the local WeChat RSS all-feed."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.wechat_feed_discovery import discover_wechat_feed_ids  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover WeChat feed IDs from /feed/all.rss")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    payload, outputs = discover_wechat_feed_ids(limit=args.limit)
    summary = payload.get("summary", {})
    print("WeChat Feed ID Discovery")
    print("=" * 40)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"latest_json: {outputs['latest_json']}")
    print(f"latest_md: {outputs['latest_md']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
