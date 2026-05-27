"""Mock-first LLM agent client with guarded Phase 7 live pilot support.

The client deliberately defaults to mock/dry-run. Non-mock live providers are
guarded by explicit environment switches and agent allowlists so the system can
validate schemas and logging without requiring paid API credentials by default.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from content_system.llm_provider_config import LLMProvider


@dataclass(frozen=True)
class LLMRequest:
    request_id: str
    agent_name: str
    provider_id: str
    model: str
    mode: str
    system_prompt: str
    user_prompt: str
    expected_output_schema: dict[str, Any]
    metadata: dict[str, Any]


@dataclass(frozen=True)
class LLMResponse:
    request_id: str
    provider_id: str
    model: str
    mode: str
    status: str
    output_text: str
    output_json: dict[str, Any]
    usage: dict[str, Any]
    error: str
    latency_ms: int
    estimated_cost_usd: float
    fallback_used: bool
    fallback_reason: str
    live_call_attempted: bool
    live_call_succeeded: bool
    raw_output_preview: str
    json_parse_status: str


def make_request_id(agent_name: str, provider_id: str, mode: str, item_id: str | None = None) -> str:
    date = datetime.now().strftime("%Y%m%d")
    digest = hashlib.sha1("|".join((agent_name, provider_id, mode, item_id or "")).encode("utf-8")).hexdigest()[:14]
    return f"llmreq_{date}_{digest}"


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _quality_score(metadata: dict[str, Any]) -> float:
    value = (metadata.get("review_item") or {}).get("quality_score", metadata.get("quality_score", 0))
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _evidence_count(metadata: dict[str, Any]) -> int:
    item = metadata.get("review_item") or {}
    evidence = item.get("evidence_ids") or metadata.get("evidence_ids") or []
    return len(evidence) if isinstance(evidence, list) else 0


def _source_count(metadata: dict[str, Any]) -> int:
    item = metadata.get("review_item") or {}
    sources = item.get("source_ids") or metadata.get("source_ids") or []
    return len(sources) if isinstance(sources, list) else 0


def _mock_proponent(metadata: dict[str, Any]) -> dict[str, Any]:
    score = _quality_score(metadata)
    evidence_count = _evidence_count(metadata)
    source_count = _source_count(metadata)
    item = metadata.get("review_item") or {}
    title = item.get("title") or "Untitled content package"
    level = "STRONG" if score >= 80 and evidence_count >= 2 else "MODERATE" if score >= 65 else "WEAK"
    confidence = min(0.93, 0.45 + score / 220 + evidence_count * 0.06 + source_count * 0.03)
    return {
        "support_level": level,
        "publish_argument": f"Mock proponent: `{title}` can advance because quality_score={score:.1f}, evidence_count={evidence_count}, source_count={source_count}.",
        "core_value": item.get("theme") or title,
        "strongest_points": [
            f"Quality score: {score:.1f}.",
            f"Evidence count: {evidence_count}.",
            f"Source count: {source_count}.",
        ],
        "recommended_platforms": item.get("target_platforms", []),
        "confidence": round(confidence, 2),
        "notes": ["Mock/dry-run proponent output. Uses supplied metadata only."],
    }


def _mock_critic(metadata: dict[str, Any]) -> dict[str, Any]:
    score = _quality_score(metadata)
    evidence_count = _evidence_count(metadata)
    item = metadata.get("review_item") or {}
    publish_status = str(item.get("publish_status") or "")
    concerns: list[str] = []
    must_fix: list[str] = []
    if score < 80:
        concerns.append(f"Quality score {score:.1f} is below the 80 ready bar.")
    if evidence_count < 2:
        concerns.append("Evidence count is below 2.")
        must_fix.append("Add independent evidence or downgrade claims.")
    if publish_status != "READY_FOR_HUMAN_REVIEW":
        concerns.append(f"Publish status is {publish_status or 'UNKNOWN'}.")
    severity = "HIGH" if score < 65 or evidence_count == 0 else "MEDIUM" if concerns else "LOW"
    return {
        "severity": severity,
        "main_concerns": concerns or ["No major issue detected in mock review."],
        "evidence_concerns": ["Evidence is thin."] if evidence_count < 2 else [],
        "logic_concerns": ["Keep facts separated from interpretation."] if score < 80 else [],
        "constructive_suggestions": [
            "Make the lead claim evidence-bounded.",
            "Keep risk disclosure visible.",
        ],
        "must_fix_before_publish": must_fix,
        "confidence": 0.86 if concerns else 0.72,
        "notes": ["Mock/dry-run critic output. Uses supplied metadata only."],
    }


def _mock_judge(metadata: dict[str, Any]) -> dict[str, Any]:
    rule = metadata.get("rule_judge_decision") or {}
    prop = metadata.get("llm_proponent_review") or {}
    critic = metadata.get("llm_critic_review") or {}
    rule_decision = str(rule.get("decision") or "NEEDS_REVISION")
    severity = str(critic.get("severity") or "MEDIUM")
    support = str(prop.get("support_level") or "MODERATE")
    decision = rule_decision
    if rule_decision == "APPROVED_FOR_QUEUE" and severity == "HIGH":
        decision = "ESCALATE_TO_HUMAN"
    elif rule_decision == "NEEDS_REVISION" and support == "STRONG" and severity == "LOW":
        decision = "NEEDS_REVISION"
    readiness = {"APPROVED_FOR_QUEUE": "READY", "HOLD": "BLOCKED"}.get(decision, "NOT_READY")
    return {
        "decision": decision,
        "decision_score": rule.get("decision_score", 70),
        "confidence": 0.74,
        "reasoning": "Mock judge mirrors the rule judge unless critic severity creates a human spot-check conflict.",
        "comparison_to_rule_judge": {
            "rule_decision": rule_decision,
            "matches_rule_decision": decision == rule_decision,
            "difference_reason": "" if decision == rule_decision else "Mock judge detected a conflict between approval and critic severity.",
        },
        "release_readiness": readiness,
        "next_action": "send_to_human_spot_check" if decision == "APPROVED_FOR_QUEUE" else "revise" if decision == "NEEDS_REVISION" else "manual_decision" if decision == "ESCALATE_TO_HUMAN" else "hold",
        "notes": ["Mock/dry-run judge output. Rule judge remains authoritative."],
    }


def _mock_rewrite(metadata: dict[str, Any]) -> dict[str, Any]:
    instruction = metadata.get("revision_instruction") or {}
    package = metadata.get("platform_package") or {}
    wechat = package.get("wechat") if isinstance(package.get("wechat"), dict) else {}
    title = str(wechat.get("title") or instruction.get("package_id") or "Untitled")
    return {
        "revision_summary": "Mock rewrite suggestion based on revision instructions. Do not auto-apply.",
        "revised_title_options": [
            f"{title}：用证据说清楚机会与风险",
            f"{title}：哪些判断值得保留，哪些需要降调",
        ],
        "opening_rewrite": "先交代事实，再说明为什么值得关注，并明确证据仍需人工复核。",
        "structure_changes": list(instruction.get("logic_fixes", []) or ["Add fact -> implication -> risk structure."]),
        "evidence_to_add": list(instruction.get("evidence_fixes", []) or ["Add at least one independent evidence item if available."]),
        "risk_disclosure_improvements": list(instruction.get("risk_fixes", []) or ["Avoid guaranteed outcomes and keep risk disclosure explicit."]),
        "platform_specific_changes": {
            "wechat": ["Strengthen section headings and source attribution."],
            "xiaohongshu": ["Keep the conclusion concise and add tags only after human review."],
        },
        "notes": ["Mock/dry-run rewrite output. Do not auto-apply."],
    }


def mock_output(agent_name: str, metadata: dict[str, Any]) -> dict[str, Any]:
    if agent_name == "llm_proponent_agent":
        return _mock_proponent(metadata)
    if agent_name == "llm_critic_agent":
        return _mock_critic(metadata)
    if agent_name == "llm_judge_agent":
        return _mock_judge(metadata)
    if agent_name == "llm_rewrite_agent":
        return _mock_rewrite(metadata)
    return {"status": "DRY_RUN", "notes": [f"Unknown mock agent: {agent_name}"]}


def live_allowlist() -> set[str]:
    raw = os.environ.get("THCAP_LLM_LIVE_AGENT_ALLOWLIST", "")
    return {item.strip() for item in raw.split(",") if item.strip()}


def is_live_call_allowed(request: LLMRequest, provider: LLMProvider) -> tuple[bool, str]:
    if request.mode != "live":
        return False, "mode_not_live"
    if provider.provider_id != "manimax":
        return False, "provider_not_allowed_for_p7_001"
    if request.agent_name != "llm_proponent_agent":
        return False, "agent_not_allowed_for_p7_001"
    if not provider.supports_live:
        return False, "provider_does_not_support_live"
    if os.environ.get("THCAP_LLM_ENABLE_LIVE", "").strip() != "1":
        return False, "live_not_enabled"
    if request.agent_name not in live_allowlist():
        return False, "agent_not_allowlisted"
    if not provider.api_key_env or not os.environ.get(provider.api_key_env):
        return False, "missing_api_key"
    if provider.adapter_type != "openai_compatible_chat_completions":
        return False, "adapter_type_not_supported"
    return True, ""


def api_base_url(provider: LLMProvider) -> str:
    configured = os.environ.get(provider.base_url_env, "").strip() if provider.base_url_env else ""
    return configured or provider.default_base_url or provider.base_url


def api_model(provider: LLMProvider, request: LLMRequest) -> str:
    configured = os.environ.get(provider.model_env, "").strip() if provider.model_env else ""
    return configured or provider.api_model or request.model


def build_openai_compatible_payload(request: LLMRequest, provider: LLMProvider) -> dict[str, Any]:
    max_tokens = int(os.environ.get("THCAP_LLM_MAX_TOKENS", "1200") or "1200")
    temperature = float(os.environ.get("THCAP_LLM_TEMPERATURE", "0.2") or "0.2")
    return {
        "model": api_model(provider, request),
        "messages": [
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }


def extract_json_object(text: str) -> tuple[dict[str, Any], str]:
    stripped = text.strip()
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        payload = None
    if isinstance(payload, dict):
        return payload, "OK"

    fenced = stripped
    if "```" in fenced:
        parts = [part for part in fenced.split("```") if part.strip()]
        for part in parts:
            candidate = part.strip()
            if candidate.startswith("json"):
                candidate = candidate[4:].strip()
            try:
                payload = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                return payload, "OK"

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = stripped[start : end + 1]
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            return {}, "FAILED"
        if isinstance(payload, dict):
            return payload, "OK"
    return {}, "FAILED"


def parse_openai_compatible_response(response_json: dict[str, Any]) -> tuple[str, dict[str, Any], str]:
    choices = response_json.get("choices")
    if not isinstance(choices, list) or not choices:
        return "", {}, "FAILED"
    first = choices[0]
    if not isinstance(first, dict):
        return "", {}, "FAILED"
    message = first.get("message")
    if not isinstance(message, dict):
        return "", {}, "FAILED"
    content = message.get("content")
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                parts.append(str(item.get("text") or item.get("content") or ""))
            else:
                parts.append(str(item))
        text = "\n".join(parts)
    else:
        text = str(content or "")
    output_json, parse_status = extract_json_object(text)
    return text, output_json, parse_status


def cost_estimate(provider: LLMProvider, prompt_tokens: int, completion_tokens: int) -> tuple[float, str]:
    if provider.estimated_cost_per_1k_input_tokens_usd <= 0 and provider.estimated_cost_per_1k_output_tokens_usd <= 0:
        return 0.0, "pricing_not_configured"
    cost = (prompt_tokens / 1000 * provider.estimated_cost_per_1k_input_tokens_usd) + (
        completion_tokens / 1000 * provider.estimated_cost_per_1k_output_tokens_usd
    )
    return round(cost, 6), ""


def call_openai_compatible_chat_completions(request: LLMRequest, provider: LLMProvider) -> tuple[dict[str, Any], str, dict[str, Any], float, str]:
    base_url = api_base_url(provider).rstrip("/")
    request_path = provider.request_path or "/chat/completions"
    url = f"{base_url}{request_path if request_path.startswith('/') else '/' + request_path}"
    api_key = os.environ.get(provider.api_key_env, "")
    payload = build_openai_compatible_payload(request, provider)
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if provider.auth_header == "x-api-key":
        headers["x-api-key"] = api_key
    else:
        headers["Authorization"] = f"Bearer {api_key}"
    timeout = int(os.environ.get("THCAP_LLM_TIMEOUT_SECONDS", "60") or "60")
    http_request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(http_request, timeout=timeout) as response:
            raw_text = response.read().decode("utf-8", errors="replace")
            response_json = json.loads(raw_text)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")[:500]
        return {}, "", {}, 0.0, f"http_{exc.code}: {error_body}"
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        return {}, "", {}, 0.0, str(exc)
    if not isinstance(response_json, dict):
        return {}, "", {}, 0.0, "provider returned non-object JSON"
    raw_output, output_json, parse_status = parse_openai_compatible_response(response_json)
    usage_raw = response_json.get("usage") if isinstance(response_json.get("usage"), dict) else {}
    prompt_tokens = int(usage_raw.get("prompt_tokens") or estimate_tokens(request.system_prompt + request.user_prompt))
    completion_tokens = int(usage_raw.get("completion_tokens") or estimate_tokens(raw_output))
    total_tokens = int(usage_raw.get("total_tokens") or prompt_tokens + completion_tokens)
    cost, cost_note = cost_estimate(provider, prompt_tokens, completion_tokens)
    usage = {
        "estimated_input_tokens": prompt_tokens,
        "estimated_output_tokens": completion_tokens,
        "estimated_total_tokens": total_tokens,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "cost_estimation_note": cost_note,
        "api_model": payload.get("model"),
    }
    if parse_status != "OK":
        return {}, raw_output, usage, cost, "invalid_json_response"
    return output_json, raw_output, usage, cost, ""


def call_llm_agent(request: LLMRequest, provider: LLMProvider) -> LLMResponse:
    started = time.monotonic()
    input_tokens = estimate_tokens(request.system_prompt) + estimate_tokens(request.user_prompt)
    fallback_used = False
    fallback_reason = ""
    live_call_attempted = False
    live_call_succeeded = False
    raw_output_preview = ""
    json_parse_status = "OK"
    live_usage: dict[str, Any] | None = None
    live_estimated_cost_usd = 0.0
    if provider.provider_id == "mock" or request.mode == "dry_run":
        output_json = mock_output(request.agent_name, request.metadata)
        output_text = json.dumps(output_json, ensure_ascii=False, indent=2)
        status = "DRY_RUN"
        error = ""
    else:
        allowed, reason = is_live_call_allowed(request, provider)
        if allowed:
            live_call_attempted = True
            output_json, output_text, usage, estimated_cost_usd, error = call_openai_compatible_chat_completions(request, provider)
            live_usage = usage
            live_estimated_cost_usd = estimated_cost_usd
            raw_output_preview = output_text[:500]
            json_parse_status = "OK" if output_json else "FAILED"
            status = "SUCCESS" if not error else "FAILED"
            live_call_succeeded = status == "SUCCESS"
            latency_ms = int((time.monotonic() - started) * 1000)
            if error:
                fallback_used = True
                fallback_reason = error
            else:
                return LLMResponse(
                    request_id=request.request_id,
                    provider_id=request.provider_id,
                    model=request.model,
                    mode=request.mode,
                    status=status,
                    output_text=output_text,
                    output_json=output_json,
                    usage=usage,
                    error="",
                    latency_ms=latency_ms,
                    estimated_cost_usd=estimated_cost_usd,
                    fallback_used=False,
                    fallback_reason="",
                    live_call_attempted=True,
                    live_call_succeeded=True,
                    raw_output_preview=raw_output_preview,
                    json_parse_status=json_parse_status,
                )
        else:
            fallback_used = request.mode == "live"
            fallback_reason = reason if request.mode == "live" else ""
        output_json = mock_output(request.agent_name, request.metadata)
        output_json["fallback_reason"] = fallback_reason
        output_text = json.dumps(output_json, ensure_ascii=False, indent=2)
        status = "DRY_RUN"
        error = "" if not live_call_attempted else fallback_reason
        json_parse_status = "FALLBACK" if fallback_used else "OK"
    latency_ms = int((time.monotonic() - started) * 1000)
    output_tokens = estimate_tokens(output_text)
    usage_payload = live_usage or {
        "estimated_input_tokens": input_tokens,
        "estimated_output_tokens": output_tokens,
        "estimated_total_tokens": input_tokens + output_tokens,
    }
    return LLMResponse(
        request_id=request.request_id,
        provider_id=request.provider_id,
        model=request.model,
        mode=request.mode,
        status=status,
        output_text=output_text,
        output_json=output_json,
        usage=usage_payload,
        error=error,
        latency_ms=latency_ms,
        estimated_cost_usd=live_estimated_cost_usd if live_call_attempted else 0.0,
        fallback_used=fallback_used,
        fallback_reason=fallback_reason,
        live_call_attempted=live_call_attempted,
        live_call_succeeded=live_call_succeeded,
        raw_output_preview=raw_output_preview or output_text[:500],
        json_parse_status=json_parse_status,
    )


def request_to_dict(request: LLMRequest) -> dict[str, Any]:
    return asdict(request)


def response_to_dict(response: LLMResponse) -> dict[str, Any]:
    return asdict(response)
