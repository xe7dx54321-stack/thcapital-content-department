#!/usr/bin/env python3
"""Validate autonomous runtime configuration."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.runtime_config import write_runtime_config_validation  # noqa: E402


def main() -> int:
    payload, _ = write_runtime_config_validation(ROOT)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"status: {payload.get('status')}")
    if payload.get("errors"):
        for error in payload["errors"]:
            print(f"ERROR: {error}")
    return 0 if payload.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
