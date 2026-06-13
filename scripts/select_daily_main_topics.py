#!/usr/bin/env python3
"""Select the daily autonomous main topic."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.autonomous_topic_selection import build_daily_main_topic_selection  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    payload, _ = build_daily_main_topic_selection(get_project_paths(ROOT), ROOT)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"status: {payload.get('status')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

