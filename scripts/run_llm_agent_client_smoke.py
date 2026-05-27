#!/usr/bin/env python3
"""Smoke test the Phase 6 LLM agent client in mock/dry-run mode."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.llm_agent_client import LLMRequest, call_llm_agent, make_request_id, response_to_dict  # noqa: E402
from content_system.llm_provider_config import load_llm_provider_config, resolve_agent_provider_and_model, resolve_mode_from_env  # noqa: E402
from content_system.prompt_registry import load_prompt_registry, render_prompt  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run LLM agent client smoke test.")
    parser.add_argument("--agent", default="llm_judge_agent", help="Agent prompt id.")
    parser.add_argument("--provider", default=None, help="Provider id. Defaults to config/env.")
    parser.add_argument("--mode", default=None, choices=("dry_run", "live"), help="dry_run or live.")
    parser.add_argument("--model", default=None, help="Model name override.")
    parser.add_argument("--json", action="store_true", help="Print JSON response.")
    args = parser.parse_args()
    config = load_llm_provider_config(repo_root=REPO_ROOT)
    provider, model = resolve_agent_provider_and_model(config, args.agent, args.provider, args.model)
    mode = resolve_mode_from_env(config, args.mode)
    registry = load_prompt_registry(repo_root=REPO_ROOT)
    sample_inputs = {
        "review_item": {"review_item_id": "sample", "title": "Sample AI update", "quality_score": 82, "evidence_ids": ["ev_1", "ev_2"], "source_ids": ["openai_blog"], "target_platforms": ["wechat"]},
        "platform_package": {"package_id": "pkg_sample", "publish_status": "READY_FOR_HUMAN_REVIEW"},
        "content_brief": {"brief_id": "brief_sample", "core_claim": "Sample claim with evidence."},
        "quality_review": {"total_score": 82},
        "llm_proponent_review": {"support_level": "STRONG"},
        "llm_critic_review": {"severity": "LOW"},
        "rule_judge_decision": {"decision": "APPROVED_FOR_QUEUE", "decision_score": 88, "release_readiness": "READY"},
        "revision_instruction": {"review_item_id": "sample", "logic_fixes": ["Clarify implication."]},
        "content_draft": {"draft_id": "draft_sample"},
        "llm_judge_decision": {"decision": "APPROVED_FOR_QUEUE"},
    }
    prompt_inputs = {key: value for key, value in sample_inputs.items()}
    system_prompt, user_prompt, schema = render_prompt(args.agent, prompt_inputs, registry=registry, repo_root=REPO_ROOT)
    request = LLMRequest(
        request_id=make_request_id(args.agent, provider.provider_id, mode, "smoke"),
        agent_name=args.agent,
        provider_id=provider.provider_id,
        model=model,
        mode=mode,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        expected_output_schema=schema,
        metadata=sample_inputs,
    )
    response = call_llm_agent(request, provider)
    if args.json:
        print(json.dumps({"request": asdict(request), "response": response_to_dict(response)}, ensure_ascii=False, indent=2))
    else:
        print("LLM Agent Client Smoke")
        print("======================")
        print(f"agent: {args.agent}")
        print(f"provider: {response.provider_id}")
        print(f"model: {response.model}")
        print(f"mode: {response.mode}")
        print(f"status: {response.status}")
        print(f"output_keys: {', '.join(response.output_json.keys())}")
    return 1 if response.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
