"""Build multi-day analytics for article versions and final candidates."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class MultidayVersionAnalyticsResult:
    run_date: str
    version_count: int
    final_candidate_count: int
    quality_trend: str
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__multiday-version-analytics.json",
        "dated_md": paths.logs_root / f"{run_date}__multiday-version-analytics.md",
        "latest_json": paths.logs_root / "latest_multiday_version_analytics.json",
        "latest_md": paths.logs_root / "latest_multiday_version_analytics.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__multiday-version-analytics-board.md",
        "board_latest_md": paths.frontstage_root / "latest_multiday_version_analytics_board.md",
    }


def quality_trend(version_count: int, average_delta: float) -> str:
    if version_count < 2:
        return "INSUFFICIENT_DATA"
    if average_delta > 2:
        return "IMPROVING"
    if average_delta < -2:
        return "REGRESSING"
    return "STABLE"


def build_multiday_version_analytics(paths: ProjectPaths, repo_root: Path) -> tuple[MultidayVersionAnalyticsResult, dict[str, Any]]:
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    article_memory = read_json(versions_root / "article_version_memory.json")
    final_memory = read_json(paths.market_content_root / "07_publishing" / "final_candidate_memory.json")
    effectiveness = read_json(paths.logs_root / "latest_action_effectiveness_analytics.json")
    feedback = read_json(paths.market_content_root / "09_workbench_actions" / "workbench_feedback_memory.json")
    run_date = today_token()
    versions = list_payload(article_memory, "versions")
    final_candidates = list_payload(final_memory, "final_candidates")
    deltas = [safe_float(item.get("score_delta")) for item in versions]
    average_delta = round(sum(deltas) / len(deltas), 2) if deltas else 0
    promoted_count = len(final_candidates)
    accepted_count = max(sum(1 for item in versions if item.get("human_decision") == "ACCEPT"), promoted_count)
    trend = quality_trend(len(versions), average_delta)
    summary = {
        "version_count": len(versions),
        "accepted_count": accepted_count,
        "promoted_count": promoted_count,
        "final_candidate_count": len(final_candidates),
        "average_score_delta": average_delta,
        "quality_trend": trend,
    }
    effective_patterns = list_payload(effectiveness, "effective_patterns")
    risk_patterns = list_payload(effectiveness, "problem_patterns")
    recommendations = []
    if trend == "IMPROVING":
        recommendations.append("Continue using accepted action patterns while preserving human final review.")
    elif trend == "REGRESSING":
        recommendations.append("Pause promotion expansion and review rewrite/prompt changes.")
    else:
        recommendations.append("Collect more accepted/rejected version outcomes before making rule changes.")
    if list_payload(feedback, "preferences"):
        recommendations.append("Use workbench feedback preferences when selecting future final candidates.")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "summary": summary,
        "by_action_type": list_payload(effectiveness, "by_action_type"),
        "effective_patterns": effective_patterns,
        "risk_patterns": risk_patterns,
        "recommendations": recommendations,
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        MultidayVersionAnalyticsResult(run_date, summary["version_count"], summary["final_candidate_count"], trend, repo_relative(outputs["latest_json"], repo_root), repo_relative(outputs["board_latest_md"], repo_root)),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('action_type')}` | `{item.get('count')}` | `{item.get('average_score_delta')}` | `{item.get('accepted_count')}` | `{item.get('rejected_count')}` |"
        for item in list_payload(payload, "by_action_type")
    ) or "| - | 0 | 0 | 0 | 0 |"
    recommendations = "\n".join(f"- {item}" for item in payload.get("recommendations", [])) or "- No recommendations yet."
    return f"""# Multi-day Version Analytics

## Summary

- Run date: `{payload.get('run_date')}`
- Versions: `{summary.get('version_count', 0)}`
- Accepted: `{summary.get('accepted_count', 0)}`
- Promoted: `{summary.get('promoted_count', 0)}`
- Final candidates: `{summary.get('final_candidate_count', 0)}`
- Average score delta: `{summary.get('average_score_delta', 0)}`
- Quality trend: `{summary.get('quality_trend')}`

## By Action Type

| Action Type | Count | Avg Delta | Accepted | Rejected |
|---|---:|---:|---:|---:|
{rows}

## Recommendations

{recommendations}
"""
