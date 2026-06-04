#!/usr/bin/env python3
"""Update image asset library metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.image_asset_library import update_asset, update_image_asset_library  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Update image asset library.")
    parser.add_argument("--register-placeholder", help="Accepted for compatibility; default update registers placeholders from tasks.")
    parser.add_argument("--mark-available")
    parser.add_argument("--mark-rejected")
    parser.add_argument("--path", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    if args.mark_available:
        payload, outputs = update_asset(paths, REPO_ROOT, args.mark_available, status="AVAILABLE", asset_path=args.path, note=args.note)
    elif args.mark_rejected:
        payload, outputs = update_asset(paths, REPO_ROOT, args.mark_rejected, status="REJECTED", note=args.note)
    else:
        payload, outputs = update_image_asset_library(paths, REPO_ROOT)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(value) for key, value in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Image Asset Library")
        print("===================")
        for key, value in payload.get("summary", {}).items():
            print(f"{key}: {value}")
        print(f"latest: {outputs['memory_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
