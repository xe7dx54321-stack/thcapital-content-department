#!/usr/bin/env python3
"""Rollback latest OpenClaw conflict resolution apply."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_conflict_resolution import rollback_latest_conflict_resolution  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Rollback OpenClaw conflict resolution.")
    parser.add_argument("--latest", action="store_true", required=True)
    args = parser.parse_args()
    _ = args
    payload, _outputs = rollback_latest_conflict_resolution(get_project_paths(ROOT))
    print(json.dumps({key: payload.get(key) for key in ("status", "restored", "backup_path", "restored_hash")}, ensure_ascii=False))
    return 0 if payload.get("status") == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
