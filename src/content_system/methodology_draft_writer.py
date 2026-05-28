"""Write methodology-aware rule-based drafts."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from content_system.article_quality_methodology import generic_language_flags, load_article_quality_methodology
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__methodology-content-drafts.json",
        "dated_md": root / f"{run_date}__methodology-content-drafts.md",
        "latest_json": root / "latest_methodology_content_drafts.json",
        "latest_md": root / "latest_methodology_content_drafts.md",
    }


def make_id(prefix: str, run_date: str, *parts: object) -> str:
    digest = hashlib.sha1("|".join(str(part) for part in (run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def by_id(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def title_options(brief: dict[str, Any], outline: dict[str, Any]) -> list[str]:
    title = str(outline.get("title_working") or brief.get("title") or "AI/Agent 观察")
    recipe = str(outline.get("recipe_id") or brief.get("recommended_recipe_id") or "")
    options = [
        f"{title}：真正值得判断的变化是什么",
        f"为什么现在要重新看 {title}",
        f"{title} 背后的预期差、证据与风险",
    ]
    if recipe == "investment_framework":
        options.insert(0, f"投资人视角：{title} 的机会与风险")
    if recipe == "industry_chain_repricing":
        options.insert(0, f"{title} 正在重估哪条产业链")
    return list(dict.fromkeys(options))[:5]


def section_markdown(section: dict[str, Any]) -> str:
    evidence = section.get("evidence_ids") if isinstance(section.get("evidence_ids"), list) else []
    evidence_line = "；".join(f"`{item}`" for item in evidence) if evidence else "这一节仍需人工补充或核验证据。"
    return f"""## {section.get('heading') or '未命名小节'}

{section.get('section_claim') or '这一节需要服务文章核心判断，而不是补充材料堆叠。'}

这一节回答的问题是：{section.get('section_question') or '为什么这件事重要？'}

证据安排：{evidence_line}
"""


def build_body(brief: dict[str, Any], outline: dict[str, Any]) -> tuple[str, str, str]:
    titles = title_options(brief, outline)
    title = titles[0] if titles else str(brief.get("title") or "")
    opening_strategy = outline.get("opening_strategy") if isinstance(outline.get("opening_strategy"), dict) else {}
    opening = (
        f"{opening_strategy.get('opening_claim') or brief.get('core_judgment') or title}\n\n"
        f"这篇文章要回答的问题是：{opening_strategy.get('reader_question') or brief.get('core_question') or '这个变化为什么现在值得判断？'}"
    )
    sections = outline.get("sections") if isinstance(outline.get("sections"), list) else []
    section_text = "\n".join(section_markdown(section) for section in sections)
    counter = "\n".join(f"- {item}" for item in (brief.get("counterarguments") or [])[:3]) or "- 反方观点需要人工补充。"
    visual_slots = [section.get("visual_slot_id") for section in sections if section.get("visual_slot_id")]
    visual_note = "\n".join(f"- {slot}: 该位置需要一张服务判断或结构理解的图。" for slot in visual_slots) or "- 暂无 visual slot。"
    closing = outline.get("closing_framework") or "结尾需要形成一句可复述的判断框架。"
    body = f"""# {title}

{opening}

## 核心判断

{brief.get('core_judgment') or '核心判断待人工明确。'}

{section_text}

## 反方与风险

{counter}

## 图片策略提示

{visual_note}

## 结尾框架

{closing}

发布前仍需人工核验证据、标题承诺和风险提示。本稿不会自动发布。
"""
    return title, opening, body


def build_draft(brief: dict[str, Any], outline: dict[str, Any], methodology: dict[str, Any], run_date: str) -> dict[str, Any]:
    title, opening, body = build_body(brief, outline)
    flags = generic_language_flags(f"{title}\n{body}", methodology)
    status = "READY_FOR_REVIEW" if outline.get("status") == "READY_FOR_DRAFT" and not flags else "NEEDS_REVISION" if outline.get("status") != "HOLD" else "HOLD"
    sections = outline.get("sections") if isinstance(outline.get("sections"), list) else []
    visual_slots = [
        {
            "visual_slot_id": section.get("visual_slot_id"),
            "placement": section.get("purpose"),
            "section_id": section.get("section_id"),
            "supports_claim": section.get("section_claim"),
        }
        for section in sections
        if section.get("visual_slot_id")
    ]
    return {
        "draft_id": make_id("mdraft", run_date, outline.get("outline_id"), title),
        "outline_id": outline.get("outline_id") or "",
        "brief_id": outline.get("brief_id") or brief.get("brief_id") or "",
        "topic_id": outline.get("topic_id") or brief.get("topic_id") or "",
        "recipe_id": outline.get("recipe_id") or brief.get("recommended_recipe_id") or "",
        "title_options": title_options(brief, outline),
        "selected_title": title,
        "opening": opening,
        "body_markdown": body,
        "closing": outline.get("closing_framework") or "",
        "visual_slots": visual_slots,
        "methodology_self_check": {
            "core_judgment": "已在开头后单独成节，仍需人工确认是否足够锋利。",
            "logic_progression": "按 outline section_question / section_claim 逐节推进。",
            "evidence_fit": "每节保留 evidence_ids 或明确证据缺口。",
            "judgment_density": "规则型草稿已避免纯资料堆叠，但仍需人工润色。",
            "risk_balance": "保留反方与风险段落。",
        },
        "generic_language_flags": flags,
        "status": status,
    }


def build_methodology_drafts(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    root = paths.market_content_root / "05_draft_packs"
    brief_payload = read_json(root / "latest_methodology_content_briefs.json")
    outline_payload = read_json(root / "latest_methodology_content_outlines.json")
    methodology = load_article_quality_methodology(repo_root)
    run_date = str(outline_payload.get("run_date") or brief_payload.get("run_date") or today_token()).replace("-", "")[:8]
    briefs = by_id(list_payload(brief_payload, "briefs"), "brief_id")
    outlines = list_payload(outline_payload, "outlines")
    warnings = []
    if not outlines:
        warnings.append("No methodology outlines found; run make methodology-outlines first.")
    drafts = [build_draft(briefs.get(str(outline.get("brief_id") or ""), {}), outline, methodology, run_date) for outline in outlines]
    summary = {
        "draft_count": len(drafts),
        "ready_for_review": sum(1 for item in drafts if item.get("status") == "READY_FOR_REVIEW"),
        "needs_revision": sum(1 for item in drafts if item.get("status") == "NEEDS_REVISION"),
        "hold": sum(1 for item in drafts if item.get("status") == "HOLD"),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "drafts": drafts, "summary": summary, "warnings": warnings}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('draft_id')}` | `{item.get('recipe_id')}` | `{item.get('status')}` | {len(item.get('visual_slots') or [])} | {escape_cell(item.get('selected_title') or '')} |"
        for item in list_payload(payload, "drafts")
    ) or "| - | - | - | 0 | No drafts |"
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings") or []) or "- None"
    return f"""# Methodology Content Drafts

## Summary

- draft_count: `{summary.get('draft_count', 0)}`
- ready_for_review: `{summary.get('ready_for_review', 0)}`
- needs_revision: `{summary.get('needs_revision', 0)}`
- hold: `{summary.get('hold', 0)}`

| Draft | Recipe | Status | Visual Slots | Title |
|---|---|---|---:|---|
{rows}

## Warnings

{warnings}
"""
