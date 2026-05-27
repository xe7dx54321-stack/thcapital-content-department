#!/usr/bin/env python3
"""Validate config/llm_providers.json."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.llm_provider_config import load_llm_provider_config, validate_llm_provider_config  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LLM provider config.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    parser.add_argument("--provider", type=str, default=None, help="Validate one provider in detail.")
    args = parser.parse_args()
    config = load_llm_provider_config(repo_root=REPO_ROOT)
    issues = validate_llm_provider_config(config, provider_filter=args.provider)
    counts = Counter(issue.severity for issue in issues)
    payload = {
        "schema_version": config.schema_version,
        "default_provider": config.default_provider,
        "default_mode": config.default_mode,
        "default_light_provider": config.default_light_provider,
        "default_light_model": config.default_light_model,
        "default_reasoning_provider": config.default_reasoning_provider,
        "default_reasoning_model": config.default_reasoning_model,
        "provider_count": len(config.providers),
        "providers": [provider.provider_id for provider in config.providers if not args.provider or provider.provider_id == args.provider],
        "agent_model_count": len(config.agent_model_map),
        "agent_model_map": [asdict(preference) for preference in config.agent_model_map],
        "issues": [asdict(issue) for issue in issues],
        "error_count": counts.get("ERROR", 0),
        "warn_count": counts.get("WARN", 0),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("LLM Provider Config Validation")
        print("==============================")
        print(f"schema_version: {payload['schema_version']}")
        print(f"default_provider: {payload['default_provider']}")
        print(f"default_mode: {payload['default_mode']}")
        print(f"default_light_model: {payload['default_light_provider']}/{payload['default_light_model']}")
        print(f"default_reasoning_model: {payload['default_reasoning_provider']}/{payload['default_reasoning_model']}")
        print(f"providers: {payload['provider_count']}")
        print(f"agent_model_map: {payload['agent_model_count']}")
        print("\nIssues:")
        print(f"  ERROR: {payload['error_count']}")
        print(f"  WARN: {payload['warn_count']}")
        for issue in issues:
            provider = issue.provider_id or "<config>"
            field = issue.field or "<unknown>"
            print(f"  {issue.severity}: {provider}.{field}: {issue.message}")
        print("\nOK" if payload["error_count"] == 0 else "\nFAILED")
    return 1 if payload["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
