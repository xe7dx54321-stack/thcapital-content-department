#!/usr/bin/env python3
"""Build article visual plans."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.visual_plan_builder import build_visual_plans  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build article visual plans.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload, outputs = build_visual_plans(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {key: str(value) for key, value in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Article Visual Plans")
        print("====================")
        for key, value in payload.get("summary", {}).items():
            print(f"{key}: {value}")
        print(f"latest: {outputs['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
