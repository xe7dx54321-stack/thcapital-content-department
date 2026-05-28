"""Content strategy recipe loader, validator, and recommendation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "v1"
REQUIRED_RECIPES = (
    "trend_judgment",
    "industry_chain_repricing",
    "company_project_deep_dive",
    "technical_route_analysis",
    "product_strategy_analysis",
    "investment_framework",
)


def config_path(repo_root: Path) -> Path:
    return repo_root / "config" / "content_strategy_recipes.json"


def load_content_strategy_recipes(repo_root: Path) -> dict[str, Any]:
    path = config_path(repo_root)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def recipes_by_id(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = registry.get("recipes")
    items = [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []
    return {str(item.get("recipe_id")): item for item in items if item.get("recipe_id")}


def validate_content_strategy_recipes(registry: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if registry.get("schema_version") != SCHEMA_VERSION:
        issues.append("schema_version must be v1.")
    if not registry.get("version"):
        issues.append("version is required.")
    recipes = recipes_by_id(registry)
    for recipe_id in REQUIRED_RECIPES:
        if recipe_id not in recipes:
            issues.append(f"Missing content strategy recipe: {recipe_id}.")
            continue
        recipe = recipes[recipe_id]
        for key in ("best_for", "not_for", "required_topic_signals", "standard_structure", "title_patterns", "opening_patterns", "common_failures"):
            if not recipe.get(key):
                issues.append(f"{recipe_id}.{key} must be non-empty.")
        evidence = recipe.get("evidence_requirements")
        if not isinstance(evidence, dict):
            issues.append(f"{recipe_id}.evidence_requirements is required.")
        if not isinstance(recipe.get("quality_bar"), dict):
            issues.append(f"{recipe_id}.quality_bar is required.")
    integration = registry.get("pattern_integration")
    if not isinstance(integration, dict) or not integration:
        issues.append("pattern_integration must be configured.")
    return issues


def recommend_recipe_from_scores(scores: dict[str, float], title: str = "") -> str:
    lowered = title.lower()
    if scores.get("industry_chain_impact", 0) >= 7.2:
        return "industry_chain_repricing"
    if scores.get("original_judgment_potential", 0) >= 7.4 and ("投资" in title or "invest" in lowered):
        return "investment_framework"
    if "route" in lowered or "技术" in title or "模型" in title:
        return "technical_route_analysis"
    if "product" in lowered or "产品" in title or "strategy" in lowered:
        return "product_strategy_analysis"
    if "openai" in lowered or "anthropic" in lowered or "google" in lowered or "nvidia" in lowered:
        return "company_project_deep_dive"
    return "trend_judgment"


def methodology_summary(registry: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": registry.get("schema_version"),
        "version": registry.get("version"),
        "recipe_count": len(recipes_by_id(registry)),
        "required_recipe_count": len(REQUIRED_RECIPES),
        "pattern_integration": registry.get("pattern_integration") if isinstance(registry.get("pattern_integration"), dict) else {},
    }
