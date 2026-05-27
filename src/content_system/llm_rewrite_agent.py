"""LLM Rewrite Suggestion Agent v1."""

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
AGENT_NAME = "llm_rewrite_agent"


@dataclass(frozen=True)
class LLMRewriteSuggestion:
    schema_version: str
    rewrite_suggestion_id: str
    review_item_id: str
    package_id: str
    draft_id: str
    run_date: str
    provider_id: str
    model: str
    mode: str
    revision_summary: str
    revised_title_options: tuple[str, ...]
    opening_rewrite: str
    structure_changes: tuple[str, ...]
    evidence_to_add: tuple[str, ...]
    risk_disclosure_improvements: tuple[str, ...]
    platform_specific_changes: dict[str, tuple[str, ...]]
    do_not_auto_apply: bool
    live_call_attempted: bool
    live_call_succeeded: bool
    fallback_reason: str
    raw_output_preview: str
    json_parse_status: str
    must_not_overwrite_original: bool
    rewrite_scope: str
    fallback_used: bool
    llm_request_id: str
    validation_issues: tuple[str, ...]


@dataclass(frozen=True)
class LLMRewriteSuggestionReport:
    schema_version: str
    generated_at: str
    run_date: str
    provider_id: str
    model: str
    mode: str
    suggestion_count: int
    suggestions: tuple[LLMRewriteSuggestion, ...]
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
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__llm-rewrite-suggestions.json",
        "dated_md": root / f"{run_date}__llm-rewrite-suggestions.md",
        "latest_json": root / "latest_llm_rewrite_suggestions.json",
        "latest_md": root / "latest_llm_rewrite_suggestions.md",
    }


def validate_output(output: dict[str, Any]) -> tuple[str, ...]:
    required = ("revision_summary", "revised_title_options", "platform_specific_changes")
    issues = [f"missing `{field}`" for field in required if field not in output]
    if not isinstance(output.get("platform_specific_changes", {}), dict):
        issues.append("platform_specific_changes must be an object")
    return tuple(issues)


def build_fallback(instruction: dict[str, Any]) -> dict[str, Any]:
    return {
        "revision_summary": "Fallback rewrite suggestion from revision instruction.",
        "revised_title_options": ["保留事实边界，突出机会与风险"],
        "opening_rewrite": "先写事实，再写判断，并提示人工复核。",
        "structure_changes": list(instruction.get("logic_fixes", []) or []),
        "evidence_to_add": list(instruction.get("evidence_fixes", []) or []),
        "risk_disclosure_improvements": list(instruction.get("risk_fixes", []) or []),
        "platform_specific_changes": {"wechat": [], "xiaohongshu": []},
    }


def tuple_strings(value: Any) -> tuple[str, ...]:
    return tuple(str(item) for item in value if item) if isinstance(value, list) else ()


