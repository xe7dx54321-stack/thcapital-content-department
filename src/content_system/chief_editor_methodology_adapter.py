"""Build methodology context for Chief Editor Agent."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.article_quality_methodology import load_article_quality_methodology
from content_system.content_strategy_recipes import load_content_strategy_recipes
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.topic_selection_methodology import load_topic_selection_methodology


SCHEMA_VERSION = "v1"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__chief-editor-methodology-context.json",
        "dated_md": paths.logs_root / f"{run_date}__chief-editor-methodology-context.md",
        "latest_json": paths.logs_root / "latest_chief_editor_methodology_context.json",
        "latest_md": paths.logs_root / "latest_chief_editor_methodology_context.md",
    }


def selected_article_id(workbench_context: dict[str, Any]) -> str:
    article = workbench_context.get("selected_article") if isinstance(workbench_context.get("selected_article"), dict) else {}
    return str(article.get("article_id") or article.get("package_id") or "")


def latest_for(items: list[dict[str, Any]], key: str, value: str) -> dict[str, Any]:
    for item in reversed(items):
        if str(item.get(key) or "") == value:
            return item
    return items[-1] if items else {}


def build_chief_editor_methodology_context(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    workbench_context = read_json(paths.logs_root / "latest_workbench_context.json")
    workbench_data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    topic_scores = read_json(paths.market_content_root / "03_topic_candidates" / "latest_methodology_topic_scores.json")
    article_review = read_json(paths.market_content_root / "05_draft_packs" / "latest_methodology_article_review.json")
    feedback_memory = read_json(paths.market_content_root / "09_workbench_actions" / "workbench_feedback_memory.json")
    performance_memory = read_json(paths.market_content_root / "07_publishing" / "content_performance_memory.json")
    selected_id = selected_article_id(workbench_context) or str(workbench_data.get("selected_article_id") or "")
    selected_article_review = latest_for(list_payload(article_review, "articles"), "article_id", selected_id)
    selected_topic = {}
    selected_article = workbench_context.get("selected_article") if isinstance(workbench_context.get("selected_article"), dict) else {}
    topic_id = str(selected_article.get("topic_id") or "")
    if topic_id:
        selected_topic = latest_for(list_payload(topic_scores, "topics"), "topic_id", topic_id)
    if not selected_topic:
        selected_topic = list_payload(topic_scores, "topics")[0] if list_payload(topic_scores, "topics") else {}
    run_date = str(workbench_data.get("run_date") or topic_scores.get("run_date") or today_token()).replace("-", "")[:8]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "selected_article_id": selected_id,
        "topic_methodology": {
            "dimension_count": len(load_topic_selection_methodology(repo_root).get("core_dimensions") or []),
            "required_questions": load_topic_selection_methodology(repo_root).get("required_questions") or [],
        },
        "article_methodology": {
            "standard_count": len(load_article_quality_methodology(repo_root).get("standards") or []),
            "discouraged_expressions": load_article_quality_methodology(repo_root).get("discouraged_expressions") or [],
        },
        "recipe_registry": {
            "recipe_count": len(load_content_strategy_recipes(repo_root).get("recipes") or []),
            "recipes": [item.get("recipe_id") for item in load_content_strategy_recipes(repo_root).get("recipes") or []],
        },
        "selected_topic_score": selected_topic,
        "selected_article_review": selected_article_review,
        "feedback_preferences": feedback_memory.get("preferences") if isinstance(feedback_memory.get("preferences"), list) else [],
        "performance_summary": performance_memory.get("summary") if isinstance(performance_memory.get("summary"), dict) else {},
        "action_guidance": {
            "generic_feedback": "If user says the article is too generic, inspect judgment_density, core_judgment, generic_language_flags, and rewrite_priorities.",
            "topic_change": "When user asks for a better topic, prefer methodology topic score and reject_flags over raw value score.",
            "title_opening": "When user criticizes title/opening, use article methodology plus recipe title/opening patterns.",
        },
        "policy": {
            "plan_only": True,
            "auto_apply": False,
            "do_not_publish": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    article = payload.get("selected_article_review") if isinstance(payload.get("selected_article_review"), dict) else {}
    topic = payload.get("selected_topic_score") if isinstance(payload.get("selected_topic_score"), dict) else {}
    priorities = "\n".join(f"- {item}" for item in article.get("rewrite_priorities") or []) or "- None"
    return f"""# Chief Editor Methodology Context

## Selected Article

- Article: `{payload.get('selected_article_id')}`
- Article score: `{article.get('methodology_total_score')}`
- Article recommendation: `{article.get('recommendation')}`
- Recipe: `{article.get('recipe_id')}`

## Selected Topic

- Topic: `{topic.get('topic_id')}`
- Topic score: `{topic.get('methodology_total_score')}`
- Topic recommendation: `{topic.get('recommendation')}`

## Rewrite Priorities

{priorities}

## Policy

- plan_only: `true`
- auto_apply: `false`
- do_not_publish: `true`
"""
