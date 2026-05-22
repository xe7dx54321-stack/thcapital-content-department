"""Rule-based Draft Writer v1."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"
DISCLAIMER = "Rule-based draft. Requires human editing before publication."


@dataclass(frozen=True)
class PlatformDraft:
    title: str
    body_markdown: str
    word_count_estimate: int | None = None
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class ContentDraft:
    schema_version: str
    draft_id: str
    outline_id: str
    brief_id: str
    run_date: str
    recommended_title: str
    content_type: str
    wechat_draft: PlatformDraft
    xiaohongshu_draft: PlatformDraft
    disclaimer: str
    source_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class ContentDraftReport:
    schema_version: str
    generated_at: str
    run_date: str
    draft_count: int
    drafts: tuple[ContentDraft, ...]
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


def make_draft_id(run_date: str, outline_id: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{outline_id}".encode("utf-8")).hexdigest()[:12]
    return f"draft_{run_date}_{digest}"


def word_count(text: str) -> int:
    return len([item for item in text.replace("\n", " ").split(" ") if item.strip()])


def brief_by_id(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_content_briefs.json")
    briefs = payload.get("briefs")
    if not isinstance(briefs, list):
        return {}
    return {str(item.get("brief_id")): item for item in briefs if isinstance(item, dict)}


def evidence_lines(evidence: list[dict[str, Any]]) -> str:
    if not evidence:
        return "- 证据不足：当前没有可展开的 supporting evidence。"
    lines = []
    for item in evidence[:5]:
        title = item.get("title") or item.get("evidence_id") or "Untitled evidence"
        url = item.get("url") or "no url"
        source = item.get("source_id") or "unknown_source"
        lines.append(f"- `{source}` {title} ({url})")
    if len(evidence) < 2:
        lines.append("- 证据不足：少于 2 条独立 evidence，发布前必须人工补充。")
    return "\n".join(lines)


def section_bullets(sections: list[dict[str, Any]], section_name: str) -> list[str]:
    for section in sections:
        if section.get("section") == section_name:
            bullets = section.get("bullets")
            if isinstance(bullets, list):
                return [str(item) for item in bullets if item]
    return []


def build_wechat_body(outline: dict[str, Any], brief: dict[str, Any]) -> str:
    title = outline.get("recommended_title") or brief.get("title") or "未命名选题"
    structure = outline.get("structure") if isinstance(outline.get("structure"), list) else []
    evidence = brief.get("supporting_evidence") if isinstance(brief.get("supporting_evidence"), list) else []
    risks = brief.get("risks") if isinstance(brief.get("risks"), list) else []
    missing = brief.get("missing_info") if isinstance(brief.get("missing_info"), list) else []

    return f"""# {title}

## 核心判断

{brief.get('core_claim') or '这是一个需要人工继续判断的 AI/Agent 选题。'}

## 为什么现在重要

{brief.get('why_now') or '当前已有候选池信号，适合进入人工编辑前的结构化准备。'}

## 关键事实

{chr(10).join(f'- {item}' for item in section_bullets(structure, 'facts')) or '- 待补充。'}

## 证据

{evidence_lines(evidence)}

## 机会与风险

{chr(10).join(f'- {item}' for item in (risks or ['Rule-based draft; requires human review before publication.']))}

## 证据缺口

{chr(10).join(f'- {item}' for item in missing) if missing else '- 暂无显式缺口，但仍需人工核验来源与上下文。'}

## 人工编辑提示

- 这是一份规则模板初稿，不是可直接发布的终稿。
- 发布前请检查事实、语气、标题承诺和证据链接。
"""


def xhs_tags(brief: dict[str, Any]) -> tuple[str, ...]:
    tags = ["AI", "Agent", "人工智能"]
    content_type = str(brief.get("content_type") or "")
    if content_type == "deep_analysis":
        tags.append("深度分析")
    elif content_type in {"short_post", "quick_take"}:
        tags.append("科技快讯")
    for source in brief.get("source_ids", [])[:2]:
        if source:
            tags.append(str(source).replace("__", "_"))
    return tuple(dict.fromkeys(tags))


def build_xhs_body(outline: dict[str, Any], brief: dict[str, Any]) -> str:
    evidence = brief.get("supporting_evidence") if isinstance(brief.get("supporting_evidence"), list) else []
    angle = next(iter(brief.get("suggested_angles", []) or []), brief.get("core_claim") or brief.get("title") or "")
    evidence_summary = "\n".join(
        f"{idx}. {item.get('title') or item.get('evidence_id')}"
        for idx, item in enumerate(evidence[:3], start=1)
    ) or "1. 当前证据不足，先做观察。"
    return f"""# {outline.get('recommended_title') or brief.get('title') or 'AI/Agent 观察'}

