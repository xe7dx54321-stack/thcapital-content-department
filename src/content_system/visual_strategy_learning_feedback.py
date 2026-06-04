"""Generate visual strategy learning feedback from manual performance observations."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__visual-strategy-learning-feedback.json",
        "dated_md": paths.logs_root / f"{run_date}__visual-strategy-learning-feedback.md",
        "latest_json": paths.logs_root / "latest_visual_strategy_learning_feedback.json",
        "latest_md": paths.logs_root / "latest_visual_strategy_learning_feedback.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__visual-strategy-learning-feedback-board.md",
        "board_latest_md": paths.frontstage_root / "latest_visual_strategy_learning_feedback_board.md",
    }


def observed_effect(helpful: int, distracting: int) -> str:
    if helpful > distracting:
        return "POSITIVE"
    if distracting > helpful:
        return "NEGATIVE"
    return "UNKNOWN"


def build_visual_strategy_learning_feedback(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    publishing_root = paths.market_content_root / "07_publishing"
    records_payload = read_json(publishing_root / "latest_post_publish_visual_performance.json")
    asset_payload = read_json(paths.market_content_root / "08_assets" / "image_asset_library.json")
    visual_plan_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_article_visual_plans.json")
    assets_by_id = {str(item.get("asset_id") or ""): item for item in list_payload(asset_payload, "assets")}
    type_counts: dict[str, dict[str, Any]] = defaultdict(lambda: {"HELPFUL": 0, "DISTRACTING": 0, "NEUTRAL": 0, "UNKNOWN": 0, "evidence": []})
    for record in list_payload(records_payload, "records"):
        for note in record.get("visual_notes", []) if isinstance(record.get("visual_notes"), list) else []:
            if not isinstance(note, dict):
                continue
            asset = assets_by_id.get(str(note.get("asset_id") or ""), {})
            visual_type = str(note.get("visual_type") or asset.get("visual_type") or "unknown_visual")
            effect = str(note.get("observed_effect") or "UNKNOWN")
            if effect not in type_counts[visual_type]:
                effect = "UNKNOWN"
            type_counts[visual_type][effect] += 1
            evidence = note.get("manual_note") or record.get("manual_note") or ""
            if evidence:
                type_counts[visual_type]["evidence"].append(evidence)
    feedback = []
    recommendations = []
    if not type_counts:
        recommendations.append(
            {
                "recommendation_id": make_id("vsf", run_date, "collect_visual_performance"),
                "target_area": "wechat_layout",
                "recommendation": "Collect manual post-publish visual performance observations before changing visual methodology.",
                "reason": "No visual performance records are available yet.",
                "auto_apply": False,
            }
        )
    for visual_type, counts in sorted(type_counts.items()):
        effect = observed_effect(int(counts["HELPFUL"]), int(counts["DISTRACTING"]))
        recommendation = "Keep using this visual type when it explains the article's core structure." if effect == "POSITIVE" else "Review whether this visual type is too decorative or hard to read on mobile." if effect == "NEGATIVE" else "Collect more observations before changing strategy."
        feedback.append(
            {
                "visual_type": visual_type,
                "observed_effect": effect,
                "evidence": counts["evidence"][:5],
                "recommendation": recommendation,
                "confidence": min(0.8, 0.2 + 0.1 * (int(counts["HELPFUL"]) + int(counts["DISTRACTING"]))),
                "auto_apply": False,
            }
        )
        recommendations.append(
            {
                "recommendation_id": make_id("vsf", run_date, visual_type),
                "target_area": visual_type if visual_type != "unknown_visual" else "visual_prompt",
                "recommendation": recommendation,
                "reason": f"Manual observations: helpful={counts['HELPFUL']}, distracting={counts['DISTRACTING']}.",
                "auto_apply": False,
            }
        )
    summary = {
        "visual_performance_record_count": len(list_payload(records_payload, "records")),
        "recommendation_count": len(recommendations),
        "visual_plan_count": len(list_payload(visual_plan_payload, "visual_plans")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "summary": summary,
        "visual_type_feedback": feedback,
        "recommendations": recommendations,
        "policy": {"auto_apply": False, "no_prompt_or_config_changes": True, "no_auto_image_generation": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('visual_type')}` | `{item.get('observed_effect')}` | {item.get('recommendation') or ''} | `{item.get('confidence')}` |"
        for item in list_payload(payload, "visual_type_feedback")
    ) or "| - | UNKNOWN | No visual performance records yet | 0 |"
    return f"""# Visual Strategy Learning Feedback

## Summary

- visual_performance_record_count: `{summary.get('visual_performance_record_count', 0)}`
- recommendation_count: `{summary.get('recommendation_count', 0)}`
- auto_apply: `false`
- no_auto_image_generation: `true`

| Visual Type | Observed Effect | Recommendation | Confidence |
|---|---|---|---:|
{rows}
"""
