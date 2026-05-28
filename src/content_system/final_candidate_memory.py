"""Persist final article candidate outcomes as local memory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class FinalCandidateMemoryResult:
    final_candidate_count: int
    ready_count: int
    needs_attention_count: int
    blocked_count: int
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "memory_json": root / "final_candidate_memory.json",
        "memory_md": root / "final_candidate_memory.md",
        "board_md": paths.frontstage_root / "final_candidate_memory_board.md",
    }


def by_key(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def status_for(candidate: dict[str, Any], checklist: dict[str, Any]) -> str:
    if candidate.get("quality_status") == "HOLD" or checklist.get("status") == "BLOCKED":
        return "hold"
    return "active"


def lessons_for(candidate: dict[str, Any], checklist: dict[str, Any]) -> list[str]:
    lessons: list[str] = []
    if candidate.get("quality_status") == "READY_FOR_FINAL_REVIEW":
        lessons.append("Accepted version reached final review candidate state.")
    if checklist.get("status") == "NEEDS_ATTENTION":
        lessons.append("Final checklist still has warnings; human review must resolve them before publishing.")
    if checklist.get("status") == "BLOCKED":
        lessons.append("Final checklist blocked this candidate; do not publish until issues are resolved.")
    if safe_float(candidate.get("version_score_delta")) > 0:
        lessons.append("Promoted version improved automated score delta.")
    return lessons or ["Keep candidate for reference until final human decision is available."]


def update_final_candidate_memory(paths: ProjectPaths, repo_root: Path) -> tuple[FinalCandidateMemoryResult, dict[str, Any]]:
    root = paths.market_content_root / "07_publishing"
    candidates_payload = read_json(root / "latest_final_article_candidates.json")
    checklist_payload = read_json(root / "latest_final_publish_checklist.json")
    existing = read_json(root / "final_candidate_memory.json")
    existing_by_id = by_key(list_payload(existing, "final_candidates"), "final_candidate_id")
    checklist_by_candidate = by_key(list_payload(checklist_payload, "items"), "final_candidate_id")
    merged = dict(existing_by_id)
    for candidate in list_payload(candidates_payload, "candidates"):
        checklist = checklist_by_candidate.get(str(candidate.get("final_candidate_id") or ""), {})
        record = {
            "final_candidate_id": candidate.get("final_candidate_id") or "",
            "version_id": candidate.get("version_id") or "",
            "source_article_id": candidate.get("source_article_id") or "",
            "title": candidate.get("wechat_title") or candidate.get("title") or "",
            "quality_status": candidate.get("quality_status") or "",
            "checklist_status": checklist.get("status") or "UNREVIEWED",
            "human_score": candidate.get("human_score"),
            "version_score_delta": safe_float(candidate.get("version_score_delta")),
            "lessons": lessons_for(candidate, checklist),
            "status": status_for(candidate, checklist),
            "do_not_publish": True,
        }
        if record["final_candidate_id"]:
            merged[str(record["final_candidate_id"])] = record
    records = sorted(merged.values(), key=lambda item: str(item.get("final_candidate_id") or ""))
    summary = {
        "final_candidate_count": len(records),
        "ready_count": sum(1 for item in records if item.get("checklist_status") == "READY"),
        "needs_attention_count": sum(1 for item in records if item.get("checklist_status") == "NEEDS_ATTENTION"),
        "blocked_count": sum(1 for item in records if item.get("checklist_status") == "BLOCKED"),
    }
    payload = {"schema_version": SCHEMA_VERSION, "updated_at": utc_now(), "final_candidates": records, "summary": summary}
    outputs = output_paths(paths)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        FinalCandidateMemoryResult(summary["final_candidate_count"], summary["ready_count"], summary["needs_attention_count"], summary["blocked_count"], repo_relative(outputs["memory_json"], repo_root), repo_relative(outputs["board_md"], repo_root)),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('final_candidate_id')}` | `{item.get('version_id')}` | `{item.get('quality_status')}` | `{item.get('checklist_status')}` | `{item.get('do_not_publish')}` | {item.get('title') or ''} |"
        for item in list_payload(payload, "final_candidates")
    ) or "| - | - | - | - | true | No final candidates |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Final Candidate Memory

## Summary

- Updated at: `{payload.get('updated_at')}`
- Final candidates: `{summary.get('final_candidate_count', 0)}`
- Ready: `{summary.get('ready_count', 0)}`
- Needs attention: `{summary.get('needs_attention_count', 0)}`
- Blocked: `{summary.get('blocked_count', 0)}`

| Final Candidate | Version | Quality | Checklist | Do Not Publish | Title |
|---|---|---|---|---|---|
{rows}
"""
