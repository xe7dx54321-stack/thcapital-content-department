"""Align methodology scores with manual performance feedback."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown
from content_system.topic_selection_methodology import REQUIRED_DIMENSIONS


SCHEMA_VERSION = "v1"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__methodology-performance-alignment.json",
        "dated_md": paths.logs_root / f"{run_date}__methodology-performance-alignment.md",
        "latest_json": paths.logs_root / "latest_methodology_performance_alignment.json",
        "latest_md": paths.logs_root / "latest_methodology_performance_alignment.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__methodology-performance-alignment-board.md",
        "board_latest_md": paths.frontstage_root / "latest_methodology_performance_alignment_board.md",
    }


def effect_from_records(records: list[dict[str, Any]]) -> tuple[str, float]:
    if not records:
        return "UNKNOWN", 0.35
    high = sum(1 for item in records if item.get("performance_rating") in {"HIGH", "EXCELLENT"})
    low = sum(1 for item in records if item.get("performance_rating") == "LOW")
    if high > low:
        return "POSITIVE", min(0.85, 0.45 + high * 0.1)
    if low > high:
        return "NEGATIVE", min(0.75, 0.45 + low * 0.08)
    return "UNKNOWN", 0.45


def build_methodology_performance_alignment(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    topic_scores = read_json(paths.market_content_root / "03_topic_candidates" / "latest_methodology_topic_scores.json")
    article_review = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_article_review.json")
    performance_memory = read_json(paths.market_content_root / "07_publishing" / "content_performance_memory.json")
    performance_feedback = read_json(paths.logs_root / "latest_performance_learning_feedback.json")
    action_effectiveness = read_json(paths.logs_root / "latest_action_effectiveness_analytics.json")
    version_memory = read_json(paths.market_content_root / "09_workbench_actions" / "versions" / "article_version_memory.json")
    records = list_payload(performance_memory, "records")
    topics = list_payload(topic_scores, "topics")
    articles = list_payload(article_review, "articles")
    observed_effect, confidence = effect_from_records(records)
    dimension_insights: list[dict[str, Any]] = []
    for dimension_id in REQUIRED_DIMENSIONS:
        values = [safe_float((topic.get("methodology_scores") or {}).get(dimension_id)) for topic in topics if isinstance(topic.get("methodology_scores"), dict)]
        avg = round(sum(values) / len(values), 2) if values else 0
        dimension_insights.append(
            {
                "dimension_id": dimension_id,
                "observed_effect": observed_effect if records and avg >= 6.0 else "UNKNOWN",
                "evidence": [f"avg_methodology_score={avg}", f"performance_records={len(records)}"],
                "recommendation": "Use as directional signal only until more performance records are available.",
                "confidence": confidence if records else 0.35,
                "auto_apply": False,
            }
        )
    recipe_counts: dict[str, int] = {}
    for article in articles:
        recipe = str(article.get("recipe_id") or "unknown")
        recipe_counts[recipe] = recipe_counts.get(recipe, 0) + 1
    recipe_insights = [
        {"recipe_id": recipe, "article_count": count, "observed_effect": observed_effect if records else "UNKNOWN", "confidence": confidence, "auto_apply": False}
        for recipe, count in sorted(recipe_counts.items())
    ]
    recommendations = list_payload(performance_feedback, "recommendations")[:5]
    if not recommendations:
        recommendations = [
            {
                "recommendation_id": "mpa_collect_more_metrics",
                "target_area": "methodology_calibration",
                "recommendation": "Collect more manual performance metrics before changing methodology weights.",
                "reason": "Insufficient performance records for calibration.",
                "confidence": 0.5,
                "auto_apply": False,
            }
        ]
    summary = {
        "topic_count": len(topics),
        "article_count": len(articles),
        "performance_record_count": len(records),
        "insight_count": len(dimension_insights) + len(recipe_insights),
    }
    run_date = str(topic_scores.get("run_date") or article_review.get("run_date") or today_token()).replace("-", "")[:8]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "summary": summary,
        "dimension_insights": dimension_insights,
        "recipe_insights": recipe_insights,
        "action_effectiveness_summary": action_effectiveness.get("summary") if isinstance(action_effectiveness.get("summary"), dict) else {},
        "version_memory_summary": version_memory.get("summary") if isinstance(version_memory.get("summary"), dict) else {},
        "recommendations": recommendations,
        "policy": {"auto_apply": False, "do_not_change_config": True, "do_not_change_prompts": True, "do_not_change_rules": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    dimension_rows = "\n".join(
        f"| `{item.get('dimension_id')}` | `{item.get('observed_effect')}` | {item.get('confidence')} | {item.get('recommendation')} |"
        for item in list_payload(payload, "dimension_insights")
    ) or "| - | UNKNOWN | 0 | No insights |"
    recipe_rows = "\n".join(
        f"| `{item.get('recipe_id')}` | {item.get('article_count')} | `{item.get('observed_effect')}` | {item.get('confidence')} |"
        for item in list_payload(payload, "recipe_insights")
    ) or "| - | 0 | UNKNOWN | 0 |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Methodology Performance Alignment

## Summary

- topic_count: `{summary.get('topic_count', 0)}`
- article_count: `{summary.get('article_count', 0)}`
- performance_record_count: `{summary.get('performance_record_count', 0)}`
- insight_count: `{summary.get('insight_count', 0)}`
- Policy: suggestions only; no config, prompt, or rule changes are auto-applied.

## Dimension Insights

| Dimension | Observed Effect | Confidence | Recommendation |
|---|---|---:|---|
{dimension_rows}

## Recipe Insights

| Recipe | Articles | Observed Effect | Confidence |
|---|---:|---|---:|
{recipe_rows}
"""
