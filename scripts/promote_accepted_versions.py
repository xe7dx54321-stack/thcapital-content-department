#!/usr/bin/env python3
"""Promote human-accepted versions into final-candidate inputs."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.accepted_version_promotion import build_accepted_version_promotions  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote accepted article versions.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = build_accepted_version_promotions(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Accepted Version Promotion")
        print("==========================")
        print(f"accepted_version_count: {result.accepted_version_count}")
        print(f"promoted_count: {result.promoted_count}")
        print(f"skipped_count: {result.skipped_count}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
