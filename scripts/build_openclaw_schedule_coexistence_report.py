#!/usr/bin/env python3
"""Build OpenClaw scheduling coexistence report."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_schedule_coexistence_guard import build_openclaw_schedule_coexistence_report  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    payload, _ = build_openclaw_schedule_coexistence_report(get_project_paths(ROOT), ROOT)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"auto_modified_openclaw: {payload.get('auto_modified_openclaw')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
