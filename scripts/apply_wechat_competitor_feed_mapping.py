#!/usr/bin/env python3
"""Apply local WeChat competitor feed mapping."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.wechat_competitor_feed_mapping import apply_competitor_feed_mapping  # noqa: E402


def main() -> int:
    payload, outputs = apply_competitor_feed_mapping()
    summary = payload.get("summary", {})
    print("WeChat Competitor Feed Mapping")
    print("=" * 40)
    print(f"status: {payload.get('status')}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"latest_json: {outputs['latest_json']}")
    print(f"latest_md: {outputs['latest_md']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
