"""Rule-based content quality review v1."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"
OVERCLAIM_TERMS = ("保证", "必然", "一定", "绝对", "100%", "必定", "guarantee", "certainly", "always")


@dataclass(frozen=True)
class DraftQualityReview:
    schema_version: str
    draft_id: str
    brief_id: str
    run_date: str
    title: str
    total_score: float
    quality_status: str
    dimensions: dict[str, float]
    issues: tuple[str, ...]
    recommended_next_step: str
    source_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class ContentQualityReviewReport:
    schema_version: str
    generated_at: str
    run_date: str
    review_count: int
    status_counts: dict[str, int]
    reviews: tuple[DraftQualityReview, ...]
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


def body_text(draft: dict[str, Any], platform: str = "wechat_draft") -> str:
    payload = draft.get(platform)
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("body_markdown") or "")


def title_text(draft: dict[str, Any]) -> str:
    return str(draft.get("recommended_title") or (draft.get("wechat_draft") or {}).get("title") or "")


def word_count(text: str) -> int:
    return len([item for item in re.split(r"\s+", text) if item.strip()])


def has_risk_disclosure(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in ("风险", "risk", "人工", "human review", "证据不足"))


def overclaim_terms(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in OVERCLAIM_TERMS if term.lower() in lowered]


def status_for(score: float) -> str:
    if score >= 80:
        return "READY_FOR_HUMAN_REVIEW"
    if score >= 65:
        return "NEEDS_LIGHT_EDIT"
    if score >= 50:
        return "NEEDS_MAJOR_EDIT"
    return "HOLD"


def next_step_for(status: str) -> str:
    return {
        "READY_FOR_HUMAN_REVIEW": "Send to human editor for factual and tone review.",
        "NEEDS_LIGHT_EDIT": "Human editor should tighten title, evidence wording, and platform fit.",
        "NEEDS_MAJOR_EDIT": "Revise structure and evidence before packaging for review.",
        "HOLD": "Do not package for publication until evidence and structure are repaired.",
    }.get(status, "Human review required.")


def review_draft(draft: dict[str, Any], run_date: str) -> DraftQualityReview:
    title = title_text(draft)
    wechat_body = body_text(draft, "wechat_draft")
    xhs_body = body_text(draft, "xiaohongshu_draft")
    combined = f"{title}\n{wechat_body}\n{xhs_body}"
    evidence_ids = tuple(str(item) for item in draft.get("evidence_ids", []) if item)
    source_ids = tuple(str(item) for item in draft.get("source_ids", []) if item)
    issues: list[str] = []

    evidence_count = len(evidence_ids)
    if evidence_count < 2:
        issues.append("Evidence count is below 2.")
    if not has_risk_disclosure(combined):
        issues.append("Risk disclosure is missing.")
    if not title.strip():
        issues.append("Title is empty.")
    if word_count(wechat_body) < 120:
        issues.append("WeChat draft body is too short.")
    if not source_ids:
        issues.append("No source_id attached.")
    if not evidence_ids:
        issues.append("No evidence_id attached.")
    claims = overclaim_terms(combined)
    if claims:
        issues.append("Contains over-strong wording: " + ", ".join(claims))

    dimensions = {
        "brief_completeness": 90.0 if draft.get("brief_id") and title else 55.0,
        "evidence_count": min(100.0, 40.0 + evidence_count * 20.0),
        "claim_clarity": 85.0 if title and "核心判断" in wechat_body else 60.0,
        "structure_completeness": 90.0 if all(marker in wechat_body for marker in ("核心判断", "为什么现在重要", "证据", "风险")) else 55.0,
        "platform_fit": 85.0 if xhs_body and (draft.get("xiaohongshu_draft") or {}).get("tags") else 60.0,
        "risk_disclosure": 90.0 if has_risk_disclosure(combined) else 35.0,
        "human_editing_need": 70.0 if "Rule-based draft" in str(draft.get("disclaimer") or "") else 45.0,
    }
    score = round(sum(dimensions.values()) / len(dimensions), 2)
    penalty = min(len(issues) * 4.0, 25.0)
    score = max(0.0, round(score - penalty, 2))
    status = status_for(score)

    return DraftQualityReview(
        schema_version=SCHEMA_VERSION,
        draft_id=str(draft.get("draft_id") or ""),
        brief_id=str(draft.get("brief_id") or ""),
        run_date=run_date,
        title=title,
        total_score=score,
        quality_status=status,
        dimensions={key: round(value, 2) for key, value in dimensions.items()},
        issues=tuple(issues),
        recommended_next_step=next_step_for(status),
        source_ids=source_ids,
        evidence_ids=evidence_ids,
    )


def build_content_quality_report(paths: ProjectPaths, run_date: str | None = None) -> ContentQualityReviewReport:
    input_path = paths.market_content_root / "05_draft_packs" / "latest_content_drafts.json"
    payload = read_json(input_path)
    final_run_date = normalize_date(run_date or payload.get("run_date"))
    raw_drafts = payload.get("drafts")
    drafts = [item for item in raw_drafts if isinstance(item, dict)] if isinstance(raw_drafts, list) else []
    warnings: list[str] = []
    if not input_path.exists():
        warnings.append("latest_content_drafts.json not found; run make content-drafts first.")
    if not drafts:
        warnings.append("No content drafts available for quality review.")
    reviews = tuple(review_draft(draft, final_run_date) for draft in drafts)
    status_counts: dict[str, int] = {}
    for review in reviews:
        status_counts[review.quality_status] = status_counts.get(review.quality_status, 0) + 1
    return ContentQualityReviewReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        review_count=len(reviews),
        status_counts=dict(sorted(status_counts.items())),
        reviews=reviews,
        warnings=tuple(warnings),
    )


def report_to_dict(report: ContentQualityReviewReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: ContentQualityReviewReport) -> str:
    rows = []
    for index, review in enumerate(report.reviews, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    escape_cell(review.quality_status),
                    f"{review.total_score:.2f}",
                    escape_cell(review.title),
                    str(len(review.evidence_ids)),
                    str(len(review.issues)),
                ]
            )
            + " |"
        )
    status_lines = "\n".join(f"- `{key}`: {value}" for key, value in report.status_counts.items()) or "- None"
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Content Quality Review v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Reviews: `{report.review_count}`

## Status Counts

{status_lines}

## Reviews

| # | Status | Score | Title | Evidence IDs | Issues |
|---:|---|---:|---|---:|---:|
{chr(10).join(rows) if rows else '| 0 | - | 0 | None | 0 | 0 |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__content-quality-review.json",
        "dated_md": root / f"{run_date}__content-quality-review.md",
        "latest_json": root / "latest_content_quality_review.json",
        "latest_md": root / "latest_content_quality_review.md",
    }


def write_content_quality_report(report: ContentQualityReviewReport, paths: ProjectPaths) -> dict[str, Path]:
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
