#!/usr/bin/env python3
"""Run live scheduler trigger validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_live_trigger_validation import run_live_trigger_validation  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate autonomous scheduler live trigger.")
    parser.add_argument("--delay-seconds", type=int, default=None)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args()
    payload, _ = run_live_trigger_validation(get_project_paths(ROOT), ROOT, args.delay_seconds, args.timeout_seconds)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"trigger_source: {payload.get('trigger_source')}")
    print(f"status: {payload.get('status')}")
    return 0 if payload.get("status") == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
