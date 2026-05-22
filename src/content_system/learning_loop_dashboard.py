"""Learning Loop Dashboard v1."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class LearningLoopDashboardReport:
    schema_version: str
    generated_at: str
    run_date: str
    summary: dict[str, int]
    pending_human_feedback: tuple[dict[str, Any], ...]
    recent_outcomes: tuple[dict[str, Any], ...]
    common_feedback_tags: tuple[dict[str, Any], ...]
    rule_update_suggestions: tuple[dict[str, Any], ...]
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


def tag_counts(records: list[dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    counts: dict[str, int] = {}
    for record in records:
        for tag in record.get("feedback_tags", []) or []:
            counts[str(tag)] = counts.get(str(tag), 0) + 1
    return tuple({"tag": key, "count": value} for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:20])


def build_learning_loop_dashboard_report(paths: ProjectPaths) -> LearningLoopDashboardReport:
    publish_root = paths.market_content_root / "07_publishing"
    candidates_payload = read_json(publish_root / "latest_publishing_candidate_queue.json")
    feedback_payload = read_json(publish_root / "latest_human_feedback_template.json")
    memory_payload = read_json(publish_root / "review_outcome_memory.json")
    suggestions_payload = read_json(publish_root / "latest_rule_update_suggestions.json")
    agent_dashboard = read_json(paths.logs_root / "latest_agent_review_dashboard.json")

    candidates = list_payload(candidates_payload, "candidates")
    feedback_items = list_payload(feedback_payload, "feedback_items")
    records = list_payload(memory_payload, "records")
    suggestions = list_payload(suggestions_payload, "suggestions")
    run_date = str(candidates_payload.get("run_date") or feedback_payload.get("run_date") or datetime.now().strftime("%Y%m%d")).replace("-", "")[:8]
    pending = [item for item in feedback_items if item.get("human_action") == "UNREVIEWED"]
    summary = {
        "publishing_candidates": len(candidates),
        "human_feedback_items": len(feedback_items),
        "approved": sum(1 for item in records if item.get("final_outcome") == "APPROVED"),
        "revise": sum(1 for item in records if item.get("final_outcome") == "REVISED"),
        "hold": sum(1 for item in records if item.get("final_outcome") == "HELD"),
        "reject": sum(1 for item in records if item.get("final_outcome") == "REJECTED"),
        "unreviewed": sum(1 for item in records if item.get("human_action") == "UNREVIEWED"),
        "rule_suggestions": len(suggestions),
        "agent_approved_for_queue": int((agent_dashboard.get("summary") or {}).get("approved_for_queue") or 0),
    }
    warnings: list[str] = []
    if not candidates:
        warnings.append("No publishing candidates available.")
    if not records:
        warnings.append("No review outcome memory records available.")
    return LearningLoopDashboardReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date,
        summary=summary,
        pending_human_feedback=tuple(pending),
        recent_outcomes=tuple(records[-20:]),
        common_feedback_tags=tag_counts(records),
        rule_update_suggestions=tuple(suggestions),
        next_actions=(
            "Fill human feedback template for pending candidates.",
            "Review rule update suggestions, but do not auto-apply them.",
            "Use Phase 5 pattern adapters to improve future briefs and outlines.",
        ),
        warnings=tuple(warnings),
    )


def report_to_dict(report: LearningLoopDashboardReport) -> dict[str, Any]:
    return asdict(report)


def list_lines(items: tuple[dict[str, Any], ...], field: str = "title") -> str:
    if not items:
        return "- None"
    return "\n".join(f"- `{item.get('package_id') or item.get('publishing_candidate_id') or item.get('suggestion_id')}` {item.get(field) or item.get('reason') or item.get('final_outcome')}" for item in items)


def render_markdown(report: LearningLoopDashboardReport) -> str:
    s = report.summary
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    next_actions = "\n".join(f"- {item}" for item in report.next_actions)
    tag_lines = "\n".join(f"- {item['tag']}: {item['count']}" for item in report.common_feedback_tags) if report.common_feedback_tags else "- None"
    return f"""# Learning Loop Dashboard

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Publishing candidates: `{s['publishing_candidates']}`
- Human feedback items: `{s['human_feedback_items']}`
- Approved: `{s['approved']}`
- Revise: `{s['revise']}`
- Hold: `{s['hold']}`
- Reject: `{s['reject']}`
- Unreviewed: `{s['unreviewed']}`
- Rule suggestions: `{s['rule_suggestions']}`

## Pending Human Feedback

{list_lines(report.pending_human_feedback)}

## Recent Outcomes

{list_lines(report.recent_outcomes)}

## Common Feedback Tags

{tag_lines}

## Rule Update Suggestions

{list_lines(report.rule_update_suggestions, field='reason')}

## Next Actions

{next_actions}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__learning-loop-dashboard.json",
        "latest_json": paths.logs_root / "latest_learning_loop_dashboard.json",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__learning-loop-dashboard.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_learning_loop_dashboard.md",
    }


def write_learning_loop_dashboard_report(report: LearningLoopDashboardReport, paths: ProjectPaths) -> dict[str, Path]:
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
