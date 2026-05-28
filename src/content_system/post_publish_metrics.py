"""Record manually entered post-publish metrics."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, safe_int, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class PostPublishMetricsResult:
    run_date: str
    metrics_count: int
    published_session_count: int
    average_views: float | None
    average_likes: float | None
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__post-publish-metrics.json",
        "dated_md": root / f"{run_date}__post-publish-metrics.md",
        "latest_json": root / "latest_post_publish_metrics.json",
        "latest_md": root / "latest_post_publish_metrics.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__post-publish-metrics-board.md",
        "board_latest_md": paths.frontstage_root / "latest_post_publish_metrics_board.md",
    }


def metrics_id(publish_session_id: str, created_at: str) -> str:
    digest = hashlib.sha1(f"{publish_session_id}|{created_at}".encode("utf-8")).hexdigest()[:12]
    return f"metric_{today_token()}_{digest}"


def performance_rating(views: int | None, likes: int | None, shares: int | None, wows: int | None) -> str:
    if views is None:
        return "UNKNOWN"
    if views >= 5000 or (likes or 0) >= 100 or (shares or 0) >= 30:
        return "EXCELLENT"
    if views >= 1000 or (likes or 0) >= 20 or (wows or 0) >= 10:
        return "HIGH"
    if views >= 200:
        return "MEDIUM"
    return "LOW"


def maybe_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return safe_int(value)


def summarize(metrics: list[dict[str, Any]], sessions: list[dict[str, Any]]) -> dict[str, Any]:
    views = [safe_float(item.get("views")) for item in metrics if item.get("views") is not None]
    likes = [safe_float(item.get("likes")) for item in metrics if item.get("likes") is not None]
    return {
        "metrics_count": len(metrics),
        "published_session_count": sum(1 for item in sessions if item.get("publish_status") == "MANUALLY_PUBLISHED"),
        "average_views": round(sum(views) / len(views), 2) if views else None,
        "average_likes": round(sum(likes) / len(likes), 2) if likes else None,
    }


def load_payload(paths: ProjectPaths) -> dict[str, Any]:
    root = paths.market_content_root / "07_publishing"
    existing = read_json(root / "latest_post_publish_metrics.json")
    sessions = list_payload(read_json(root / "latest_manual_publish_sessions.json"), "sessions")
    metrics = list_payload(existing, "metrics")
    run_date = str(existing.get("run_date") or today_token()).replace("-", "")[:8]
    return {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "metrics": metrics, "summary": summarize(metrics, sessions)}


def session_lookup(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    sessions = list_payload(read_json(paths.market_content_root / "07_publishing" / "latest_manual_publish_sessions.json"), "sessions")
    return {str(item.get("publish_session_id")): item for item in sessions if item.get("publish_session_id")}


def record_post_publish_metrics(
    paths: ProjectPaths,
    repo_root: Path,
    publish_session_id: str = "",
    views: int | None = None,
    likes: int | None = None,
    wows: int | None = None,
    shares: int | None = None,
    saves: int | None = None,
    comments: int | None = None,
    new_followers: int | None = None,
    note: str = "",
    metric_time: str = "",
    hours_after_publish: float | None = None,
) -> tuple[PostPublishMetricsResult, dict[str, Any], bool]:
    payload = load_payload(paths)
    changed = False
    sessions = session_lookup(paths)
    if publish_session_id:
        session = sessions.get(publish_session_id)
        if not session:
            raise ValueError(f"Unknown publish_session_id: {publish_session_id}")
        created_at = utc_now()
        payload["metrics"].append(
            {
                "metrics_id": metrics_id(publish_session_id, created_at),
                "publish_session_id": publish_session_id,
                "final_candidate_id": session.get("final_candidate_id") or "",
                "platform": session.get("platform") or "wechat",
                "metric_time": metric_time,
                "hours_after_publish": hours_after_publish,
                "views": views,
                "likes": likes,
                "wows": wows,
                "shares": shares,
                "saves": saves,
                "comments": comments,
                "new_followers": new_followers,
                "manual_quality_note": note,
                "performance_rating": performance_rating(views, likes, shares, wows),
                "created_at": created_at,
            }
        )
        changed = True
    sessions_list = list(sessions.values())
    payload["summary"] = summarize(list_payload(payload, "metrics"), sessions_list)
    result = write_post_publish_metrics(payload, paths, repo_root)
    return result, payload, changed


def write_post_publish_metrics(payload: dict[str, Any], paths: ProjectPaths, repo_root: Path) -> PostPublishMetricsResult:
    run_date = str(payload.get("run_date") or today_token()).replace("-", "")[:8]
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return PostPublishMetricsResult(
        run_date,
        int(summary.get("metrics_count", 0)),
        int(summary.get("published_session_count", 0)),
        summary.get("average_views"),
        summary.get("average_likes"),
        repo_relative(outputs["latest_json"], repo_root),
        repo_relative(outputs["board_latest_md"], repo_root),
    )


def build_post_publish_metrics_board(paths: ProjectPaths, repo_root: Path) -> tuple[PostPublishMetricsResult, dict[str, Any]]:
    payload = load_payload(paths)
    return write_post_publish_metrics(payload, paths, repo_root), payload


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('metrics_id')}` | `{item.get('publish_session_id')}` | `{item.get('performance_rating')}` | `{item.get('views')}` | `{item.get('likes')}` | `{item.get('wows')}` |"
        for item in list_payload(payload, "metrics")
    ) or "| - | - | UNKNOWN | - | - | - |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Post-publish Metrics Board

## Summary

- Metrics: `{summary.get('metrics_count', 0)}`
- Published sessions: `{summary.get('published_session_count', 0)}`
- Average views: `{summary.get('average_views')}`
- Average likes: `{summary.get('average_likes')}`
- Policy: all metrics are manually entered; no backend scraping.

| Metrics | Session | Rating | Views | Likes | Wows |
|---|---|---|---:|---:|---:|
{rows}
"""
