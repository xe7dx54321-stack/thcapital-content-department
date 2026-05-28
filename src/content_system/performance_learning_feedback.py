"""Generate learning feedback from manually entered content performance."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class PerformanceLearningFeedbackResult:
    run_date: str
    performance_record_count: int
    high_performing_count: int
    low_performing_count: int
    suggestion_count: int
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__performance-learning-feedback.json",
        "dated_md": paths.logs_root / f"{run_date}__performance-learning-feedback.md",
        "latest_json": paths.logs_root / "latest_performance_learning_feedback.json",
        "latest_md": paths.logs_root / "latest_performance_learning_feedback.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__performance-learning-feedback-board.md",
        "board_latest_md": paths.frontstage_root / "latest_performance_learning_feedback_board.md",
    }


def recommendation_id(target_area: str, reason: str) -> str:
    digest = hashlib.sha1(f"{today_token()}|{target_area}|{reason}".encode("utf-8")).hexdigest()[:10]
    return f"plf_{digest}"


def recommendation(target_area: str, text: str, reason: str, confidence: float) -> dict[str, Any]:
    return {
        "recommendation_id": recommendation_id(target_area, reason),
        "target_area": target_area,
        "recommendation": text,
        "reason": reason,
        "confidence": confidence,
        "auto_apply": False,
    }


def build_performance_learning_feedback(paths: ProjectPaths, repo_root: Path) -> tuple[PerformanceLearningFeedbackResult, dict[str, Any]]:
    root = paths.market_content_root / "07_publishing"
    performance_memory = read_json(root / "content_performance_memory.json")
    multiday = read_json(paths.logs_root / "latest_multiday_version_analytics.json")
    action_effectiveness = read_json(paths.logs_root / "latest_action_effectiveness_analytics.json")
    regression = read_json(paths.logs_root / "latest_prompt_rule_regression_dashboard.json")
    recipe = read_json(paths.market_content_root / "08_learning_patterns" / "latest_content_recipe_suggestions.json")
    adapters = read_json(paths.market_content_root / "08_learning_patterns" / "latest_pattern_adapters.json")
    records = list_payload(performance_memory, "records")
    high_records = [item for item in records if item.get("performance_rating") in {"HIGH", "EXCELLENT"}]
    low_records = [item for item in records if item.get("performance_rating") == "LOW"]
    recommendations: list[dict[str, Any]] = []
    topic_feedback: list[str] = []
    title_feedback: list[str] = []
    opening_feedback: list[str] = []
    evidence_feedback: list[str] = []
    agent_feedback: list[str] = []
    if not records:
        recommendations.append(recommendation("topic_selection", "Collect manual post-publish metrics before changing topic scoring.", "No performance records are available yet.", 0.5))
    if high_records:
        patterns = sorted({str(item.get("title_pattern") or "") for item in high_records if item.get("title_pattern")})
        if patterns:
            title_feedback.append(f"High-performing title patterns observed: {', '.join(patterns)}.")
            recommendations.append(recommendation("title_pattern", f"Prioritize observed high-performing title patterns: {', '.join(patterns)}.", "Manual metrics marked at least one record HIGH/EXCELLENT.", 0.72))
        if any("investor" in " ".join(item.get("lessons") or []).lower() or "投资" in " ".join(item.get("lessons") or []) for item in high_records):
            topic_feedback.append("Investor-angle framing appears in high-performing records.")
            recommendations.append(recommendation("chief_editor", "Keep investor-angle rewrite suggestions available for broad AI/Agent topics.", "High-performing record contains investor-angle lesson.", 0.68))
    if low_records:
        evidence_feedback.append("Some low-performing records may need title/opening diagnosis before assuming evidence strategy failed.")
        recommendations.append(recommendation("opening_pattern", "When performance is low, inspect opening strength before expanding evidence collection.", "Low-performing records can still contain evidence, so weak hook may be the bottleneck.", 0.62))
    action_summary = action_effectiveness.get("summary") if isinstance(action_effectiveness.get("summary"), dict) else {}
    if safe_float(action_summary.get("average_score_delta")) > 0:
        agent_feedback.append("Action effectiveness remains positive on automated score delta.")
    if list_payload(regression, "suggestions"):
        recommendations.append(recommendation("scoring_rule", "Review prompt/rule regression suggestions manually before applying any scoring changes.", "Regression dashboard contains active suggestions.", 0.6))
    if list_payload(recipe, "suggestions"):
        recommendations.append(recommendation("content_recipe", "Compare content recipe suggestions against real performance records before expanding usage.", "Recipe suggestions exist but should be validated by manual metrics.", 0.55))
    if list_payload(adapters, "adapters"):
        recommendations.append(recommendation("pattern_adapter", "Use performance memory to validate which pattern adapters deserve promotion.", "Pattern adapters are available; performance evidence can now rank them.", 0.55))
    summary = {
        "performance_record_count": len(records),
        "high_performing_count": len(high_records),
        "low_performing_count": len(low_records),
        "suggestion_count": len(recommendations),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "summary": summary,
        "topic_feedback": topic_feedback,
        "title_feedback": title_feedback,
        "opening_feedback": opening_feedback,
        "structure_feedback": [],
        "evidence_feedback": evidence_feedback,
        "agent_feedback": agent_feedback,
        "multiday_summary": multiday.get("summary") if isinstance(multiday.get("summary"), dict) else {},
        "recommendations": recommendations,
    }
    outputs = output_paths(paths, payload["run_date"])
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        PerformanceLearningFeedbackResult(
            payload["run_date"],
            summary["performance_record_count"],
            summary["high_performing_count"],
            summary["low_performing_count"],
            summary["suggestion_count"],
            repo_relative(outputs["latest_json"], repo_root),
            repo_relative(outputs["board_latest_md"], repo_root),
        ),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('recommendation_id')}` | `{item.get('target_area')}` | `{item.get('confidence')}` | {item.get('recommendation')} |"
        for item in list_payload(payload, "recommendations")
    ) or "| - | - | 0 | No recommendations yet |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Performance-to-Learning Feedback

## Summary

- Performance records: `{summary.get('performance_record_count', 0)}`
- High-performing: `{summary.get('high_performing_count', 0)}`
- Low-performing: `{summary.get('low_performing_count', 0)}`
- Suggestions: `{summary.get('suggestion_count', 0)}`
- Policy: suggestions only; no prompt, rule, or scoring config is changed automatically.

| Recommendation | Target | Confidence | Text |
|---|---|---:|---|
{rows}
"""
