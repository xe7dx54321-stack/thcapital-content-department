"""Build content operations review for post-publish metrics."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__post-publish-metrics-review.json",
        "dated_md": paths.logs_root / f"{run_date}__post-publish-metrics-review.md",
        "latest_json": paths.logs_root / "latest_post_publish_metrics_review.json",
        "latest_md": paths.logs_root / "latest_post_publish_metrics_review.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__post-publish-metrics-review-board.md",
        "board_latest_md": paths.frontstage_root / "latest_post_publish_metrics_review_board.md",
    }


def metric(article: dict[str, Any], key: str) -> float:
    metrics = article.get("metrics") if isinstance(article.get("metrics"), dict) else {}
    return safe_float(metrics.get(key))


def average(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 2) if values else None


def build_post_publish_metrics_review(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing_root = paths.market_content_root / "07_publishing"
    archive_payload = read_json(publishing_root / "published_article_archive.json")
    visual_feedback_payload = read_json(paths.logs_root / "latest_visual_strategy_learning_feedback.json")
    articles = list_payload(archive_payload, "articles")
    with_metrics = [item for item in articles if isinstance(item.get("metrics"), dict) and item.get("metrics", {}).get("views") is not None]
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for article in articles:
        by_type[str(article.get("content_type") or "unknown")].append(article)
    by_content_type = [
        {"content_type": key, "article_count": len(value), "average_views": average([metric(item, "views") for item in value if metric(item, "views")])}
        for key, value in sorted(by_type.items())
    ]
    top_articles = sorted(with_metrics, key=lambda item: metric(item, "views"), reverse=True)[:5]
    underperforming = sorted([item for item in with_metrics if str(item.get("performance_rating") or "") in {"LOW", "UNKNOWN"}], key=lambda item: metric(item, "views"))[:5]
    insights = []
    if top_articles:
        insights.append(f"Best current article by views: {top_articles[0].get('title') or top_articles[0].get('published_article_id')}.")
    if underperforming:
        insights.append("Some published articles need title/opening or distribution review.")
    if not with_metrics:
        insights.append("No manual metrics have been entered yet; operations review remains qualitative.")
    recommendations = [
        {"recommendation_id": make_id("pmr", run_date, "metrics_input"), "recommendation": "Enter manual post-publish metrics for each manually published article.", "auto_apply": False}
    ]
    for item in list_payload(visual_feedback_payload, "recommendations")[:3]:
        recommendations.append({"recommendation_id": make_id("pmr", run_date, item.get("recommendation_id")), "recommendation": item.get("recommendation") or "", "auto_apply": False})
    views = [metric(item, "views") for item in with_metrics]
    likes = [metric(item, "likes") for item in with_metrics]
    wows = [metric(item, "wows") for item in with_metrics]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "summary": {
            "published_article_count": sum(1 for item in articles if item.get("status") == "published"),
            "with_metrics_count": len(with_metrics),
            "average_views": average(views),
            "average_likes": average(likes),
            "average_wows": average(wows),
            "high_or_excellent_count": sum(1 for item in articles if item.get("performance_rating") in {"HIGH", "EXCELLENT"}),
        },
        "by_content_type": by_content_type,
        "by_visual_type": list_payload(visual_feedback_payload, "visual_type_feedback"),
        "top_articles": top_articles,
        "underperforming_articles": underperforming,
        "insights": insights,
        "recommendations": recommendations,
        "policy": {"manual_metrics_only": True, "no_backend_scraping": True, "auto_apply": False},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    top_rows = "\n".join(
        f"| `{item.get('published_article_id')}` | `{item.get('performance_rating')}` | `{(item.get('metrics') or {}).get('views')}` | {item.get('title') or ''} |"
        for item in list_payload(payload, "top_articles")
    ) or "| - | UNKNOWN | - | No metrics yet |"
    insights = "\n".join(f"- {item}" for item in payload.get("insights", [])) or "- No insights yet."
    return f"""# Post-publish Metrics Review

## Summary

- published_article_count: `{summary.get('published_article_count', 0)}`
- with_metrics_count: `{summary.get('with_metrics_count', 0)}`
- average_views: `{summary.get('average_views')}`
- average_likes: `{summary.get('average_likes')}`
- average_wows: `{summary.get('average_wows')}`
- high_or_excellent_count: `{summary.get('high_or_excellent_count', 0)}`

## Top Articles

| Article | Rating | Views | Title |
|---|---|---:|---|
{top_rows}

## Insights

{insights}
"""
