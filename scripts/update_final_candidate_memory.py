#!/usr/bin/env python3
"""Update final candidate memory."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.final_candidate_memory import update_final_candidate_memory  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Update final candidate memory.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = update_final_candidate_memory(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Final Candidate Memory")
        print("======================")
        print(f"final_candidate_count: {result.final_candidate_count}")
        print(f"ready_count: {result.ready_count}")
        print(f"needs_attention_count: {result.needs_attention_count}")
        print(f"blocked_count: {result.blocked_count}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
