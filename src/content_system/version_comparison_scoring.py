"""Score new workbench article versions against their source article."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import (
    list_payload,
    read_json,
    repo_relative,
    safe_float,
    today_token,
    utc_now,
    write_json_and_markdown,
)


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class VersionComparisonScoringResult:
    run_date: str
    comparison_count: int
    accept_recommended: int
    reject_recommended: int
    revise_more_recommended: int
    output_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "dated_json": root / f"{run_date}__version-comparison-scores.json",
        "dated_md": root / f"{run_date}__version-comparison-scores.md",
        "latest_json": root / "latest_version_comparison_scores.json",
        "latest_md": root / "latest_version_comparison_scores.md",
    }


def article_by_id(workbench_data: dict[str, Any], article_id: str) -> dict[str, Any]:
    articles = list_payload(workbench_data, "articles")
    for article in articles:
        if article_id in {article.get("article_id"), article.get("package_id"), article.get("draft_id")}:
            return article
    selected_id = str(workbench_data.get("selected_article_id") or "")
    for article in articles:
        if article.get("article_id") == selected_id:
            return article
    return articles[0] if articles else {}


def first_paragraph(body: str) -> str:
    for raw in body.splitlines():
        text = raw.strip()
        if text and not text.startswith("#") and not text.startswith("- "):
            return text
    return ""


def text_tokens(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z][A-Za-z0-9_.-]{2,}|[\u4e00-\u9fff]{2,}", text or "")}


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def keyword_score(text: str, keywords: tuple[str, ...], weight: float = 4.0, cap: float = 24.0) -> float:
    return min(cap, sum(weight for keyword in keywords if keyword.lower() in text.lower() or keyword in text))


def score_title(title: str) -> float:
    length = len(title.strip())
    score = 42.0
    if 12 <= length <= 70:
        score += 18
    elif length > 0:
        score += 8
    score += keyword_score(title, ("为什么", "投资人", "机会", "风险", "趋势", "真正", "现在", "下一步", "AI", "Agent"), 3, 22)
    if "：" in title or ":" in title or "？" in title or "?" in title:
        score += 8
    return clamp(score)


def score_opening(body: str) -> float:
    opening = first_paragraph(body)
    score = 38.0
    if 36 <= len(opening) <= 240:
        score += 18
    elif opening:
        score += 8
    score += keyword_score(opening, ("这件事", "信号", "变化", "问题", "机会", "风险", "不是", "为什么", "投资人"), 3.5, 24)
    if re.search(r"\d|GPT|Claude|OpenAI|Anthropic|Google|Agent", opening, re.I):
        score += 8
    return clamp(score)


def score_logic(body: str) -> float:
    headings = len(re.findall(r"^##\s+", body, flags=re.M))
    score = 38 + min(24, headings * 6)
    score += keyword_score(body, ("为什么", "因此", "但是", "首先", "其次", "最后", "核心判断", "下一步"), 3, 22)
    return clamp(score)


def score_evidence(body: str, article: dict[str, Any] | None = None) -> float:
    article = article or {}
    evidence_refs = len(article.get("evidence_ids") or []) + len(article.get("source_ids") or [])
    url_hits = len(re.findall(r"https?://|source|evidence|证据|来源|官方", body, flags=re.I))
    return clamp(36 + min(28, evidence_refs * 4) + min(24, url_hits * 3))


def score_readability(body: str) -> float:
    paragraphs = [line.strip() for line in body.splitlines() if line.strip() and not line.startswith("#")]
    if not paragraphs:
        return 20.0
    avg_len = sum(len(item) for item in paragraphs) / len(paragraphs)
    score = 45.0 + min(20, len(paragraphs) * 1.4)
    if 35 <= avg_len <= 180:
        score += 18
    elif avg_len > 260:
        score -= 12
    if len(body) > 600:
        score += 8
    return clamp(score)


def score_investment_angle(title: str, body: str) -> float:
    text = f"{title}\n{body}"
    return clamp(34 + keyword_score(text, ("投资", "投资人", "产业", "商业", "市场", "公司", "机会", "风险", "估值", "壁垒"), 4.5, 46))


def score_risk_control(body: str) -> float:
    score = 40 + keyword_score(body, ("风险", "不确定", "核验", "证据", "人工确认", "发布前", "边界"), 5, 35)
    overclaims = len(re.findall(r"必然|一定|保证|颠覆一切|唯一答案|确定会", body))
    score -= min(28, overclaims * 8)
    return clamp(score)


def score_article(title: str, body: str, article: dict[str, Any] | None = None) -> dict[str, float]:
    title_strength = score_title(title)
    opening_strength = score_opening(body)
    logic_clarity = score_logic(body)
    evidence_strength = score_evidence(body, article)
    wechat_readability = score_readability(body)
    investment_angle = score_investment_angle(title, body)
    risk_control = score_risk_control(body)
    overall = (
        title_strength * 0.16
        + opening_strength * 0.16
        + logic_clarity * 0.17
        + evidence_strength * 0.17
        + wechat_readability * 0.14
        + investment_angle * 0.12
        + risk_control * 0.08
    )
    return {
        "overall": round(clamp(overall), 1),
        "title_strength": round(title_strength, 1),
        "opening_strength": round(opening_strength, 1),
        "logic_clarity": round(logic_clarity, 1),
        "evidence_strength": round(evidence_strength, 1),
        "wechat_readability": round(wechat_readability, 1),
        "investment_angle": round(investment_angle, 1),
        "risk_control": round(risk_control, 1),
    }


def component_delta(original: dict[str, float], new: dict[str, float], key: str) -> float:
    return round(safe_float(new.get(key)) - safe_float(original.get(key)), 1)


def build_improvements_and_regressions(scores: dict[str, float]) -> tuple[list[str], list[str]]:
    labels = {
        "title_strength_delta": "标题强度",
        "opening_strength_delta": "开头吸引力",
        "logic_clarity_delta": "逻辑清晰度",
        "evidence_strength_delta": "证据强度",
        "wechat_readability_delta": "公众号可读性",
        "investment_angle_delta": "投资人视角",
        "risk_control_delta": "风险控制",
    }
    improvements = [f"{label} +{scores[key]}" for key, label in labels.items() if safe_float(scores.get(key)) >= 3]
    regressions = [f"{label} {scores[key]}" for key, label in labels.items() if safe_float(scores.get(key)) <= -3]
    return improvements, regressions


def recommendation_for(delta: float, regressions: list[str], issues: list[str]) -> str:
    if issues:
        return "HUMAN_REVIEW"
    if delta >= 8 and len(regressions) <= 1:
        return "ACCEPT"
    if delta <= -5 or len(regressions) >= 3:
        return "REJECT"
    if delta >= 2:
        return "REVISE_MORE"
    return "HUMAN_REVIEW"


def comparison_for_rewrite(run_date: str, version: dict[str, Any], workbench_data: dict[str, Any]) -> dict[str, Any]:
    article = article_by_id(workbench_data, str(version.get("source_article_id") or ""))
    original_title = str(article.get("wechat_title") or article.get("title") or "")
    original_body = str(article.get("wechat_body_markdown") or "")
    new_title = str(version.get("new_title") or original_title)
    new_body = str(version.get("new_body_markdown") or original_body)
    issues = [str(item) for item in version.get("issues") or []]
    if not article:
        issues.append("source_article_not_found")
    if not new_body.strip():
        issues.append("new_body_missing")
    original = score_article(original_title, original_body, article)
    new = score_article(new_title, new_body, article)
    scores = {
        "original_overall": original["overall"],
        "new_overall": new["overall"],
        "delta": round(new["overall"] - original["overall"], 1),
        "title_strength_delta": component_delta(original, new, "title_strength"),
        "opening_strength_delta": component_delta(original, new, "opening_strength"),
        "logic_clarity_delta": component_delta(original, new, "logic_clarity"),
        "evidence_strength_delta": component_delta(original, new, "evidence_strength"),
        "wechat_readability_delta": component_delta(original, new, "wechat_readability"),
        "investment_angle_delta": component_delta(original, new, "investment_angle"),
        "risk_control_delta": component_delta(original, new, "risk_control"),
    }
    improvements, regressions = build_improvements_and_regressions(scores)
    recommendation = recommendation_for(safe_float(scores.get("delta")), regressions, issues)
    confidence = 0.72 if not issues else 0.42
    return {
        "comparison_id": f"vcomp_{run_date}_{str(version.get('version_id') or 'version').replace('ver_', '')}",
        "version_id": version.get("version_id") or "",
        "source_action_id": version.get("source_action_id") or "",
        "source_article_id": version.get("source_article_id") or "",
        "version_type": version.get("version_type") or "rewrite",
        "original_title": original_title,
        "new_title": new_title,
        "scores": scores,
        "improvements": improvements,
        "regressions": regressions,
        "recommendation": recommendation,
        "confidence": confidence,
        "scoring_mode": "rule_based",
        "issues": issues,
    }


def build_version_comparison_scores(paths: ProjectPaths, repo_root: Path) -> tuple[VersionComparisonScoringResult, dict[str, Any]]:
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    rewrite_payload = read_json(versions_root / "latest_rewrite_versions.json")
    workbench_data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    preview_payload = read_json(paths.logs_root / "latest_versioned_article_preview.json")
    run_date = str(
        rewrite_payload.get("run_date") or workbench_data.get("run_date") or preview_payload.get("run_date") or today_token()
    ).replace("-", "")[:8]
    comparisons = [
        comparison_for_rewrite(run_date, version, workbench_data)
        for version in list_payload(rewrite_payload, "versions")
        if version.get("version_id")
    ]
    summary = {
        "comparison_count": len(comparisons),
        "accept_recommended": sum(1 for item in comparisons if item.get("recommendation") == "ACCEPT"),
        "reject_recommended": sum(1 for item in comparisons if item.get("recommendation") == "REJECT"),
        "revise_more_recommended": sum(1 for item in comparisons if item.get("recommendation") == "REVISE_MORE"),
        "human_review_recommended": sum(1 for item in comparisons if item.get("recommendation") == "HUMAN_REVIEW"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "comparisons": comparisons,
        "summary": summary,
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        VersionComparisonScoringResult(
            run_date,
            summary["comparison_count"],
            summary["accept_recommended"],
            summary["reject_recommended"],
            summary["revise_more_recommended"],
            repo_relative(outputs["latest_json"], repo_root),
        ),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('version_id')}` | `{(item.get('scores') or {}).get('delta')}` | `{item.get('recommendation')}` | {', '.join(item.get('improvements') or []) or '-'} | {', '.join(item.get('regressions') or []) or '-'} |"
        for item in list_payload(payload, "comparisons")
    ) or "| - | 0 | HUMAN_REVIEW | No versions to score | - |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Version Comparison Scores

## Summary

- Run date: `{payload.get('run_date')}`
- Comparisons: `{summary.get('comparison_count', 0)}`
- Accept recommended: `{summary.get('accept_recommended', 0)}`
- Reject recommended: `{summary.get('reject_recommended', 0)}`
- Revise more recommended: `{summary.get('revise_more_recommended', 0)}`
- Human review recommended: `{summary.get('human_review_recommended', 0)}`
- Policy: scores are advisory only; no version is accepted automatically.

| Version | Delta | Recommendation | Improvements | Regressions |
|---|---:|---|---|---|
{rows}
"""