def build_llm_rewrite_suggestion_report(
    paths: ProjectPaths,
    repo_root: Path,
    provider_id: str | None = None,
    mode: str | None = None,
    model: str | None = None,
    limit: int | None = None,
) -> LLMRewriteSuggestionReport:
    config = load_llm_provider_config(repo_root=repo_root)
    provider, resolved_model = resolve_agent_provider_and_model(config, AGENT_NAME, provider_id, model)
    resolved_mode = resolve_mode_from_env(config, mode)
    registry = load_prompt_registry(repo_root=repo_root)
    review_root = paths.market_content_root / "06_review_queue"
    draft_root = paths.market_content_root / "05_draft_packs"
    revision_payload = read_json(review_root / "latest_revision_instructions.json")
    instructions = list_payload(revision_payload, "instructions")
    packages = by_key(list_payload(read_json(draft_root / "latest_platform_packages.json"), "packages"), "package_id")
    drafts = by_key(list_payload(read_json(draft_root / "latest_content_drafts.json"), "drafts"), "draft_id")
    critics = by_key(list_payload(read_json(review_root / "latest_llm_critic_reviews.json"), "reviews"), "review_item_id")
    judges = by_key(list_payload(read_json(review_root / "latest_llm_judge_gate.json"), "decisions"), "review_item_id")
    run_date = str(revision_payload.get("run_date") or today_token()).replace("-", "")[:8]
    latest_output = output_paths(paths, run_date)["latest_json"]
    source_artifact = repo_relative(review_root / "latest_revision_instructions.json", repo_root)
    output_artifact = repo_relative(latest_output, repo_root)
    warnings: list[str] = []
    suggestions: list[LLMRewriteSuggestion] = []
    if limit is not None and limit > 0:
        instructions = instructions[:limit]
    if not instructions:
        warnings.append("No revision instructions available.")

    for instruction in instructions:
        review_item_id = str(instruction.get("review_item_id") or "")
        package = packages.get(str(instruction.get("package_id")), {})
        draft = drafts.get(str(package.get("draft_id")), {})
        critic = critics.get(review_item_id, {})
        judge = judges.get(review_item_id, {})
        system_prompt, user_prompt, schema = render_prompt(
            AGENT_NAME,
            {"revision_instruction": instruction, "platform_package": package, "content_draft": draft, "llm_critic_review": critic, "llm_judge_decision": judge},
            registry=registry,
            repo_root=repo_root,
        )
        request_id = make_request_id(AGENT_NAME, provider.provider_id, resolved_mode, review_item_id)
        request = LLMRequest(request_id, AGENT_NAME, provider.provider_id, resolved_model, resolved_mode, system_prompt, user_prompt, schema, {"revision_instruction": instruction, "platform_package": package, "content_draft": draft, "llm_critic_review": critic, "llm_judge_decision": judge})
        response = call_llm_agent(request, provider)
        output = dict(response.output_json)
        validation_issues = validate_output(output)
        fallback_used = bool(validation_issues or response.fallback_used)
        fallback_reason = response.fallback_reason
        if fallback_used:
            if validation_issues and not fallback_reason:
                fallback_reason = "validation_failed"
            output = build_fallback(instruction)
        json_parse_status = response.json_parse_status
        if validation_issues and json_parse_status == "OK":
            json_parse_status = "FALLBACK"
        platform_changes_raw = output.get("platform_specific_changes")
        platform_changes = {}
        if isinstance(platform_changes_raw, dict):
            for key, value in platform_changes_raw.items():
                platform_changes[str(key)] = tuple_strings(value)
        suggestion = LLMRewriteSuggestion(
            schema_version=SCHEMA_VERSION,
            rewrite_suggestion_id=f"llm_rw_{request_id.removeprefix('llmreq_')}",
            review_item_id=review_item_id,
            package_id=str(instruction.get("package_id") or ""),
            draft_id=str(package.get("draft_id") or ""),
            run_date=run_date,
            provider_id=provider.provider_id,
            model=resolved_model,
            mode=resolved_mode,
            revision_summary=str(output.get("revision_summary") or ""),
            revised_title_options=tuple_strings(output.get("revised_title_options", [])),
            opening_rewrite=str(output.get("opening_rewrite") or ""),
            structure_changes=tuple_strings(output.get("structure_changes", [])),
            evidence_to_add=tuple_strings(output.get("evidence_to_add", [])),
            risk_disclosure_improvements=tuple_strings(output.get("risk_disclosure_improvements", [])),
            platform_specific_changes=platform_changes,
            do_not_auto_apply=True,
            live_call_attempted=response.live_call_attempted,
            live_call_succeeded=response.live_call_succeeded,
            fallback_reason=fallback_reason,
            raw_output_preview=response.raw_output_preview[:500],
            json_parse_status=json_parse_status,
            must_not_overwrite_original=True,
            rewrite_scope="suggestion_only",
            fallback_used=fallback_used,
            llm_request_id=request_id,
            validation_issues=validation_issues,
        )
        suggestions.append(suggestion)
        upsert_agent_run_record(paths, response_to_record(response=response, agent_name=AGENT_NAME, run_date=run_date, fallback_used=fallback_used, source_artifact=source_artifact, output_artifact=output_artifact))
    return LLMRewriteSuggestionReport(SCHEMA_VERSION, utc_now(), run_date, provider.provider_id, resolved_model, resolved_mode, len(suggestions), tuple(suggestions), tuple(warnings))


def report_to_dict(report: LLMRewriteSuggestionReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: LLMRewriteSuggestionReport) -> str:
    rows = [
        f"| {idx} | {item.provider_id} | {item.mode} | {item.live_call_attempted} | {item.live_call_succeeded} | {item.fallback_used} | {escape_cell(item.fallback_reason)} | {escape_cell(item.package_id)} | {len(item.revised_title_options)} |"
        for idx, item in enumerate(report.suggestions, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# LLM Rewrite Suggestions v1

> Rewrite suggestions are never auto-applied.

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Provider: `{report.provider_id}`
- Model: `{report.model}`
- Mode: `{report.mode}`
- Suggestions: `{report.suggestion_count}`

## Suggestions

| # | Provider | Mode | Live Attempted | Live Succeeded | Fallback | Fallback Reason | Package | Title Options |
|---:|---|---|---|---|---|---|---|---:|
{chr(10).join(rows) if rows else '| 0 | - | - | false | false | false | - | None | 0 |'}

## Warnings

{warnings}
"""


def write_llm_rewrite_suggestion_report(report: LLMRewriteSuggestionReport, paths: ProjectPaths) -> dict[str, Path]:
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
