#!/usr/bin/env python3
"""Run the autonomous Content Factory runtime loop."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.autonomous_scheduler import run_autonomous_runtime_loop, run_scheduler_once  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run autonomous runtime.")
    parser.add_argument("--once", action="store_true", help="Run one scheduler tick and exit.")
    parser.add_argument("--execute", action="store_true", help="Execute due jobs instead of scheduler dry-run.")
    args = parser.parse_args()
    if args.once:
        payload, _ = run_scheduler_once(ROOT, execute=args.execute)
        print(f"status: {payload.get('status')}")
        return 0 if payload.get("status") in {"SUCCESS", "ACTIONABLE", "PAUSED", "LOCKED"} else 1
    run_autonomous_runtime_loop(ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
