"""Persist published article archive metadata."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "memory_json": root / "published_article_archive.json",
        "memory_md": root / "published_article_archive.md",
        "board_md": paths.frontstage_root / "published_article_archive_board.md",
    }


def make_archive_id(session_id: str, copy_pack_id: str) -> str:
    digest = hashlib.sha1(f"{session_id}|{copy_pack_id}".encode("utf-8")).hexdigest()[:12]
    return f"pubart_{digest}"


def latest_metric_for(metrics: list[dict[str, Any]], session_id: str, final_candidate_id: str) -> dict[str, Any]:
    matched = [item for item in metrics if item.get("publish_session_id") == session_id or item.get("final_candidate_id") == final_candidate_id]
    return matched[-1] if matched else {}


def visual_for_session(records: list[dict[str, Any]], session_id: str, copy_pack_id: str) -> dict[str, Any]:
    return next((item for item in reversed(records) if item.get("publish_session_id") == session_id or item.get("copy_pack_id") == copy_pack_id), {})


def summarize(articles: list[dict[str, Any]]) -> dict[str, Any]:
    views = [safe_float(item.get("metrics", {}).get("views")) for item in articles if isinstance(item.get("metrics"), dict) and item.get("metrics", {}).get("views") is not None]
    return {
        "article_count": len(articles),
        "published_count": sum(1 for item in articles if item.get("status") == "published"),
        "planned_count": sum(1 for item in articles if item.get("status") == "planned"),
        "average_views": round(sum(views) / len(views), 2) if views else None,
        "high_or_excellent_count": sum(1 for item in articles if item.get("performance_rating") in {"HIGH", "EXCELLENT"}),
    }


def status_from_session(session: dict[str, Any]) -> str:
    return {
        "MANUALLY_PUBLISHED": "published",
        "PLANNED": "planned",
        "DEFERRED": "deferred",
        "CANCELLED": "cancelled",
    }.get(str(session.get("publish_status") or ""), "unknown")


def update_published_article_archive(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    publishing_root = paths.market_content_root / "07_publishing"
    sessions = list_payload(read_json(publishing_root / "latest_manual_publish_sessions.json"), "sessions")
    packs = list_payload(read_json(publishing_root / "latest_wechat_copy_pack_with_images.json"), "packs")
    metrics = list_payload(read_json(publishing_root / "latest_post_publish_metrics.json"), "metrics")
    visual_records = list_payload(read_json(publishing_root / "latest_post_publish_visual_performance.json"), "records")
    performance_memory = list_payload(read_json(publishing_root / "content_performance_memory.json"), "records")
    assets = list_payload(read_json(paths.market_content_root / "08_assets" / "image_asset_library.json"), "assets")
    pack = packs[0] if packs else {}
    articles = []
    for session in sessions:
        final_candidate_id = str(session.get("final_candidate_id") or "")
        copy_pack_id = str(pack.get("copy_pack_id") or "")
        metric = latest_metric_for(metrics, str(session.get("publish_session_id") or ""), final_candidate_id)
        visual_record = visual_for_session(visual_records, str(session.get("publish_session_id") or ""), copy_pack_id)
        perf = next((item for item in performance_memory if item.get("publish_session_id") == session.get("publish_session_id")), {})
        visual_asset_ids = [str(item.get("asset_id")) for item in assets if item.get("article_id") == final_candidate_id and item.get("asset_id")]
        articles.append(
            {
                "published_article_id": make_archive_id(str(session.get("publish_session_id") or ""), copy_pack_id),
                "publish_session_id": session.get("publish_session_id") or "",
                "copy_pack_id": copy_pack_id,
                "final_candidate_id": final_candidate_id,
                "title": pack.get("title_to_copy") or perf.get("title") or "",
                "platform": session.get("platform") or "wechat",
                "published_url": session.get("published_url") or "",
                "published_at": session.get("actual_publish_at") or "",
                "content_type": perf.get("action_types", ["unknown"])[0] if isinstance(perf.get("action_types"), list) and perf.get("action_types") else "unknown",
                "topic_tags": perf.get("topic_tags") or [],
                "visual_asset_ids": visual_asset_ids,
                "metrics": {
                    "views": metric.get("views"),
                    "likes": metric.get("likes"),
                    "wows": metric.get("wows"),
                    "shares": metric.get("shares"),
                    "comments": metric.get("comments"),
                },
                "visual_performance": visual_record,
                "performance_rating": metric.get("performance_rating") or perf.get("performance_rating") or "UNKNOWN",
                "lessons": perf.get("lessons") or [],
                "status": status_from_session(session),
            }
        )
    payload = {"schema_version": SCHEMA_VERSION, "updated_at": utc_now(), "articles": articles, "summary": summarize(articles)}
    outputs = output_paths(paths)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('published_article_id')}` | `{item.get('status')}` | `{item.get('performance_rating')}` | `{(item.get('metrics') or {}).get('views')}` | {item.get('title') or ''} |"
        for item in list_payload(payload, "articles")
    ) or "| - | - | UNKNOWN | - | No published article archive records |"
    return f"""# Published Article Archive

## Summary

- article_count: `{summary.get('article_count', 0)}`
- published_count: `{summary.get('published_count', 0)}`
- planned_count: `{summary.get('planned_count', 0)}`
- average_views: `{summary.get('average_views')}`
- high_or_excellent_count: `{summary.get('high_or_excellent_count', 0)}`

| Article | Status | Rating | Views | Title |
|---|---|---|---:|---|
{rows}
"""
