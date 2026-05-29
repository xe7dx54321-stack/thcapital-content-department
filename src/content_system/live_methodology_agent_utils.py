"""Shared helpers for Phase 16 live methodology pilot agents."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from content_system.agent_run_log import response_to_record, upsert_agent_run_record
from content_system.cost_budget_guard import build_cost_budget_guard
from content_system.llm_agent_client import (
    LLMRequest,
    LLMResponse,
    call_llm_agent,
    estimate_tokens,
    is_live_call_allowed,
    make_request_id,
)
from content_system.llm_provider_config import LLMProvider, load_llm_provider_config
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
DEFAULT_PROVIDER_ID = "anthropic"
DEFAULT_MODEL = "claude-sonnet-4.6"
PHASE16_AGENT_NAMES = {
    "live_methodology_brief_agent",
    "live_methodology_draft_agent",
    "live_methodology_rewrite_agent",
    "live_visual_prompt_agent",
}


def make_id(prefix: str, run_date: str, *parts: object) -> str:
    digest = hashlib.sha1("|".join(str(part) for part in (run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def short_json(value: Any, limit: int = 5000) -> str:
    text = json.dumps(value, ensure_ascii=False, indent=2)
    return text[:limit]


def provider_for_agent(repo_root: Path, agent_name: str) -> tuple[LLMProvider | None, str, str]:
    config = load_llm_provider_config(repo_root=repo_root)
    preference = config.get_agent_model(agent_name)
    provider_id = preference.preferred_provider if preference else DEFAULT_PROVIDER_ID
    model = preference.preferred_model if preference else DEFAULT_MODEL
    provider = config.get_provider(provider_id)
    return provider, provider_id, model


def synthetic_response(
    *,
    request: LLMRequest,
    status: str,
    error: str,
    fallback_reason: str,
    live_call_attempted: bool = False,
    live_call_succeeded: bool = False,
) -> LLMResponse:
    output_json = {"status": status, "fallback_reason": fallback_reason, "notes": ["Synthetic Phase 16 readiness response."]}
    output_text = json.dumps(output_json, ensure_ascii=False, indent=2)
    input_tokens = estimate_tokens(request.system_prompt) + estimate_tokens(request.user_prompt)
    output_tokens = estimate_tokens(output_text)
    return LLMResponse(
        request_id=request.request_id,
        provider_id=request.provider_id,
        model=request.model,
        mode=request.mode,
        status=status,
        output_text=output_text,
        output_json=output_json,
        usage={
            "estimated_input_tokens": input_tokens,
            "estimated_output_tokens": output_tokens,
            "estimated_total_tokens": input_tokens + output_tokens,
            "cost_estimation_note": "synthetic_ready_check",
        },
        error=error,
        latency_ms=0,
        estimated_cost_usd=0.0,
        fallback_used=bool(fallback_reason),
        fallback_reason=fallback_reason,
        live_call_attempted=live_call_attempted,
        live_call_succeeded=live_call_succeeded,
        raw_output_preview=output_text[:500],
        json_parse_status="FALLBACK" if fallback_reason else "OK",
    )


def run_pilot_llm(
    *,
    paths: ProjectPaths,
    repo_root: Path,
    agent_name: str,
    mode: str,
    item_id: str,
    metadata: dict[str, Any],
    expected_output_schema: dict[str, Any],
    system_prompt: str,
    user_prompt: str,
    source_artifact: str,
    output_artifact: str,
) -> tuple[LLMResponse, str, str, str, str, str]:
    provider, provider_id, model = provider_for_agent(repo_root, agent_name)
    request = LLMRequest(
        request_id=make_request_id(agent_name, provider_id, mode, item_id),
        agent_name=agent_name,
        provider_id=provider_id,
        model=model,
        mode=mode,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        expected_output_schema=expected_output_schema,
        metadata=metadata,
    )
    ready_check_status = "NOT_REQUIRED"
    ready_check_reason = ""
    cost_guard_status = "NOT_REQUIRED"
    if mode == "live":
        guard = build_cost_budget_guard(paths)
        cost_guard_status = guard.status
        if guard.status == "BLOCK":
            ready_check_status = "FAILED"
            ready_check_reason = "cost_guard_block"
        elif os.environ.get("THCAP_LLM_MODE", "").strip() != "live":
            ready_check_status = "FAILED"
            ready_check_reason = "THCAP_LLM_MODE_not_live"
        elif provider is None:
            ready_check_status = "FAILED"
            ready_check_reason = "provider_not_configured"
        else:
            allowed, reason = is_live_call_allowed(request, provider)
            ready_check_status = "PASSED" if allowed else "FAILED"
            ready_check_reason = reason
    if provider is None:
        response = synthetic_response(request=request, status="DRY_RUN", error="provider_not_configured", fallback_reason="provider_not_configured")
    elif mode == "live" and ready_check_status != "PASSED":
        response = synthetic_response(request=request, status="READY_CHECK_FAILED", error=ready_check_reason, fallback_reason=ready_check_reason)
    else:
        response = call_llm_agent(request, provider)
    upsert_agent_run_record(
        paths,
        response_to_record(
            response=response,
            agent_name=agent_name,
            run_date=today_token(),
            fallback_used=response.fallback_used,
            source_artifact=source_artifact,
            output_artifact=output_artifact,
        ),
    )
    return response, provider_id, model, ready_check_status, ready_check_reason, cost_guard_status


def status_for_response(response: LLMResponse, mode: str, ready_check_status: str) -> str:
    if mode == "live" and ready_check_status == "FAILED":
        return "READY_CHECK_FAILED"
    if response.status == "FAILED" and not response.output_json:
        return "FAILED"
    return "SUCCESS"


def live_summary(response: LLMResponse, ready_check_status: str, ready_check_reason: str, cost_guard_status: str) -> dict[str, Any]:
    return {
        "live_attempted": bool(response.live_call_attempted),
        "live_succeeded": bool(response.live_call_succeeded),
        "ready_check_status": ready_check_status,
        "ready_check_reason": ready_check_reason,
        "cost_guard_status": cost_guard_status,
        "fallback_used": bool(response.fallback_used),
        "fallback_reason": response.fallback_reason,
        "estimated_cost_usd": response.estimated_cost_usd,
    }


def outputs_with_repo_relative(payload: dict[str, Any], outputs: dict[str, Path], repo_root: Path) -> dict[str, Any]:
    enriched = dict(payload)
    enriched["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return enriched


def write_pilot_payload(payload: dict[str, Any], markdown: str, outputs: dict[str, Path], repo_root: Path) -> dict[str, Path]:
    return write_json_and_markdown(outputs_with_repo_relative(payload, outputs, repo_root), markdown, outputs)


def bullet_list(items: list[Any], empty: str = "None") -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {empty}"


def score_text_quality(text: str, keywords: list[str] | None = None) -> int:
    keywords = keywords or []
    score = 40
    score += min(20, len(text) // 250)
    score += min(20, sum(1 for keyword in keywords if keyword and keyword in text) * 4)
    if "风险" in text or "反方" in text:
        score += 8
    if "证据" in text or "来源" in text:
        score += 8
    if "不会自动" in text or "人工" in text:
        score += 4
    return max(0, min(100, score))


def render_policy_section() -> str:
    return """## Policy

- Live is disabled by default.
- Live requires explicit env + allowlist + API key + cost guard.
- Outputs are sidecar candidates only.
- No publishing, no image generation, no prompt/config/rule auto-apply.
"""
