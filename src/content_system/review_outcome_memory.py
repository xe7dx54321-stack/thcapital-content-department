"""Review Outcome Memory v1."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class ReviewOutcomeRecord:
    record_id: str
    run_date: str
    publishing_candidate_id: str
    package_id: str
    title: str
    judge_decision: str
    critic_severity: str
    proponent_support_level: str
    publish_priority: str
    human_action: str
    human_score: float | None
    feedback_tags: tuple[str, ...]
    human_notes: str
    final_outcome: str
    lessons: tuple[str, ...]
    source_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class ReviewOutcomeMemory:
    schema_version: str
    updated_at: str
    records: tuple[ReviewOutcomeRecord, ...]
    summary: dict[str, int]


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


def by_key(items: list[dict[str, Any]], field: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(field)): item for item in items if item.get(field)}


def final_outcome(action: str) -> str:
    return {
        "APPROVE": "APPROVED",
        "REVISE": "REVISED",
        "HOLD": "HELD",
        "REJECT": "REJECTED",
    }.get(action, "PENDING")


def lessons_for(action: str, feedback: dict[str, Any], critic: dict[str, Any]) -> tuple[str, ...]:
    lessons: list[str] = []
    if action == "UNREVIEWED":
        lessons.append("Awaiting human feedback; keep current rules until reviewed.")
    if action == "REVISE":
        lessons.append("Human requested revision; inspect feedback tags before rule changes.")
    if action == "REJECT":
        lessons.append("Human rejected the item; consider stricter pre-publish checks.")
    tags = [str(item) for item in feedback.get("feedback_tags", []) if item]
    if tags:
        lessons.append("Feedback tags: " + ", ".join(tags))
    for concern in critic.get("must_fix_before_publish", [])[:2]:
        lessons.append(str(concern))
    return tuple(dict.fromkeys(lessons))


def build_record(candidate: dict[str, Any], feedback: dict[str, Any], judge: dict[str, Any], critic: dict[str, Any], prop: dict[str, Any]) -> ReviewOutcomeRecord:
    run_date = str(candidate.get("run_date") or feedback.get("run_date") or "").replace("-", "")[:8]
    action = str(feedback.get("human_action") or "UNREVIEWED")
    score = feedback.get("human_score")
    return ReviewOutcomeRecord(
        record_id=make_id("rom", run_date, str(candidate.get("publishing_candidate_id") or "")),
        run_date=run_date,
        publishing_candidate_id=str(candidate.get("publishing_candidate_id") or ""),
        package_id=str(candidate.get("package_id") or ""),
        title=str(candidate.get("title") or feedback.get("title") or ""),
        judge_decision=str(judge.get("decision") or candidate.get("judge_decision") or ""),
        critic_severity=str(critic.get("severity") or ""),
        proponent_support_level=str(prop.get("support_level") or ""),
        publish_priority=str(candidate.get("publish_priority") or ""),
        human_action=action,
        human_score=float(score) if score is not None else None,
        feedback_tags=tuple(str(item) for item in feedback.get("feedback_tags", []) if item),
        human_notes=str(feedback.get("human_notes") or ""),
        final_outcome=final_outcome(action),
        lessons=lessons_for(action, feedback, critic),
        source_ids=tuple(str(item) for item in candidate.get("source_ids", []) if item),
        evidence_ids=tuple(str(item) for item in candidate.get("evidence_ids", []) if item),
    )


def summary_for(records: tuple[ReviewOutcomeRecord, ...]) -> dict[str, int]:
    return {
        "record_count": len(records),
        "approved_count": sum(1 for item in records if item.final_outcome == "APPROVED"),
        "revise_count": sum(1 for item in records if item.final_outcome == "REVISED"),
        "hold_count": sum(1 for item in records if item.final_outcome == "HELD"),
        "reject_count": sum(1 for item in records if item.final_outcome == "REJECTED"),
        "unreviewed_count": sum(1 for item in records if item.human_action == "UNREVIEWED"),
    }


def build_review_outcome_memory(paths: ProjectPaths) -> ReviewOutcomeMemory:
    publish_root = paths.market_content_root / "07_publishing"
    review_root = paths.market_content_root / "06_review_queue"
    existing = read_json(publish_root / "review_outcome_memory.json")
    existing_records = {
        str(item.get("publishing_candidate_id")): item
        for item in list_payload(existing, "records")
        if item.get("publishing_candidate_id")
    }
    candidates = list_payload(read_json(publish_root / "latest_publishing_candidate_queue.json"), "candidates")
    feedback = by_key(list_payload(read_json(publish_root / "latest_human_feedback_template.json"), "feedback_items"), "publishing_candidate_id")
    judges = by_key(list_payload(read_json(review_root / "latest_judge_gate.json"), "decisions"), "package_id")
    critics = by_key(list_payload(read_json(review_root / "latest_critic_reviews.json"), "reviews"), "package_id")
    props = by_key(list_payload(read_json(review_root / "latest_proponent_reviews.json"), "reviews"), "package_id")

    merged: dict[str, dict[str, Any]] = dict(existing_records)
    for candidate in candidates:
        key = str(candidate.get("publishing_candidate_id") or "")
        if not key:
            continue
        record = build_record(
            candidate,
            feedback.get(key, {}),
            judges.get(str(candidate.get("package_id")), {}),
            critics.get(str(candidate.get("package_id")), {}),
            props.get(str(candidate.get("package_id")), {}),
        )
        merged[key] = asdict(record)
    records = tuple(
        ReviewOutcomeRecord(**item)
        for item in sorted(merged.values(), key=lambda value: (str(value.get("run_date") or ""), str(value.get("publishing_candidate_id") or "")))
    )
    return ReviewOutcomeMemory(SCHEMA_VERSION, utc_now(), records, summary_for(records))


def memory_to_dict(memory: ReviewOutcomeMemory) -> dict[str, Any]:
    return asdict(memory)


def render_markdown(memory: ReviewOutcomeMemory) -> str:
    rows = [
        f"| {idx} | {item.human_action} | {item.final_outcome} | {item.publish_priority} | {item.package_id} | {item.title.replace('|', '\\|')} |"
        for idx, item in enumerate(memory.records, start=1)
    ]
    summary = memory.summary
    return f"""# Review Outcome Memory v1

## Summary

- Updated at: `{memory.updated_at}`
- Records: `{summary['record_count']}`
- Approved: `{summary['approved_count']}`
- Revise: `{summary['revise_count']}`
- Hold: `{summary['hold_count']}`
- Reject: `{summary['reject_count']}`
- Unreviewed: `{summary['unreviewed_count']}`

## Records

| # | Human Action | Final Outcome | Priority | Package | Title |
|---:|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | - | None |'}
"""


def output_paths(paths: ProjectPaths) -> dict[str, Path]:
    return {
        "json": paths.market_content_root / "07_publishing" / "review_outcome_memory.json",
        "md": paths.market_content_root / "07_publishing" / "review_outcome_memory.md",
        "frontstage": paths.frontstage_root / "review_outcome_memory_board.md",
    }


def write_review_outcome_memory(memory: ReviewOutcomeMemory, paths: ProjectPaths) -> dict[str, Path]:
    paths_by_name = output_paths(paths)
    for path in paths_by_name.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(memory_to_dict(memory), ensure_ascii=False, indent=2)
    markdown = render_markdown(memory)
    paths_by_name["json"].write_text(payload + "\n", encoding="utf-8")
    paths_by_name["md"].write_text(markdown, encoding="utf-8")
    paths_by_name["frontstage"].write_text(markdown, encoding="utf-8")
    return paths_by_name
