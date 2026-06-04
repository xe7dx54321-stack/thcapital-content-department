"""Build ops-to-methodology feedback from stable trial calibration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__ops-to-methodology-feedback.json",
        "dated_md": paths.logs_root / f"{run_date}__ops-to-methodology-feedback.md",
        "latest_json": paths.logs_root / "latest_ops_to_methodology_feedback.json",
        "latest_md": paths.logs_root / "latest_ops_to_methodology_feedback.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__ops-to-methodology-feedback-board.md",
        "board_latest_md": paths.frontstage_root / "latest_ops_to_methodology_feedback_board.md",
    }


def build_feedback_item(
    run_date: str,
    target_config: str,
    feedback_type: str,
    observation: str,
    suggested_change: str,
    evidence: list[str],
    confidence: float,
) -> dict[str, Any]:
    return {
        "feedback_id": make_id("ops_method", run_date, target_config, feedback_type, observation),
        "target_config": target_config,
        "feedback_type": feedback_type,
        "observation": observation,
        "suggested_change": suggested_change,
        "evidence": evidence,
        "confidence": round(confidence, 2),
        "auto_apply": False,
    }


def build_ops_to_methodology_feedback(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing = paths.market_content_root / "07_publishing"
    calibration = read_json(paths.logs_root / "latest_content_quality_calibration.json")
    days = [read_json(paths.logs_root / f"latest_stable_trial_day_{day}.json") for day in range(1, 4)]
    queue_repair = read_json(publishing / "latest_content_queue_readiness_repair.json")
    calendar = read_json(publishing / "latest_publishing_calendar_readiness_calibration.json")
    visual_feedback = read_json(paths.logs_root / "latest_visual_strategy_learning_feedback.json")
    config_inputs = {
        "topic_selection_methodology": repo_root / "config/topic_selection_methodology.json",
        "article_quality_methodology": repo_root / "config/article_quality_methodology.json",
        "content_strategy_recipes": repo_root / "config/content_strategy_recipes.json",
        "article_visual_methodology": repo_root / "config/article_visual_methodology.json",
    }
    warnings = [f"Missing config: {name}" for name, path in config_inputs.items() if not path.exists()]

    quality_issues = list_payload(calibration, "quality_issues")
    queue_summary = queue_repair.get("summary") if isinstance(queue_repair.get("summary"), dict) else {}
    calendar_summary = calendar.get("summary") if isinstance(calendar.get("summary"), dict) else {}
    area_counts: dict[str, int] = {}
    blocking_by_area: dict[str, int] = {}
    for issue in quality_issues:
        area = str(issue.get("area") or "logic")
        area_counts[area] = area_counts.get(area, 0) + 1
        if issue.get("blocks_publish"):
            blocking_by_area[area] = blocking_by_area.get(area, 0) + 1
    feedback: list[dict[str, Any]] = []
    if area_counts:
        top_area, top_count = max(area_counts.items(), key=lambda item: item[1])
        feedback.append(
            build_feedback_item(
                run_date,
                "article_quality_methodology",
                "weight_adjustment",
                f"{top_area} is the most frequent stable-trial quality friction.",
                f"Review scoring/checklist prominence for `{top_area}`; do not auto-change weights until human calibration confirms.",
                [f"{top_area}: {top_count} issue(s)", f"blocking areas: {blocking_by_area}"],
                0.72,
            )
        )
    ready_to_publish = int(queue_summary.get("ready_to_publish") or 0)
    ready_for_review = int(queue_summary.get("ready_for_review") or 0)
    if ready_for_review and not ready_to_publish:
        feedback.append(
            build_feedback_item(
                run_date,
                "content_strategy_recipes",
                "recipe_refinement",
                "Queue has READY_FOR_REVIEW items but no READY_TO_PUBLISH item.",
                "Add recipe-specific publish-readiness handoff checks: title promise, opening tension, evidence chain, visual slot completion.",
                [f"ready_for_review={ready_for_review}", f"ready_to_publish={ready_to_publish}"],
                0.68,
            )
        )
    actionable_days = int(calendar_summary.get("actionable_days") or 0)
    ready_days = int(calendar_summary.get("ready_days") or 0)
    if actionable_days and not ready_days:
        feedback.append(
            build_feedback_item(
                run_date,
                "topic_selection_methodology",
                "threshold_review",
                "Calendar is actionable across days but not ready.",
                "Review topic selection threshold for publish-window urgency versus evidence/visual readiness; keep manual confirmation required.",
                [f"actionable_days={actionable_days}", f"ready_days={ready_days}"],
                0.62,
            )
        )
    visual_issue_count = area_counts.get("visual", 0)
    visual_recommendations = list_payload(visual_feedback, "recommendations")
    if visual_issue_count or visual_recommendations:
        feedback.append(
            build_feedback_item(
                run_date,
                "article_visual_methodology",
                "visual_standard_refinement",
                "Visual checklist and visual strategy feedback still affect publish readiness.",
                "Keep visual assets, mobile readability, source/copyright, and slot-marker cleanup as explicit pre-publish checks.",
                [f"visual_quality_issues={visual_issue_count}", f"visual_strategy_recommendations={len(visual_recommendations)}"],
                0.7,
            )
        )
    day_evidence = []
    for day in days:
        if day:
            result = day.get("day_result") if isinstance(day.get("day_result"), dict) else {}
            day_evidence.append(f"day{day.get('stable_trial_day')}: {result.get('day_status')} / continue={result.get('can_continue')}")
    if day_evidence:
        feedback.append(
            build_feedback_item(
                run_date,
                "article_quality_methodology",
                "new_check",
                "Stable trial can continue, but operator actions remain necessary before publishing.",
                "Add an operator-facing final quality handoff check linking methodology review to publish readiness.",
                day_evidence,
                0.64,
            )
        )

    summary = {
        "feedback_count": len(feedback),
        "topic_methodology": sum(1 for item in feedback if item.get("target_config") == "topic_selection_methodology"),
        "article_methodology": sum(1 for item in feedback if item.get("target_config") == "article_quality_methodology"),
        "recipe": sum(1 for item in feedback if item.get("target_config") == "content_strategy_recipes"),
        "visual_methodology": sum(1 for item in feedback if item.get("target_config") == "article_visual_methodology"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "feedback": feedback,
        "summary": summary,
        "warnings": warnings,
        "policy": {"auto_apply": False, "no_config_prompt_rule_changes": True, "sidecar_only": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        f"| `{item.get('target_config')}` | `{item.get('feedback_type')}` | {item.get('observation')} | {item.get('suggested_change')} | `{item.get('confidence')}` |"
        for item in list_payload(payload, "feedback")
    ]
    return f"""# Ops-to-Methodology Feedback

## Summary

- feedback_count: `{summary.get('feedback_count', 0)}`
- topic_methodology: `{summary.get('topic_methodology', 0)}`
- article_methodology: `{summary.get('article_methodology', 0)}`
- recipe: `{summary.get('recipe', 0)}`
- visual_methodology: `{summary.get('visual_methodology', 0)}`

| Target | Type | Observation | Suggested change | Confidence |
|---|---|---|---|---|
{chr(10).join(rows)}

All suggestions are `auto_apply=false`.
"""
