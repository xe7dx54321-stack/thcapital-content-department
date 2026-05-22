"""Content Outline Builder v1."""

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
class ContentOutline:
    schema_version: str
    outline_id: str
    brief_id: str
    run_date: str
    title_options: tuple[str, ...]
    recommended_title: str
    content_type: str
    target_platforms: tuple[str, ...]
    structure: tuple[dict[str, Any], ...]
    wechat_outline: tuple[dict[str, Any], ...]
    xiaohongshu_outline: tuple[dict[str, Any], ...]
    required_evidence: tuple[dict[str, Any], ...]
    editor_notes: tuple[str, ...]
    source_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class ContentOutlineReport:
    schema_version: str
    generated_at: str
    run_date: str
    outline_count: int
    outlines: tuple[ContentOutline, ...]
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


def make_outline_id(run_date: str, brief_id: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{brief_id}".encode("utf-8")).hexdigest()[:12]
    return f"outline_{run_date}_{digest}"


def title_options(brief: dict[str, Any]) -> tuple[str, ...]:
    theme = str(brief.get("theme") or brief.get("title") or "AI/Agent 新信号")
    score_band = str(brief.get("score_band") or "D")
    options = [
        theme,
        f"{theme}：为什么值得关注",
        f"一个 {score_band} 级 AI/Agent 信号：{theme}",
    ]
    return tuple(dict.fromkeys(options))


def base_structure(brief: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    evidence = brief.get("supporting_evidence") if isinstance(brief.get("supporting_evidence"), list) else []
    risks = brief.get("risks") if isinstance(brief.get("risks"), list) else []
    return (
        {
            "section": "hook",
            "heading": "发生了什么",
            "purpose": "用一句话交代事件和读者为什么要继续看。",
            "bullets": [str(brief.get("core_claim") or brief.get("title") or "")],
        },
        {
            "section": "facts",
            "heading": "核心事实",
            "purpose": "列出已知信息，不扩大解释。",
            "bullets": [str(item.get("title") or item.get("evidence_id") or "") for item in evidence[:3]] or ["证据不足，需人工补充。"],
        },
        {
            "section": "meaning",
            "heading": "为什么重要",
            "purpose": "解释产业、技术、市场或投资含义。",
            "bullets": [str(brief.get("why_it_matters") or "待人工编辑补充。")],
        },
        {
            "section": "evidence",
            "heading": "证据展开",
            "purpose": "逐条展开 supporting evidence。",
            "bullets": [str(item.get("url") or item.get("title") or "") for item in evidence[:5]] or ["证据不足。"],
        },
        {
            "section": "risks",
            "heading": "机会与风险",
            "purpose": "明确哪些判断仍需验证。",
            "bullets": [str(item) for item in risks] or ["Rule-based outline; requires human review."],
        },
        {
            "section": "closing",
            "heading": "下一步观察",
            "purpose": "给出后续观察点，不自动给结论。",
            "bullets": ["观察是否出现更多独立来源、产品采用案例或社区二次传播。"],
        },
    )


def wechat_outline_for(brief: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    if brief.get("content_type") == "deep_analysis":
        return base_structure(brief)
    return (
        {"section": "hook", "heading": "一句话判断", "bullets": [str(brief.get("core_claim") or brief.get("title") or "")]},
        {"section": "facts", "heading": "三条关键信息", "bullets": [str(item.get("title") or "") for item in brief.get("supporting_evidence", [])[:3]]},
        {"section": "takeaway", "heading": "我们怎么看", "bullets": [str(brief.get("why_it_matters") or "待人工补充。")]},
    )


def xiaohongshu_outline_for(brief: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    evidence = brief.get("supporting_evidence") if isinstance(brief.get("supporting_evidence"), list) else []
    return (
        {"section": "point", "heading": "一句话观点", "bullets": [str(brief.get("core_claim") or brief.get("title") or "")]},
        {"section": "three_points", "heading": "三个要点", "bullets": [str(item.get("title") or "") for item in evidence[:3]] or ["证据不足，先做观察。"]},
        {"section": "why_care", "heading": "为什么要关注", "bullets": [str(brief.get("why_it_matters") or "影响 AI/Agent 工具、产业和投资判断。")]},
        {"section": "save", "heading": "收藏型总结", "bullets": ["先收藏，后续观察是否有更多来源确认。"]},
        {"section": "question", "heading": "互动问题", "bullets": ["你觉得这个变化会先影响开发者，还是企业客户？"]},
    )


def editor_notes_for(brief: dict[str, Any]) -> tuple[str, ...]:
    notes = ["Rule-based outline; human editor must verify evidence before publication."]
    missing = brief.get("missing_info")
    if isinstance(missing, list):
        notes.extend(str(item) for item in missing if item)
    return tuple(dict.fromkeys(notes))


def build_outline(brief: dict[str, Any], run_date: str) -> ContentOutline:
    brief_id = str(brief.get("brief_id") or "")
    titles = title_options(brief)
    evidence = tuple(item for item in brief.get("supporting_evidence", []) if isinstance(item, dict))
    return ContentOutline(
        schema_version=SCHEMA_VERSION,
        outline_id=make_outline_id(run_date, brief_id),
        brief_id=brief_id,
        run_date=run_date,
        title_options=titles,
        recommended_title=titles[0] if titles else str(brief.get("title") or ""),
        content_type=str(brief.get("content_type") or "monitor_note"),
        target_platforms=tuple(str(item) for item in brief.get("target_platforms", []) if item),
        structure=base_structure(brief),
        wechat_outline=wechat_outline_for(brief),
        xiaohongshu_outline=xiaohongshu_outline_for(brief),
        required_evidence=evidence,
        editor_notes=editor_notes_for(brief),
        source_ids=tuple(str(item) for item in brief.get("source_ids", []) if item),
        evidence_ids=tuple(str(item) for item in brief.get("evidence_ids", []) if item),
    )


def build_content_outline_report(paths: ProjectPaths, run_date: str | None = None) -> ContentOutlineReport:
    input_path = paths.market_content_root / "05_draft_packs" / "latest_content_briefs.json"
    payload = read_json(input_path)
    final_run_date = normalize_date(run_date or payload.get("run_date"))
    raw_briefs = payload.get("briefs")
    briefs = [item for item in raw_briefs if isinstance(item, dict)] if isinstance(raw_briefs, list) else []
    warnings: list[str] = []
    if not input_path.exists():
        warnings.append("latest_content_briefs.json not found; run make content-briefs first.")
    if not briefs:
        warnings.append("No content briefs available for outline generation.")
    outlines = tuple(build_outline(brief, final_run_date) for brief in briefs)
    return ContentOutlineReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        outline_count=len(outlines),
        outlines=outlines,
        warnings=tuple(warnings),
    )


def report_to_dict(report: ContentOutlineReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: ContentOutlineReport) -> str:
    rows = []
    for index, outline in enumerate(report.outlines, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    escape_cell(outline.recommended_title),
                    escape_cell(outline.content_type),
                    escape_cell(", ".join(outline.target_platforms)),
                    str(len(outline.required_evidence)),
                ]
            )
            + " |"
        )
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Content Outlines v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Outlines: `{report.outline_count}`

## Outlines

| # | Recommended Title | Type | Platforms | Required Evidence |
|---:|---|---|---|---:|
{chr(10).join(rows) if rows else '| 0 | None | - | - | 0 |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__content-outlines.json",
        "dated_md": root / f"{run_date}__content-outlines.md",
        "latest_json": root / "latest_content_outlines.json",
        "latest_md": root / "latest_content_outlines.md",
    }


def write_content_outline_report(report: ContentOutlineReport, paths: ProjectPaths) -> dict[str, Path]:
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
