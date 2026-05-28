#!/usr/bin/env python3
"""Build final human publish checklist."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.final_publish_checklist import build_final_publish_checklist  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build final publish checklist.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = build_final_publish_checklist(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Final Publish Checklist")
        print("=======================")
        print(f"checklist_count: {result.checklist_count}")
        print(f"ready: {result.ready}")
        print(f"needs_attention: {result.needs_attention}")
        print(f"blocked: {result.blocked}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
