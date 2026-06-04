"""Build post-publish performance feedback for content operations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, safe_int, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__post-publish-feedback.json",
        "dated_md": paths.logs_root / f"{run_date}__post-publish-feedback.md",
        "latest_json": paths.logs_root / "latest_post_publish_feedback.json",
        "latest_md": paths.logs_root / "latest_post_publish_feedback.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__post-publish-feedback-board.md",
        "board_latest_md": paths.frontstage_root / "latest_post_publish_feedback_board.md",
    }


def build_content_ops_performance_feedback(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing = paths.market_content_root / "07_publishing"
    archive = read_json(publishing / "published_article_archive.json")
    metrics_review = read_json(paths.logs_root / "latest_post_publish_metrics_review.json")
    content_memory = read_json(publishing / "content_performance_memory.json")
    performance_learning = read_json(paths.logs_root / "latest_performance_learning_feedback.json")
    visual_feedback = read_json(paths.logs_root / "latest_visual_strategy_learning_feedback.json")
    visual_performance = read_json(publishing / "latest_post_publish_visual_performance.json")

    articles = list_payload(archive, "articles")
    published = [item for item in articles if item.get("status") == "published"]
    with_metrics = [item for item in published if any((item.get("metrics") or {}).get(key) is not None for key in ("views", "likes", "wows", "shares", "comments"))]
    views = [safe_float((item.get("metrics") or {}).get("views")) for item in with_metrics if (item.get("metrics") or {}).get("views") is not None]
    recommendations: list[dict[str, Any]] = []

    review_summary = metrics_review.get("summary") if isinstance(metrics_review.get("summary"), dict) else {}
    if safe_int(review_summary.get("with_metrics_count")) == 0:
        recommendations.append(
            {
                "recommendation_id": make_id("ppfb", run_date, "metrics_missing"),
                "target_area": "metrics_input",
                "recommendation": "优先为已发布文章补录 views/likes/wows/shares/comments，避免策略反馈只停留在定性层。",
                "reason": "当前 post-publish metrics review 缺少可用指标。",
                "priority": "HIGH",
                "auto_apply": False,
            }
        )
    for item in list_payload(metrics_review, "recommendations")[:6]:
        recommendations.append(
            {
                "recommendation_id": make_id("ppfb", run_date, item.get("recommendation") or item),
                "target_area": item.get("target_area") or "content_strategy",
                "recommendation": item.get("recommendation") or str(item),
                "reason": item.get("reason") or "来自 post-publish metrics review。",
                "priority": "MEDIUM",
                "auto_apply": False,
            }
        )
    for item in list_payload(performance_learning, "recommendations")[:4]:
        recommendations.append(
            {
                "recommendation_id": make_id("ppfb", run_date, "learning", item.get("recommendation")),
                "target_area": item.get("target_area") or "strategy_learning",
                "recommendation": item.get("recommendation") or "",
                "reason": item.get("reason") or "来自 performance learning feedback。",
                "priority": "MEDIUM",
                "auto_apply": False,
            }
        )
    for item in list_payload(visual_feedback, "recommendations")[:4]:
        recommendations.append(
            {
                "recommendation_id": make_id("ppfb", run_date, "visual", item.get("recommendation")),
                "target_area": item.get("target_area") or "visual_strategy",
                "recommendation": item.get("recommendation") or "",
                "reason": item.get("reason") or "来自 visual strategy learning feedback。",
                "priority": "LOW",
                "auto_apply": False,
            }
        )
    if not recommendations:
        recommendations.append(
            {
                "recommendation_id": make_id("ppfb", run_date, "continue"),
                "target_area": "ops_memory",
                "recommendation": "继续积累 publish session、metrics 和 visual performance，等待更多样本后再调整策略。",
                "reason": "当前样本量不足。",
                "priority": "LOW",
                "auto_apply": False,
            }
        )
    deduped = []
    seen = set()
    for item in recommendations:
        key = f"{item.get('target_area')}::{item.get('recommendation')}"
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    visual_records = list_payload(visual_performance, "records")
    summary = {
        "published_article_count": len(published),
        "with_metrics_count": len(with_metrics),
        "average_views": round(sum(views) / len(views), 2) if views else None,
        "content_memory_records": len(list_payload(content_memory, "records")) or len(list_payload(content_memory, "items")),
        "visual_performance_record_count": len(visual_records),
        "recommendation_count": len(deduped),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "summary": summary,
        "top_articles": list_payload(metrics_review, "top_articles")[:5],
        "underperforming_articles": list_payload(metrics_review, "underperforming_articles")[:5],
        "visual_feedback": list_payload(visual_feedback, "visual_type_feedback")[:8],
        "recommendations": deduped,
        "policy": {"advisory_only": True, "auto_apply": False, "no_metrics_scraping": True, "no_strategy_config_changes": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [f"| `{item.get('priority')}` | {item.get('target_area')} | {item.get('recommendation')} | {item.get('reason')} |" for item in list_payload(payload, "recommendations")]
    return f"""# Post-publish Feedback

## Summary

- published_article_count: `{summary.get('published_article_count', 0)}`
- with_metrics_count: `{summary.get('with_metrics_count', 0)}`
- average_views: `{summary.get('average_views')}`
- visual_performance_record_count: `{summary.get('visual_performance_record_count', 0)}`
- recommendation_count: `{summary.get('recommendation_count', 0)}`

| Priority | Target | Recommendation | Reason |
|---|---|---|---|
{chr(10).join(rows)}

No backend scraping, no strategy config changes, no auto publish.
"""
