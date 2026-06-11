#!/usr/bin/env python3
"""Run one autonomous scheduler tick."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.autonomous_scheduler import run_scheduler_once  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one scheduler tick.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--force-slot", default="")
    args = parser.parse_args()
    payload, _ = run_scheduler_once(ROOT, execute=args.execute, force_slot=args.force_slot)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"status: {payload.get('status')}")
    return 0 if payload.get("status") in {"SUCCESS", "ACTIONABLE", "PAUSED", "LOCKED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
