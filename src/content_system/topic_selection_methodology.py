"""Topic selection methodology loader and validator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "v1"
REQUIRED_DIMENSIONS = (
    "change_intensity",
    "expectation_gap",
    "industry_chain_impact",
    "evidence_strength",
    "narrative_tension",
    "timing_window",
    "original_judgment_potential",
    "reader_value",
)


def config_path(repo_root: Path) -> Path:
    return repo_root / "config" / "topic_selection_methodology.json"


def load_topic_selection_methodology(repo_root: Path) -> dict[str, Any]:
    path = config_path(repo_root)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def dimensions_by_id(methodology: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = methodology.get("core_dimensions")
    items = [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []
    return {str(item.get("dimension_id")): item for item in items if item.get("dimension_id")}


def validate_topic_selection_methodology(methodology: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if methodology.get("schema_version") != SCHEMA_VERSION:
        issues.append("schema_version must be v1.")
    if not methodology.get("version"):
        issues.append("version is required.")
    dims = dimensions_by_id(methodology)
    for dimension_id in REQUIRED_DIMENSIONS:
        if dimension_id not in dims:
            issues.append(f"Missing core dimension: {dimension_id}.")
            continue
        dimension = dims[dimension_id]
        if not isinstance(dimension.get("scoring_guide"), dict) or not dimension.get("scoring_guide"):
            issues.append(f"{dimension_id} scoring_guide is required.")
        if not dimension.get("label") or not dimension.get("description"):
            issues.append(f"{dimension_id} label and description are required.")
    if not methodology.get("reject_rules"):
        issues.append("reject_rules must be non-empty.")
    if not methodology.get("required_questions"):
        issues.append("required_questions must be non-empty.")
    thresholds = methodology.get("recommendation_thresholds")
    if not isinstance(thresholds, dict):
        issues.append("recommendation_thresholds must exist.")
    return issues


def methodology_summary(methodology: dict[str, Any]) -> dict[str, Any]:
    dims = dimensions_by_id(methodology)
    return {
        "schema_version": methodology.get("schema_version"),
        "version": methodology.get("version"),
        "dimension_count": len(dims),
        "required_dimension_count": len(REQUIRED_DIMENSIONS),
        "reject_rule_count": len(methodology.get("reject_rules") or []),
        "required_question_count": len(methodology.get("required_questions") or []),
    }
