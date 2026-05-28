"""Analyze whether approved workbench actions improve article versions."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class ActionEffectivenessResult:
    run_date: str
    action_count: int
    version_count: int
    average_score_delta: float
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__action-effectiveness-analytics.json",
        "dated_md": paths.logs_root / f"{run_date}__action-effectiveness-analytics.md",
        "latest_json": paths.logs_root / "latest_action_effectiveness_analytics.json",
        "latest_md": paths.logs_root / "latest_action_effectiveness_analytics.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__action-effectiveness-analytics-board.md",
        "board_latest_md": paths.frontstage_root / "latest_action_effectiveness_analytics_board.md",
    }


def by_key(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def build_action_effectiveness_analytics(paths: ProjectPaths, repo_root: Path) -> tuple[ActionEffectivenessResult, dict[str, Any]]:
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    memory = read_json(versions_root / "article_version_memory.json")
    comparisons = read_json(versions_root / "latest_version_comparison_scores.json")
    decisions = read_json(versions_root / "latest_version_review_decisions.json")
    approved = read_json(paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json")
    feedback = read_json(paths.market_content_root / "09_workbench_actions" / "workbench_feedback_memory.json")
    run_date = str(comparisons.get("run_date") or approved.get("run_date") or today_token()).replace("-", "")[:8]
    actions_by_id = by_key(list_payload(approved, "actions"), "action_id")
    versions = list_payload(memory, "versions")
    decisions_by_version = by_key(list_payload(decisions, "decisions"), "version_id")

    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for version in versions:
        action = actions_by_id.get(str(version.get("source_action_id") or ""), {})
        action_type = str(action.get("action_type") or version.get("version_type") or "unknown")
        buckets[action_type].append({**version, "action": action, "decision": decisions_by_version.get(str(version.get("version_id") or ""), {})})

    by_action_type: list[dict[str, Any]] = []
    for action_type, rows in sorted(buckets.items()):
        deltas = [safe_float(item.get("score_delta")) for item in rows]
        accepted = sum(1 for item in rows if item.get("human_decision") == "ACCEPT")
        rejected = sum(1 for item in rows if item.get("human_decision") == "REJECT")
        revise_more = sum(1 for item in rows if item.get("human_decision") == "REVISE_MORE")
        by_action_type.append(
            {
                "action_type": action_type,
                "count": len(rows),
                "average_score_delta": round(sum(deltas) / len(deltas), 2) if deltas else 0,
                "accepted_count": accepted,
                "rejected_count": rejected,
                "revise_more_count": revise_more,
                "unreviewed_count": sum(1 for item in rows if item.get("human_decision") == "UNREVIEWED"),
            }
        )

    deltas = [safe_float(item.get("score_delta")) for item in versions]
    summary = {
        "action_count": len(list_payload(approved, "actions")),
        "version_count": len(versions),
        "accepted_count": sum(1 for item in versions if item.get("human_decision") == "ACCEPT"),
        "rejected_count": sum(1 for item in versions if item.get("human_decision") == "REJECT"),
        "average_score_delta": round(sum(deltas) / len(deltas), 2) if deltas else 0,
    }
    effective_patterns = [
        {
            "pattern": item["action_type"],
            "reason": f"Average score delta {item['average_score_delta']} with {item['accepted_count']} accepted versions.",
        }
        for item in by_action_type
        if safe_float(item.get("average_score_delta")) > 0 or item.get("accepted_count", 0) > 0
    ]
    problem_patterns = [
        {
            "pattern": item["action_type"],
            "reason": f"Average score delta {item['average_score_delta']} with {item['rejected_count']} rejected versions.",
        }
        for item in by_action_type
        if safe_float(item.get("average_score_delta")) < 0 or item.get("rejected_count", 0) > 0
    ]
    preferences = list_payload(feedback, "preferences")
    recommendations = []
    if effective_patterns:
        recommendations.append("Keep successful action patterns as references for Chief Editor routing.")
    if problem_patterns:
        recommendations.append("Review weak action patterns before reusing them in rewrite prompts.")
    if not versions:
        recommendations.append("No version outcomes yet; collect human accept/reject decisions before changing rules.")
    if preferences:
        recommendations.append("Compare version outcomes with workbench feedback preferences before updating prompts.")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "summary": summary,
        "by_action_type": by_action_type,
        "effective_patterns": effective_patterns,
        "problem_patterns": problem_patterns,
        "recommendations": recommendations,
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        ActionEffectivenessResult(
            run_date,
            summary["action_count"],
            summary["version_count"],
            summary["average_score_delta"],
            repo_relative(outputs["latest_json"], repo_root),
            repo_relative(outputs["board_latest_md"], repo_root),
        ),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('action_type')}` | `{item.get('count')}` | `{item.get('average_score_delta')}` | `{item.get('accepted_count')}` | `{item.get('rejected_count')}` |"
        for item in list_payload(payload, "by_action_type")
    ) or "| - | 0 | 0 | 0 | 0 |"
    effective = "\n".join(f"- {item.get('pattern')}: {item.get('reason')}" for item in list_payload(payload, "effective_patterns")) or "- None yet."
    problem = "\n".join(f"- {item.get('pattern')}: {item.get('reason')}" for item in list_payload(payload, "problem_patterns")) or "- None yet."
    recommendations = "\n".join(f"- {item}" for item in payload.get("recommendations", [])) or "- Keep collecting version outcomes."
    return f"""# Action Effectiveness Analytics

## Summary

- Run date: `{payload.get('run_date')}`
- Actions: `{summary.get('action_count', 0)}`
- Versions: `{summary.get('version_count', 0)}`
- Accepted: `{summary.get('accepted_count', 0)}`
- Rejected: `{summary.get('rejected_count', 0)}`
- Average score delta: `{summary.get('average_score_delta', 0)}`

## By Action Type

| Action Type | Count | Avg Delta | Accepted | Rejected |
|---|---:|---:|---:|---:|
{rows}

## Effective Patterns

{effective}

## Problem Patterns

{problem}

## Recommendations

{recommendations}
"""
