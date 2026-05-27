#!/usr/bin/env python3
"""Initialize the local SQLite runtime store."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_store import default_db_path, init_runtime_store  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize SQLite runtime store.")
    parser.add_argument("--db-path", default=None)
    parser.add_argument("--reset-confirm", default="", help="Use I_UNDERSTAND to drop and recreate tables.")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    db_path = Path(args.db_path).expanduser().resolve() if args.db_path else default_db_path(paths)
    reset = args.reset_confirm == "I_UNDERSTAND"
    if args.reset_confirm and not reset:
        print("Refusing reset: --reset-confirm must equal I_UNDERSTAND")
        return 2
    final_path = init_runtime_store(paths, db_path, reset=reset)
    print("Runtime Store Init")
    print("==================")
    print(f"db_path: {final_path}")
    print(f"reset: {reset}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
