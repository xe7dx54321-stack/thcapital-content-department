"""Platform Packaging v1."""

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
class PlatformPackage:
    schema_version: str
    package_id: str
    draft_id: str
    brief_id: str
    quality_status: str
    wechat: dict[str, Any]
    xiaohongshu: dict[str, Any]
    publish_status: str
    human_review_required: bool


@dataclass(frozen=True)
class PlatformPackageReport:
    schema_version: str
    generated_at: str
    run_date: str
    package_count: int
    blocked_count: int
    packages: tuple[PlatformPackage, ...]
    blocked: tuple[dict[str, Any], ...]
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


def make_package_id(run_date: str, draft_id: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{draft_id}".encode("utf-8")).hexdigest()[:12]
    return f"pkg_{run_date}_{digest}"


def reviews_by_draft(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_content_quality_review.json")
    reviews = payload.get("reviews")
    if not isinstance(reviews, list):
        return {}
    return {str(item.get("draft_id")): item for item in reviews if isinstance(item, dict)}


def publish_status_for(quality_status: str) -> str:
    if quality_status in {"READY_FOR_HUMAN_REVIEW", "NEEDS_LIGHT_EDIT"}:
        return "READY_FOR_HUMAN_REVIEW"
    if quality_status == "NEEDS_MAJOR_EDIT":
        return "NOT_READY"
    return "HOLD"


def editor_checklist(quality_status: str) -> list[str]:
    checklist = [
        "Verify every factual claim against supporting evidence.",
        "Check title does not overpromise.",
        "Confirm risk disclosure is visible.",
        "Human editor approval required before publication.",
    ]
    if quality_status != "READY_FOR_HUMAN_REVIEW":
        checklist.insert(0, f"Resolve quality status: {quality_status}.")
    return checklist


def image_brief(draft: dict[str, Any]) -> list[str]:
    title = str(draft.get("recommended_title") or "AI/Agent signal")
    return [
        f"Cover image should communicate: {title[:80]}",
        "Use clean tech/business visual language; avoid implying unverified claims.",
    ]


def build_package(draft: dict[str, Any], review: dict[str, Any], run_date: str) -> PlatformPackage:
    draft_id = str(draft.get("draft_id") or "")
    quality_status = str(review.get("quality_status") or "HOLD")
    wechat_draft = draft.get("wechat_draft") if isinstance(draft.get("wechat_draft"), dict) else {}
    xhs_draft = draft.get("xiaohongshu_draft") if isinstance(draft.get("xiaohongshu_draft"), dict) else {}
    return PlatformPackage(
        schema_version=SCHEMA_VERSION,
        package_id=make_package_id(run_date, draft_id),
        draft_id=draft_id,
        brief_id=str(draft.get("brief_id") or ""),
        quality_status=quality_status,
        wechat={
            "title": wechat_draft.get("title") or draft.get("recommended_title") or "",
            "body_markdown": wechat_draft.get("body_markdown") or "",
            "editor_checklist": editor_checklist(quality_status),
        },
        xiaohongshu={
            "title": xhs_draft.get("title") or draft.get("recommended_title") or "",
            "body_markdown": xhs_draft.get("body_markdown") or "",
            "tags": xhs_draft.get("tags") or [],
            "image_brief": image_brief(draft),
        },
        publish_status=publish_status_for(quality_status),
        human_review_required=True,
    )


def build_platform_package_report(paths: ProjectPaths, run_date: str | None = None) -> PlatformPackageReport:
    input_path = paths.market_content_root / "05_draft_packs" / "latest_content_drafts.json"
    review_path = paths.market_content_root / "05_draft_packs" / "latest_content_quality_review.json"
    payload = read_json(input_path)
    review_payload = read_json(review_path)
    final_run_date = normalize_date(run_date or payload.get("run_date") or review_payload.get("run_date"))
    raw_drafts = payload.get("drafts")
    drafts = [item for item in raw_drafts if isinstance(item, dict)] if isinstance(raw_drafts, list) else []
    reviews = reviews_by_draft(paths)
    warnings: list[str] = []
    if not input_path.exists():
        warnings.append("latest_content_drafts.json not found; run make content-drafts first.")
    if not review_path.exists():
        warnings.append("latest_content_quality_review.json not found; run make content-quality-review first.")
    if not drafts:
        warnings.append("No content drafts available for platform packaging.")

    packages: list[PlatformPackage] = []
    blocked: list[dict[str, Any]] = []
    for draft in drafts:
        review = reviews.get(str(draft.get("draft_id")), {})
        quality_status = str(review.get("quality_status") or "HOLD")
        if quality_status == "HOLD":
            blocked.append(
                {
                    "draft_id": draft.get("draft_id"),
                    "brief_id": draft.get("brief_id"),
                    "title": draft.get("recommended_title"),
                    "blocked_reason": "Quality status is HOLD.",
                    "issues": review.get("issues", []),
                }
            )
            continue
        packages.append(build_package(draft, review, final_run_date))

    return PlatformPackageReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        package_count=len(packages),
        blocked_count=len(blocked),
        packages=tuple(packages),
        blocked=tuple(blocked),
        warnings=tuple(warnings),
    )


def report_to_dict(report: PlatformPackageReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: PlatformPackageReport) -> str:
    rows = []
    for index, package in enumerate(report.packages, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    escape_cell(package.publish_status),
                    escape_cell(package.quality_status),
                    escape_cell(package.wechat.get("title", "")),
                    str(package.human_review_required),
                ]
            )
            + " |"
        )
    blocked = "\n".join(
        f"- `{item.get('draft_id')}` {item.get('title')}：{item.get('blocked_reason')}"
        for item in report.blocked
    ) or "- None"
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Platform Packages v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Packages: `{report.package_count}`
- Blocked: `{report.blocked_count}`

## Packages

| # | Publish Status | Quality Status | WeChat Title | Human Review |
|---:|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | None | true |'}

## Blocked

{blocked}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__platform-packages.json",
        "dated_md": root / f"{run_date}__platform-packages.md",
        "latest_json": root / "latest_platform_packages.json",
        "latest_md": root / "latest_platform_packages.md",
    }


def write_platform_package_report(report: PlatformPackageReport, paths: ProjectPaths) -> dict[str, Path]:
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
