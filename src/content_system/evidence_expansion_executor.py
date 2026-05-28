"""Execute approved evidence expansion actions into research plans."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.sources import load_source_registry


SCHEMA_VERSION = "v1"
EVIDENCE_ACTION_TYPES = {"evidence_expansion_request", "research_request"}
KNOWN_TARGETS = ("OpenAI", "Anthropic", "Google", "NVIDIA", "Meta", "Microsoft", "Claude", "Gemini", "AI Agent 浏览器")


@dataclass(frozen=True)
class EvidenceExpansionExecutorResult:
    run_date: str
    status: str
    expansion_count: int
    output_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "dated_json": root / f"{run_date}__evidence-expansion.json",
        "dated_md": root / f"{run_date}__evidence-expansion.md",
        "latest_json": root / "latest_evidence_expansion.json",
        "latest_md": root / "latest_evidence_expansion.md",
    }


def approved_evidence_actions(paths: ProjectPaths) -> list[dict[str, Any]]:
    payload = read_json(paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json")
    return [
        action
        for action in list_payload(payload, "actions")
        if action.get("approval_status") == "APPROVED" and action.get("action_type") in EVIDENCE_ACTION_TYPES
    ]


def extract_requested_sources(description: str) -> list[str]:
    lowered = description.lower()
    targets = [name for name in KNOWN_TARGETS if name.lower() in lowered or name in description]
    return targets or ["official first-party sources"]


def token_set(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z][A-Za-z0-9_.-]{2,}|[\u4e00-\u9fff]{2,}", text or "")}


def find_local_evidence(evidence_packets: list[dict[str, Any]], description: str, article_title: str, limit: int = 6) -> list[dict[str, Any]]:
    wanted = token_set(description) | set(list(token_set(article_title))[:8])
    scored: list[tuple[int, dict[str, Any]]] = []
    for packet in evidence_packets:
        haystack = " ".join(str(packet.get(key) or "") for key in ("title", "summary", "source_id", "source_label", "raw_text_preview"))
        score = len(wanted & token_set(haystack))
        if score:
            scored.append((score, packet))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            "evidence_id": packet.get("evidence_id"),
            "source_id": packet.get("source_id"),
            "title": packet.get("title"),
            "url": packet.get("url"),
            "summary": packet.get("summary"),
        }
        for _, packet in scored[:limit]
    ]


def suggested_source_targets(repo_root: Path, requested_sources: list[str]) -> list[dict[str, Any]]:
    registry = load_source_registry(repo_root=repo_root)
    rows: list[dict[str, Any]] = []
    requested_text = " ".join(requested_sources).lower()
    for source in registry.sources:
        label = f"{source.source_id} {source.label} {source.primary_url}".lower()
        if any(token.lower() in label or token.lower() in requested_text for token in requested_sources):
            rows.append({"source_id": source.source_id, "label": source.label, "primary_url": source.primary_url, "category": source.category})
    return rows[:8]


def expansion_id(run_date: str, action: dict[str, Any]) -> str:
    digest = hashlib.sha1(f"{run_date}|{action.get('action_id')}|{action.get('description')}".encode("utf-8")).hexdigest()[:12]
    return f"evx_{run_date}_{digest}"


def selected_article(workbench_data: dict[str, Any], target_artifact_id: str) -> dict[str, Any]:
    articles = list_payload(workbench_data, "articles")
    for article in articles:
        if target_artifact_id in {article.get("article_id"), article.get("package_id"), article.get("draft_id")}:
            return article
    selected_id = workbench_data.get("selected_article_id")
    for article in articles:
        if article.get("article_id") == selected_id:
            return article
    return articles[0] if articles else {}


def execute_evidence_expansion_actions(paths: ProjectPaths, repo_root: Path) -> tuple[EvidenceExpansionExecutorResult, dict[str, Any]]:
    approved_payload = read_json(paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json")
    workbench_data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    evidence_packets = list_payload(read_json(paths.market_content_root / "03_topic_candidates" / "latest_evidence_packets.json"), "evidence_packets")
    run_date = str(approved_payload.get("run_date") or workbench_data.get("run_date") or today_token()).replace("-", "")[:8]
    expansions: list[dict[str, Any]] = []
    for action in approved_evidence_actions(paths):
        article = selected_article(workbench_data, str(action.get("target_artifact_id") or ""))
        requested = extract_requested_sources(str(action.get("description") or ""))
        local = find_local_evidence(evidence_packets, str(action.get("description") or ""), str(article.get("title") or ""))
        targets = suggested_source_targets(repo_root, requested)
        insertions = [
            f"- {item.get('source_id')}: {item.get('title')} ({item.get('url')})"
            for item in local[:3]
        ]
        expansions.append(
            {
                "expansion_id": expansion_id(run_date, action),
                "source_action_id": action.get("action_id"),
                "target_article_id": article.get("article_id") or action.get("target_artifact_id") or "",
                "requested_sources": requested,
                "available_local_evidence": local,
                "missing_evidence": [] if local else requested,
                "suggested_source_targets": targets,
                "search_tasks": [] if local else [f"Collect recent first-party updates for {name}" for name in requested],
                "article_insertions": insertions,
                "status": "READY" if local else "NEEDS_RESEARCH",
            }
        )
    status = "SUCCESS" if expansions else "SUCCESS_EMPTY"
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "status": status, "expansions": expansions}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return EvidenceExpansionExecutorResult(run_date, status, len(expansions), repo_relative(outputs["latest_json"], repo_root)), payload


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('expansion_id')}` | `{item.get('source_action_id')}` | `{item.get('status')}` | `{len(item.get('available_local_evidence') or [])}` |"
        for item in list_payload(payload, "expansions")
    ) or "| - | - | SUCCESS_EMPTY | 0 |"
    return f"""# Evidence Expansion

## Summary

- Run date: `{payload.get('run_date')}`
- Status: `{payload.get('status')}`
- Expansions: `{len(list_payload(payload, 'expansions'))}`
- Policy: local evidence lookup only; no web fetch is executed.

| Expansion | Source Action | Status | Local Evidence |
|---|---|---|---:|
{rows}
"""
