#!/usr/bin/env python3
"""Compare live pilot sidecars with rule outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.live_output_quality_comparison import build_live_output_quality_comparison  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare live outputs.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload, outputs = build_live_output_quality_comparison(get_project_paths(REPO_ROOT))
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {k: str(v) for k, v in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Live Output Quality Comparison")
        print("==============================")
        for key, value in payload.get("summary", {}).items():
            print(f"{key}: {value}")
        print(f"latest: {outputs['latest_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
