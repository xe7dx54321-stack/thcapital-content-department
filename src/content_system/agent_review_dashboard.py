"""Agent Review Dashboard v1."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class AgentReviewDashboardReport:
    schema_version: str
    generated_at: str
    run_date: str
    summary: dict[str, int]
    human_attention_required: tuple[dict[str, Any], ...]
    approved_ready: tuple[dict[str, Any], ...]
    needs_revision: tuple[dict[str, Any], ...]
    hold: tuple[dict[str, Any], ...]
    agent_disagreement: tuple[dict[str, Any], ...]
    next_actions: tuple[str, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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


def title_for(decision: dict[str, Any], queue_items: dict[str, dict[str, Any]]) -> str:
    item = queue_items.get(str(decision.get("review_item_id")), {})
    return str(item.get("title") or decision.get("package_id") or "")


def compact_decision(decision: dict[str, Any], queue_items: dict[str, dict[str, Any]]) -> dict[str, Any]:
    item = queue_items.get(str(decision.get("review_item_id")), {})
    return {
        "review_item_id": decision.get("review_item_id"),
        "package_id": decision.get("package_id"),
        "title": title_for(decision, queue_items),
        "decision": decision.get("decision"),
        "decision_score": decision.get("decision_score"),
        "confidence": decision.get("confidence"),
        "risk_level": decision.get("risk_level"),
        "next_action": decision.get("next_action"),
        "quality_score": item.get("quality_score"),
        "priority": item.get("priority"),
        "reasoning": decision.get("reasoning"),
    }


def compact_exception(exception: dict[str, Any], queue_items: dict[str, dict[str, Any]]) -> dict[str, Any]:
    item = queue_items.get(str(exception.get("review_item_id")), {})
    return {
        "exception_id": exception.get("exception_id"),
        "review_item_id": exception.get("review_item_id"),
        "package_id": exception.get("package_id"),
        "title": item.get("title") or exception.get("package_id"),
        "urgency": exception.get("urgency"),
        "estimated_review_minutes": exception.get("estimated_review_minutes"),
        "recommended_human_action": exception.get("recommended_human_action"),
        "reason": exception.get("reason"),
    }


def build_disagreements(
    proponents: dict[str, dict[str, Any]],
    critics: dict[str, dict[str, Any]],
    queue_items: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], ...]:
    items: list[dict[str, Any]] = []
    for review_item_id, prop in proponents.items():
        critic = critics.get(review_item_id, {})
        if prop.get("support_level") == "STRONG" and critic.get("severity") == "HIGH":
            queue_item = queue_items.get(review_item_id, {})
            items.append(
                {
                    "review_item_id": review_item_id,
                    "package_id": prop.get("package_id") or critic.get("package_id"),
                    "title": queue_item.get("title") or prop.get("suggested_title_angle"),
                    "proponent_support": prop.get("support_level"),
                    "critic_severity": critic.get("severity"),
                    "recommended_action": "human_or_senior_editor_check",
                }
            )
    return tuple(items)


def build_agent_review_dashboard_report(paths: ProjectPaths) -> AgentReviewDashboardReport:
    review_root = paths.market_content_root / "06_review_queue"
    queue_payload = read_json(review_root / "latest_agent_review_queue.json")
    prop_payload = read_json(review_root / "latest_proponent_reviews.json")
    critic_payload = read_json(review_root / "latest_critic_reviews.json")
    judge_payload = read_json(review_root / "latest_judge_gate.json")
    revision_payload = read_json(review_root / "latest_revision_instructions.json")
    exception_payload = read_json(review_root / "latest_human_exception_queue.json")

    queue_items_list = list_payload(queue_payload, "items")
    decisions = list_payload(judge_payload, "decisions")
    exceptions = list_payload(exception_payload, "exceptions")
    revisions = list_payload(revision_payload, "instructions")
    proponents = by_key(list_payload(prop_payload, "reviews"), "review_item_id")
    critics = by_key(list_payload(critic_payload, "reviews"), "review_item_id")
    queue_items = by_key(queue_items_list, "review_item_id")
    run_date = str(judge_payload.get("run_date") or queue_payload.get("run_date") or datetime.now().strftime("%Y%m%d")).replace("-", "")[:8]

    approved = [compact_decision(item, queue_items) for item in decisions if item.get("decision") == "APPROVED_FOR_QUEUE"]
    needs = [compact_decision(item, queue_items) for item in decisions if item.get("decision") == "NEEDS_REVISION"]
    hold = [compact_decision(item, queue_items) for item in decisions if item.get("decision") == "HOLD"]
    escalated = [compact_decision(item, queue_items) for item in decisions if item.get("decision") == "ESCALATE_TO_HUMAN"]
    human_items = [compact_exception(item, queue_items) for item in exceptions]
    estimated_minutes = sum(int(item.get("estimated_review_minutes") or 0) for item in exceptions)

    next_actions = [
        "Review the human exception queue first; it is designed to stay small.",
        "Move APPROVED_FOR_QUEUE items into the next publishing-prep phase only after human spot check.",
        "Apply revision instructions to NEEDS_REVISION items before rerunning judge gate.",
        "Keep HOLD items out of publishing preparation until evidence and risk gaps are fixed.",
    ]
    warnings: list[str] = []
    if not decisions:
        warnings.append("Judge gate output is missing or empty.")
    if not queue_items_list:
        warnings.append("Agent review queue is missing or empty.")

    return AgentReviewDashboardReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date,
        summary={
            "review_items": len(queue_items_list),
            "approved_for_queue": len(approved),
            "needs_revision": len(needs),
            "hold": len(hold),
            "escalated_to_human": len(escalated),
            "human_exceptions": len(human_items),
            "revision_instructions": len(revisions),
            "estimated_human_review_minutes": estimated_minutes,
        },
        human_attention_required=tuple(human_items or escalated),
        approved_ready=tuple(approved),
        needs_revision=tuple(needs),
        hold=tuple(hold),
        agent_disagreement=build_disagreements(proponents, critics, queue_items),
        next_actions=tuple(next_actions),
        warnings=tuple(warnings),
    )


def report_to_dict(report: AgentReviewDashboardReport) -> dict[str, Any]:
    return asdict(report)


def item_lines(items: tuple[dict[str, Any], ...], empty: str = "- None") -> str:
    if not items:
        return empty
    lines = []
    for item in items:
        title = str(item.get("title") or item.get("package_id") or "").replace("\n", " ")
        status = item.get("decision") or item.get("urgency") or item.get("recommended_action") or "-"
        score = item.get("decision_score") or item.get("quality_score") or "-"
        lines.append(f"- `{item.get('package_id')}` {title} ({status}; score={score})")
    return "\n".join(lines)


def render_markdown(report: AgentReviewDashboardReport) -> str:
    summary = report.summary
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    next_actions = "\n".join(f"- {item}" for item in report.next_actions)
    return f"""# Agent Review Dashboard

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Review items: `{summary['review_items']}`
- Approved for queue: `{summary['approved_for_queue']}`
- Needs revision: `{summary['needs_revision']}`
- Hold: `{summary['hold']}`
- Escalated to human: `{summary['escalated_to_human']}`
- Human exceptions: `{summary['human_exceptions']}`
- Estimated human review minutes: `{summary['estimated_human_review_minutes']}`

## Human Attention Required

{item_lines(report.human_attention_required)}

## Approved / Ready

{item_lines(report.approved_ready)}

## Needs Revision

{item_lines(report.needs_revision)}

## Hold

{item_lines(report.hold)}

## Agent Disagreement

{item_lines(report.agent_disagreement)}

## Next Actions

{next_actions}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__agent-review-dashboard.json",
        "latest_json": paths.logs_root / "latest_agent_review_dashboard.json",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__agent-review-dashboard.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_agent_review_dashboard.md",
    }


def write_agent_review_dashboard_report(report: AgentReviewDashboardReport, paths: ProjectPaths) -> dict[str, Path]:
    paths_by_name = output_paths(paths, report.run_date)
    for path in paths_by_name.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (paths_by_name["dated_json"], paths_by_name["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (paths_by_name["frontstage_dated_md"], paths_by_name["frontstage_latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return paths_by_name