一句话观点：{angle}

三个要点：

{evidence_summary}

为什么要关注：

{brief.get('why_it_matters') or '这个信号可能影响 AI/Agent 工具、企业采用和投资观察。'}

风险提示：

- 规则型草稿，需要人工核验后再发布。
- 如果证据少于 2 条，建议先作为观察笔记，不做强结论。

互动问题：你觉得这个变化会先影响开发者，还是企业客户？
"""


def build_draft(outline: dict[str, Any], brief: dict[str, Any], run_date: str) -> ContentDraft:
    outline_id = str(outline.get("outline_id") or "")
    title = str(outline.get("recommended_title") or brief.get("title") or "未命名选题")
    wechat_body = build_wechat_body(outline, brief)
    xhs_body = build_xhs_body(outline, brief)
    return ContentDraft(
        schema_version=SCHEMA_VERSION,
        draft_id=make_draft_id(run_date, outline_id),
        outline_id=outline_id,
        brief_id=str(outline.get("brief_id") or brief.get("brief_id") or ""),
        run_date=run_date,
        recommended_title=title,
        content_type=str(outline.get("content_type") or brief.get("content_type") or "monitor_note"),
        wechat_draft=PlatformDraft(title=title, body_markdown=wechat_body, word_count_estimate=word_count(wechat_body)),
        xiaohongshu_draft=PlatformDraft(title=title[:48], body_markdown=xhs_body, tags=xhs_tags(brief)),
        disclaimer=DISCLAIMER,
        source_ids=tuple(str(item) for item in (outline.get("source_ids") or brief.get("source_ids") or []) if item),
        evidence_ids=tuple(str(item) for item in (outline.get("evidence_ids") or brief.get("evidence_ids") or []) if item),
    )


def build_content_draft_report(paths: ProjectPaths, run_date: str | None = None) -> ContentDraftReport:
    input_path = paths.market_content_root / "05_draft_packs" / "latest_content_outlines.json"
    payload = read_json(input_path)
    final_run_date = normalize_date(run_date or payload.get("run_date"))
    raw_outlines = payload.get("outlines")
    outlines = [item for item in raw_outlines if isinstance(item, dict)] if isinstance(raw_outlines, list) else []
    briefs = brief_by_id(paths)
    warnings: list[str] = []
    if not input_path.exists():
        warnings.append("latest_content_outlines.json not found; run make content-outlines first.")
    if not outlines:
        warnings.append("No content outlines available for draft generation.")
    drafts = []
    for outline in outlines:
        brief = briefs.get(str(outline.get("brief_id")), {})
        drafts.append(build_draft(outline, brief, final_run_date))
    return ContentDraftReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        draft_count=len(drafts),
        drafts=tuple(drafts),
        warnings=tuple(warnings),
    )


def report_to_dict(report: ContentDraftReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: ContentDraftReport) -> str:
    rows = []
    for index, draft in enumerate(report.drafts, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    escape_cell(draft.recommended_title),
                    escape_cell(draft.content_type),
                    str(draft.wechat_draft.word_count_estimate or 0),
                    str(len(draft.evidence_ids)),
                    escape_cell(", ".join(draft.source_ids)),
                ]
            )
            + " |"
        )
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Content Drafts v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Drafts: `{report.draft_count}`

## Drafts

| # | Title | Type | WeChat Words | Evidence IDs | Sources |
|---:|---|---|---:|---:|---|
{chr(10).join(rows) if rows else '| 0 | None | - | 0 | 0 | - |'}

## Warnings

{warnings}

## Disclaimer

{DISCLAIMER}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__content-drafts.json",
        "dated_md": root / f"{run_date}__content-drafts.md",
        "latest_json": root / "latest_content_drafts.json",
        "latest_md": root / "latest_content_drafts.md",
    }


def write_content_draft_report(report: ContentDraftReport, paths: ProjectPaths) -> dict[str, Path]:
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
