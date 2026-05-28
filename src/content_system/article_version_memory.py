"""Persist article version outcomes as local memory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class ArticleVersionMemoryResult:
    version_count: int
    accepted_count: int
    rejected_count: int
    average_score_delta: float
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "memory_json": root / "article_version_memory.json",
        "memory_md": root / "article_version_memory.md",
        "board_md": paths.frontstage_root / "article_version_memory_board.md",
    }


def by_key(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def version_status(decision: str) -> str:
    if decision == "ACCEPT":
        return "active"
    if decision == "REJECT":
        return "rejected"
    if decision in {"REVISE_MORE", "DEFER"}:
        return "reference"
    return "pending"


def lesson_for(version: dict[str, Any], comparison: dict[str, Any], decision: dict[str, Any]) -> list[str]:
    lessons: list[str] = []
    version_type = str(version.get("version_type") or comparison.get("version_type") or "rewrite")
    human_decision = str(decision.get("decision") or "UNREVIEWED")
    change = str(version.get("change_summary") or "")
    delta = safe_float((comparison.get("scores") or {}).get("delta"))
    if version_type == "rewrite" and human_decision == "ACCEPT":
        lessons.append("Approved rewrite pattern can be used as a future reference.")
    if "投资人" in change and human_decision == "ACCEPT":
        lessons.append("User preference signal: prefer investor-angle revisions for broad AI/Agent topics.")
    if version_type == "evidence_expansion" and human_decision == "REVISE_MORE":
        lessons.append("Evidence expansion did not satisfy the request; strengthen first-party evidence collection.")
    if human_decision == "REJECT":
        lessons.append("This action pattern may reduce article quality and should be reviewed before reuse.")
    if delta > 5 and human_decision == "UNREVIEWED":
        lessons.append("Automated score suggests improvement, but human decision is still required.")
    if not lessons:
        lessons.append("Keep as neutral version outcome until more human feedback is available.")
    return lessons


def build_records(paths: ProjectPaths) -> list[dict[str, Any]]:
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    rewrite = list_payload(read_json(versions_root / "latest_rewrite_versions.json"), "versions")
    comparisons = by_key(list_payload(read_json(versions_root / "latest_version_comparison_scores.json"), "comparisons"), "version_id")
    decisions = by_key(list_payload(read_json(versions_root / "latest_version_review_decisions.json"), "decisions"), "version_id")
    records: list[dict[str, Any]] = []
    for version in rewrite:
        version_id = str(version.get("version_id") or "")
        comparison = comparisons.get(version_id, {})
        decision = decisions.get(version_id, {})
        scores = comparison.get("scores") if isinstance(comparison.get("scores"), dict) else {}
        human_decision = str(decision.get("decision") or "UNREVIEWED")
        records.append(
            {
                "version_id": version_id,
                "source_article_id": version.get("source_article_id") or comparison.get("source_article_id") or "",
                "source_action_id": version.get("source_action_id") or comparison.get("source_action_id") or "",
                "version_type": version.get("version_type") or comparison.get("version_type") or "rewrite",
                "change_summary": version.get("change_summary") or "",
                "score_delta": safe_float(scores.get("delta")),
                "recommendation": comparison.get("recommendation") or "HUMAN_REVIEW",
                "human_decision": human_decision,
                "human_score": decision.get("human_score"),
                "human_notes": decision.get("human_notes") or "",
                "lessons": lesson_for(version, comparison, decision),
                "status": version_status(human_decision),
            }
        )
    return records


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    deltas = [safe_float(item.get("score_delta")) for item in records]
    return {
        "version_count": len(records),
        "accepted_count": sum(1 for item in records if item.get("human_decision") == "ACCEPT"),
        "rejected_count": sum(1 for item in records if item.get("human_decision") == "REJECT"),
        "average_score_delta": round(sum(deltas) / len(deltas), 2) if deltas else 0,
    }


def update_article_version_memory(paths: ProjectPaths, repo_root: Path) -> tuple[ArticleVersionMemoryResult, dict[str, Any]]:
    existing = read_json(output_paths(paths)["memory_json"])
    existing_by_id = by_key(list_payload(existing, "versions"), "version_id")
    records = build_records(paths)
    merged: dict[str, dict[str, Any]] = {key: value for key, value in existing_by_id.items()}
    for record in records:
        if record.get("version_id"):
            merged[str(record["version_id"])] = record
    versions = sorted(merged.values(), key=lambda item: str(item.get("version_id") or ""))
    summary = summarize(versions)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "updated_at": utc_now(),
        "versions": versions,
        "summary": summary,
    }
    outputs = output_paths(paths)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        ArticleVersionMemoryResult(
            summary["version_count"],
            summary["accepted_count"],
            summary["rejected_count"],
            summary["average_score_delta"],
            repo_relative(outputs["memory_json"], repo_root),
            repo_relative(outputs["board_md"], repo_root),
        ),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('version_id')}` | `{item.get('human_decision')}` | `{item.get('score_delta')}` | `{item.get('status')}` | {item.get('change_summary') or ''} |"
        for item in list_payload(payload, "versions")
    ) or "| - | UNREVIEWED | 0 | pending | No versions recorded |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    lessons = []
    for item in list_payload(payload, "versions")[-8:]:
        for lesson in item.get("lessons") or []:
            lessons.append(f"- `{item.get('version_id')}`: {lesson}")
    lessons_text = "\n".join(lessons) if lessons else "- No lessons yet."
    return f"""# Article Version Memory

## Summary

- Updated at: `{payload.get('updated_at')}`
- Versions: `{summary.get('version_count', 0)}`
- Accepted: `{summary.get('accepted_count', 0)}`
- Rejected: `{summary.get('rejected_count', 0)}`
- Average score delta: `{summary.get('average_score_delta', 0)}`

## Versions

| Version | Human Decision | Score Delta | Status | Change Summary |
|---|---|---:|---|---|
{rows}

## Lessons

{lessons_text}
"""
