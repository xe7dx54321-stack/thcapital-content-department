"""Build methodology-aware article outlines."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from content_system.content_strategy_recipes import load_content_strategy_recipes, recipes_by_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


PURPOSE_BY_COMPONENT = {
    "hook": "establish_change",
    "core_judgment": "state_judgment",
    "judgment": "state_judgment",
    "evidence_chain": "prove_trend",
    "why_now": "explain_timing",
    "industry_implication": "explain_impact",
    "implication": "explain_impact",
    "risks": "address_risk",
    "risk": "address_risk",
    "closing_framework": "close_framework",
}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__methodology-content-outlines.json",
        "dated_md": root / f"{run_date}__methodology-content-outlines.md",
        "latest_json": root / "latest_methodology_content_outlines.json",
        "latest_md": root / "latest_methodology_content_outlines.md",
    }


def make_id(prefix: str, run_date: str, *parts: object) -> str:
    digest = hashlib.sha1("|".join(str(part) for part in (run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def recipe_structure(recipe: dict[str, Any]) -> list[str]:
    raw = recipe.get("standard_structure")
    if isinstance(raw, list) and raw:
        return [str(item) for item in raw]
    return ["hook", "core_judgment", "evidence_chain", "industry_implication", "risks", "closing_framework"]


def opening_strategy(brief: dict[str, Any], recipe_id: str) -> dict[str, Any]:
    if "预期差" in str(brief.get("expectation_gap") or "") or recipe_id in {"trend_judgment", "industry_chain_repricing"}:
        hook_type = "expectation_gap"
    elif recipe_id == "technical_route_analysis":
        hook_type = "signal_cluster"
    elif recipe_id == "investment_framework":
        hook_type = "counterintuitive"
    else:
        hook_type = "why_now"
    return {
        "hook_type": hook_type,
        "opening_claim": f"{brief.get('title')} 的关键不是新闻本身，而是它暴露出的变化。",
        "reader_question": brief.get("core_question") or "这个变化为什么现在值得写？",
    }


def section_for(component: str, index: int, brief: dict[str, Any]) -> dict[str, Any]:
    evidence_ids = []
    evidence_plan = brief.get("evidence_plan") if isinstance(brief.get("evidence_plan"), list) else []
    if evidence_plan:
        evidence_ids = evidence_plan[min(index, len(evidence_plan) - 1)].get("available_evidence_ids") or []
    headings = {
        "hook": "这不是一次普通更新",
        "core_judgment": "核心判断：变化在哪里",
        "judgment": "核心判断：变化在哪里",
        "evidence_chain": "三条证据如何支撑判断",
        "why_now": "为什么是现在",
        "industry_implication": "产业链和公司含义",
        "implication": "产业链和公司含义",
        "risks": "反方与风险",
        "risk": "反方与风险",
        "closing_framework": "一句话框架",
    }
    claims = {
        "hook": brief.get("expectation_gap") or "读者可能低估了这条信息的结构性含义。",
        "core_judgment": brief.get("core_judgment") or "",
        "judgment": brief.get("core_judgment") or "",
        "evidence_chain": "证据链需要证明变化真实、窗口明确、影响具体。",
        "why_now": brief.get("why_now") or "",
        "industry_implication": brief.get("industry_chain_impact") or "",
        "implication": brief.get("industry_chain_impact") or "",
        "risks": "; ".join(str(item) for item in (brief.get("counterarguments") or brief.get("risks") or [])[:2]),
        "risk": "; ".join(str(item) for item in (brief.get("counterarguments") or brief.get("risks") or [])[:2]),
        "closing_framework": "把全文收束成一个可复述的判断框架。",
    }
    return {
        "section_id": f"sec_{index + 1}",
        "heading": headings.get(component, component.replace("_", " ").title()),
        "section_question": f"这一节要回答：{headings.get(component, component)}？",
        "section_claim": claims.get(component, ""),
        "evidence_ids": evidence_ids,
        "visual_slot_id": f"vis_{index + 1}" if component in {"hook", "evidence_chain", "industry_implication", "implication", "closing_framework"} else "",
        "purpose": PURPOSE_BY_COMPONENT.get(component, "explain_impact"),
    }


def build_outline(brief: dict[str, Any], recipes: dict[str, dict[str, Any]], run_date: str) -> dict[str, Any]:
    recipe_id = str(brief.get("recommended_recipe_id") or "trend_judgment")
    recipe = recipes.get(recipe_id, {})
    sections = [section_for(component, index, brief) for index, component in enumerate(recipe_structure(recipe))]
    has_risk = any(section.get("purpose") == "address_risk" for section in sections)
    if not has_risk:
        sections.insert(-1, section_for("risks", len(sections), brief))
    status = "READY_FOR_DRAFT" if brief.get("status") == "READY_FOR_OUTLINE" else "NEEDS_EVIDENCE" if brief.get("status") == "NEEDS_EVIDENCE" else "HOLD"
    weak_points = []
    if status == "NEEDS_EVIDENCE":
        weak_points.append("Evidence plan still has missing evidence.")
    if not any(section.get("visual_slot_id") for section in sections):
        weak_points.append("No visual slots reserved.")
    return {
        "outline_id": make_id("moutline", run_date, brief.get("brief_id"), recipe_id),
        "brief_id": brief.get("brief_id") or "",
        "topic_id": brief.get("topic_id") or "",
        "recipe_id": recipe_id,
        "title_working": brief.get("title") or "",
        "opening_strategy": opening_strategy(brief, recipe_id),
        "sections": sections,
        "closing_framework": "结尾用一句话说明：这条信号改变了什么判断、影响谁、下一步看什么。",
        "logic_chain": [section.get("section_claim") for section in sections if section.get("section_claim")],
        "weak_points": weak_points,
        "status": status,
    }


def build_methodology_outlines(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    brief_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_content_briefs.json")
    recipes = recipes_by_id(load_content_strategy_recipes(repo_root))
    run_date = str(brief_payload.get("run_date") or today_token()).replace("-", "")[:8]
    briefs = list_payload(brief_payload, "briefs")
    warnings = []
    if not briefs:
        warnings.append("No methodology briefs found; run make methodology-briefs first.")
    outlines = [build_outline(brief, recipes, run_date) for brief in briefs]
    summary = {
        "outline_count": len(outlines),
        "ready_for_draft": sum(1 for item in outlines if item.get("status") == "READY_FOR_DRAFT"),
        "needs_evidence": sum(1 for item in outlines if item.get("status") == "NEEDS_EVIDENCE"),
        "hold": sum(1 for item in outlines if item.get("status") == "HOLD"),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "outlines": outlines, "summary": summary, "warnings": warnings}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('outline_id')}` | `{item.get('recipe_id')}` | `{item.get('status')}` | {len(item.get('sections') or [])} | {escape_cell(item.get('title_working') or '')} |"
        for item in list_payload(payload, "outlines")
    ) or "| - | - | - | 0 | No outlines |"
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings") or []) or "- None"
    return f"""# Methodology Content Outlines

## Summary

- outline_count: `{summary.get('outline_count', 0)}`
- ready_for_draft: `{summary.get('ready_for_draft', 0)}`
- needs_evidence: `{summary.get('needs_evidence', 0)}`
- hold: `{summary.get('hold', 0)}`

| Outline | Recipe | Status | Sections | Title |
|---|---|---|---:|---|
{rows}

## Warnings

{warnings}
"""
