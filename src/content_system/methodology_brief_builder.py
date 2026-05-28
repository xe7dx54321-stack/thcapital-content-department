"""Build methodology-aware content briefs."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from content_system.content_strategy_recipes import load_content_strategy_recipes, recipes_by_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__methodology-content-briefs.json",
        "dated_md": root / f"{run_date}__methodology-content-briefs.md",
        "latest_json": root / "latest_methodology_content_briefs.json",
        "latest_md": root / "latest_methodology_content_briefs.md",
    }


def make_id(prefix: str, run_date: str, *parts: object) -> str:
    digest = hashlib.sha1("|".join(str(part) for part in (run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def by_topic_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        for key in ("topic_id", "cluster_id", "candidate_id"):
            value = str(item.get(key) or "")
            if value:
                result[value] = item
    return result


def evidence_ids_from_candidate(candidate: dict[str, Any]) -> list[str]:
    evidence = candidate.get("key_evidence") if isinstance(candidate.get("key_evidence"), list) else []
    ids = [str(item.get("evidence_id")) for item in evidence if isinstance(item, dict) and item.get("evidence_id")]
    ids.extend(str(item) for item in candidate.get("evidence_ids", []) if item)
    return list(dict.fromkeys(ids))


def visual_opportunities_for(recipe_id: str, topic: dict[str, Any]) -> list[str]:
    opportunities = ["cover_visual: 用封面承载核心判断，而不是泛科技感背景。"]
    if recipe_id == "industry_chain_repricing":
        opportunities.append("value_chain_map: 展示受影响的产业链环节和价值流向。")
    if recipe_id in {"technical_route_analysis", "product_strategy_analysis"}:
        opportunities.append("process_flow: 展示技术路线或产品工作流变化。")
    if "why_now" in str(topic.get("why_now") or "").lower() or safe_float((topic.get("methodology_scores") or {}).get("timing_window")) >= 6:
        opportunities.append("timeline_chart: 说明为什么当前是窗口期。")
    opportunities.append("framework_diagram: 在结尾帮助读者复述判断框架。")
    return opportunities[:4]


def build_evidence_plan(topic: dict[str, Any], candidate: dict[str, Any]) -> list[dict[str, Any]]:
    evidence_ids = evidence_ids_from_candidate(candidate)
    claims = [
        ("变化是否真实", "官方发布、产品变更、开发者反馈或一手数据"),
        ("为什么现在写", "时间窗口、连续信号或竞争动作"),
        ("影响谁", "产业链、公司、产品或投资判断的具体影响"),
    ]
    plan = []
    for index, (claim, needed) in enumerate(claims):
        available = evidence_ids[index:index + 1]
        plan.append(
            {
                "claim": claim,
                "evidence_needed": needed,
                "available_evidence_ids": available,
                "missing_evidence": not bool(available),
            }
        )
    return plan


def build_brief(topic: dict[str, Any], candidate: dict[str, Any], recipes: dict[str, dict[str, Any]], run_date: str) -> dict[str, Any]:
    topic_id = str(topic.get("topic_id") or candidate.get("cluster_id") or candidate.get("candidate_id") or "")
    recipe_id = str(topic.get("recommended_recipe_id") or "trend_judgment")
    recipe = recipes.get(recipe_id, {})
    score = safe_float(topic.get("methodology_total_score"))
    evidence_plan = build_evidence_plan(topic, candidate)
    missing_count = sum(1 for item in evidence_plan if item.get("missing_evidence"))
    recommendation = str(topic.get("recommendation") or "HOLD")
    if recommendation in {"WRITE", "WATCH"} and missing_count <= 1:
        status = "READY_FOR_OUTLINE"
    elif recommendation in {"WRITE", "WATCH"}:
        status = "NEEDS_EVIDENCE"
    else:
        status = "HOLD"
    title = str(topic.get("title") or candidate.get("theme") or candidate.get("title") or "未命名选题")
    warnings = []
    if missing_count:
        warnings.append(f"{missing_count} evidence plan items need more evidence.")
    if recommendation != "WRITE":
        warnings.append(f"Topic recommendation is {recommendation}; human editor should confirm before drafting.")
    return {
        "brief_id": make_id("mbrief", run_date, topic_id, title),
        "topic_id": topic_id,
        "title": title,
        "recommended_recipe_id": recipe_id,
        "methodology_topic_score": score,
        "core_question": f"这篇文章要回答：{title} 代表什么变化，为什么现在值得判断？",
        "core_judgment": topic.get("core_judgment") or f"{title} 不是普通更新，而是一个需要判断变化强度和产业影响的信号。",
        "why_now": topic.get("why_now") or "需要补充当前窗口期判断。",
        "expectation_gap": "读者可能把它看成普通新闻，文章需要说明它背后的预期差。",
        "industry_chain_impact": "需要明确影响哪些产业链环节、公司类型或产品入口。",
        "reader_value": topic.get("reader_value_summary") or "帮助读者形成可复述的产业/投资判断。",
        "evidence_plan": evidence_plan,
        "counterarguments": ["这可能只是短期营销信号，而不是结构性变化。", "证据可能还不足以支撑强判断。"],
        "risks": topic.get("reject_flags") or ["需要人工核验事实、来源和标题承诺。"],
        "visual_opportunities": visual_opportunities_for(recipe_id, topic),
        "writing_angle": f"采用「{recipe.get('label') or recipe_id}」打法，先给判断，再展开证据和影响。",
        "not_to_write": ["不要写成新闻复述。", "不要堆砌空泛行业热词。", "不要在证据不足时做绝对化结论。"],
        "status": status,
        "warnings": warnings,
    }


def build_methodology_briefs(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    topic_payload = read_json(paths.market_content_root / "03_topic_candidates" / "latest_methodology_topic_scores.json")
    high_value_payload = read_json(paths.market_content_root / "03_topic_candidates" / "latest_high_value_candidates.json")
    recipes = recipes_by_id(load_content_strategy_recipes(repo_root))
    run_date = str(topic_payload.get("run_date") or high_value_payload.get("run_date") or today_token()).replace("-", "")[:8]
    topics = list_payload(topic_payload, "topics")
    candidates_by_id = by_topic_id(list_payload(high_value_payload, "candidates"))
    warnings: list[str] = []
    if not topics:
        warnings.append("No methodology topic scores found; run make methodology-topic-score first.")
    briefs = [
        build_brief(topic, candidates_by_id.get(str(topic.get("topic_id") or ""), {}), recipes, run_date)
        for topic in topics
        if topic.get("recommendation") != "REJECT"
    ]
    summary = {
        "brief_count": len(briefs),
        "ready_for_outline": sum(1 for item in briefs if item.get("status") == "READY_FOR_OUTLINE"),
        "needs_evidence": sum(1 for item in briefs if item.get("status") == "NEEDS_EVIDENCE"),
        "hold": sum(1 for item in briefs if item.get("status") == "HOLD"),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "briefs": briefs, "summary": summary, "warnings": warnings}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('brief_id')}` | `{item.get('recommended_recipe_id')}` | {item.get('methodology_topic_score')} | `{item.get('status')}` | {escape_cell(item.get('title') or '')} |"
        for item in list_payload(payload, "briefs")
    ) or "| - | - | 0 | - | No briefs |"
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings") or []) or "- None"
    return f"""# Methodology Content Briefs

## Summary

- brief_count: `{summary.get('brief_count', 0)}`
- ready_for_outline: `{summary.get('ready_for_outline', 0)}`
- needs_evidence: `{summary.get('needs_evidence', 0)}`
- hold: `{summary.get('hold', 0)}`

| Brief | Recipe | Score | Status | Title |
|---|---|---:|---|---|
{rows}

## Policy

- Does not replace original content briefs.
- Does not publish or call live models.

## Warnings

{warnings}
"""
