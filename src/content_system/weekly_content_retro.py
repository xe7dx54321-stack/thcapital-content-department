"""Weekly content retro report for Phase 7."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class WeeklyContentRetroReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    summary: dict[str, Any]
    highlights: tuple[str, ...]
    rule_suggestions: tuple[str, ...]
    next_week_focus: tuple[str, ...]
    warnings: tuple[str, ...]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__weekly-content-retro.json",
        "latest_json": paths.logs_root / "latest_weekly_content_retro.json",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__weekly-content-retro.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_weekly_content_retro.md",
    }


def build_weekly_content_retro_report(paths: ProjectPaths) -> WeeklyContentRetroReport:
    publishing_root = paths.market_content_root / "07_publishing"
    topic_root = paths.market_content_root / "03_topic_candidates"
    memory = read_json(publishing_root / "review_outcome_memory.json")
    rule = read_json(publishing_root / "latest_rule_update_suggestions.json")
    learning = read_json(paths.logs_root / "latest_learning_loop_dashboard.json")
    evaluation = read_json(publishing_root / "latest_agent_evaluation_template.json")
    ab = read_json(paths.logs_root / "latest_llm_ab_comparison.json")
    candidates = read_json(topic_root / "latest_high_value_candidates.json")
    publishing = read_json(publishing_root / "latest_publishing_candidate_queue.json")
    records = list_payload(memory, "records")
    candidate_items = list_payload(candidates, "candidates")
    publishing_items = list_payload(publishing, "candidates")
    suggestions = list_payload(rule, "suggestions")
    feedback_counter = Counter(str(item.get("human_action") or "UNREVIEWED") for item in records)
    warnings: list[str] = []
    if not records:
        warnings.append("No review outcome memory records available.")
    if not candidate_items:
        warnings.append("No high-value candidates available for retro.")
    highlights = [
        f"High-value candidates this week: {len(candidate_items)}.",
        f"Publishing queue items: {len(publishing_items)}.",
        f"Agent A/B decision conflicts: {(ab.get('summary') or {}).get('judge_decision_conflict_count', 0)}.",
        f"Human feedback unreviewed: {feedback_counter.get('UNREVIEWED', 0)}.",
    ]
    rule_suggestions = [str(item.get("proposed_change") or item.get("reason") or "") for item in suggestions if item]
    if not rule_suggestions:
        rule_suggestions = ["Keep collecting human feedback before changing rules."]
    next_week_focus = [
        "Keep live pilots allowlisted and low-volume.",
        "Review any judge conflicts before publishing.",
        "Collect human feedback for publishing candidates.",
    ]
    summary = {
        "high_value_candidate_count": len(candidate_items),
        "publishing_queue_count": len(publishing_items),
        "memory_record_count": len(records),
        "feedback_distribution": dict(feedback_counter),
        "rule_suggestion_count": len(suggestions),
        "agent_evaluation_count": safe_int(evaluation.get("evaluation_count")),
        "learning_dashboard_status": learning.get("status", "UNKNOWN"),
        "ab_comparison_status": ab.get("status", "UNKNOWN"),
    }
    return WeeklyContentRetroReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=today_token(),
        status="DEGRADED" if warnings else "SUCCESS",
        summary=summary,
        highlights=tuple(highlights),
        rule_suggestions=tuple(rule_suggestions),
        next_week_focus=tuple(next_week_focus),
        warnings=tuple(warnings),
    )


def render_markdown(report: WeeklyContentRetroReport) -> str:
    highlights = "\n".join(f"- {item}" for item in report.highlights)
    suggestions = "\n".join(f"- {item}" for item in report.rule_suggestions)
    focus = "\n".join(f"- {item}" for item in report.next_week_focus)
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Weekly Content Retro v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**
- High-value candidates: `{report.summary.get('high_value_candidate_count')}`
- Publishing queue: `{report.summary.get('publishing_queue_count')}`
- Memory records: `{report.summary.get('memory_record_count')}`
- Rule suggestions: `{report.summary.get('rule_suggestion_count')}`
- Agent evaluations: `{report.summary.get('agent_evaluation_count')}`

## Highlights

{highlights}

## Rule Suggestions

{suggestions}

## Next Week Focus

{focus}

## Warnings

{warnings}
"""


def write_weekly_content_retro_report(report: WeeklyContentRetroReport, paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    outputs = output_paths(paths, report.run_date)
    payload = asdict(report)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return write_json_and_markdown(payload, render_markdown(report), outputs)


def report_to_dict(report: WeeklyContentRetroReport) -> dict[str, Any]:
    return asdict(report)
