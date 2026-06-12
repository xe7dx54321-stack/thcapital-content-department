#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_fallback_strategy import render_fallback_strategy_validation, validate_fallback_strategies
from content_system.acquisition_playbook_common import write_latest_report
from content_system.paths import get_project_paths


def main() -> int:
    payload = validate_fallback_strategies(ROOT)
    write_latest_report(get_project_paths(ROOT), ROOT, "acquisition_fallback_strategies_validation", payload, render_fallback_strategy_validation(payload))
    print(f"acquisition-fallback-strategies-validate status={payload.get('status')} strategy_count={payload.get('strategy_count', 0)}")
    return 0 if payload.get("status") in {"PASS", "ACTIONABLE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
