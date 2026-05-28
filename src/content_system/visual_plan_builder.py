"""Build article visual plans."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from content_system.article_visual_methodology import load_article_visual_methodology, visual_types_by_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, safe_int, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__article-visual-plans.json",
        "dated_md": root / f"{run_date}__article-visual-plans.md",
        "latest_json": root / "latest_article_visual_plans.json",
        "latest_md": root / "latest_article_visual_plans.md",
    }


def make_id(prefix: str, run_date: str, *parts: object) -> str:
    digest = hashlib.sha1("|".join(str(part) for part in (run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def visual_type_for(recipe_id: str, text: str, index: int) -> str:
    lowered = text.lower()
    if index == 0:
        return "cover_visual"
    if "产业链" in text or "chain" in lowered:
        return "value_chain_map"
    if "路线" in text or "流程" in text or "route" in lowered or "workflow" in lowered:
        return "process_flow"
    if "为什么是现在" in text or "时间" in text:
        return "timeline_chart"
    if "对比" in text or "预期差" in text:
        return "comparison_table_visual"
    if recipe_id in {"investment_framework", "trend_judgment"}:
        return "framework_diagram"
    return "concept_diagram"


def source_strategy_for(visual_type: str) -> str:
    return {
        "cover_visual": "generated_concept_visual",
        "concept_diagram": "manual_design_request",
        "value_chain_map": "internal_chart",
        "timeline_chart": "internal_chart",
        "comparison_table_visual": "internal_chart",
        "framework_diagram": "internal_chart",
        "process_flow": "internal_chart",
        "evidence_snapshot": "evidence_snapshot",
    }.get(visual_type, "manual_design_request")


def build_visuals(article: dict[str, Any], methodology: dict[str, Any]) -> list[dict[str, Any]]:
    visual_types = visual_types_by_id(methodology)
    title = str(article.get("selected_title") or article.get("title") or article.get("wechat_title") or "")
    recipe_id = str(article.get("recipe_id") or "trend_judgment")
    slots = article.get("visual_slots") if isinstance(article.get("visual_slots"), list) else []
    seed_slots = [{"visual_slot_id": "cover", "placement": "cover", "supports_claim": title}]
    seed_slots.extend(slots[:3])
    visuals = []
    for index, slot in enumerate(seed_slots[:4]):
        text = " ".join(str(slot.get(key) or "") for key in ("placement", "supports_claim", "section_id"))
        visual_type = visual_type_for(recipe_id, f"{title} {text}", index)
        meta = visual_types.get(visual_type, {})
        strategy = source_strategy_for(visual_type)
        placement = "cover" if index == 0 else str(slot.get("placement") or f"section_{index}")
        status = "READY_FOR_PROMPT" if strategy in {"generated_concept_visual", "manual_design_request"} else "PLANNED"
        visuals.append(
            {
                "visual_id": make_id("vis", str(article.get("run_date") or today_token()).replace("-", "")[:8], article.get("draft_id") or article.get("article_id"), index),
                "visual_type": visual_type,
                "placement": placement,
                "information_job": meta.get("information_job") or "帮助读者理解文章核心判断。",
                "supports_claim": slot.get("supports_claim") or title,
                "source_strategy": strategy,
                "required_inputs": ["core_judgment", "article_title"] if index == 0 else ["section_claim", "evidence_ids"],
                "quality_checks": meta.get("quality_standards") or [],
                "status": status,
            }
        )
    return visuals


def candidate_articles(paths: ProjectPaths) -> list[dict[str, Any]]:
    draft_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_content_drafts.json")
    final_payload = read_json(paths.market_content_root / "07_publishing" / "latest_final_article_candidates.json")
    drafts = list_payload(draft_payload, "drafts")
    if drafts:
        return drafts
    return [
        {
            "draft_id": item.get("final_candidate_id"),
            "article_id": item.get("source_article_id"),
            "selected_title": item.get("wechat_title") or item.get("title"),
            "body_markdown": item.get("wechat_body_markdown") or item.get("body_markdown"),
            "recipe_id": "trend_judgment",
            "visual_slots": [],
        }
        for item in list_payload(final_payload, "candidates")
    ]


def build_visual_plans(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    methodology = load_article_visual_methodology(repo_root)
    draft_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_content_drafts.json")
    run_date = str(draft_payload.get("run_date") or today_token()).replace("-", "")[:8]
    articles = candidate_articles(paths)
    warnings = []
    if not articles:
        warnings.append("No methodology drafts or final candidates found for visual planning.")
    plans = []
    for article in articles:
        visuals = build_visuals({**article, "run_date": run_date}, methodology)
        needs_input = sum(1 for visual in visuals if visual.get("status") == "NEEDS_INPUT")
        plans.append(
            {
                "visual_plan_id": make_id("vplan", run_date, article.get("draft_id") or article.get("article_id")),
                "article_id": article.get("draft_id") or article.get("article_id") or "",
                "title": article.get("selected_title") or article.get("title") or article.get("wechat_title") or "",
                "recommended_visual_count": len(visuals),
                "visuals": visuals,
                "warnings": ["No automatic image generation; prompts and asset requests require human review."] if needs_input else [],
            }
        )
    summary = {
        "plan_count": len(plans),
        "visual_count": sum(len(item.get("visuals") or []) for item in plans),
        "ready_for_prompt": sum(1 for plan in plans for visual in plan.get("visuals", []) if visual.get("status") == "READY_FOR_PROMPT"),
        "needs_input": sum(1 for plan in plans for visual in plan.get("visuals", []) if visual.get("status") == "NEEDS_INPUT"),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "visual_plans": plans, "summary": summary, "warnings": warnings, "policy": {"do_not_auto_generate_images": True}}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{plan.get('visual_plan_id')}` | {safe_int(plan.get('recommended_visual_count'))} | {plan.get('title')} |"
        for plan in list_payload(payload, "visual_plans")
    ) or "| - | 0 | No visual plans |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Article Visual Plans

## Summary

- plan_count: `{summary.get('plan_count', 0)}`
- visual_count: `{summary.get('visual_count', 0)}`
- ready_for_prompt: `{summary.get('ready_for_prompt', 0)}`
- needs_input: `{summary.get('needs_input', 0)}`
- do_not_auto_generate_images: `true`

| Plan | Visuals | Title |
|---|---:|---|
{rows}
"""
