"""Methodology-based topic scoring sidecar."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from content_system.content_strategy_recipes import recommend_recipe_from_scores
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.topic_selection_methodology import REQUIRED_DIMENSIONS, load_topic_selection_methodology


SCHEMA_VERSION = "v1"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "03_topic_candidates"
    return {
        "dated_json": root / f"{run_date}__methodology-topic-scores.json",
        "dated_md": root / f"{run_date}__methodology-topic-scores.md",
        "latest_json": root / "latest_methodology_topic_scores.json",
        "latest_md": root / "latest_methodology_topic_scores.md",
    }


def clamp(value: float, low: float = 0.0, high: float = 10.0) -> float:
    return max(low, min(high, value))


def text_blob(topic: dict[str, Any]) -> str:
    evidence = topic.get("key_evidence") if isinstance(topic.get("key_evidence"), list) else []
    evidence_text = " ".join(str(item.get("title") or item.get("summary") or "") for item in evidence if isinstance(item, dict))
    angles = " ".join(str(item) for item in topic.get("suggested_angles") or [])
    return " ".join([str(topic.get("theme") or topic.get("title") or ""), str(topic.get("why_it_matters") or ""), angles, evidence_text])


def score_topic(topic: dict[str, Any], methodology: dict[str, Any]) -> dict[str, Any]:
    title = str(topic.get("theme") or topic.get("title") or "")
    text = text_blob(topic)
    lowered = text.lower()
    evidence_count = safe_int(topic.get("evidence_count") or len(topic.get("key_evidence") or []))
    source_count = safe_int(topic.get("source_count") or len(topic.get("source_ids") or []))
    base_value = safe_float(topic.get("total_score") or topic.get("score")) / 10.0
    ai_relevance = 1.0 if re.search(r"ai|agent|model|openai|anthropic|google|nvidia|claude|gemini|模型|智能体|开发者", lowered, re.I) else -1.0
    scores = {
        "change_intensity": clamp(4.5 + min(evidence_count, 5) * 0.65 + (1.0 if re.search(r"release|launch|announce|发布|推出|升级", lowered) else 0.0)),
        "expectation_gap": clamp(4.0 + (1.2 if re.search(r"why|为什么|不是|转向|重估|bet|big", lowered) else 0.0) + base_value * 0.15),
        "industry_chain_impact": clamp(4.0 + (1.5 if re.search(r"developer|agent|infrastructure|factory|chain|产业|算力|工具|入口", lowered) else 0.0) + ai_relevance),
        "evidence_strength": clamp(2.8 + min(evidence_count, 5) * 0.9 + min(source_count, 4) * 0.45),
        "narrative_tension": clamp(4.0 + (1.3 if re.search(r"bet|future|mean|why|冲突|误读|重估|风险", lowered) else 0.0) + base_value * 0.12),
        "timing_window": clamp(5.2 + (1.0 if topic.get("run_date") else 0.0) + min(evidence_count, 3) * 0.35),
        "original_judgment_potential": clamp(4.0 + (1.4 if topic.get("why_it_matters") else 0.0) + (1.0 if topic.get("suggested_angles") else 0.0) + ai_relevance * 0.7),
        "reader_value": clamp(4.2 + (1.4 if re.search(r"invest|投资|organization|developer|企业|产品|产业", lowered) else 0.0) + ai_relevance * 0.8),
    }
    reject_flags: list[str] = []
    if evidence_count == 0:
        reject_flags.append("只有标题党、没有证据")
    if evidence_count < 2:
        reject_flags.append("缺少一手来源且无法补证据" if source_count == 0 else "证据不足，需要补证据")
    if ai_relevance < 0:
        reject_flags.append("与用户关注的 AI/Agent/产业/投资主线弱相关")
    if not title or not str(topic.get("why_it_matters") or ""):
        reject_flags.append("无法形成一句核心判断")
    total = round(sum(scores.values()) / len(REQUIRED_DIMENSIONS) * 10, 2)
    thresholds = methodology.get("recommendation_thresholds") if isinstance(methodology.get("recommendation_thresholds"), dict) else {}
    if any(flag in reject_flags for flag in methodology.get("reject_rules") or []):
        recommendation = "REJECT"
    elif total >= safe_float(thresholds.get("WRITE") or 72) and scores["evidence_strength"] >= 5.8:
        recommendation = "WRITE"
    elif total >= safe_float(thresholds.get("WATCH") or 58):
        recommendation = "WATCH"
    elif total >= safe_float(thresholds.get("HOLD") or 42):
        recommendation = "HOLD"
    else:
        recommendation = "REJECT"
    if total >= safe_float(thresholds.get("WRITE") or 72) and scores["evidence_strength"] < 5.8:
        recommendation = "WATCH"
    missing: list[str] = []
    if evidence_count < 3:
        missing.append("至少 3 条证据是什么？")
    if not str(topic.get("why_it_matters") or ""):
        missing.append("为什么现在写？")
    recipe_id = recommend_recipe_from_scores(scores, title)
    return {
        "topic_id": str(topic.get("cluster_id") or topic.get("candidate_id") or topic.get("topic_id") or ""),
        "title": title,
        "methodology_scores": {key: round(value, 2) for key, value in scores.items()},
        "methodology_total_score": total,
        "core_judgment": f"{title} 不是单纯新闻更新，而是一个需要判断其变化强度和产业影响的信号。",
        "why_now": str(topic.get("why_it_matters") or "窗口期需要人工补充判断。"),
        "reader_value_summary": "帮助读者理解这条 AI/Agent 信号是否值得纳入产业或投资判断。",
        "reject_flags": reject_flags,
        "recommended_recipe_id": recipe_id,
        "recommendation": recommendation,
        "reasons": [
            f"methodology_total_score={total}",
            f"evidence_count={evidence_count}",
            f"source_count={source_count}",
            f"recommended_recipe={recipe_id}",
        ],
        "missing_requirements": missing,
    }


def build_methodology_topic_scores(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    topic_root = paths.market_content_root / "03_topic_candidates"
    high_value = read_json(topic_root / "latest_high_value_candidates.json")
    clusters_payload = read_json(topic_root / "latest_topic_clusters.json")
    methodology = load_topic_selection_methodology(repo_root)
    run_date = str(high_value.get("run_date") or clusters_payload.get("run_date") or today_token()).replace("-", "")[:8]
    candidates = list_payload(high_value, "candidates")
    clusters_by_id = {str(item.get("cluster_id")): item for item in list_payload(clusters_payload, "clusters") if item.get("cluster_id")}
    topics: list[dict[str, Any]] = []
    for candidate in candidates:
        merged = dict(clusters_by_id.get(str(candidate.get("cluster_id")), {}))
        merged.update(candidate)
        topics.append(score_topic(merged, methodology))
    summary = {
        "topic_count": len(topics),
        "write": sum(1 for item in topics if item.get("recommendation") == "WRITE"),
        "watch": sum(1 for item in topics if item.get("recommendation") == "WATCH"),
        "hold": sum(1 for item in topics if item.get("recommendation") == "HOLD"),
        "reject": sum(1 for item in topics if item.get("recommendation") == "REJECT"),
    }
    warnings = []
    if not candidates:
        warnings.append("No high-value candidates found; run make high-value-candidates first.")
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "topics": topics, "summary": summary, "warnings": warnings}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('topic_id')}` | {item.get('methodology_total_score')} | `{item.get('recommendation')}` | `{item.get('recommended_recipe_id')}` | {escape_cell(item.get('title') or '')} |"
        for item in list_payload(payload, "topics")
    ) or "| - | 0 | - | - | No topics |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings") or []) or "- None"
    return f"""# Methodology Topic Scores

## Summary

- topic_count: `{summary.get('topic_count', 0)}`
- write: `{summary.get('write', 0)}`
- watch: `{summary.get('watch', 0)}`
- hold: `{summary.get('hold', 0)}`
- reject: `{summary.get('reject', 0)}`

| Topic | Score | Recommendation | Recipe | Title |
|---|---:|---|---|---|
{rows}

## Warnings

{warnings}
"""
