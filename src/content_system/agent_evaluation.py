"""Human-in-the-loop Agent Evaluation v1."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths


SCHEMA_VERSION = "v1"
ACTION_ENUM = {"UNREVIEWED", "ACCEPT", "REVISE_PROMPT", "REJECT_OUTPUT", "ESCALATE"}


@dataclass(frozen=True)
class AgentEvaluationItem:
    schema_version: str
    evaluation_id: str
    run_date: str
    agent_name: str
    artifact_id: str
    human_rating: float | None
    accuracy_rating: float | None
    usefulness_rating: float | None
    tone_rating: float | None
    risk_rating: float | None
    human_notes: str
    action: str
    feedback_tags: tuple[str, ...]


@dataclass(frozen=True)
class AgentEvaluationTemplate:
    schema_version: str
    generated_at: str
    run_date: str
    evaluation_count: int
    evaluation_items: tuple[AgentEvaluationItem, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    evaluation_id: str | None
    field: str | None
    message: str


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


def make_id(prefix: str, run_date: str, *parts: str) -> str:
    digest = hashlib.sha1("|".join((run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def evaluation_from_artifact(run_date: str, agent_name: str, artifact_id: str) -> AgentEvaluationItem:
    return AgentEvaluationItem(
        schema_version=SCHEMA_VERSION,
        evaluation_id=make_id("aeval", run_date, agent_name, artifact_id),
        run_date=run_date,
        agent_name=agent_name,
        artifact_id=artifact_id,
        human_rating=None,
        accuracy_rating=None,
        usefulness_rating=None,
        tone_rating=None,
        risk_rating=None,
        human_notes="",
        action="UNREVIEWED",
        feedback_tags=(),
    )


def build_agent_evaluation_template(paths: ProjectPaths) -> AgentEvaluationTemplate:
    review_root = paths.market_content_root / "06_review_queue"
    draft_root = paths.market_content_root / "05_draft_packs"
    logs_root = paths.logs_root
    artifacts: list[tuple[str, str]] = []
    proponent = read_json(review_root / "latest_llm_proponent_reviews.json")
    critic = read_json(review_root / "latest_llm_critic_reviews.json")
    judge = read_json(review_root / "latest_llm_judge_gate.json")
    rewrite = read_json(draft_root / "latest_llm_rewrite_suggestions.json")
    for item in list_payload(proponent, "reviews"):
        artifacts.append(("llm_proponent_agent", str(item.get("llm_proponent_review_id") or item.get("review_item_id") or "")))
    for item in list_payload(critic, "reviews"):
        artifacts.append(("llm_critic_agent", str(item.get("llm_critic_review_id") or item.get("review_item_id") or "")))
    for item in list_payload(judge, "decisions"):
        artifacts.append(("llm_judge_agent", str(item.get("llm_judge_decision_id") or item.get("review_item_id") or "")))
    for item in list_payload(rewrite, "suggestions"):
        artifacts.append(("llm_rewrite_agent", str(item.get("rewrite_suggestion_id") or item.get("review_item_id") or "")))
    run_date = str(proponent.get("run_date") or critic.get("run_date") or judge.get("run_date") or rewrite.get("run_date") or today_token()).replace("-", "")[:8]
    summary = read_json(logs_root / "latest_agent_run_summary.json")
    warnings = [] if artifacts else ["No LLM agent artifacts available for evaluation template."]
    if not summary:
        warnings.append("latest_agent_run_summary.json not found; run make agent-run-summary first for full context.")
    items = tuple(evaluation_from_artifact(run_date, agent_name, artifact_id) for agent_name, artifact_id in artifacts if artifact_id)
    return AgentEvaluationTemplate(SCHEMA_VERSION, utc_now(), run_date, len(items), items, tuple(warnings))


def validate_agent_evaluation_payload(payload: dict[str, Any]) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    raw_items = payload.get("evaluation_items")
    if not isinstance(raw_items, list):
        issues.append(ValidationIssue("ERROR", None, "evaluation_items", "evaluation_items must be a list"))
        return tuple(issues)
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        evaluation_id = str(item.get("evaluation_id") or "")
        if not item.get("agent_name"):
            issues.append(ValidationIssue("ERROR", evaluation_id, "agent_name", "agent_name is required"))
        if not item.get("artifact_id"):
            issues.append(ValidationIssue("ERROR", evaluation_id, "artifact_id", "artifact_id is required"))
        action = str(item.get("action") or "")
        if action not in ACTION_ENUM:
            issues.append(ValidationIssue("ERROR", evaluation_id, "action", "action is outside allowed enum"))
        for field in ("human_rating", "accuracy_rating", "usefulness_rating", "tone_rating", "risk_rating"):
            value = item.get(field)
            if value is None:
                continue
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                issues.append(ValidationIssue("ERROR", evaluation_id, field, "rating must be numeric or null"))
                continue
            if numeric < 0 or numeric > 10:
                issues.append(ValidationIssue("ERROR", evaluation_id, field, "rating must be between 0 and 10"))
    return tuple(issues)


def template_to_dict(template: AgentEvaluationTemplate) -> dict[str, Any]:
    return asdict(template)


def render_markdown(template: AgentEvaluationTemplate) -> str:
    rows = [
        f"| {idx} | {item.agent_name} | {item.artifact_id} | {item.action} | | | |"
        for idx, item in enumerate(template.evaluation_items, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in template.warnings) if template.warnings else "- None"
    return f"""# Agent Evaluation Template v1

## Summary

- Generated at: `{template.generated_at}`
- Run date: `{template.run_date}`
- Evaluation items: `{template.evaluation_count}`

## Evaluation Items

| # | Agent | Artifact | Action | Human Rating | Notes | Tags |
|---:|---|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | UNREVIEWED | | | |'}

## Allowed Actions

- UNREVIEWED
- ACCEPT
- REVISE_PROMPT
- REJECT_OUTPUT
- ESCALATE

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__agent-evaluation-template.json",
        "dated_md": root / f"{run_date}__agent-evaluation-template.md",
        "latest_json": root / "latest_agent_evaluation_template.json",
        "latest_md": root / "latest_agent_evaluation_template.md",
    }


def write_agent_evaluation_template(template: AgentEvaluationTemplate, paths: ProjectPaths) -> dict[str, Path]:
    outputs = output_paths(paths, template.run_date)
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(template_to_dict(template), ensure_ascii=False, indent=2)
    markdown = render_markdown(template)
    for path in (outputs["dated_json"], outputs["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (outputs["dated_md"], outputs["latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return outputs
