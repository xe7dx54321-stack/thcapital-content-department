"""LLM Judge Agent v1 sidecar gate."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.agent_run_log import response_to_record, upsert_agent_run_record
from content_system.llm_agent_client import LLMRequest, call_llm_agent, make_request_id
from content_system.llm_provider_config import load_llm_provider_config, resolve_agent_provider_and_model, resolve_mode_from_env
from content_system.paths import ProjectPaths
from content_system.prompt_registry import load_prompt_registry, render_prompt


SCHEMA_VERSION = "v1"
AGENT_NAME = "llm_judge_agent"


@dataclass(frozen=True)
class LLMJudgeDecision:
    schema_version: str
    llm_judge_decision_id: str
    review_item_id: str
    package_id: str
    run_date: str
    agent_role: str
    provider_id: str
    model: str
    mode: str
    decision: str
    decision_score: float
    confidence: float
    reasoning: str
    comparison_to_rule_judge: dict[str, Any]
    release_readiness: str
    next_action: str
    fallback_used: bool
    live_call_attempted: bool
    live_call_succeeded: bool
    fallback_reason: str
    raw_output_preview: str
    json_parse_status: str
    must_not_override_rule_judge: bool
    llm_request_id: str
    validation_issues: tuple[str, ...]


@dataclass(frozen=True)
class LLMJudgeGateReport:
    schema_version: str
    generated_at: str
    run_date: str
    provider_id: str
    model: str
    mode: str
    decision_count: int
    conflict_count: int
    decisions: tuple[LLMJudgeDecision, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def list_payload(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    raw = payload.get(key)
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def by_key(items: list[dict[str, Any]], field: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(field)): item for item in items if item.get(field)}


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "06_review_queue"
    return {
        "dated_json": root / f"{run_date}__llm-judge-gate.json",
        "dated_md": root / f"{run_date}__llm-judge-gate.md",
        "latest_json": root / "latest_llm_judge_gate.json",
        "latest_md": root / "latest_llm_judge_gate.md",
    }


def validate_output(output: dict[str, Any]) -> tuple[str, ...]:
    required = ("decision", "decision_score", "confidence", "reasoning", "comparison_to_rule_judge")
    issues = [f"missing `{field}`" for field in required if field not in output]
    if output.get("decision") not in {"APPROVED_FOR_QUEUE", "NEEDS_REVISION", "HOLD", "ESCALATE_TO_HUMAN"}:
        issues.append("decision is outside allowed enum")
    return tuple(issues)


def safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def build_fallback(rule: dict[str, Any]) -> dict[str, Any]:
    rule_decision = str(rule.get("decision") or "NEEDS_REVISION")
    return {
        "decision": rule_decision,
        "decision_score": rule.get("decision_score", 0),
        "confidence": 0.55,
        "reasoning": "Fallback LLM judge mirrors rule judge.",
        "comparison_to_rule_judge": {"rule_decision": rule_decision, "matches_rule_decision": True, "difference_reason": "", "requires_human_spot_check": False},
        "release_readiness": rule.get("release_readiness") or "NOT_READY",
        "next_action": rule.get("next_action") or "manual_decision",
    }


def build_llm_judge_gate_report(
    paths: ProjectPaths,
    repo_root: Path,
    provider_id: str | None = None,
    mode: str | None = None,
    model: str | None = None,
    limit: int | None = None,
) -> LLMJudgeGateReport:
    config = load_llm_provider_config(repo_root=repo_root)
    provider, resolved_model = resolve_agent_provider_and_model(config, AGENT_NAME, provider_id, model)
    resolved_mode = resolve_mode_from_env(config, mode)
    registry = load_prompt_registry(repo_root=repo_root)
    review_root = paths.market_content_root / "06_review_queue"
    draft_root = paths.market_content_root / "05_draft_packs"
    queue_payload = read_json(review_root / "latest_agent_review_queue.json")
    items = list_payload(queue_payload, "items")
    props = by_key(list_payload(read_json(review_root / "latest_llm_proponent_reviews.json"), "reviews"), "review_item_id")
    critics = by_key(list_payload(read_json(review_root / "latest_llm_critic_reviews.json"), "reviews"), "review_item_id")
    rules = by_key(list_payload(read_json(review_root / "latest_judge_gate.json"), "decisions"), "review_item_id")
    packages = by_key(list_payload(read_json(draft_root / "latest_platform_packages.json"), "packages"), "package_id")
    run_date = str(queue_payload.get("run_date") or today_token()).replace("-", "")[:8]
    latest_output = output_paths(paths, run_date)["latest_json"]
    source_artifact = repo_relative(review_root / "latest_agent_review_queue.json", repo_root)
    output_artifact = repo_relative(latest_output, repo_root)
    warnings: list[str] = []
    decisions: list[LLMJudgeDecision] = []
    if limit is not None and limit > 0:
        items = items[:limit]
    if not items:
        warnings.append("No agent review queue items available.")

    for item in items:
        review_item_id = str(item.get("review_item_id") or "")
        rule = rules.get(review_item_id, {})
        prop = props.get(review_item_id, {})
        critic = critics.get(review_item_id, {})
        package = packages.get(str(item.get("package_id")), {})
        system_prompt, user_prompt, schema = render_prompt(
            AGENT_NAME,
            {"review_item": item, "llm_proponent_review": prop, "llm_critic_review": critic, "rule_judge_decision": rule, "platform_package": package},
            registry=registry,
            repo_root=repo_root,
        )
        request_id = make_request_id(AGENT_NAME, provider.provider_id, resolved_mode, review_item_id)
        request = LLMRequest(request_id, AGENT_NAME, provider.provider_id, resolved_model, resolved_mode, system_prompt, user_prompt, schema, {"review_item": item, "llm_proponent_review": prop, "llm_critic_review": critic, "rule_judge_decision": rule, "platform_package": package})
        response = call_llm_agent(request, provider)
        output = dict(response.output_json)
        validation_issues = validate_output(output)
        fallback_used = bool(validation_issues or response.fallback_used)
        fallback_reason = response.fallback_reason
        if fallback_used:
            if validation_issues and not fallback_reason:
                fallback_reason = "validation_failed"
            output = build_fallback(rule)
        json_parse_status = response.json_parse_status
        if validation_issues and json_parse_status == "OK":
            json_parse_status = "FALLBACK"
        comparison = output.get("comparison_to_rule_judge") if isinstance(output.get("comparison_to_rule_judge"), dict) else {}
        rule_decision = str(rule.get("decision") or comparison.get("rule_decision") or "")
        decision = str(output.get("decision") or "NEEDS_REVISION")
        matches_rule = decision == rule_decision
        comparison = {
            "rule_decision": rule_decision,
            "llm_decision": decision,
            "matches_rule_decision": matches_rule,
            "difference_reason": str(comparison.get("difference_reason") or ("" if matches_rule else "LLM sidecar differs from rule judge; human spot check recommended.")),
            "requires_human_spot_check": bool(comparison.get("requires_human_spot_check") or not matches_rule),
        }
        decisions.append(
            LLMJudgeDecision(
                schema_version=SCHEMA_VERSION,
                llm_judge_decision_id=f"llm_judge_{request_id.removeprefix('llmreq_')}",
                review_item_id=review_item_id,
                package_id=str(item.get("package_id") or ""),
                run_date=run_date,
                agent_role="llm_third_party_judge",
                provider_id=provider.provider_id,
                model=resolved_model,
                mode=resolved_mode,
                decision=decision,
                decision_score=safe_float(output.get("decision_score"), 0.0),
                confidence=safe_float(output.get("confidence"), 0.0),
                reasoning=str(output.get("reasoning") or ""),
                comparison_to_rule_judge=comparison,
                release_readiness=str(output.get("release_readiness") or rule.get("release_readiness") or "NOT_READY"),
                next_action=str(output.get("next_action") or rule.get("next_action") or "manual_decision"),
                fallback_used=fallback_used,
                live_call_attempted=response.live_call_attempted,
                live_call_succeeded=response.live_call_succeeded,
                fallback_reason=fallback_reason,
                raw_output_preview=response.raw_output_preview[:500],
                json_parse_status=json_parse_status,
                must_not_override_rule_judge=True,
                llm_request_id=request_id,
                validation_issues=validation_issues,
            )
        )
        upsert_agent_run_record(paths, response_to_record(response=response, agent_name=AGENT_NAME, run_date=run_date, fallback_used=fallback_used, source_artifact=source_artifact, output_artifact=output_artifact))
    conflict_count = sum(1 for item in decisions if not item.comparison_to_rule_judge.get("matches_rule_decision"))
    return LLMJudgeGateReport(SCHEMA_VERSION, utc_now(), run_date, provider.provider_id, resolved_model, resolved_mode, len(decisions), conflict_count, tuple(decisions), tuple(warnings))


def report_to_dict(report: LLMJudgeGateReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: LLMJudgeGateReport) -> str:
    rows = [
        f"| {idx} | {item.decision} | {item.decision_score:.2f} | {item.confidence:.2f} | {item.live_call_attempted} | {item.live_call_succeeded} | {item.fallback_used} | {item.comparison_to_rule_judge.get('matches_rule_decision')} | {item.comparison_to_rule_judge.get('requires_human_spot_check')} | {escape_cell(item.package_id)} |"
        for idx, item in enumerate(report.decisions, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# LLM Judge Gate v1

> Sidecar LLM judge output. It does not override the rule judge automatically.

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Provider: `{report.provider_id}`
- Model: `{report.model}`
- Mode: `{report.mode}`
- Decisions: `{report.decision_count}`
- Conflicts with rule judge: `{report.conflict_count}`

## Decisions

| # | Decision | Score | Confidence | Live Attempted | Live Succeeded | Fallback | Matches Rule | Human Spot Check | Package |
|---:|---|---:|---:|---|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | 0 | 0 | false | false | false | true | false | None |'}

## Warnings

{warnings}
"""


def write_llm_judge_gate_report(report: LLMJudgeGateReport, paths: ProjectPaths) -> dict[str, Path]:
    outputs = output_paths(paths, report.run_date)
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (outputs["dated_json"], outputs["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (outputs["dated_md"], outputs["latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return outputs
