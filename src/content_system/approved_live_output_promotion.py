"""Promote human-approved Phase 16 live brief/draft outputs as sidecar candidates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


APPROVABLE_DECISIONS = {"ACCEPT_LIVE", "MERGE"}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__promoted-live-content-candidates.json",
        "dated_md": root / f"{run_date}__promoted-live-content-candidates.md",
        "latest_json": root / "latest_promoted_live_content_candidates.json",
        "latest_md": root / "latest_promoted_live_content_candidates.md",
    }


def by_key(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key)}


def content_payload_for(source_type: str, item: dict[str, Any]) -> dict[str, Any]:
    if source_type == "live_brief":
        return {
            "core_question": item.get("core_question") or "",
            "core_judgment": item.get("core_judgment") or "",
            "why_now": item.get("why_now") or "",
            "expectation_gap": item.get("expectation_gap") or "",
            "industry_chain_impact": item.get("industry_chain_impact") or "",
            "reader_value": item.get("reader_value") or "",
            "evidence_plan": item.get("evidence_plan") or [],
            "counterarguments": item.get("counterarguments") or [],
            "visual_opportunities": item.get("visual_opportunities") or [],
        }
    return {
        "title_options": item.get("title_options") or [],
        "selected_title": item.get("selected_title") or item.get("title") or "",
        "opening": item.get("opening") or "",
        "body_markdown": item.get("body_markdown") or "",
        "closing": item.get("closing") or "",
        "visual_placeholders": item.get("visual_placeholders") or [],
        "methodology_self_check": item.get("methodology_self_check") or {},
    }


def build_promotions(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    draft_root = paths.market_content_root / "05_draft_packs"
    brief_payload = read_json(draft_root / "latest_live_methodology_brief_pilot.json")
    draft_payload = read_json(draft_root / "latest_live_methodology_draft_pilot.json")
    comparison_payload = read_json(paths.logs_root / "latest_live_output_quality_comparison.json")
    calibration_payload = read_json(paths.logs_root / "latest_live_calibration_feedback.json")
    live_briefs = by_key(list_payload(brief_payload, "briefs"), "live_brief_id")
    live_drafts = by_key(list_payload(draft_payload, "drafts"), "live_draft_id")
    feedback_by_comparison = by_key(list_payload(calibration_payload, "feedback"), "comparison_id")
    promoted: list[dict[str, Any]] = []
    skipped = 0
    for comparison in list_payload(comparison_payload, "comparisons"):
        comparison_type = str(comparison.get("comparison_type") or "")
        if comparison_type not in {"brief", "draft"}:
            continue
        feedback = feedback_by_comparison.get(str(comparison.get("comparison_id") or ""), {})
        decision = str(feedback.get("decision") or "")
        if decision not in APPROVABLE_DECISIONS:
            skipped += 1
            continue
        live_output_id = str(comparison.get("live_output_id") or "")
        source_type = "live_brief" if comparison_type == "brief" else "live_draft"
        live_item = live_briefs.get(live_output_id) if source_type == "live_brief" else live_drafts.get(live_output_id)
        if not live_item:
            skipped += 1
            continue
        title = live_item.get("title") or live_item.get("selected_title") or ""
        source_topic_id = live_item.get("source_topic_id") or comparison.get("source_id") or ""
        source_article_id = live_item.get("source_draft_id") or live_item.get("source_article_id") or ""
        promoted.append(
            {
                "promotion_id": make_id("lpromo", run_date, live_output_id, comparison.get("comparison_id")),
                "source_live_output_id": live_output_id,
                "source_type": source_type,
                "source_topic_id": source_topic_id,
                "source_article_id": source_article_id,
                "comparison_id": comparison.get("comparison_id") or "",
                "calibration_decision": decision,
                "promotion_status": "PROMOTED_TO_CANDIDATE",
                "title": title,
                "content_payload": content_payload_for(source_type, live_item),
                "promotion_reason": feedback.get("human_note") or f"Human calibration decision is {decision}; promote as sidecar candidate only.",
                "do_not_overwrite_original": True,
                "do_not_publish": True,
                "created_at": utc_now(),
            }
        )
    summary = {
        "candidate_count": len(promoted),
        "brief_promotions": sum(1 for item in promoted if item.get("source_type") == "live_brief"),
        "draft_promotions": sum(1 for item in promoted if item.get("source_type") == "live_draft"),
        "skipped": skipped,
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "promoted_candidates": promoted,
        "summary": summary,
        "policy": {"sidecar_only": True, "do_not_overwrite_original": True, "do_not_publish": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('promotion_id')}` | `{item.get('source_type')}` | `{item.get('source_live_output_id')}` | `{item.get('calibration_decision')}` | {item.get('title') or ''} |"
        for item in list_payload(payload, "promoted_candidates")
    ) or "| - | - | - | - | No promoted live brief/draft candidates |"
    return f"""# Promoted Live Content Candidates

## Summary

- candidate_count: `{summary.get('candidate_count', 0)}`
- brief_promotions: `{summary.get('brief_promotions', 0)}`
- draft_promotions: `{summary.get('draft_promotions', 0)}`
- skipped: `{summary.get('skipped', 0)}`
- sidecar_only: `true`
- do_not_publish: `true`

| Promotion | Type | Source Live Output | Calibration | Title |
|---|---|---|---|---|
{rows}
"""
