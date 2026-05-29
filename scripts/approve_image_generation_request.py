#!/usr/bin/env python3
"""Approve, reject, or defer an image generation request for future phases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.image_generation_approval_queue import build_queue, update_approval  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import list_payload  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Approve image generation request.")
    parser.add_argument("--list", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--approve")
    group.add_argument("--reject")
    group.add_argument("--defer")
    parser.add_argument("--note", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    if args.approve:
        payload, outputs = update_approval(paths, args.approve, "APPROVED", args.note)
    elif args.reject:
        payload, outputs = update_approval(paths, args.reject, "REJECTED", args.note)
    elif args.defer:
        payload, outputs = update_approval(paths, args.defer, "DEFERRED", args.note)
    else:
        payload, outputs = build_queue(paths)
    if args.json:
        print(json.dumps({"payload": payload, "outputs": {k: str(v) for k, v in outputs.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Image Generation Approval Requests")
        print("==================================")
        for item in list_payload(payload, "requests"):
            print(f"{item.get('approval_id')}: {item.get('approval_status')} generation_allowed={item.get('generation_allowed')} do_not_auto_generate={item.get('do_not_auto_generate')}")
        for key, value in payload.get("summary", {}).items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
