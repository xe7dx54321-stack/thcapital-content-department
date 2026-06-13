#!/usr/bin/env python3
"""Validate content production playbooks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.content_production_playbook import validate_content_production_playbooks  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    payload, _ = validate_content_production_playbooks(get_project_paths(ROOT), ROOT)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"validate_status: {payload.get('validate_status')}")
    return 0 if payload.get("validate_status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

