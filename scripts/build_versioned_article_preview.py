#!/usr/bin/env python3
"""Build versioned article preview HTML."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.versioned_article_preview import build_versioned_article_preview  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build versioned article preview.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = build_versioned_article_preview(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Versioned Article Preview")
        print("=========================")
        print(f"versions: {result.version_count}")
        print(f"html: {result.html_path}")
        print(f"json: {result.json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
