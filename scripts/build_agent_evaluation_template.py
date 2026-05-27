#!/usr/bin/env python3
"""Build human-in-the-loop agent evaluation template."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.agent_evaluation import build_agent_evaluation_template, template_to_dict, write_agent_evaluation_template  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Agent Evaluation Template v1.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    template = build_agent_evaluation_template(paths)
    outputs = write_agent_evaluation_template(template, paths)
    if args.json:
        print(json.dumps(template_to_dict(template), ensure_ascii=False, indent=2))
    else:
        print("Agent Evaluation Template v1")
        print("============================")
        print(f"run_date: {template.run_date}")
        print(f"evaluation_count: {template.evaluation_count}")
        for key, path in outputs.items():
            print(f"  {key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
