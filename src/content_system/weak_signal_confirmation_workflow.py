"""Build a confirmation workflow for OpenClaw migrated weak signals."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


WEAK_LANES = {"reddit_llm_discussion", "youtube_signal", "x_signal", "trend_heat"}


def evidence_root(paths: ProjectPaths) -> Path:
    return paths.market_content_root / "03_topic_candidates"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__weak-signal-confirmation-workflow.json",
        "dated_md": paths.logs_root / f"{run_date}__weak-signal-confirmation-workflow.md",
        "latest_json": paths.logs_root / "latest_weak_signal_confirmation_workflow.json",
        "latest_md": paths.logs_root / "latest_weak_signal_confirmation_workflow.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__weak-signal-confirmation-workflow-board.md",
        "board_latest_md": paths.frontstage_root / "latest_weak_signal_confirmation_workflow_board.md",
    }


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def source_risk_by_id(risk: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("source_id")): item for item in list_payload(risk, "classified_sources") if item.get("source_id")}


def signal_by_id(normalized: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("signal_id")): item for item in list_payload(normalized, "signals") if item.get("signal_id")}


def status_for_backfill(item: dict[str, Any], signal: dict[str, Any], risk: dict[str, Any]) -> tuple[str, str, str, bool, str]:
    lane = str(item.get("lane") or signal.get("lane") or risk.get("lane") or "")
    role = str(item.get("evidence_role") or signal.get("evidence_role") or risk.get("evidence_role") or "weak_signal")
    backfill_status = str(item.get("backfill_status") or "")
    if backfill_status == "BLOCKED":
        return "BLOCKED", "Blocked by safety gate; do not activate.", "none", False, "Blocked source or unsafe migrated signal."
    if lane == "chinese_ai_media" or role == "manual_only":
        return "MANUAL_REVIEW", "Manual media/source review required; do not auto-fetch article body.", "manual", False, "Chinese media/manual-only signal."
    if lane in WEAK_LANES or role in {"weak_signal", "heat_validation"}:
        if backfill_status == "WATCH":
            return "WATCH", "Observe until stronger or primary source appears.", "none", False, "Weak signal remains watch-only."
        return "NEEDS_SECOND_SOURCE", "Find an official or reputable second source before topic activation.", "official", False, "Weak signal needs corroboration."
    if backfill_status == "READY_FOR_CONFIRMATION" and role == "supporting_evidence":
        return "CONFIRMABLE", "Review metadata and confirm against source URL before activation.", "media", True, "Supporting evidence metadata is complete enough for operator confirmation."
    if backfill_status == "NEEDS_PRIMARY_SOURCE":
        return "NEEDS_PRIMARY_SOURCE", "Find the primary company/project/source before activation.", "primary_company", False, "Primary source is still missing."
    if backfill_status == "WATCH":
        return "WATCH", "Monitor for stronger signal or fresher source.", "none", False, "Not strong enough for activation."
    return "NEEDS_PRIMARY_SOURCE", "Confirm with primary source before activation.", "primary_company", False, "Conservative fallback."


def suggested_queries(title: str, source_name: str, lane: str) -> list[str]:
    base = compact_text(title or source_name, 120)
    if not base:
        return []
    queries = [f"{base} official announcement", f"{base} primary source"]
    if lane == "funding_startup":
        queries.append(f"{base} funding announcement")
    elif lane == "builder_research":
        queries.append(f"{base} GitHub blog technical source")
    elif lane in WEAK_LANES:
        queries.append(f"{base} reputable media confirmation")
    return queries[:3]


def confirmation_from_backfill(item: dict[str, Any], signals: dict[str, dict[str, Any]], risks: dict[str, dict[str, Any]]) -> dict[str, Any]:
    signal = signals.get(str(item.get("signal_id") or ""), {})
    risk = risks.get(str(item.get("source_id") or ""), {})
    title = compact_text(item.get("title"), 180)
    lane = str(item.get("lane") or signal.get("lane") or risk.get("lane") or "")
    status, action, required_type, can_promote, note = status_for_backfill(item, signal, risk)
    return {
        "confirmation_id": stable_id("confirm", item.get("backfill_id"), item.get("signal_id")),
        "signal_id": item.get("signal_id", ""),
        "backfill_id": item.get("backfill_id", ""),
        "title": title,
        "source_name": item.get("source_name", ""),
        "lane": lane,
        "confirmation_status": status,
        "required_action": action,
        "suggested_search_queries": suggested_queries(title, str(item.get("source_name") or ""), lane),
        "required_source_type": required_type,
        "can_promote_to_topic": can_promote,
        "can_use_as_hard_evidence": False,
        "operator_note": note,
    }


def build_weak_signal_confirmation_workflow(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    inputs = {
        "openclaw_signal_evidence_backfill": evidence_root(paths) / "latest_openclaw_signal_evidence_backfill.json",
        "weak_signal_safety_gate": paths.logs_root / "latest_weak_signal_safety_gate.json",
        "normalized_openclaw_signals": paths.logs_root / "latest_normalized_openclaw_signals.json",
        "openclaw_source_risk_classification": paths.logs_root / "latest_openclaw_source_risk_classification.json",
    }
    warnings = warning_for_missing(inputs)
    backfill = read_json(inputs["openclaw_signal_evidence_backfill"])
    weak_gate = read_json(inputs["weak_signal_safety_gate"])
    normalized = read_json(inputs["normalized_openclaw_signals"])
    risk = read_json(inputs["openclaw_source_risk_classification"])
    signals = signal_by_id(normalized)
    risks = source_risk_by_id(risk)
    confirmation_items = [
        confirmation_from_backfill(item, signals, risks)
        for item in list_payload(backfill, "backfill_items")
    ]
    summary = {
        "confirmation_count": len(confirmation_items),
        "confirmable": sum(1 for item in confirmation_items if item.get("confirmation_status") == "CONFIRMABLE"),
        "needs_primary_source": sum(1 for item in confirmation_items if item.get("confirmation_status") == "NEEDS_PRIMARY_SOURCE"),
        "needs_second_source": sum(1 for item in confirmation_items if item.get("confirmation_status") == "NEEDS_SECOND_SOURCE"),
        "manual_review": sum(1 for item in confirmation_items if item.get("confirmation_status") == "MANUAL_REVIEW"),
        "watch": sum(1 for item in confirmation_items if item.get("confirmation_status") == "WATCH"),
        "blocked": sum(1 for item in confirmation_items if item.get("confirmation_status") == "BLOCKED"),
        "can_promote_to_topic": sum(1 for item in confirmation_items if item.get("can_promote_to_topic")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "confirmation_items": confirmation_items,
        "summary": summary,
        "input_status": {
            "weak_signal_gate_status": weak_gate.get("gate_status", "UNKNOWN"),
            "backfill_count": (backfill.get("summary") or {}).get("backfill_count", 0) if isinstance(backfill.get("summary"), dict) else 0,
        },
        "warnings": warnings,
        "policy": {
            "weak_signals_not_hard_evidence": True,
            "confirmation_workflow_only": True,
            "no_full_text": True,
            "no_auto_fetch_login_sources": True,
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
            "status": item.get("confirmation_status"),
            "promote": item.get("can_promote_to_topic"),
            "source_type": item.get("required_source_type"),
            "lane": item.get("lane"),
            "title": compact_text(item.get("title"), 62),
        }
        for item in list_payload(payload, "confirmation_items")[:40]
    ]
    return f"""# Weak Signal Confirmation Workflow

## Summary

- confirmation_count: `{summary.get('confirmation_count', 0)}`
- confirmable: `{summary.get('confirmable', 0)}`
- needs_primary_source: `{summary.get('needs_primary_source', 0)}`
- needs_second_source: `{summary.get('needs_second_source', 0)}`
- manual_review: `{summary.get('manual_review', 0)}`
- watch: `{summary.get('watch', 0)}`
- blocked: `{summary.get('blocked', 0)}`
- can_promote_to_topic: `{summary.get('can_promote_to_topic', 0)}`

## Confirmation Items

{markdown_table(rows, ('status', 'promote', 'source_type', 'lane', 'title'))}

## Boundary

Weak signals need confirmation before topic activation and can never be used as hard evidence in this workflow.
"""
