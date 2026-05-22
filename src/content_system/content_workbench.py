"""Content Workbench Board v1."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class ContentWorkbenchReport:
    schema_version: str
    generated_at: str
    run_date: str
    summary: dict[str, int]
    ready_for_human_review: tuple[dict[str, Any], ...]
    needs_editing: tuple[dict[str, Any], ...]
    hold: tuple[dict[str, Any], ...]
    top_briefs: tuple[dict[str, Any], ...]
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


def compact_review(review: dict[str, Any]) -> dict[str, Any]:
    return {
        "draft_id": review.get("draft_id"),
        "brief_id": review.get("brief_id"),
        "title": review.get("title"),
        "quality_status": review.get("quality_status"),
        "total_score": review.get("total_score"),
        "issues": review.get("issues", []),
        "recommended_next_step": review.get("recommended_next_step"),
    }


def build_content_workbench_report(paths: ProjectPaths, run_date: str | None = None) -> ContentWorkbenchReport:
    root = paths.market_content_root / "05_draft_packs"
    briefs_payload = read_json(root / "latest_content_briefs.json")
    outlines_payload = read_json(root / "latest_content_outlines.json")
    drafts_payload = read_json(root / "latest_content_drafts.json")
    reviews_payload = read_json(root / "latest_content_quality_review.json")
    packages_payload = read_json(root / "latest_platform_packages.json")
    final_run_date = normalize_date(
        run_date
        or packages_payload.get("run_date")
        or reviews_payload.get("run_date")
        or drafts_payload.get("run_date")
        or briefs_payload.get("run_date")
    )

    briefs = [item for item in briefs_payload.get("briefs", []) if isinstance(item, dict)]
    outlines = [item for item in outlines_payload.get("outlines", []) if isinstance(item, dict)]
    drafts = [item for item in drafts_payload.get("drafts", []) if isinstance(item, dict)]
    reviews = [item for item in reviews_payload.get("reviews", []) if isinstance(item, dict)]
    packages = [item for item in packages_payload.get("packages", []) if isinstance(item, dict)]

    ready = [compact_review(item) for item in reviews if item.get("quality_status") == "READY_FOR_HUMAN_REVIEW"]
    needs = [
        compact_review(item)
        for item in reviews
        if item.get("quality_status") in {"NEEDS_LIGHT_EDIT", "NEEDS_MAJOR_EDIT"}
    ]
    hold = [compact_review(item) for item in reviews if item.get("quality_status") == "HOLD"]
    top_briefs = tuple(
        {
            "brief_id": item.get("brief_id"),
            "title": item.get("title"),
            "score": item.get("score"),
            "score_band": item.get("score_band"),
            "content_type": item.get("content_type"),
            "editorial_priority": item.get("editorial_priority"),
        }
        for item in sorted(briefs, key=lambda brief: float(brief.get("score") or 0), reverse=True)[:10]
    )

    warnings: list[str] = []
    if not briefs_payload:
        warnings.append("Content briefs are missing.")
    if not reviews_payload:
        warnings.append("Content quality review is missing.")
    if not packages_payload:
        warnings.append("Platform packages are missing.")

    return ContentWorkbenchReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        summary={
            "briefs": len(briefs),
            "outlines": len(outlines),
            "drafts": len(drafts),
            "packages": len(packages),
            "ready_for_human_review": len(ready),
            "needs_edit": len(needs),
            "hold": len(hold),
        },
        ready_for_human_review=tuple(ready),
        needs_editing=tuple(needs),
        hold=tuple(hold),
        top_briefs=top_briefs,
        warnings=tuple(warnings),
    )


def report_to_dict(report: ContentWorkbenchReport) -> dict[str, Any]:
    return asdict(report)


def item_lines(items: tuple[dict[str, Any], ...]) -> str:
    if not items:
        return "- None"
    return "\n".join(
        f"- `{item.get('draft_id') or item.get('brief_id')}` {item.get('title')} "
        f"({item.get('quality_status') or item.get('score_band')}; score={item.get('total_score') or item.get('score')})"
        for item in items
    )


def render_markdown(report: ContentWorkbenchReport) -> str:
    summary = report.summary
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Content Workbench

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Briefs: `{summary['briefs']}`
- Outlines: `{summary['outlines']}`
- Drafts: `{summary['drafts']}`
- Packages: `{summary['packages']}`
- Ready for human review: `{summary['ready_for_human_review']}`
- Needs edit: `{summary['needs_edit']}`
- Hold: `{summary['hold']}`

## Ready for Human Review

{item_lines(report.ready_for_human_review)}

## Needs Editing

{item_lines(report.needs_editing)}

## Hold

{item_lines(report.hold)}

## Top Briefs

{item_lines(report.top_briefs)}

## Next Actions

- 人工编辑优先处理 Ready for Human Review。
- Needs Editing 先修证据、标题和风险披露。
- Hold 不进入平台发布包，直到证据和结构问题修复。

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__content-workbench.json",
        "latest_json": paths.logs_root / "latest_content_workbench.json",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__content-workbench.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_content_workbench.md",
    }


def write_content_workbench_report(report: ContentWorkbenchReport, paths: ProjectPaths) -> dict[str, Path]:
    paths_by_name = output_paths(paths, report.run_date)
    for path in paths_by_name.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (paths_by_name["dated_json"], paths_by_name["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (paths_by_name["frontstage_dated_md"], paths_by_name["frontstage_latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return paths_by_name
