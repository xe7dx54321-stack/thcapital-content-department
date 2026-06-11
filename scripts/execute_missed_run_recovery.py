#!/usr/bin/env python3
"""Execute missed-run recovery plan in plan-only mode."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.missed_run_recovery import execute_missed_run_recovery  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    payload, _ = execute_missed_run_recovery(get_project_paths(ROOT), ROOT)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print("execution_mode: PLAN_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
