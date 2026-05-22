"""Rule-based critical senior editor review simulation."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"
OVERCLAIM_TERMS = ("必然", "一定", "保证", "确定", "绝对", "100%", "guarantee", "always")


@dataclass(frozen=True)
class CriticReview:
    schema_version: str
    critic_review_id: str
    review_item_id: str
    package_id: str
    run_date: str
    agent_role: str
    severity: str
    main_concerns: tuple[str, ...]
    evidence_concerns: tuple[str, ...]
    logic_concerns: tuple[str, ...]
    title_concerns: tuple[str, ...]
    platform_fit_concerns: tuple[str, ...]
    risk_concerns: tuple[str, ...]
    constructive_suggestions: tuple[str, ...]
    must_fix_before_publish: tuple[str, ...]
    confidence: float


@dataclass(frozen=True)
class CriticReviewReport:
    schema_version: str
    generated_at: str
    run_date: str
    review_count: int
    severity_distribution: dict[str, int]
    reviews: tuple[CriticReview, ...]
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


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def load_reviews(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_content_quality_review.json")
    raw = payload.get("reviews")
    if not isinstance(raw, list):
        return {}
    return {str(item.get("draft_id")): item for item in raw if isinstance(item, dict)}


def load_packages(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_platform_packages.json")
    raw = payload.get("packages")
    if not isinstance(raw, list):
        return {}
    return {str(item.get("package_id")): item for item in raw if isinstance(item, dict)}


def body_text(package: dict[str, Any], key: str) -> str:
    payload = package.get(key)
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("body_markdown") or "")


def title_text(package: dict[str, Any], item: dict[str, Any]) -> str:
    wechat = package.get("wechat") if isinstance(package.get("wechat"), dict) else {}
    return str(wechat.get("title") or item.get("title") or "")


def contains_overclaim(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in OVERCLAIM_TERMS if term.lower() in lowered]


def severity_for(must_fix_count: int, quality_score: float, publish_status: str) -> str:
    if publish_status != "READY_FOR_HUMAN_REVIEW" or quality_score < 65 or must_fix_count >= 3:
        return "HIGH"
    if quality_score < 80 or must_fix_count:
        return "MEDIUM"
    return "LOW"


def confidence(severity: str, concern_count: int) -> float:
    base = {"LOW": 0.70, "MEDIUM": 0.78, "HIGH": 0.86}[severity]
    return round(min(0.95, base + min(concern_count, 5) * 0.02), 2)


def build_review(item: dict[str, Any], quality: dict[str, Any], package: dict[str, Any], run_date: str) -> CriticReview:
    title = title_text(package, item)
    wechat_body = body_text(package, "wechat")
    xhs_body = body_text(package, "xiaohongshu")
    evidence_ids = item.get("evidence_ids") or quality.get("evidence_ids") or []
    source_ids = item.get("source_ids") or quality.get("source_ids") or []
    quality_score = safe_float(item.get("quality_score") or quality.get("total_score"))
    publish_status = str(item.get("publish_status") or package.get("publish_status") or "NOT_READY")

    evidence_concerns: list[str] = []
    logic_concerns: list[str] = []
    title_concerns: list[str] = []
    platform_fit_concerns: list[str] = []
    risk_concerns: list[str] = []
    must_fix: list[str] = []

    if len(evidence_ids) < 2:
        evidence_concerns.append("Evidence count is below 2; add independent evidence or downgrade claim strength.")
        must_fix.append("Add at least one more independent evidence item or mark as observation.")
    if not source_ids:
        evidence_concerns.append("No source_ids attached.")
        must_fix.append("Attach source_ids before publish review.")
    if quality_score < 80:
        logic_concerns.append(f"Quality score is {quality_score:.2f}, below the 80 human-review-ready bar.")
    if not title or len(title) < 12:
        title_concerns.append("Title is empty or too generic.")
        must_fix.append("Rewrite title with a concrete subject and claim.")
    if len(wechat_body) < 500:
        platform_fit_concerns.append("WeChat body is short; may read as a note rather than an article.")
    if not (package.get("xiaohongshu") or {}).get("tags"):
        platform_fit_concerns.append("Xiaohongshu package has no tags.")
    if "##" not in wechat_body:
        platform_fit_concerns.append("WeChat body lacks visible section structure.")
    if "风险" not in wechat_body and "risk" not in wechat_body.lower():
        risk_concerns.append("Risk disclosure is missing.")
        must_fix.append("Add explicit risk disclosure.")
    overclaims = contains_overclaim(f"{title}\n{wechat_body}\n{xhs_body}")
    if overclaims:
        risk_concerns.append("Over-strong wording detected: " + ", ".join(overclaims))
        must_fix.append("Replace over-strong wording with evidence-bounded language.")
    if publish_status != "READY_FOR_HUMAN_REVIEW":
        main = [f"Publish status is {publish_status}; do not advance without revision."]
    else:
        main = ["No blocking publish-status issue; review evidence and platform fit."]

    concern_count = sum(len(items) for items in (evidence_concerns, logic_concerns, title_concerns, platform_fit_concerns, risk_concerns))
    severity = severity_for(len(must_fix), quality_score, publish_status)
    suggestions = [
        "Tighten the opening to separate facts from interpretation.",
        "Keep risk disclosure visible near the end.",
        "Add a human editor note if evidence remains thin.",
    ]
    return CriticReview(
        schema_version=SCHEMA_VERSION,
        critic_review_id=make_id("crit", run_date, str(item.get("review_item_id") or "")),
        review_item_id=str(item.get("review_item_id") or ""),
        package_id=str(item.get("package_id") or ""),
        run_date=run_date,
        agent_role="critical_senior_editor",
        severity=severity,
        main_concerns=tuple(main),
        evidence_concerns=tuple(evidence_concerns),
        logic_concerns=tuple(logic_concerns),
        title_concerns=tuple(title_concerns),
        platform_fit_concerns=tuple(platform_fit_concerns),
        risk_concerns=tuple(risk_concerns),
        constructive_suggestions=tuple(suggestions),
        must_fix_before_publish=tuple(dict.fromkeys(must_fix)),
        confidence=confidence(severity, concern_count),
    )


def build_critic_review_report(paths: ProjectPaths) -> CriticReviewReport:
    queue = read_json(paths.market_content_root / "06_review_queue" / "latest_agent_review_queue.json")
    raw_items = queue.get("items")
    items = [item for item in raw_items if isinstance(item, dict)] if isinstance(raw_items, list) else []
    qualities = load_reviews(paths)
    packages = load_packages(paths)
    run_date = str(queue.get("run_date") or datetime.now().strftime("%Y%m%d")).replace("-", "")[:8]
    reviews = tuple(
        build_review(
            item,
            qualities.get(str(item.get("draft_id")), {}),
            packages.get(str(item.get("package_id")), {}),
            run_date,
        )
        for item in items
    )
    distribution: dict[str, int] = {}
    for review in reviews:
        distribution[review.severity] = distribution.get(review.severity, 0) + 1
    warnings = () if items else ("No agent review queue items available.",)
    return CriticReviewReport(SCHEMA_VERSION, utc_now(), run_date, len(reviews), dict(sorted(distribution.items())), reviews, warnings)


def report_to_dict(report: CriticReviewReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: CriticReviewReport) -> str:
    rows = [
        f"| {idx} | {review.severity} | {review.confidence:.2f} | {review.package_id} | {len(review.must_fix_before_publish)} |"
        for idx, review in enumerate(report.reviews, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Critic Reviews v1

> Rule-based critical senior editor simulation.

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Reviews: `{report.review_count}`
- Severity distribution: `{report.severity_distribution}`

## Reviews

| # | Severity | Confidence | Package | Must Fix Count |
|---:|---|---:|---|---:|
{chr(10).join(rows) if rows else '| 0 | - | 0 | - | 0 |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "06_review_queue"
    return {
        "dated_json": root / f"{run_date}__critic-reviews.json",
        "dated_md": root / f"{run_date}__critic-reviews.md",
        "latest_json": root / "latest_critic_reviews.json",
        "latest_md": root / "latest_critic_reviews.md",
    }


def write_critic_review_report(report: CriticReviewReport, paths: ProjectPaths) -> dict[str, Path]:
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
