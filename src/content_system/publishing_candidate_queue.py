"""Publishing Candidate Queue v1.

This module turns approved Judge Gate decisions into a file-based publishing
preparation queue. It never publishes content automatically.
"""

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
class PublishingCandidate:
    schema_version: str
    publishing_candidate_id: str
    run_date: str
    review_item_id: str
    package_id: str
    brief_id: str
    draft_id: str
    title: str
    platforms: tuple[str, ...]
    judge_decision: str
    release_readiness: str
    publish_priority: str
    publish_status: str
    human_confirmation_required: bool
    recommended_publish_window: str
    why_ready: tuple[str, ...]
    remaining_checks: tuple[str, ...]
    risk_notes: tuple[str, ...]
    source_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    links: dict[str, str]


@dataclass(frozen=True)
class PublishingCandidateQueueReport:
    schema_version: str
    generated_at: str
    run_date: str
    candidate_count: int
    candidates: tuple[PublishingCandidate, ...]
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


def make_id(prefix: str, run_date: str, *parts: str) -> str:
    digest = hashlib.sha1("|".join((run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def list_payload(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    raw = payload.get(key)
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def by_key(items: list[dict[str, Any]], field: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(field)): item for item in items if item.get(field)}


def title_from_package(package: dict[str, Any]) -> str:
    wechat = package.get("wechat") if isinstance(package.get("wechat"), dict) else {}
    xhs = package.get("xiaohongshu") if isinstance(package.get("xiaohongshu"), dict) else {}
    return str(wechat.get("title") or xhs.get("title") or package.get("package_id") or "")


def platforms_from_package(package: dict[str, Any]) -> tuple[str, ...]:
    platforms: list[str] = []
    if isinstance(package.get("wechat"), dict):
        platforms.append("wechat")
    if isinstance(package.get("xiaohongshu"), dict):
        platforms.append("xiaohongshu")
    return tuple(platforms)


def publish_priority(package: dict[str, Any], queue_item: dict[str, Any]) -> str:
    priority = str(queue_item.get("priority") or "")
    if priority in {"HIGH", "MEDIUM", "LOW"}:
        return priority
    if package.get("quality_status") == "READY_FOR_HUMAN_REVIEW":
        return "MEDIUM"
    return "LOW"


def publish_window(priority: str) -> str:
    if priority == "HIGH":
        return "today"
    if priority == "MEDIUM":
        return "this_week"
    return "watch"


def build_candidate(
    decision: dict[str, Any],
    package: dict[str, Any],
    queue_item: dict[str, Any],
    revision: dict[str, Any],
    run_date: str,
) -> PublishingCandidate:
    source_ids = tuple(str(item) for item in queue_item.get("source_ids", []) if item)
    evidence_ids = tuple(str(item) for item in queue_item.get("evidence_ids", []) if item)
    priority = publish_priority(package, queue_item)
    ready = bool(source_ids and evidence_ids and decision.get("release_readiness") == "READY")
    remaining_checks = [
        "Human confirmation before any external publish.",
        "Final factual and tone review.",
        "Platform formatting review.",
    ]
    if not source_ids:
        remaining_checks.append("Attach source_ids before publish preparation.")
    if not evidence_ids:
        remaining_checks.append("Attach evidence_ids before publish preparation.")
    why_ready = [
        str(decision.get("reasoning") or "Judge Gate approved this item."),
        f"Quality status: {package.get('quality_status') or 'UNKNOWN'}.",
        f"Evidence count: {len(evidence_ids)}.",
    ]
    return PublishingCandidate(
        schema_version=SCHEMA_VERSION,
        publishing_candidate_id=make_id("pub", run_date, str(decision.get("package_id") or "")),
        run_date=run_date,
        review_item_id=str(decision.get("review_item_id") or ""),
        package_id=str(decision.get("package_id") or ""),
        brief_id=str(package.get("brief_id") or ""),
        draft_id=str(package.get("draft_id") or ""),
        title=title_from_package(package),
        platforms=platforms_from_package(package),
        judge_decision=str(decision.get("decision") or ""),
        release_readiness=str(decision.get("release_readiness") or "NOT_READY"),
        publish_priority=priority,
        publish_status="PENDING_HUMAN_CONFIRMATION" if ready else "PENDING_REVIEW",
        human_confirmation_required=True,
        recommended_publish_window=publish_window(priority),
        why_ready=tuple(why_ready),
        remaining_checks=tuple(remaining_checks),
        risk_notes=("No automatic publishing is allowed.", "Rule-based queue; human confirmation remains mandatory."),
        source_ids=source_ids,
        evidence_ids=evidence_ids,
        links={
            "platform_package": str(package.get("package_id") or decision.get("package_id") or ""),
            "judge_gate": str(decision.get("judge_decision_id") or ""),
            "revision_instruction": str(revision.get("revision_id") or ""),
        },
    )


def build_publishing_candidate_queue_report(paths: ProjectPaths) -> PublishingCandidateQueueReport:
    review_root = paths.market_content_root / "06_review_queue"
    draft_root = paths.market_content_root / "05_draft_packs"
    judge = read_json(review_root / "latest_judge_gate.json")
    packages = by_key(list_payload(read_json(draft_root / "latest_platform_packages.json"), "packages"), "package_id")
    queue_items = by_key(list_payload(read_json(review_root / "latest_agent_review_queue.json"), "items"), "review_item_id")
    revisions = by_key(list_payload(read_json(review_root / "latest_revision_instructions.json"), "instructions"), "package_id")
    run_date = str(judge.get("run_date") or datetime.now().strftime("%Y%m%d")).replace("-", "")[:8]
    decisions = list_payload(judge, "decisions")
    approved = [item for item in decisions if item.get("decision") == "APPROVED_FOR_QUEUE"]
    warnings: list[str] = []
    if not decisions:
        warnings.append("Judge Gate output is missing or empty.")
    if not approved:
        warnings.append("No APPROVED_FOR_QUEUE decisions available.")
    candidates = tuple(
        build_candidate(
            decision,
            packages.get(str(decision.get("package_id")), {}),
            queue_items.get(str(decision.get("review_item_id")), {}),
            revisions.get(str(decision.get("package_id")), {}),
            run_date,
        )
        for decision in approved
    )
    return PublishingCandidateQueueReport(SCHEMA_VERSION, utc_now(), run_date, len(candidates), candidates, tuple(warnings))


def report_to_dict(report: PublishingCandidateQueueReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: PublishingCandidateQueueReport) -> str:
    rows = [
        f"| {idx} | {item.publish_priority} | {item.publish_status} | {item.recommended_publish_window} | {item.package_id} | {escape_cell(item.title)} |"
        for idx, item in enumerate(report.candidates, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Publishing Candidate Queue v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Candidates: `{report.candidate_count}`

## Candidates

| # | Priority | Status | Window | Package | Title |
|---:|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | - | None |'}

## Policy

- This is a publishing preparation queue, not an automatic publisher.
- Every candidate requires human confirmation before external publication.

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__publishing-candidate-queue.json",
        "dated_md": root / f"{run_date}__publishing-candidate-queue.md",
        "latest_json": root / "latest_publishing_candidate_queue.json",
        "latest_md": root / "latest_publishing_candidate_queue.md",
    }


def write_publishing_candidate_queue_report(report: PublishingCandidateQueueReport, paths: ProjectPaths) -> dict[str, Path]:
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
