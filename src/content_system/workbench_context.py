"""Build context for the Chief Editor Agent."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.sources import load_source_registry


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class WorkbenchContextResult:
    run_date: str
    selected_article_id: str
    outputs: dict[str, str]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__workbench-context.json",
        "latest_json": paths.logs_root / "latest_workbench_context.json",
        "dated_md": paths.logs_root / f"{run_date}__workbench-context.md",
        "latest_md": paths.logs_root / "latest_workbench_context.md",
    }


def selected_article(data: dict[str, Any]) -> dict[str, Any]:
    selected_id = str(data.get("selected_article_id") or "")
    for article in data.get("articles", []) if isinstance(data.get("articles"), list) else []:
        if isinstance(article, dict) and article.get("article_id") == selected_id:
            return article
    articles = data.get("articles")
    return articles[0] if isinstance(articles, list) and articles and isinstance(articles[0], dict) else {}


def by_package(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item.get("package_id")): item for item in items if item.get("package_id")}


def source_guidance(repo_root: Path) -> dict[str, list[dict[str, Any]]]:
    registry = load_source_registry(repo_root=repo_root)
    grouped: dict[str, list[dict[str, Any]]] = {"official": [], "developer_community": [], "research": [], "chinese_media": []}
    for source in registry.sources:
        if source.category in grouped:
            grouped[source.category].append(
                {
                    "source_id": source.source_id,
                    "label": source.label,
                    "tier": source.tier,
                    "primary_url": source.primary_url,
                    "enabled": source.enabled,
                }
            )
    return grouped


def build_workbench_context(paths: ProjectPaths, repo_root: Path) -> dict[str, Any]:
    data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    run_date = str(data.get("run_date") or today_token()).replace("-", "")[:8]
    article = selected_article(data)
    package_id = str(article.get("package_id") or "")
    review_root = paths.market_content_root / "06_review_queue"
    proponent = by_package(list_payload(read_json(review_root / "latest_proponent_reviews.json"), "reviews"))
    critic = by_package(list_payload(read_json(review_root / "latest_critic_reviews.json"), "reviews"))
    judge = by_package(list_payload(read_json(review_root / "latest_judge_gate.json"), "decisions"))
    revision = by_package(list_payload(read_json(review_root / "latest_revision_instructions.json"), "instructions"))
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "selected_article": article,
        "available_topics": data.get("topics") or [],
        "available_evidence": list_payload(read_json(paths.market_content_root / "03_topic_candidates" / "latest_evidence_packets.json"), "evidence_packets")[:20],
        "agent_reviews": {
            "proponent": proponent.get(package_id, {}),
            "critic": critic.get(package_id, {}),
            "judge": judge.get(package_id, {}),
            "revision": revision.get(package_id, {}),
        },
        "system_capabilities": [
            "change_topic",
            "rewrite_angle",
            "strengthen_evidence",
            "rewrite_title",
            "rewrite_opening",
            "approve",
            "hold",
            "create_research_request",
        ],
        "source_guidance": source_guidance(repo_root),
        "routing_guidance": {
            "change_topic": "topic_replacement_request",
            "rewrite_angle": "rewrite_instruction",
            "strengthen_evidence": "evidence_expansion_request",
            "rewrite_title": "title_rewrite_request",
            "rewrite_opening": "opening_rewrite_request",
            "approve": "publishing_status_update",
            "hold": "publishing_status_update",
        },
        "runtime_store_summary": read_json(paths.logs_root / "latest_runtime_store_summary.json").get("summary") or {},
        "artifact_repository_summary": read_json(paths.logs_root / "latest_artifact_repository_summary.json").get("summary") or {},
        "weekly_retro_markdown": (paths.frontstage_root / "latest_weekly_content_retro.md").read_text(encoding="utf-8")[:4000]
        if (paths.frontstage_root / "latest_weekly_content_retro.md").exists()
        else "",
        "pattern_adapters": list_payload(read_json(paths.market_content_root / "08_learning_patterns" / "latest_pattern_adapters.json"), "adapters"),
    }
    return payload


def render_markdown(context: dict[str, Any]) -> str:
    article = context.get("selected_article") if isinstance(context.get("selected_article"), dict) else {}
    topics = context.get("available_topics") if isinstance(context.get("available_topics"), list) else []
    capabilities = "\n".join(f"- `{item}`" for item in context.get("system_capabilities", []))
    topic_lines = "\n".join(f"- {item.get('title')} ({item.get('score_band')}, {item.get('score')})" for item in topics[:8]) or "- None"
    return f"""# Workbench Context

## Selected Article

- Article: `{article.get('article_id', '')}`
- Title: {article.get('wechat_title') or article.get('title') or ''}
- Status: `{article.get('status', '')}`
- Judge: `{article.get('judge_decision', '')}`

## Available Topics

{topic_lines}

## System Capabilities

{capabilities}
"""


def write_workbench_context(context: dict[str, Any], paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    run_date = str(context.get("run_date") or today_token()).replace("-", "")[:8]
    outputs = output_paths(paths, run_date)
    return write_json_and_markdown(context, render_markdown(context), outputs)


def build_and_write_workbench_context(paths: ProjectPaths, repo_root: Path) -> WorkbenchContextResult:
    context = build_workbench_context(paths, repo_root)
    outputs = write_workbench_context(context, paths, repo_root)
    article = context.get("selected_article") if isinstance(context.get("selected_article"), dict) else {}
    return WorkbenchContextResult(
        str(context.get("run_date") or today_token()),
        str(article.get("article_id") or ""),
        {key: repo_relative(path, repo_root) for key, path in outputs.items()},
    )
