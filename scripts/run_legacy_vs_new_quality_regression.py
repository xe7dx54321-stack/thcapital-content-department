#!/usr/bin/env python3
"""Run legacy-vs-new quality regression."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.legacy_vs_new_quality_regression import build_legacy_vs_new_quality_regression  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    payload, _ = build_legacy_vs_new_quality_regression(get_project_paths(ROOT), ROOT)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"regression_status: {payload.get('regression_status')}")
    return 0 if payload.get("regression_status") in {"PASS", "ACTIONABLE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

