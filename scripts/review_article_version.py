#!/usr/bin/env python3
"""Accept, reject, revise-more, defer, or list article versions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.version_acceptance import update_version_review  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Review generated article versions.")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--accept", default="")
    parser.add_argument("--reject", default="")
    parser.add_argument("--revise-more", default="")
    parser.add_argument("--defer", default="")
    parser.add_argument("--score", type=float, default=None)
    parser.add_argument("--note", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    version_id = args.accept or args.reject or args.revise_more or args.defer or None
    decision = "ACCEPT" if args.accept else "REJECT" if args.reject else "REVISE_MORE" if args.revise_more else "DEFER" if args.defer else None
    result, payload, changed = update_version_review(
        get_project_paths(REPO_ROOT),
        REPO_ROOT,
        version_id,
        decision,
        args.score,
        args.note,
    )
    if args.json:
        print(json.dumps({"result": asdict(result), "changed": changed, "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Article Version Review")
        print("======================")
        print(f"decisions: {result.decision_count}")
        print(f"accepted: {result.accepted_count}")
        print(f"rejected: {result.rejected_count}")
        print(f"changed: {changed}")
        print(f"output: {result.output_path}")
        for item in payload.get("decisions", []):
            print(f"- {item.get('version_id')} | {item.get('decision')} | score={item.get('human_score')} | {item.get('human_notes')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
