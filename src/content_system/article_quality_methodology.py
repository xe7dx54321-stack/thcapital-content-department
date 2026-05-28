"""Article quality methodology loader, validator, and text helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "v1"
REQUIRED_STANDARDS = (
    "clear_question",
    "core_judgment",
    "logic_progression",
    "evidence_fit",
    "narrative_tension",
    "reader_relevance",
    "judgment_density",
    "risk_balance",
    "wechat_readability",
    "memorability",
)
REQUIRED_COMPONENTS = ("hook", "judgment", "evidence_chain", "implication", "risk", "closing_framework")


def config_path(repo_root: Path) -> Path:
    return repo_root / "config" / "article_quality_methodology.json"


def load_article_quality_methodology(repo_root: Path) -> dict[str, Any]:
    path = config_path(repo_root)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def standards_by_id(methodology: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = methodology.get("standards")
    items = [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []
    return {str(item.get("standard_id")): item for item in items if item.get("standard_id")}


def components_by_id(methodology: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = methodology.get("structure_components")
    items = [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []
    return {str(item.get("component_id")): item for item in items if item.get("component_id")}


def validate_article_quality_methodology(methodology: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if methodology.get("schema_version") != SCHEMA_VERSION:
        issues.append("schema_version must be v1.")
    if not methodology.get("version"):
        issues.append("version is required.")
    standards = standards_by_id(methodology)
    for standard_id in REQUIRED_STANDARDS:
        if standard_id not in standards:
            issues.append(f"Missing article quality standard: {standard_id}.")
            continue
        standard = standards[standard_id]
        if not isinstance(standard.get("scoring_guide"), dict) or not standard.get("scoring_guide"):
            issues.append(f"{standard_id} scoring_guide is required.")
        if not standard.get("review_questions"):
            issues.append(f"{standard_id} review_questions are required.")
    if not methodology.get("discouraged_expressions"):
        issues.append("discouraged_expressions must be non-empty.")
    components = components_by_id(methodology)
    for component_id in REQUIRED_COMPONENTS:
        if component_id not in components:
            issues.append(f"Missing structure component: {component_id}.")
    return issues


def generic_language_flags(text: str, methodology: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    for expression in methodology.get("discouraged_expressions") or []:
        if str(expression) and str(expression) in text:
            flags.append(str(expression))
    return flags


def methodology_summary(methodology: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": methodology.get("schema_version"),
        "version": methodology.get("version"),
        "standard_count": len(standards_by_id(methodology)),
        "required_standard_count": len(REQUIRED_STANDARDS),
        "discouraged_expression_count": len(methodology.get("discouraged_expressions") or []),
        "structure_component_count": len(components_by_id(methodology)),
    }
