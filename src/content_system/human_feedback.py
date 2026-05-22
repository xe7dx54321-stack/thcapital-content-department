"""Human Feedback Capture v1."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"
VALID_ACTIONS = {"UNREVIEWED", "APPROVE", "REVISE", "HOLD", "REJECT"}


@dataclass(frozen=True)
class HumanFeedbackItem:
    schema_version: str
    feedback_id: str
    run_date: str
    publishing_candidate_id: str
    package_id: str
    title: str
    human_action: str
    human_score: float | None
    feedback_tags: tuple[str, ...]
    human_notes: str
    publish_platforms: tuple[str, ...]
    final_publish_decision: str
    reviewer: str
    updated_at: str


@dataclass(frozen=True)
class HumanFeedbackTemplateReport:
    schema_version: str
    generated_at: str
    run_date: str
    feedback_item_count: int
    feedback_items: tuple[HumanFeedbackItem, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class FeedbackValidationIssue:
    severity: str
    feedback_id: str
    field: str
    message: str


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


def make_id(prefix: str, run_date: str, *parts: str) -> str:
    digest = hashlib.sha1("|".join((run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def list_payload(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    raw = payload.get(key)
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def build_item(candidate: dict[str, Any], run_date: str) -> HumanFeedbackItem:
    return HumanFeedbackItem(
        schema_version=SCHEMA_VERSION,
        feedback_id=make_id("fb", run_date, str(candidate.get("publishing_candidate_id") or "")),
        run_date=run_date,
        publishing_candidate_id=str(candidate.get("publishing_candidate_id") or ""),
        package_id=str(candidate.get("package_id") or ""),
        title=str(candidate.get("title") or ""),
        human_action="UNREVIEWED",
        human_score=None,
        feedback_tags=(),
        human_notes="",
        publish_platforms=tuple(str(item) for item in candidate.get("platforms", []) if item),
        final_publish_decision="PENDING",
        reviewer="human",
        updated_at="",
    )


def build_human_feedback_template_report(paths: ProjectPaths) -> HumanFeedbackTemplateReport:
    payload = read_json(paths.market_content_root / "07_publishing" / "latest_publishing_candidate_queue.json")
    candidates = list_payload(payload, "candidates")
    run_date = str(payload.get("run_date") or datetime.now().strftime("%Y%m%d")).replace("-", "")[:8]
    items = tuple(build_item(candidate, run_date) for candidate in candidates)
    warnings = () if candidates else ("No publishing candidates available for feedback template.",)
    return HumanFeedbackTemplateReport(SCHEMA_VERSION, utc_now(), run_date, len(items), items, warnings)


def validate_feedback_payload(payload: dict[str, Any]) -> tuple[FeedbackValidationIssue, ...]:
    issues: list[FeedbackValidationIssue] = []
    items = list_payload(payload, "feedback_items")
    if not items:
        issues.append(FeedbackValidationIssue("WARN", "", "feedback_items", "No feedback items found."))
    for item in items:
        feedback_id = str(item.get("feedback_id") or "")
        action = str(item.get("human_action") or "")
        if action not in VALID_ACTIONS:
            issues.append(FeedbackValidationIssue("ERROR", feedback_id, "human_action", f"Invalid action: {action}"))
        score = item.get("human_score")
        if score is not None:
            try:
                value = float(score)
            except (TypeError, ValueError):
                issues.append(FeedbackValidationIssue("ERROR", feedback_id, "human_score", "human_score must be 0-10 or null."))
            else:
                if value < 0 or value > 10:
                    issues.append(FeedbackValidationIssue("ERROR", feedback_id, "human_score", "human_score must be between 0 and 10."))
        if not item.get("publishing_candidate_id"):
            issues.append(FeedbackValidationIssue("ERROR", feedback_id, "publishing_candidate_id", "publishing_candidate_id is required."))
        if not item.get("title"):
            issues.append(FeedbackValidationIssue("ERROR", feedback_id, "title", "title is required."))
    return tuple(issues)


def report_to_dict(report: HumanFeedbackTemplateReport) -> dict[str, Any]:
    return asdict(report)


def issues_to_dict(issues: tuple[FeedbackValidationIssue, ...]) -> list[dict[str, str]]:
    return [asdict(issue) for issue in issues]


def render_markdown(report: HumanFeedbackTemplateReport) -> str:
    blocks = []
    for item in report.feedback_items:
        blocks.append(
            f"""## Candidate: {item.title}

- Publishing candidate: `{item.publishing_candidate_id}`
- Package: `{item.package_id}`
- Suggested action: APPROVE / REVISE / HOLD / REJECT
- Human score:
- Notes:
- Tags:
- Platforms: `{', '.join(item.publish_platforms)}`
"""
        )
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Human Feedback Template v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Feedback items: `{report.feedback_item_count}`

## Feedback Items

{chr(10).join(blocks) if blocks else '- None'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__human-feedback-template.json",
        "dated_md": root / f"{run_date}__human-feedback-template.md",
        "latest_json": root / "latest_human_feedback_template.json",
        "latest_md": root / "latest_human_feedback_template.md",
    }


def write_human_feedback_template_report(report: HumanFeedbackTemplateReport, paths: ProjectPaths) -> dict[str, Path]:
    paths_by_name = output_paths(paths, report.run_date)
    for path in paths_by_name.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (paths_by_name["dated_json"], paths_by_name["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (paths_by_name["dated_md"], paths_by_name["latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return paths_by_name
