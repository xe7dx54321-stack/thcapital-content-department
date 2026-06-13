#!/usr/bin/env python3
"""Map audited legacy know-how to current methodology sidecars."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.legacy_knowhow_methodology_mapper import build_legacy_knowhow_methodology_mapping  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    payload, _ = build_legacy_knowhow_methodology_mapping(get_project_paths(ROOT), ROOT)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

