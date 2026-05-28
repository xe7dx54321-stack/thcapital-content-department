"""Persist manually entered content performance as local memory."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class ContentPerformanceMemoryResult:
    record_count: int
    high_or_excellent_count: int
    low_count: int
    average_views: float | None
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "memory_json": root / "content_performance_memory.json",
        "memory_md": root / "content_performance_memory.md",
        "board_md": paths.frontstage_root / "content_performance_memory_board.md",
    }


def by_key(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def performance_record_id(metrics_id: str, final_candidate_id: str) -> str:
    digest = hashlib.sha1(f"{metrics_id}|{final_candidate_id}".encode("utf-8")).hexdigest()[:12]
    return f"perf_{digest}"


def title_pattern(title: str) -> str:
    lowered = title.lower()
    if "投资" in title or "investor" in lowered:
        return "investor_angle"
    if "为什么" in title or "why" in lowered or "?" in title or "？" in title:
        return "question_hook"
    if "如何" in title or "怎么" in title or "how" in lowered:
        return "how_to"
    if "机会" in title or "风险" in title:
        return "opportunity_risk"
    return "signal_analysis"


def opening_pattern(body: str) -> str:
    first = ""
    for raw in body.splitlines():
        text = raw.strip()
        if text and not text.startswith("#") and not text.startswith("- "):
            first = text
            break
    if re.search(r"判断|结论|核心", first):
        return "judgment_first"
    if re.search(r"数据|证据|来源|官方|OpenAI|Anthropic|Google|NVIDIA", first, re.I):
        return "evidence_first"
    if re.search(r"为什么|问题|[?？]", first):
        return "question_first"
    return "context_first" if first else ""


def lessons_for(metric: dict[str, Any], candidate: dict[str, Any], version: dict[str, Any]) -> list[str]:
    rating = str(metric.get("performance_rating") or "UNKNOWN")
    lessons: list[str] = []
    title = str(candidate.get("title") or "")
    body = str(candidate.get("body_markdown") or candidate.get("wechat_body_markdown") or "")
    version_type = str(version.get("version_type") or "")
    if rating in {"HIGH", "EXCELLENT"} and version_type == "rewrite":
        lessons.append("High-performing rewritten final candidate; preserve the accepted rewrite pattern for future reference.")
    if rating in {"HIGH", "EXCELLENT"} and ("投资" in title or "投资人" in body):
        lessons.append("Investor-angle framing may improve WeChat performance for this content type.")
    if rating == "LOW" and re.search(r"证据|来源|https?://", body, re.I):
        lessons.append("Strong evidence alone did not drive performance; inspect title and opening hook.")
    if rating == "LOW" and len(body) > 3500:
        lessons.append("Long article underperformed; consider tighter structure and stronger opening.")
    return lessons or ["Keep performance record as neutral evidence until more manual metrics are entered."]


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    views = [safe_float(item.get("views")) for item in records if item.get("views") is not None]
    return {
        "record_count": len(records),
        "high_or_excellent_count": sum(1 for item in records if item.get("performance_rating") in {"HIGH", "EXCELLENT"}),
        "low_count": sum(1 for item in records if item.get("performance_rating") == "LOW"),
        "average_views": round(sum(views) / len(views), 2) if views else None,
    }


def update_content_performance_memory(paths: ProjectPaths, repo_root: Path) -> tuple[ContentPerformanceMemoryResult, dict[str, Any]]:
    root = paths.market_content_root / "07_publishing"
    metrics_payload = read_json(root / "latest_post_publish_metrics.json")
    sessions = by_key(list_payload(read_json(root / "latest_manual_publish_sessions.json"), "sessions"), "publish_session_id")
    candidates = by_key(list_payload(read_json(root / "latest_final_article_candidates.json"), "candidates"), "final_candidate_id")
    final_memory = by_key(list_payload(read_json(root / "final_candidate_memory.json"), "final_candidates"), "final_candidate_id")
    version_memory = by_key(list_payload(read_json(paths.market_content_root / "09_workbench_actions" / "versions" / "article_version_memory.json"), "versions"), "version_id")
    existing = read_json(root / "content_performance_memory.json")
    records = by_key(list_payload(existing, "records"), "performance_record_id")
    for metric in list_payload(metrics_payload, "metrics"):
        session = sessions.get(str(metric.get("publish_session_id") or ""), {})
        final_candidate_id = str(metric.get("final_candidate_id") or session.get("final_candidate_id") or "")
        candidate = candidates.get(final_candidate_id) or final_memory.get(final_candidate_id) or {}
        version_id = str(candidate.get("version_id") or session.get("version_id") or "")
        version = version_memory.get(version_id, {})
        title = str(candidate.get("wechat_title") or candidate.get("title") or "")
        body = str(candidate.get("wechat_body_markdown") or candidate.get("body_markdown") or "")
        record = {
            "performance_record_id": performance_record_id(str(metric.get("metrics_id") or ""), final_candidate_id),
            "final_candidate_id": final_candidate_id,
            "publish_session_id": metric.get("publish_session_id") or "",
            "version_id": version_id,
            "title": title,
            "platform": metric.get("platform") or "wechat",
            "performance_rating": metric.get("performance_rating") or "UNKNOWN",
            "views": metric.get("views"),
            "likes": metric.get("likes"),
            "wows": metric.get("wows"),
            "shares": metric.get("shares"),
            "saves": metric.get("saves"),
            "comments": metric.get("comments"),
            "new_followers": metric.get("new_followers"),
            "topic_tags": [],
            "action_types": [version.get("version_type") or "unknown"],
            "title_pattern": title_pattern(title),
            "opening_pattern": opening_pattern(body),
            "lessons": lessons_for(metric, candidate, version),
            "status": "active",
        }
        if record["performance_record_id"]:
            records[str(record["performance_record_id"])] = record
    ordered = sorted(records.values(), key=lambda item: str(item.get("performance_record_id") or ""))
    summary = summarize(ordered)
    payload = {"schema_version": SCHEMA_VERSION, "updated_at": utc_now(), "records": ordered, "summary": summary}
    outputs = output_paths(paths)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        ContentPerformanceMemoryResult(
            summary["record_count"],
            summary["high_or_excellent_count"],
            summary["low_count"],
            summary["average_views"],
            repo_relative(outputs["memory_json"], repo_root),
            repo_relative(outputs["board_md"], repo_root),
        ),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('performance_record_id')}` | `{item.get('final_candidate_id')}` | `{item.get('performance_rating')}` | `{item.get('views')}` | `{item.get('title_pattern')}` | {item.get('title') or ''} |"
        for item in list_payload(payload, "records")
    ) or "| - | - | UNKNOWN | - | - | No performance records |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    lessons = []
    for item in list_payload(payload, "records")[-8:]:
        for lesson in item.get("lessons") or []:
            lessons.append(f"- `{item.get('performance_record_id')}`: {lesson}")
    lessons_text = "\n".join(lessons) if lessons else "- No lessons yet."
    return f"""# Content Performance Memory

## Summary

- Records: `{summary.get('record_count', 0)}`
- High or excellent: `{summary.get('high_or_excellent_count', 0)}`
- Low: `{summary.get('low_count', 0)}`
- Average views: `{summary.get('average_views')}`

| Record | Final Candidate | Rating | Views | Title Pattern | Title |
|---|---|---|---:|---|---|
{rows}

## Lessons

{lessons_text}
"""
