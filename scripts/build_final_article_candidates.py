#!/usr/bin/env python3
"""Build final article candidates from promoted versions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.final_article_candidate import build_final_article_candidates  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build final article candidates.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, payload = build_final_article_candidates(get_project_paths(REPO_ROOT), REPO_ROOT)
    if args.json:
        print(json.dumps({"result": asdict(result), "payload": payload}, ensure_ascii=False, indent=2))
    else:
        print("Final Article Candidates")
        print("========================")
        print(f"candidate_count: {result.candidate_count}")
        print(f"ready_for_final_review: {result.ready_for_final_review}")
        print(f"needs_final_check: {result.needs_final_check}")
        print(f"hold: {result.hold}")
        print(f"output: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
