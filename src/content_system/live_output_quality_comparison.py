"""Compare Phase 16 live sidecar outputs with rule-based outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id, score_text_quality
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__live-output-quality-comparison.json",
        "dated_md": paths.logs_root / f"{run_date}__live-output-quality-comparison.md",
        "latest_json": paths.logs_root / "latest_live_output_quality_comparison.json",
        "latest_md": paths.logs_root / "latest_live_output_quality_comparison.md",
    }


def text_for(item: dict[str, Any], keys: tuple[str, ...]) -> str:
    return "\n".join(str(item.get(key) or "") for key in keys if item.get(key))


def compare_pair(run_date: str, comparison_type: str, rule: dict[str, Any], live: dict[str, Any], rule_id_key: str, live_id_key: str, keys: tuple[str, ...]) -> dict[str, Any]:
    rule_text = text_for(rule, keys)
    live_text = text_for(live, keys)
    rule_score = score_text_quality(rule_text, ["核心", "判断", "证据", "风险", "读者"])
    live_score = score_text_quality(live_text, ["核心", "判断", "证据", "风险", "读者"])
    delta = live_score - rule_score
    if not live:
        recommendation = "USE_RULE"
        confidence = 0.7
    elif delta >= 8:
        recommendation = "USE_LIVE"
        confidence = 0.72
    elif delta <= -8:
        recommendation = "USE_RULE"
        confidence = 0.72
    elif abs(delta) <= 3:
        recommendation = "MERGE"
        confidence = 0.58
    else:
        recommendation = "HUMAN_REVIEW"
        confidence = 0.55
    return {
        "comparison_id": make_id("locomp", run_date, comparison_type, live.get(live_id_key) or rule.get(rule_id_key)),
        "comparison_type": comparison_type,
        "source_id": live.get("source_topic_id") or live.get("source_draft_id") or live.get("source_article_id") or live.get("source_request_id") or rule.get(rule_id_key) or "",
        "rule_output_id": rule.get(rule_id_key) or "",
        "live_output_id": live.get(live_id_key) or "",
        "scores": {"rule_score": rule_score, "live_score": live_score, "delta": delta},
        "live_strengths": ["Live sidecar has stronger methodology coverage."] if delta > 0 else [],
        "live_weaknesses": ["Live sidecar does not clearly beat the rule output."] if delta <= 0 else [],
        "recommendation": recommendation,
        "confidence": confidence,
    }


def build_live_output_quality_comparison(paths: ProjectPaths) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    draft_root = paths.market_content_root / "05_draft_packs"
    version_root = paths.market_content_root / "09_workbench_actions" / "versions"
    rule_briefs = list_payload(read_json(draft_root / "latest_methodology_content_briefs.json"), "briefs")
    live_briefs = list_payload(read_json(draft_root / "latest_live_methodology_brief_pilot.json"), "briefs")
    rule_drafts = list_payload(read_json(draft_root / "latest_methodology_content_drafts.json"), "drafts")
    live_drafts = list_payload(read_json(draft_root / "latest_live_methodology_draft_pilot.json"), "drafts")
    rule_rewrites = list_payload(read_json(version_root / "latest_methodology_rewrite_versions.json"), "versions")
    live_rewrites = list_payload(read_json(version_root / "latest_live_methodology_rewrite_pilot.json"), "rewrites")
    rule_requests = list_payload(read_json(draft_root / "latest_image_asset_requests.json"), "requests")
    live_prompts = list_payload(read_json(draft_root / "latest_live_visual_prompt_pilot.json"), "visual_prompts")
    comparisons: list[dict[str, Any]] = []
    if rule_briefs:
        comparisons.append(compare_pair(run_date, "brief", rule_briefs[0], live_briefs[0] if live_briefs else {}, "brief_id", "live_brief_id", ("core_question", "core_judgment", "why_now", "reader_value")))
    if rule_drafts:
        comparisons.append(compare_pair(run_date, "draft", rule_drafts[0], live_drafts[0] if live_drafts else {}, "draft_id", "live_draft_id", ("selected_title", "opening", "body_markdown", "closing")))
    if rule_rewrites:
        comparisons.append(compare_pair(run_date, "rewrite", rule_rewrites[0], live_rewrites[0] if live_rewrites else {}, "version_id", "live_rewrite_id", ("new_title", "new_opening", "new_body_markdown", "change_summary")))
    if rule_requests:
        comparisons.append(compare_pair(run_date, "visual_prompt", rule_requests[0], live_prompts[0] if live_prompts else {}, "request_id", "live_visual_prompt_id", ("image_prompt", "design_brief", "layout_guidance", "copyright_note")))
    summary = {
        "comparison_count": len(comparisons),
        "use_live": sum(1 for item in comparisons if item.get("recommendation") == "USE_LIVE"),
        "use_rule": sum(1 for item in comparisons if item.get("recommendation") == "USE_RULE"),
        "merge": sum(1 for item in comparisons if item.get("recommendation") == "MERGE"),
        "human_review": sum(1 for item in comparisons if item.get("recommendation") == "HUMAN_REVIEW"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "comparisons": comparisons,
        "summary": summary,
        "policy": {"advisory_only": True, "do_not_replace_rule_output": True, "auto_apply": False},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('comparison_id')}` | `{item.get('comparison_type')}` | `{item.get('recommendation')}` | {item.get('scores', {}).get('delta', 0)} |"
        for item in list_payload(payload, "comparisons")
    ) or "| - | - | - | 0 |"
    return f"""# Live Output Quality Comparison

## Summary

- comparison_count: `{summary.get('comparison_count', 0)}`
- use_live: `{summary.get('use_live', 0)}`
- use_rule: `{summary.get('use_rule', 0)}`
- merge: `{summary.get('merge', 0)}`
- human_review: `{summary.get('human_review', 0)}`

| Comparison | Type | Recommendation | Delta |
|---|---|---|---:|
{rows}

## Policy

- Advisory only.
- Does not replace rule-based outputs.
- Does not auto-use live outputs.
"""
