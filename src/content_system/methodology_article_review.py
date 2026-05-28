"""Methodology-based article review sidecar."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from content_system.article_quality_methodology import generic_language_flags, load_article_quality_methodology
from content_system.content_strategy_recipes import load_content_strategy_recipes, recipes_by_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
STANDARD_IDS = (
    "clear_question",
    "core_judgment",
    "logic_progression",
    "evidence_fit",
    "narrative_tension",
    "reader_relevance",
    "judgment_density",
    "risk_balance",
    "wechat_readability",
    "memorability",
)


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__methodology-article-review.json",
        "dated_md": root / f"{run_date}__methodology-article-review.md",
        "latest_json": root / "latest_methodology_article_review.json",
        "latest_md": root / "latest_methodology_article_review.md",
    }


def clamp(value: float, low: float = 0.0, high: float = 10.0) -> float:
    return max(low, min(high, value))


def section_count(body: str) -> int:
    return len(re.findall(r"^##\s+", body, flags=re.M))


def first_paragraph(body: str) -> str:
    for raw in body.splitlines():
        text = raw.strip()
        if text and not text.startswith("#") and not text.startswith("-"):
            return text
    return ""


def choose_recipe(article: dict[str, Any], recipes: dict[str, dict[str, Any]]) -> str:
    title = str(article.get("wechat_title") or article.get("title") or "")
    text = f"{title} {article.get('wechat_body_markdown') or article.get('body_markdown') or ''}".lower()
    if "投资" in title or "投资人" in text:
        return "investment_framework"
    if re.search(r"产业链|算力|预算|chain|repricing", text):
        return "industry_chain_repricing"
    if re.search(r"技术|路线|模型|route|architecture", text):
        return "technical_route_analysis"
    if re.search(r"产品|入口|工作流|product|strategy", text):
        return "product_strategy_analysis"
    if re.search(r"openai|anthropic|google|nvidia|公司|项目", text):
        return "company_project_deep_dive"
    return "trend_judgment" if "trend_judgment" in recipes else next(iter(recipes.keys()), "trend_judgment")


def review_article(article: dict[str, Any], methodology: dict[str, Any], recipes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    title = str(article.get("wechat_title") or article.get("title") or "")
    body = str(article.get("wechat_body_markdown") or article.get("body_markdown") or "")
    combined = f"{title}\n{body}"
    first = first_paragraph(body)
    evidence_count = len(article.get("evidence_ids") or [])
    if not evidence_count:
        evidence_count = len(re.findall(r"https?://|`web__", body))
    generic_flags = generic_language_flags(combined, methodology)
    sections = section_count(body)
    has_question = bool(re.search(r"[?？]|为什么|如何|怎么|到底|是否", first + title))
    has_core = bool(re.search(r"核心判断|判断|不是.*而是|意味着|真正", combined))
    has_risk = bool(re.search(r"风险|反方|不确定|证据不足|边界", combined))
    has_evidence = evidence_count >= 2 or "证据" in body
    body_len = len(body)
    scores = {
        "clear_question": clamp(6.0 + (2.0 if has_question else -1.0) + (0.8 if len(first) < 140 and first else 0.0)),
        "core_judgment": clamp(5.0 + (2.4 if has_core else -1.2) + (0.6 if "：" in first or ":" in first else 0.0)),
        "logic_progression": clamp(4.5 + min(sections, 6) * 0.7),
        "evidence_fit": clamp(3.8 + min(evidence_count, 5) * 0.9 + (0.8 if has_evidence else 0.0)),
        "narrative_tension": clamp(4.2 + (1.2 if re.search(r"不是|而是|变化|重估|风险|冲突", combined) else 0.0)),
        "reader_relevance": clamp(5.0 + (1.4 if re.search(r"投资|产业|公司|开发者|企业|预算|用户", combined) else 0.0)),
        "judgment_density": clamp(6.0 - len(generic_flags) * 0.8 + (1.0 if has_core else 0.0)),
        "risk_balance": clamp(4.2 + (2.2 if has_risk else -0.8)),
        "wechat_readability": clamp(5.0 + (1.5 if 800 <= body_len <= 4500 else 0.2) + min(sections, 5) * 0.35),
        "memorability": clamp(4.6 + (1.2 if has_core else 0.0) + (0.8 if re.search(r"一句话|结论|框架", combined) else 0.0)),
    }
    total = round(sum(scores.values()) / len(STANDARD_IDS) * 10, 2)
    missing_sections = []
    for marker, label in (("核心判断", "judgment"), ("证据", "evidence_chain"), ("风险", "risk")):
        if marker not in body:
            missing_sections.append(label)
    weaknesses: list[str] = []
    if not has_question:
        weaknesses.append("开头问题不够清晰")
    if not has_core:
        weaknesses.append("核心判断不够明确")
    if len(generic_flags) > 0:
        weaknesses.append("存在空泛表达")
    if evidence_count < 3:
        weaknesses.append("证据链仍可加强")
    if not has_risk:
        weaknesses.append("风险与反方不足")
    strengths = []
    if has_core:
        strengths.append("包含核心判断")
    if has_evidence:
        strengths.append("包含证据段落")
    if sections >= 4:
        strengths.append("结构组件较完整")
    thresholds = methodology.get("recommendation_thresholds") if isinstance(methodology.get("recommendation_thresholds"), dict) else {}
    if total >= safe_float(thresholds.get("READY") or 78) and not missing_sections:
        recommendation = "READY"
    elif total >= safe_float(thresholds.get("REVISE") or 58):
        recommendation = "REVISE"
    else:
        recommendation = "HOLD"
    recipe_id = choose_recipe(article, recipes)
    rewrite_priorities = weaknesses[:5] or ["继续提升判断密度和可复述性"]
    return {
        "article_id": str(article.get("article_id") or article.get("final_candidate_id") or article.get("version_id") or ""),
        "title": title,
        "recipe_id": recipe_id,
        "scores": {key: round(value, 2) for key, value in scores.items()},
        "methodology_total_score": total,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "generic_language_flags": generic_flags,
        "missing_sections": missing_sections,
        "rewrite_priorities": rewrite_priorities,
        "recommendation": recommendation,
        "review_summary": f"Methodology score {total}; recipe={recipe_id}; recommendation={recommendation}.",
    }


def candidate_articles(paths: ProjectPaths) -> list[dict[str, Any]]:
    workbench = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    final_candidates = read_json(paths.market_content_root / "07_publishing" / "latest_final_article_candidates.json")
    rewrite_versions = read_json(paths.market_content_root / "09_workbench_actions" / "versions" / "latest_rewrite_versions.json")
    articles = list_payload(workbench, "articles")
    seen = {str(item.get("article_id")) for item in articles}
    for candidate in list_payload(final_candidates, "candidates"):
        article_id = str(candidate.get("final_candidate_id") or "")
        if article_id and article_id not in seen:
            articles.append({**candidate, "article_id": article_id})
            seen.add(article_id)
    for version in list_payload(rewrite_versions, "versions"):
        article_id = str(version.get("version_id") or "")
        if article_id and article_id not in seen:
            articles.append(
                {
                    "article_id": article_id,
                    "title": version.get("new_title") or "",
                    "wechat_title": version.get("new_title") or "",
                    "wechat_body_markdown": version.get("new_body_markdown") or "",
                    "evidence_ids": [],
                }
            )
            seen.add(article_id)
    return articles


def build_methodology_article_review(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    methodology = load_article_quality_methodology(repo_root)
    recipe_registry = load_content_strategy_recipes(repo_root)
    recipes = recipes_by_id(recipe_registry)
    workbench = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    run_date = str(workbench.get("run_date") or today_token()).replace("-", "")[:8]
    reviews = [review_article(article, methodology, recipes) for article in candidate_articles(paths)]
    summary = {
        "article_count": len(reviews),
        "ready": sum(1 for item in reviews if item.get("recommendation") == "READY"),
        "revise": sum(1 for item in reviews if item.get("recommendation") == "REVISE"),
        "hold": sum(1 for item in reviews if item.get("recommendation") == "HOLD"),
    }
    warnings = []
    if not reviews:
        warnings.append("No articles found for methodology review.")
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "articles": reviews, "summary": summary, "warnings": warnings}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('article_id')}` | {item.get('methodology_total_score')} | `{item.get('recommendation')}` | `{item.get('recipe_id')}` | {escape_cell(item.get('title') or '')} |"
        for item in list_payload(payload, "articles")
    ) or "| - | 0 | - | - | No articles |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings") or []) or "- None"
    return f"""# Methodology Article Review

## Summary

- article_count: `{summary.get('article_count', 0)}`
- ready: `{summary.get('ready', 0)}`
- revise: `{summary.get('revise', 0)}`
- hold: `{summary.get('hold', 0)}`

| Article | Score | Recommendation | Recipe | Title |
|---|---:|---|---|---|
{rows}

## Warnings

{warnings}
"""
