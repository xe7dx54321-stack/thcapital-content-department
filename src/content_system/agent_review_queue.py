"""Agent Review Queue v1.

This module builds a deterministic review queue from Phase 2 platform packages.
It is a rule-based workflow input, not a real LLM agent.
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
class AgentReviewQueueItem:
    schema_version: str
    review_item_id: str
    run_date: str
    package_id: str
    draft_id: str
    brief_id: str
    title: str
    theme: str
    content_type: str
    target_platforms: tuple[str, ...]
    quality_status: str
    quality_score: float
    publish_status: str
    source_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    agent_review_status: str
    risk_level: str
    priority: str
    human_review_required: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class AgentReviewQueueReport:
    schema_version: str
    generated_at: str
    run_date: str
    item_count: int
    risk_distribution: dict[str, int]
    priority_distribution: dict[str, int]
    items: tuple[AgentReviewQueueItem, ...]
    warnings: tuple[str, ...]


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


def normalize_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return today_token()
    return text.replace("-", "")[:8]


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def make_id(prefix: str, run_date: str, *parts: str) -> str:
    digest = hashlib.sha1("|".join((run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def load_reviews(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_content_quality_review.json")
    raw = payload.get("reviews")
    if not isinstance(raw, list):
        return {}
    return {str(item.get("draft_id")): item for item in raw if isinstance(item, dict)}


def load_briefs(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_content_briefs.json")
    raw = payload.get("briefs")
    if not isinstance(raw, list):
        return {}
    return {str(item.get("brief_id")): item for item in raw if isinstance(item, dict)}


def load_drafts(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_content_drafts.json")
    raw = payload.get("drafts")
    if not isinstance(raw, list):
        return {}
    return {str(item.get("draft_id")): item for item in raw if isinstance(item, dict)}


def target_platforms(package: dict[str, Any]) -> tuple[str, ...]:
    platforms = []
    if isinstance(package.get("wechat"), dict):
        platforms.append("wechat")
    if isinstance(package.get("xiaohongshu"), dict):
        platforms.append("xiaohongshu")
    return tuple(platforms)


def risk_and_reasons(quality_score: float, publish_status: str, source_ids: tuple[str, ...], evidence_ids: tuple[str, ...]) -> tuple[str, tuple[str, ...]]:
    reasons: list[str] = []
    if quality_score < 65:
        reasons.append("Quality score below 65.")
    elif quality_score < 80:
        reasons.append("Quality score between 65 and 79.")
    if publish_status == "HOLD":
        reasons.append("Publish status is HOLD.")
    if not source_ids:
        reasons.append("No source_ids attached.")
    if not evidence_ids:
        reasons.append("No evidence_ids attached.")
    if len(evidence_ids) < 2:
        reasons.append("Evidence count below 2.")

    if publish_status == "HOLD" or quality_score < 65 or not source_ids or not evidence_ids:
        return "HIGH", tuple(reasons)
    if quality_score < 80 or len(evidence_ids) < 2:
        return "MEDIUM", tuple(reasons)
    return "LOW", tuple(reasons or ["Quality score >= 80 and evidence count >= 2."])


def priority_for(brief: dict[str, Any], risk_level: str) -> str:
    priority = str(brief.get("editorial_priority") or "")
    if priority in {"HIGH", "MEDIUM", "LOW"}:
        return priority
    if risk_level == "HIGH":
        return "HIGH"
    if risk_level == "MEDIUM":
        return "MEDIUM"
    return "LOW"


def build_item(package: dict[str, Any], review: dict[str, Any], brief: dict[str, Any], draft: dict[str, Any], run_date: str) -> AgentReviewQueueItem:
    package_id = str(package.get("package_id") or "")
    draft_id = str(package.get("draft_id") or "")
    brief_id = str(package.get("brief_id") or "")
    quality_score = safe_float(review.get("total_score"))
    publish_status = str(package.get("publish_status") or "NOT_READY")
    source_ids = tuple(str(item) for item in review.get("source_ids", []) if item)
    evidence_ids = tuple(str(item) for item in review.get("evidence_ids", []) if item)
    risk_level, reasons = risk_and_reasons(quality_score, publish_status, source_ids, evidence_ids)
    return AgentReviewQueueItem(
        schema_version=SCHEMA_VERSION,
        review_item_id=make_id("review", run_date, package_id, draft_id),
        run_date=run_date,
        package_id=package_id,
        draft_id=draft_id,
        brief_id=brief_id,
        title=str((package.get("wechat") or {}).get("title") or draft.get("recommended_title") or review.get("title") or ""),
        theme=str(brief.get("theme") or review.get("title") or ""),
        content_type=str(draft.get("content_type") or brief.get("content_type") or "unknown"),
        target_platforms=target_platforms(package),
        quality_status=str(review.get("quality_status") or package.get("quality_status") or "UNKNOWN"),
        quality_score=round(quality_score, 2),
        publish_status=publish_status,
        source_ids=source_ids,
        evidence_ids=evidence_ids,
        agent_review_status="PENDING_AGENT_REVIEW",
        risk_level=risk_level,
        priority=priority_for(brief, risk_level),
        human_review_required=risk_level == "HIGH",
        reasons=reasons,
    )


def build_agent_review_queue_report(paths: ProjectPaths, run_date: str | None = None) -> AgentReviewQueueReport:
    package_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_platform_packages.json")
    raw_packages = package_payload.get("packages")
    packages = [item for item in raw_packages if isinstance(item, dict)] if isinstance(raw_packages, list) else []
    reviews = load_reviews(paths)
    briefs = load_briefs(paths)
    drafts = load_drafts(paths)
    final_run_date = normalize_date(run_date or package_payload.get("run_date"))
    warnings: list[str] = []
    if not packages:
        warnings.append("No platform packages available for agent review queue.")

    items = tuple(
        build_item(
            package,
            reviews.get(str(package.get("draft_id")), {}),
            briefs.get(str(package.get("brief_id")), {}),
            drafts.get(str(package.get("draft_id")), {}),
            final_run_date,
        )
        for package in packages
    )
    risk_counts: dict[str, int] = {}
    priority_counts: dict[str, int] = {}
    for item in items:
        risk_counts[item.risk_level] = risk_counts.get(item.risk_level, 0) + 1
        priority_counts[item.priority] = priority_counts.get(item.priority, 0) + 1
    return AgentReviewQueueReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        item_count=len(items),
        risk_distribution=dict(sorted(risk_counts.items())),
        priority_distribution=dict(sorted(priority_counts.items())),
        items=items,
        warnings=tuple(warnings),
    )


def report_to_dict(report: AgentReviewQueueReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: AgentReviewQueueReport) -> str:
    rows = []
    for idx, item in enumerate(report.items, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(idx),
                    item.priority,
                    item.risk_level,
                    item.quality_status,
                    f"{item.quality_score:.2f}",
                    item.publish_status,
                    escape_cell(item.title),
                ]
            )
            + " |"
        )
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Agent Review Queue v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Review items: `{report.item_count}`
- Risk distribution: `{report.risk_distribution}`
- Priority distribution: `{report.priority_distribution}`

## Queue

| # | Priority | Risk | Quality | Score | Publish | Title |
|---:|---|---|---|---:|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | 0 | - | None |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "06_review_queue"
    return {
        "dated_json": root / f"{run_date}__agent-review-queue.json",
        "dated_md": root / f"{run_date}__agent-review-queue.md",
        "latest_json": root / "latest_agent_review_queue.json",
        "latest_md": root / "latest_agent_review_queue.md",
    }


def write_agent_review_queue_report(report: AgentReviewQueueReport, paths: ProjectPaths) -> dict[str, Path]:
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
