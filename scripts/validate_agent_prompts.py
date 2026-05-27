#!/usr/bin/env python3
"""Validate config/agent_prompts.json."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.prompt_registry import load_prompt_registry, validate_prompt_registry  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LLM agent prompt registry.")
    parser.add_argument("--list", action="store_true", help="List prompts.")
    parser.add_argument("--prompt", type=str, default=None, help="Show one prompt.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    args = parser.parse_args()
    registry = load_prompt_registry(repo_root=REPO_ROOT)
    issues = validate_prompt_registry(registry, prompt_filter=args.prompt)
    counts = Counter(issue.severity for issue in issues)
    prompts = [prompt for prompt in registry.prompts if not args.prompt or prompt.prompt_id == args.prompt]
    payload = {
        "schema_version": registry.schema_version,
        "updated_at": registry.updated_at,
        "prompt_count": len(registry.prompts),
        "prompts": [asdict(prompt) for prompt in prompts],
        "issues": [asdict(issue) for issue in issues],
        "error_count": counts.get("ERROR", 0),
        "warn_count": counts.get("WARN", 0),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Agent Prompt Registry Validation")
        print("===============================")
        print(f"schema_version: {registry.schema_version}")
        print(f"updated_at: {registry.updated_at}")
        print(f"prompts: {len(registry.prompts)}")
        print("\nIssues:")
        print(f"  ERROR: {payload['error_count']}")
        print(f"  WARN: {payload['warn_count']}")
        for issue in issues:
            print(f"  {issue.severity}: {issue.prompt_id or '<registry>'}.{issue.field or '<unknown>'}: {issue.message}")
        if args.list or args.prompt:
            print("\nPrompts:")
            for prompt in prompts:
                print(f"  {prompt.prompt_id} {prompt.version} {prompt.agent_role}")
        print("\nOK" if payload["error_count"] == 0 else "\nFAILED")
    return 1 if payload["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
