"""Rule-based proponent editor review simulation."""

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
class ProponentReview:
    schema_version: str
    proponent_review_id: str
    review_item_id: str
    package_id: str
    run_date: str
    agent_role: str
    support_level: str
    publish_argument: str
    core_value: str
    target_reader: str
    strongest_points: tuple[str, ...]
    recommended_platforms: tuple[str, ...]
    suggested_title_angle: str
    why_now: str
    confidence: float
    notes: tuple[str, ...]


@dataclass(frozen=True)
class ProponentReviewReport:
    schema_version: str
    generated_at: str
    run_date: str
    review_count: int
    reviews: tuple[ProponentReview, ...]
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


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def make_id(prefix: str, run_date: str, *parts: str) -> str:
    digest = hashlib.sha1("|".join((run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def load_briefs(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_content_briefs.json")
    raw = payload.get("briefs")
    if not isinstance(raw, list):
        return {}
    return {str(item.get("brief_id")): item for item in raw if isinstance(item, dict)}


def support_level(score: float, priority: str, evidence_count: int) -> str:
    if score >= 80 or (priority == "HIGH" and evidence_count >= 2):
        return "STRONG"
    if score >= 65:
        return "MODERATE"
    return "WEAK"


def confidence(score: float, evidence_count: int, source_count: int) -> float:
    value = 0.35 + min(score, 100) / 200 + min(evidence_count, 3) * 0.06 + min(source_count, 3) * 0.04
    return round(min(value, 0.95), 2)


def build_review(item: dict[str, Any], brief: dict[str, Any], run_date: str) -> ProponentReview:
    score = safe_float(item.get("quality_score"))
    evidence_count = len(item.get("evidence_ids", []) or [])
    source_count = len(item.get("source_ids", []) or [])
    level = support_level(score, str(item.get("priority")), evidence_count)
    title = str(item.get("title") or brief.get("title") or "")
    strongest = [
        f"Quality score is {score:.2f}.",
        f"Evidence count is {evidence_count}.",
        str(brief.get("why_it_matters") or "Topic has AI/Agent editorial relevance."),
    ]
    if item.get("priority") == "HIGH":
        strongest.append("Editorial priority is HIGH.")
    return ProponentReview(
        schema_version=SCHEMA_VERSION,
        proponent_review_id=make_id("prop", run_date, str(item.get("review_item_id") or "")),
        review_item_id=str(item.get("review_item_id") or ""),
        package_id=str(item.get("package_id") or ""),
        run_date=run_date,
        agent_role="proponent_editor",
        support_level=level,
        publish_argument=f"Rule-based proponent agent simulation: {title} is worth advancing because it has {evidence_count} evidence item(s), {source_count} source(s), and quality score {score:.2f}.",
        core_value=str(brief.get("core_claim") or item.get("theme") or title),
        target_reader=str(brief.get("audience") or "AI/Agent builders and investors"),
        strongest_points=tuple(strongest),
        recommended_platforms=tuple(str(platform) for platform in item.get("target_platforms", []) if platform),
        suggested_title_angle=f"{title}：为什么现在值得关注",
        why_now=str(brief.get("why_now") or "The item is already in the Phase 2 platform package queue."),
        confidence=confidence(score, evidence_count, source_count),
        notes=("Rule-based proponent agent simulation.",),
    )


def build_proponent_review_report(paths: ProjectPaths) -> ProponentReviewReport:
    queue = read_json(paths.market_content_root / "06_review_queue" / "latest_agent_review_queue.json")
    raw_items = queue.get("items")
    items = [item for item in raw_items if isinstance(item, dict)] if isinstance(raw_items, list) else []
    briefs = load_briefs(paths)
    run_date = str(queue.get("run_date") or datetime.now().strftime("%Y%m%d")).replace("-", "")[:8]
    warnings = [] if items else ["No agent review queue items available."]
    reviews = tuple(build_review(item, briefs.get(str(item.get("brief_id")), {}), run_date) for item in items)
    return ProponentReviewReport(SCHEMA_VERSION, utc_now(), run_date, len(reviews), reviews, tuple(warnings))


def report_to_dict(report: ProponentReviewReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: ProponentReviewReport) -> str:
    rows = [
        f"| {idx} | {review.support_level} | {review.confidence:.2f} | {review.package_id} | {escape_cell(review.suggested_title_angle)} |"
        for idx, review in enumerate(report.reviews, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Proponent Reviews v1

> Rule-based proponent agent simulation.

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Reviews: `{report.review_count}`

## Reviews

| # | Support | Confidence | Package | Suggested Title Angle |
|---:|---|---:|---|---|
{chr(10).join(rows) if rows else '| 0 | - | 0 | - | None |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "06_review_queue"
    return {
        "dated_json": root / f"{run_date}__proponent-reviews.json",
        "dated_md": root / f"{run_date}__proponent-reviews.md",
        "latest_json": root / "latest_proponent_reviews.json",
        "latest_md": root / "latest_proponent_reviews.md",
    }


def write_proponent_review_report(report: ProponentReviewReport, paths: ProjectPaths) -> dict[str, Path]:
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
