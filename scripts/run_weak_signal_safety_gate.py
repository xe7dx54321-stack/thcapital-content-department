#!/usr/bin/env python3
"""Run the OpenClaw weak signal safety gate."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.weak_signal_safety_gate import run_weak_signal_safety_gate


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = run_weak_signal_safety_gate(paths, ROOT)
    summary = payload.get("summary", {})
    print("Weak Signal Safety Gate")
    print("=======================")
    print(f"gate_status: {payload.get('gate_status')}")
    for key in ("item_count", "allow_as_weak_signal", "require_confirmation", "manual_review", "blocked", "hard_evidence_allowed"):
        print(f"{key}: {summary.get(key, 0)}")
    print(f"latest: {payload['outputs']['latest_json']}")
    return 0 if payload.get("gate_status") in {"PASS", "ACTIONABLE", "WARN", "BLOCKED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
