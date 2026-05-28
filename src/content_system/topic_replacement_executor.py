"""Execute approved topic replacement actions from existing candidates."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
TOPIC_ACTION_TYPES = {"topic_replacement_request", "change_topic"}


@dataclass(frozen=True)
class TopicReplacementExecutorResult:
    run_date: str
    status: str
    replacement_count: int
    output_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "dated_json": root / f"{run_date}__topic-replacements.json",
        "dated_md": root / f"{run_date}__topic-replacements.md",
        "latest_json": root / "latest_topic_replacements.json",
        "latest_md": root / "latest_topic_replacements.md",
    }


def approved_topic_actions(paths: ProjectPaths) -> list[dict[str, Any]]:
    payload = read_json(paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json")
    return [
        action
        for action in list_payload(payload, "actions")
        if action.get("approval_status") == "APPROVED" and action.get("action_type") in TOPIC_ACTION_TYPES
    ]


def tokens(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z][A-Za-z0-9_.-]{2,}|[\u4e00-\u9fff]{2,}", text or "")}


def score_topic(direction: str, topic: dict[str, Any]) -> float:
    wanted = tokens(direction)
    haystack = " ".join(str(topic.get(key) or "") for key in ("theme", "title", "why_it_matters", "recommended_action"))
    overlap = len(wanted & tokens(haystack))
    return overlap * 10 + safe_float(topic.get("total_score") or topic.get("score"))


def replacement_id(run_date: str, action: dict[str, Any]) -> str:
    digest = hashlib.sha1(f"{run_date}|{action.get('action_id')}|{action.get('description')}".encode("utf-8")).hexdigest()[:12]
    return f"trep_{run_date}_{digest}"


def select_topics(direction: str, candidates: list[dict[str, Any]], clusters: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any], str]:
    candidate_rows = sorted(candidates, key=lambda item: score_topic(direction, item), reverse=True)
    if candidate_rows and score_topic(direction, candidate_rows[0]) > 0:
        return candidate_rows[:5], candidate_rows[0], "Selected from high-value candidates."
    cluster_rows = sorted(clusters, key=lambda item: score_topic(direction, item), reverse=True)
    if cluster_rows and score_topic(direction, cluster_rows[0]) > 0:
        return cluster_rows[:5], cluster_rows[0], "Selected from topic clusters."
    return [], {}, "No sufficiently matching local topic found; create research task."


def execute_topic_replacement_actions(paths: ProjectPaths, repo_root: Path) -> tuple[TopicReplacementExecutorResult, dict[str, Any]]:
    approved_payload = read_json(paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json")
    candidates_payload = read_json(paths.market_content_root / "03_topic_candidates" / "latest_high_value_candidates.json")
    clusters_payload = read_json(paths.market_content_root / "03_topic_candidates" / "latest_topic_clusters.json")
    workbench_data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    run_date = str(approved_payload.get("run_date") or candidates_payload.get("run_date") or workbench_data.get("run_date") or today_token()).replace("-", "")[:8]
    candidates = list_payload(candidates_payload, "candidates")
    clusters = list_payload(clusters_payload, "clusters")
    replacements: list[dict[str, Any]] = []
    for action in approved_topic_actions(paths):
        direction = str(action.get("description") or "")
        rows, selected, reason = select_topics(direction, candidates, clusters)
        replacements.append(
            {
                "replacement_id": replacement_id(run_date, action),
                "source_action_id": action.get("action_id"),
                "original_article_id": action.get("target_artifact_id") or workbench_data.get("selected_article_id") or "",
                "requested_direction": direction,
                "candidate_topics": rows[:5],
                "selected_topic": selected,
                "reason": reason,
                "status": "FOUND" if selected else "NEEDS_RESEARCH",
                "next_action": "build_new_brief" if selected else "research_more",
            }
        )
    status = "SUCCESS" if replacements else "SUCCESS_EMPTY"
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "status": status, "replacements": replacements}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return TopicReplacementExecutorResult(run_date, status, len(replacements), repo_relative(outputs["latest_json"], repo_root)), payload


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('replacement_id')}` | `{item.get('source_action_id')}` | `{item.get('status')}` | {item.get('reason')} |"
        for item in list_payload(payload, "replacements")
    ) or "| - | - | SUCCESS_EMPTY | No approved topic replacement actions |"
    return f"""# Topic Replacements

## Summary

- Run date: `{payload.get('run_date')}`
- Status: `{payload.get('status')}`
- Replacements: `{len(list_payload(payload, 'replacements'))}`
- Policy: select from existing candidates/clusters only; no new fetch is executed.

| Replacement | Source Action | Status | Reason |
|---|---|---|---|
{rows}
"""
