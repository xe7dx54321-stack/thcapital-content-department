"""LLM Critic Agent v1 with mock/dry-run default."""

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
AGENT_NAME = "llm_critic_agent"


@dataclass(frozen=True)
class LLMCriticReview:
    schema_version: str
    llm_critic_review_id: str
    review_item_id: str
    package_id: str
    run_date: str
    agent_role: str
    provider_id: str
    model: str
    mode: str
    severity: str
    main_concerns: tuple[str, ...]
    evidence_concerns: tuple[str, ...]
    logic_concerns: tuple[str, ...]
    constructive_suggestions: tuple[str, ...]
    must_fix_before_publish: tuple[str, ...]
    confidence: float
    fallback_used: bool
    live_call_attempted: bool
    live_call_succeeded: bool
    fallback_reason: str
    raw_output_preview: str
    json_parse_status: str
    llm_request_id: str
    validation_issues: tuple[str, ...]


@dataclass(frozen=True)
class LLMCriticReviewReport:
    schema_version: str
    generated_at: str
    run_date: str
    provider_id: str
    model: str
    mode: str
    review_count: int
    reviews: tuple[LLMCriticReview, ...]
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
        "dated_json": root / f"{run_date}__llm-critic-reviews.json",
        "dated_md": root / f"{run_date}__llm-critic-reviews.md",
        "latest_json": root / "latest_llm_critic_reviews.json",
        "latest_md": root / "latest_llm_critic_reviews.md",
    }


def validate_output(output: dict[str, Any]) -> tuple[str, ...]:
    required = ("severity", "main_concerns", "constructive_suggestions", "confidence")
    issues = [f"missing `{field}`" for field in required if field not in output]
    if output.get("severity") not in {"LOW", "MEDIUM", "HIGH"}:
        issues.append("severity must be LOW, MEDIUM, or HIGH")
    return tuple(issues)


def safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def build_fallback(item: dict[str, Any]) -> dict[str, Any]:
    score = safe_float(item.get("quality_score"))
    severity = "HIGH" if score < 65 else "MEDIUM" if score < 80 else "LOW"
    return {
        "severity": severity,
        "main_concerns": [f"Fallback critic review based on quality score {score:.1f}."],
        "evidence_concerns": [],
        "logic_concerns": [],
        "constructive_suggestions": ["Keep claims evidence-bounded."],
        "must_fix_before_publish": [],
        "confidence": 0.55,
    }


