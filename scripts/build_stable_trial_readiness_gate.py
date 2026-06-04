#!/usr/bin/env python3
"""Build Phase 23 stable trial readiness gate."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.stable_trial_readiness_gate import build_stable_trial_readiness_gate


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _ = build_stable_trial_readiness_gate(paths, ROOT)
    summary = payload.get("summary", {})
    print("Stable Trial Readiness Gate")
    print("===========================")
    print(f"gate_status: {payload.get('gate_status')}")
    print(f"pass: {summary.get('pass', 0)}")
    print(f"warn: {summary.get('warn', 0)}")
    print(f"fail: {summary.get('fail', 0)}")
    print(f"blocking_failures: {summary.get('blocking_failures', 0)}")
    print(f"latest: {paths.logs_root / 'latest_stable_trial_readiness_gate.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
