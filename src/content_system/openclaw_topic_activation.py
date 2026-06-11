"""Promote confirmed migrated OpenClaw signals into conservative topic candidates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


WEAK_LANES = {"reddit_llm_discussion", "youtube_signal", "x_signal", "trend_heat", "chinese_ai_media"}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "03_topic_candidates"
    return {
        "dated_json": root / f"{run_date}__openclaw-activated-topic-candidates.json",
        "dated_md": root / f"{run_date}__openclaw-activated-topic-candidates.md",
        "latest_json": root / "latest_openclaw_activated_topic_candidates.json",
        "latest_md": root / "latest_openclaw_activated_topic_candidates.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__openclaw-activated-topic-candidates-board.md",
        "board_latest_md": paths.frontstage_root / "latest_openclaw_activated_topic_candidates_board.md",
    }


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def by_id(payload: dict[str, Any], key: str, list_name: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in list_payload(payload, list_name) if item.get(key)}


def topic_type_for(lane: str) -> str:
    return {
        "funding_startup": "startup_tracking",
        "builder_research": "builder_insight",
        "reddit_llm_discussion": "trend_judgment",
        "youtube_signal": "product_strategy_analysis",
        "x_signal": "trend_judgment",
        "trend_heat": "trend_judgment",
        "chinese_ai_media": "news_explainer",
        "industry_deep_research": "industry_deep_dive",
    }.get(lane, "news_explainer")


def activation_for(confirmation: dict[str, Any], backfill: dict[str, Any]) -> tuple[str, str, bool, list[str], str]:
    lane = str(confirmation.get("lane") or backfill.get("lane") or "")
    role = str(backfill.get("evidence_role") or "weak_signal")
    status = str(confirmation.get("confirmation_status") or "")
    if status == "CONFIRMABLE" and role == "supporting_evidence":
        strength = "MEDIUM"
        can_brief = lane not in WEAK_LANES
        missing: list[str] = [] if can_brief else ["Weak lane still needs stronger primary evidence before brief."]
        next_action = "Operator confirms source metadata, then run confirmed topic scoring/brief."
        return "ACTIVATED", strength, can_brief, missing, next_action
    if status in {"NEEDS_PRIMARY_SOURCE", "NEEDS_SECOND_SOURCE"}:
        missing = ["Primary source" if status == "NEEDS_PRIMARY_SOURCE" else "Second corroborating source"]
        return "NEEDS_EVIDENCE", "LOW", False, missing, "Backfill required evidence before topic scoring."
    if status == "MANUAL_REVIEW":
        return "WATCH", "LOW", False, ["Manual source review"], "Manual review before any topic activation."
    if status == "BLOCKED":
        return "REJECTED", "UNKNOWN", False, ["Blocked by regression/safety policy"], "Do not move into content pipeline."
    return "WATCH", "UNKNOWN", False, ["Stronger confirmation signal"], "Keep watching until the signal strengthens."


def candidate_from_confirmation(confirmation: dict[str, Any], backfills: dict[str, dict[str, Any]], signals: dict[str, dict[str, Any]]) -> dict[str, Any]:
    backfill = backfills.get(str(confirmation.get("backfill_id") or ""), {})
    signal = signals.get(str(confirmation.get("signal_id") or ""), {})
    lane = str(confirmation.get("lane") or backfill.get("lane") or signal.get("lane") or "")
    activation_status, strength, can_brief, missing, next_action = activation_for(confirmation, backfill)
    title = compact_text(confirmation.get("title") or backfill.get("title") or signal.get("title"), 180)
    why_now = compact_text(backfill.get("claim_summary") or signal.get("required_confirmation") or "", 260)
    core_angle = compact_text(
        f"Use migrated OpenClaw {lane} signal as a starting point, then confirm with stronger source evidence before making claims.",
        260,
    )
    return {
        "topic_candidate_id": stable_id("octopic", confirmation.get("confirmation_id"), confirmation.get("signal_id")),
        "signal_id": confirmation.get("signal_id", ""),
        "confirmation_id": confirmation.get("confirmation_id", ""),
        "title": title,
        "lane": lane,
        "topic_type": topic_type_for(lane),
        "activation_status": activation_status,
        "why_now": why_now,
        "core_angle": core_angle,
        "evidence_role": backfill.get("evidence_role", "weak_signal"),
        "evidence_strength": strength,
        "can_enter_brief_pipeline": can_brief,
        "missing_evidence": missing,
        "next_action": next_action,
        "can_use_as_hard_evidence": False,
    }


def activate_openclaw_migrated_topics(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    topic_root = paths.market_content_root / "03_topic_candidates"
    inputs = {
        "weak_signal_confirmation_workflow": paths.logs_root / "latest_weak_signal_confirmation_workflow.json",
        "openclaw_signal_evidence_backfill": topic_root / "latest_openclaw_signal_evidence_backfill.json",
        "normalized_openclaw_signals": paths.logs_root / "latest_normalized_openclaw_signals.json",
        "connector_promoted_topic_candidates": topic_root / "latest_connector_promoted_topic_candidates.json",
        "methodology_topic_scores": topic_root / "latest_methodology_topic_scores.json",
    }
    warnings = warning_for_missing(inputs)
    confirmation = read_json(inputs["weak_signal_confirmation_workflow"])
    backfill = read_json(inputs["openclaw_signal_evidence_backfill"])
    normalized = read_json(inputs["normalized_openclaw_signals"])
    connector_topics = read_json(inputs["connector_promoted_topic_candidates"])
    topic_scores = read_json(inputs["methodology_topic_scores"])
    backfills = by_id(backfill, "backfill_id", "backfill_items")
    signals = by_id(normalized, "signal_id", "signals")
    candidates = [
        candidate_from_confirmation(item, backfills, signals)
        for item in list_payload(confirmation, "confirmation_items")
    ]
    summary = {
        "candidate_count": len(candidates),
        "activated": sum(1 for item in candidates if item.get("activation_status") == "ACTIVATED"),
        "needs_evidence": sum(1 for item in candidates if item.get("activation_status") == "NEEDS_EVIDENCE"),
        "watch": sum(1 for item in candidates if item.get("activation_status") == "WATCH"),
        "rejected": sum(1 for item in candidates if item.get("activation_status") == "REJECTED"),
        "can_enter_brief_pipeline": sum(1 for item in candidates if item.get("can_enter_brief_pipeline")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "topic_candidates": candidates,
        "summary": summary,
        "input_status": {
            "connector_topic_candidate_count": len(list_payload(connector_topics, "topic_candidates")),
            "methodology_topic_scores_available": bool(topic_scores),
        },
        "warnings": warnings,
        "policy": {
            "does_not_create_briefs": True,
            "weak_signals_not_hard_evidence": True,
            "weak_signal_not_direct_brief": True,
            "metadata_only": True,
            "no_full_text": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        {
            "status": item.get("activation_status"),
            "brief": item.get("can_enter_brief_pipeline"),
            "strength": item.get("evidence_strength"),
            "lane": item.get("lane"),
            "title": compact_text(item.get("title"), 62),
        }
        for item in list_payload(payload, "topic_candidates")[:40]
    ]
    return f"""# OpenClaw Activated Topic Candidates

## Summary

- candidate_count: `{summary.get('candidate_count', 0)}`
- activated: `{summary.get('activated', 0)}`
- needs_evidence: `{summary.get('needs_evidence', 0)}`
- watch: `{summary.get('watch', 0)}`
- rejected: `{summary.get('rejected', 0)}`
- can_enter_brief_pipeline: `{summary.get('can_enter_brief_pipeline', 0)}`

## Topic Candidates

{markdown_table(rows, ('status', 'brief', 'strength', 'lane', 'title'))}

## Boundary

OpenClaw migrated topics can only enter brief planning when confirmation is sufficient. Weak lanes do not directly enter the brief pipeline and no signal is treated as hard evidence.
"""
