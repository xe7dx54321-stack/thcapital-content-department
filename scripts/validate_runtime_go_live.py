#!/usr/bin/env python3
"""Validate installed autonomous runtime go-live state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_go_live_validation import validate_runtime_go_live  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate runtime go-live state.")
    parser.add_argument("--no-restart", action="store_true")
    args = parser.parse_args()
    payload, _ = validate_runtime_go_live(get_project_paths(ROOT), ROOT, restart=not args.no_restart)
    print(json.dumps(payload.get("runtime", {}), ensure_ascii=False))
    print(f"status: {payload.get('status')}")
    return 0 if payload.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
