"""Build human methodology calibration board."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__human-methodology-calibration-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_human_methodology_calibration_board.md",
        "dated_json": paths.logs_root / f"{run_date}__human-methodology-calibration.json",
        "latest_json": paths.logs_root / "latest_human_methodology_calibration.json",
    }


def build_human_methodology_calibration(paths: ProjectPaths) -> tuple[dict[str, Any], dict[str, Path]]:
    topic_payload = read_json(paths.market_content_root / "03_topic_candidates" / "latest_methodology_topic_scores.json")
    article_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_article_review.json")
    visual_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_article_visual_plans.json")
    image_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_image_asset_requests.json")
    regression_payload = read_json(paths.logs_root / "latest_methodology_regression_tests.json")
    alignment_payload = read_json(paths.logs_root / "latest_methodology_performance_alignment.json")
    run_date = str(topic_payload.get("run_date") or article_payload.get("run_date") or today_token()).replace("-", "")[:8]
    topics = list_payload(topic_payload, "topics")
    articles = list_payload(article_payload, "articles")
    visual_plans = list_payload(visual_payload, "visual_plans")
    requests = list_payload(image_payload, "requests")
    questions = [
        "系统推荐 WRITE/WATCH/HOLD 的边界是否符合你的主编判断？",
        "文章弱点排序是否符合真实改稿优先级？",
        "推荐 recipe 是否适合该选题？",
        "视觉计划是否服务核心判断，而不是装饰？",
        "图片 prompt 是否符合专业、克制、高级的公众号气质？",
    ]
    summary = {
        "topic_count": len(topics),
        "article_count": len(articles),
        "visual_plan_count": len(visual_plans),
        "image_request_count": len(requests),
        "regression_fail_count": (regression_payload.get("summary") or {}).get("fail_count", 0) if isinstance(regression_payload.get("summary"), dict) else 0,
        "alignment_insight_count": (alignment_payload.get("summary") or {}).get("insight_count", 0) if isinstance(alignment_payload.get("summary"), dict) else 0,
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "summary": summary,
        "write_topics": [item for item in topics if item.get("recommendation") == "WRITE"],
        "watch_or_hold_topics": [item for item in topics if item.get("recommendation") in {"WATCH", "HOLD"}],
        "article_weaknesses": articles[:10],
        "visual_plans": visual_plans[:10],
        "image_requests": requests[:12],
        "calibration_questions": questions,
        "policy": {"auto_apply": False, "human_calibration_required": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    questions = "\n".join(f"- {item}" for item in payload.get("calibration_questions") or [])
    topic_rows = "\n".join(
        f"| `{item.get('topic_id')}` | {item.get('methodology_total_score')} | `{item.get('recommendation')}` | `{item.get('recommended_recipe_id')}` | {item.get('title')} |"
        for item in (payload.get("write_topics") or payload.get("watch_or_hold_topics") or [])[:12]
    ) or "| - | 0 | - | - | No topics |"
    visual_rows = "\n".join(
        f"| `{item.get('visual_plan_id')}` | {item.get('recommended_visual_count')} | {item.get('title')} |"
        for item in payload.get("visual_plans") or []
    ) or "| - | 0 | No visual plans |"
    return f"""# Human Methodology Calibration Board

## Summary

- topic_count: `{summary.get('topic_count', 0)}`
- article_count: `{summary.get('article_count', 0)}`
- visual_plan_count: `{summary.get('visual_plan_count', 0)}`
- image_request_count: `{summary.get('image_request_count', 0)}`
- regression_fail_count: `{summary.get('regression_fail_count', 0)}`
- alignment_insight_count: `{summary.get('alignment_insight_count', 0)}`

## Topics To Calibrate

| Topic | Score | Recommendation | Recipe | Title |
|---|---:|---|---|---|
{topic_rows}

## Visual Plans

| Plan | Visuals | Title |
|---|---:|---|
{visual_rows}

## Questions For Human Calibration

{questions}

## Policy

- `auto_apply=false`
- No prompt/config/rule changes are applied automatically.
"""
