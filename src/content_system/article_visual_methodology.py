"""Article visual strategy methodology helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_VISUAL_TYPES = (
    "cover_visual",
    "concept_diagram",
    "value_chain_map",
    "timeline_chart",
    "comparison_table_visual",
    "framework_diagram",
    "process_flow",
    "evidence_snapshot",
)

REQUIRED_QUALITY_STANDARDS = (
    "relevance_to_core_judgment",
    "information_density",
    "clarity",
    "narrative_fit",
    "visual_hierarchy",
    "evidence_integrity",
    "originality",
    "wechat_readability",
    "copyright_safety",
    "aesthetic_fit",
)

REQUIRED_SOURCE_STRATEGIES = (
    "evidence_snapshot",
    "internal_chart",
    "generated_concept_visual",
    "manual_design_request",
)


def load_article_visual_methodology(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "config" / "article_visual_methodology.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def validate_article_visual_methodology(methodology: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if methodology.get("schema_version") != "v1":
        issues.append("schema_version must be v1.")
    if not methodology.get("version"):
        issues.append("version is required.")
    visual_types = methodology.get("visual_types")
    if not isinstance(visual_types, list):
        issues.append("visual_types must be a list.")
        visual_types = []
    visual_by_id = {str(item.get("visual_type")): item for item in visual_types if isinstance(item, dict)}
    for visual_type in REQUIRED_VISUAL_TYPES:
        item = visual_by_id.get(visual_type)
        if not item:
            issues.append(f"missing visual_type: {visual_type}")
            continue
        for key in ("label", "best_for", "not_for", "information_job", "quality_standards", "common_failures", "generation_guidance", "source_guidance", "wechat_usage_guidance"):
            if key not in item or item.get(key) in ({}, [], ""):
                issues.append(f"visual_type {visual_type} missing {key}.")
    standards = methodology.get("quality_standards")
    if not isinstance(standards, list):
        issues.append("quality_standards must be a list.")
        standards = []
    standard_ids = {str(item.get("standard_id")) for item in standards if isinstance(item, dict)}
    for standard_id in REQUIRED_QUALITY_STANDARDS:
        if standard_id not in standard_ids:
            issues.append(f"missing quality standard: {standard_id}")
    strategies = methodology.get("source_strategies")
    if not isinstance(strategies, list):
        issues.append("source_strategies must be a list.")
        strategies = []
    strategy_ids = {str(item.get("strategy_id")) for item in strategies if isinstance(item, dict)}
    for strategy_id in REQUIRED_SOURCE_STRATEGIES:
        if strategy_id not in strategy_ids:
            issues.append(f"missing source strategy: {strategy_id}")
    policy = methodology.get("policy") if isinstance(methodology.get("policy"), dict) else {}
    if policy.get("do_not_auto_generate_images") is not True:
        issues.append("policy.do_not_auto_generate_images must be true.")
    if policy.get("human_review_required") is not True:
        issues.append("policy.human_review_required must be true.")
    return issues


def visual_types_by_id(methodology: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("visual_type")): item
        for item in methodology.get("visual_types", [])
        if isinstance(item, dict) and item.get("visual_type")
    }


def visual_methodology_summary(methodology: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": methodology.get("schema_version"),
        "version": methodology.get("version"),
        "visual_type_count": len(methodology.get("visual_types") or []),
        "required_visual_type_count": len(REQUIRED_VISUAL_TYPES),
        "quality_standard_count": len(methodology.get("quality_standards") or []),
        "source_strategy_count": len(methodology.get("source_strategies") or []),
        "issues": validate_article_visual_methodology(methodology),
    }
