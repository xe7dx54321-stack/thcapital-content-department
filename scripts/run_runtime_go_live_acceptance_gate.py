#!/usr/bin/env python3
"""Run Phase31B go-live acceptance gate."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_go_live_acceptance_gate import run_go_live_acceptance_gate  # noqa: E402


def main() -> int:
    payload, _ = run_go_live_acceptance_gate(get_project_paths(ROOT), ROOT)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"gate_status: {payload.get('gate_status')}")
    return 0 if payload.get("gate_status") in {"GO_LIVE_APPROVED", "GO_LIVE_WITH_WARNINGS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
