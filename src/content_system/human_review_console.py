"""Local human review console summaries."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class HumanReviewConsoleReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    summary: dict[str, int]
    publishing_candidates: tuple[dict[str, Any], ...]
    human_exceptions: tuple[dict[str, Any], ...]
    pending_feedback: tuple[dict[str, Any], ...]
    dry_run_items: tuple[dict[str, Any], ...]
    agent_conflicts: tuple[dict[str, Any], ...]
    weekly_highlights: tuple[str, ...]
    recommended_human_actions: tuple[str, ...]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__human-review-console.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_human_review_console.md",
        "dated_json": paths.logs_root / f"{run_date}__human-review-console.json",
        "latest_json": paths.logs_root / "latest_human_review_console.json",
    }


def build_human_review_console(paths: ProjectPaths) -> HumanReviewConsoleReport:
    publishing_root = paths.market_content_root / "07_publishing"
    review_root = paths.market_content_root / "06_review_queue"
    candidates_payload = read_json(publishing_root / "latest_publishing_candidate_queue.json")
    exceptions_payload = read_json(review_root / "latest_human_exception_queue.json")
    feedback_payload = read_json(publishing_root / "latest_human_feedback_template.json")
    dry_run_payload = read_json(publishing_root / "latest_publishing_dry_run.json")
    ab_payload = read_json(paths.logs_root / "latest_llm_ab_comparison.json")
    retro_payload = read_json(paths.logs_root / "latest_weekly_content_retro.json")
    run_date = str(candidates_payload.get("run_date") or today_token()).replace("-", "")[:8]
    candidates = list_payload(candidates_payload, "candidates")
    exceptions = list_payload(exceptions_payload, "exceptions")
    feedback = [item for item in list_payload(feedback_payload, "feedback_items") if str(item.get("human_action") or "UNREVIEWED") == "UNREVIEWED"]
    dry_run_items = list_payload(dry_run_payload, "items")
    conflicts = list_payload(ab_payload, "decision_conflicts") + list_payload(ab_payload, "human_spot_check_items")
    highlights_raw = retro_payload.get("highlights")
    highlights = [str(item) for item in highlights_raw if isinstance(item, str)] if isinstance(highlights_raw, list) else []
    actions: list[str] = []
    if exceptions:
        actions.append("Review human exception queue before approving any candidate.")
    if feedback:
        actions.append("Fill the human feedback template for pending publishing candidates.")
    if any(item.get("dry_run_status") != "READY" for item in dry_run_items):
        actions.append("Resolve publishing dry-run issues before external platform work.")
    if conflicts:
        actions.append("Check rule-vs-LLM conflicts before relying on agent recommendations.")
    if not actions:
        actions.append("Review the top publishing candidate and confirm whether to proceed manually.")
    summary = {
        "publishing_candidates": len(candidates),
        "human_exceptions": len(exceptions),
        "pending_feedback": len(feedback),
        "dry_run_ready": sum(1 for item in dry_run_items if item.get("dry_run_status") == "READY"),
        "dry_run_not_ready": sum(1 for item in dry_run_items if item.get("dry_run_status") == "NOT_READY"),
        "agent_conflicts": len(conflicts),
        "weekly_highlights": len(highlights),
    }
    status = "DEGRADED" if summary["human_exceptions"] or summary["dry_run_not_ready"] or summary["agent_conflicts"] else "SUCCESS"
    return HumanReviewConsoleReport(
        SCHEMA_VERSION,
        utc_now(),
        run_date,
        status,
        summary,
        tuple(candidates),
        tuple(exceptions),
        tuple(feedback),
        tuple(dry_run_items),
        tuple(conflicts),
        tuple(highlights),
        tuple(actions),
    )


def render_markdown(report: HumanReviewConsoleReport) -> str:
    candidate_rows = "\n".join(
        f"| {item.get('publishing_candidate_id')} | {item.get('title')} | {item.get('publish_priority')} | {item.get('publish_status')} |"
        for item in report.publishing_candidates
    ) or "| - | - | - | - |"
    exception_lines = "\n".join(f"- `{item.get('exception_id')}` {item.get('reason')}" for item in report.human_exceptions) or "- None"
    feedback_lines = "\n".join(f"- `{item.get('feedback_id')}` {item.get('title')}" for item in report.pending_feedback) or "- None"
    dry_rows = "\n".join(
        f"| {item.get('publishing_candidate_id')} | {item.get('platform')} | {item.get('dry_run_status')} |"
        for item in report.dry_run_items
    ) or "| - | - | - |"
    conflict_lines = "\n".join(
        f"- `{item.get('review_item_id')}` rule `{item.get('rule_decision')}` vs LLM `{item.get('llm_decision')}`"
        for item in report.agent_conflicts
    ) or "- None"
    highlights = "\n".join(f"- {item}" for item in report.weekly_highlights) if report.weekly_highlights else "- None"
    actions = "\n".join(f"- {item}" for item in report.recommended_human_actions)
    return f"""# Human Review Console

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**
- Publishing candidates: `{report.summary.get('publishing_candidates')}`
- Human exceptions: `{report.summary.get('human_exceptions')}`
- Pending feedback: `{report.summary.get('pending_feedback')}`
- Dry-run ready: `{report.summary.get('dry_run_ready')}`
- Dry-run not ready: `{report.summary.get('dry_run_not_ready')}`
- Agent conflicts: `{report.summary.get('agent_conflicts')}`

## Publishing Candidates

| Candidate | Title | Priority | Status |
|---|---|---|---|
{candidate_rows}

## Human Exceptions

{exception_lines}

## Pending Feedback

{feedback_lines}

## Publishing Dry-run Status

| Candidate | Platform | Status |
|---|---|---|
{dry_rows}

## Agent Conflicts

{conflict_lines}

## Weekly Retro Highlights

{highlights}

## Recommended Human Actions

{actions}
"""


def write_human_review_console(report: HumanReviewConsoleReport, paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    outputs = output_paths(paths, report.run_date)
    payload = asdict(report)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return write_json_and_markdown(payload, render_markdown(report), outputs)


def report_to_dict(report: HumanReviewConsoleReport) -> dict[str, Any]:
    return asdict(report)
