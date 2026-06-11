#!/usr/bin/env python3
"""Initialize autonomous runtime SQLite state."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_state_store import initialize_runtime_state  # noqa: E402


def main() -> int:
    paths = get_project_paths(ROOT)
    db_path = initialize_runtime_state(paths)
    print(f"initialized: {db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