def build_llm_critic_review_report(
    paths: ProjectPaths,
    repo_root: Path,
    provider_id: str | None = None,
    mode: str | None = None,
    model: str | None = None,
    limit: int | None = None,
) -> LLMCriticReviewReport:
    config = load_llm_provider_config(repo_root=repo_root)
    provider, resolved_model = resolve_agent_provider_and_model(config, AGENT_NAME, provider_id, model)
    resolved_mode = resolve_mode_from_env(config, mode)
    registry = load_prompt_registry(repo_root=repo_root)
    review_root = paths.market_content_root / "06_review_queue"
    draft_root = paths.market_content_root / "05_draft_packs"
    queue_payload = read_json(review_root / "latest_agent_review_queue.json")
    items = list_payload(queue_payload, "items")
    packages = by_key(list_payload(read_json(draft_root / "latest_platform_packages.json"), "packages"), "package_id")
    quality_reviews = by_key(list_payload(read_json(draft_root / "latest_content_quality_review.json"), "reviews"), "draft_id")
    run_date = str(queue_payload.get("run_date") or today_token()).replace("-", "")[:8]
    latest_output = output_paths(paths, run_date)["latest_json"]
    source_artifact = repo_relative(review_root / "latest_agent_review_queue.json", repo_root)
    output_artifact = repo_relative(latest_output, repo_root)
    warnings: list[str] = []
    reviews: list[LLMCriticReview] = []
    if limit is not None and limit > 0:
        items = items[:limit]
    if not items:
        warnings.append("No agent review queue items available.")

    for item in items:
        review_item_id = str(item.get("review_item_id") or "")
        package = packages.get(str(item.get("package_id")), {})
        quality = quality_reviews.get(str(item.get("draft_id")), {})
        system_prompt, user_prompt, schema = render_prompt(
            AGENT_NAME,
            {"review_item": item, "platform_package": package, "quality_review": quality},
            registry=registry,
            repo_root=repo_root,
        )
        request_id = make_request_id(AGENT_NAME, provider.provider_id, resolved_mode, review_item_id)
        request = LLMRequest(request_id, AGENT_NAME, provider.provider_id, resolved_model, resolved_mode, system_prompt, user_prompt, schema, {"review_item": item, "platform_package": package, "quality_review": quality})
        response = call_llm_agent(request, provider)
        output = dict(response.output_json)
        validation_issues = validate_output(output)
        fallback_used = bool(validation_issues or response.fallback_used)
        fallback_reason = response.fallback_reason
        if fallback_used:
            if validation_issues and not fallback_reason:
                fallback_reason = "validation_failed"
            output = build_fallback(item)
        json_parse_status = response.json_parse_status
        if validation_issues and json_parse_status == "OK":
            json_parse_status = "FALLBACK"
        review = LLMCriticReview(
            schema_version=SCHEMA_VERSION,
            llm_critic_review_id=f"llm_crit_{request_id.removeprefix('llmreq_')}",
            review_item_id=review_item_id,
            package_id=str(item.get("package_id") or ""),
            run_date=run_date,
            agent_role="llm_critical_senior_editor",
            provider_id=provider.provider_id,
            model=resolved_model,
            mode=resolved_mode,
            severity=str(output.get("severity") or "MEDIUM"),
            main_concerns=tuple(str(value) for value in output.get("main_concerns", []) if value),
            evidence_concerns=tuple(str(value) for value in output.get("evidence_concerns", []) if value),
            logic_concerns=tuple(str(value) for value in output.get("logic_concerns", []) if value),
            constructive_suggestions=tuple(str(value) for value in output.get("constructive_suggestions", []) if value),
            must_fix_before_publish=tuple(str(value) for value in output.get("must_fix_before_publish", []) if value),
            confidence=safe_float(output.get("confidence"), 0.0),
            fallback_used=fallback_used,
            live_call_attempted=response.live_call_attempted,
            live_call_succeeded=response.live_call_succeeded,
            fallback_reason=fallback_reason,
            raw_output_preview=response.raw_output_preview[:500],
            json_parse_status=json_parse_status,
            llm_request_id=request_id,
            validation_issues=validation_issues,
        )
        reviews.append(review)
        upsert_agent_run_record(
            paths,
            response_to_record(response=response, agent_name=AGENT_NAME, run_date=run_date, fallback_used=fallback_used, source_artifact=source_artifact, output_artifact=output_artifact),
        )
    return LLMCriticReviewReport(SCHEMA_VERSION, utc_now(), run_date, provider.provider_id, resolved_model, resolved_mode, len(reviews), tuple(reviews), tuple(warnings))


def report_to_dict(report: LLMCriticReviewReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: LLMCriticReviewReport) -> str:
    rows = [
        f"| {idx} | {item.severity} | {item.confidence:.2f} | {item.provider_id} | {item.mode} | {item.live_call_attempted} | {item.live_call_succeeded} | {item.fallback_used} | {escape_cell(item.fallback_reason)} | {escape_cell(item.package_id)} | {len(item.must_fix_before_publish)} |"
        for idx, item in enumerate(report.reviews, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# LLM Critic Reviews v1

> Mock/dry-run LLM critic agent output. Rule-based fallback remains available.

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Provider: `{report.provider_id}`
- Model: `{report.model}`
- Mode: `{report.mode}`
- Reviews: `{report.review_count}`

## Reviews

| # | Severity | Confidence | Provider | Mode | Live Attempted | Live Succeeded | Fallback | Fallback Reason | Package | Must Fix |
|---:|---|---:|---|---|---|---|---|---|---|---:|
{chr(10).join(rows) if rows else '| 0 | - | 0 | - | - | false | false | false | - | None | 0 |'}

## Warnings

{warnings}
"""


def write_llm_critic_review_report(report: LLMCriticReviewReport, paths: ProjectPaths) -> dict[str, Path]:
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
