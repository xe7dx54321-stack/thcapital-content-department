"""Mock-first LLM agent client for Phase 6.

The client deliberately defaults to mock/dry-run. Non-mock live providers are
placeholder responses in v1 so the system can validate schemas and logging
without requiring paid API credentials or SDK dependencies.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from content_system.llm_provider_config import LLMProvider, is_live_enabled


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


def call_llm_agent(request: LLMRequest, provider: LLMProvider) -> LLMResponse:
    started = time.monotonic()
    input_tokens = estimate_tokens(request.system_prompt) + estimate_tokens(request.user_prompt)
    if provider.provider_id == "mock" or request.mode == "dry_run":
        output_json = mock_output(request.agent_name, request.metadata)
        output_text = json.dumps(output_json, ensure_ascii=False, indent=2)
        status = "DRY_RUN"
        error = ""
    elif is_live_enabled(provider, request.mode):
        output_json = {
            "status": "NOT_IMPLEMENTED",
            "notes": ["Live adapter is intentionally not implemented in Phase 6 v1."],
        }
        output_text = json.dumps(output_json, ensure_ascii=False, indent=2)
        status = "FAILED"
        error = "live provider adapter is not implemented in Phase 6 v1"
    else:
        output_json = {
            "status": "DRY_RUN_UNLESS_EXPLICITLY_ENABLED",
            "notes": ["Provider is not available for live calls; falling back to dry-run placeholder."],
        }
        output_text = json.dumps(output_json, ensure_ascii=False, indent=2)
        status = "DRY_RUN"
        error = ""
    latency_ms = int((time.monotonic() - started) * 1000)
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
        },
        error=error,
        latency_ms=latency_ms,
        estimated_cost_usd=0.0 if status == "DRY_RUN" else 0.0,
    )


def request_to_dict(request: LLMRequest) -> dict[str, Any]:
    return asdict(request)


def response_to_dict(response: LLMResponse) -> dict[str, Any]:
    return asdict(response)
