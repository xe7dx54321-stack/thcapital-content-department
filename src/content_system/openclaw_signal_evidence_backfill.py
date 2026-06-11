"""Build metadata-only evidence backfill tasks for migrated OpenClaw signals."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


WEAK_LANES = {"reddit_llm_discussion", "youtube_signal", "x_signal", "trend_heat"}


def evidence_root(paths: ProjectPaths) -> Path:
    # This repository stores evidence-adjacent generated artifacts in 03_topic_candidates.
    return paths.market_content_root / "03_topic_candidates"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = evidence_root(paths)
    return {
        "dated_json": root / f"{run_date}__openclaw-signal-evidence-backfill.json",
        "dated_md": root / f"{run_date}__openclaw-signal-evidence-backfill.md",
        "latest_json": root / "latest_openclaw_signal_evidence_backfill.json",
        "latest_md": root / "latest_openclaw_signal_evidence_backfill.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__openclaw-signal-evidence-backfill-board.md",
        "board_latest_md": paths.frontstage_root / "latest_openclaw_signal_evidence_backfill_board.md",
    }


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def flatten_connector_items(connector_run: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for connector in list_payload(connector_run, "connectors"):
        connector_type = connector.get("connector_type", "")
        for item in connector.get("items", []) if isinstance(connector.get("items"), list) else []:
            if isinstance(item, dict):
                merged = dict(item)
                merged["connector_type"] = connector_type
                items.append(merged)
    return items


def connector_lookup(connector_run: dict[str, Any]) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for item in flatten_connector_items(connector_run):
        for key in (item.get("item_id"), item.get("source_id"), item.get("url")):
            if key:
                lookup[str(key)] = item
    return lookup


def safety_lookup(gate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("item_id")): item for item in list_payload(gate, "items") if item.get("item_id")}


def suggested_confirmation_sources(lane: str, role: str) -> list[str]:
    if lane == "funding_startup":
        return ["primary company announcement", "funding announcement", "second reputable media source"]
    if lane == "builder_research":
        return ["original author/source page", "official project/company page", "second technical source"]
    if lane == "chinese_ai_media":
        return ["original official source", "manual Chinese media review"]
    if lane in WEAK_LANES:
        return ["official company/lab source", "primary project page", "reputable media confirmation"]
    if role == "manual_only":
        return ["manual operator review"]
    return ["primary source", "second corroborating source"]


def claim_summary_for(signal: dict[str, Any]) -> str:
    title = compact_text(signal.get("title") or signal.get("source_name"), 180)
    source = compact_text(signal.get("source_name"), 80)
    lane = signal.get("lane") or "unknown"
    return compact_text(f"OpenClaw migrated metadata suggests a {lane} signal from {source}: {title}.", 260)


def status_for_signal(signal: dict[str, Any], connector_item: dict[str, Any], safety: dict[str, Any]) -> tuple[str, bool, list[str]]:
    lane = str(signal.get("lane") or "")
    role = str(signal.get("evidence_role") or "weak_signal")
    has_core_metadata = bool(signal.get("url")) and bool(signal.get("title")) and bool(signal.get("source_name"))
    has_time = bool(connector_item.get("published_at") or connector_item.get("fetched_at"))
    limitations = ["Metadata-only backfill task; no full text was fetched or retained."]
    if safety.get("safety_decision") == "BLOCK":
        return "BLOCKED", False, limitations + ["Blocked by weak signal safety gate."]
    if role == "manual_only" or lane == "chinese_ai_media":
        return "NEEDS_MANUAL_REVIEW", False, limitations + ["Manual review is required before any topic activation."]
    if lane in WEAK_LANES or role in {"weak_signal", "heat_validation"}:
        return "NEEDS_PRIMARY_SOURCE", False, limitations + ["Weak signal requires primary or second-source confirmation."]
    if role == "supporting_evidence" and has_core_metadata and has_time:
        return "READY_FOR_CONFIRMATION", True, limitations + ["Can be reviewed as supporting evidence, but not hard evidence."]
    if role == "supporting_evidence" and has_core_metadata:
        return "NEEDS_PRIMARY_SOURCE", False, limitations + ["Missing reliable timestamp; confirm with primary source."]
    if has_core_metadata:
        return "WATCH", False, limitations + ["Signal is usable for monitoring but not ready for activation."]
    return "NEEDS_PRIMARY_SOURCE", False, limitations + ["Missing title, URL, or source metadata."]


def backfill_from_signal(signal: dict[str, Any], connector_items: dict[str, dict[str, Any]], safety_items: dict[str, dict[str, Any]]) -> dict[str, Any]:
    connector_item = (
        connector_items.get(str(signal.get("source_id") or ""))
        or connector_items.get(str(signal.get("url") or ""))
        or {}
    )
    safety = safety_items.get(str(connector_item.get("item_id") or "")) or {}
    status, eligible, limitations = status_for_signal(signal, connector_item, safety)
    lane = str(signal.get("lane") or "")
    role = str(signal.get("evidence_role") or "weak_signal")
    return {
        "backfill_id": stable_id("ocbev", signal.get("signal_id"), signal.get("url")),
        "signal_id": signal.get("signal_id", ""),
        "source_id": signal.get("source_id", ""),
        "source_name": signal.get("source_name", ""),
        "title": compact_text(signal.get("title") or signal.get("source_name"), 180),
        "url": signal.get("url", ""),
        "lane": lane,
        "evidence_role": role if role in {"supporting_evidence", "weak_signal", "heat_validation", "manual_only"} else "weak_signal",
        "backfill_status": status,
        "suggested_confirmation_sources": suggested_confirmation_sources(lane, role),
        "claim_summary": claim_summary_for(signal),
        "limitations": limitations,
        "metadata_only": True,
        "copyright_safe": True,
        "can_use_as_hard_evidence": False,
        "eligible_for_topic_activation": eligible,
    }


def build_openclaw_signal_evidence_backfill(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    topic_root = paths.market_content_root / "03_topic_candidates"
    inputs = {
        "normalized_openclaw_signals": paths.logs_root / "latest_normalized_openclaw_signals.json",
        "weak_signal_safety_gate": paths.logs_root / "latest_weak_signal_safety_gate.json",
        "openclaw_metadata_connector_run": paths.logs_root / "latest_openclaw_metadata_connector_run.json",
        "connector_evidence_packets": topic_root / "latest_connector_evidence_packets.json",
        "hot_material_quality_gate": paths.logs_root / "latest_hot_material_quality_gate.json",
    }
    warnings = warning_for_missing(inputs)
    normalized = read_json(inputs["normalized_openclaw_signals"])
    safety_gate = read_json(inputs["weak_signal_safety_gate"])
    connector_run = read_json(inputs["openclaw_metadata_connector_run"])
    connector_evidence = read_json(inputs["connector_evidence_packets"])
    hot_gate = read_json(inputs["hot_material_quality_gate"])

    connector_items = connector_lookup(connector_run)
    safety_items = safety_lookup(safety_gate)
    backfill_items = [
        backfill_from_signal(signal, connector_items, safety_items)
        for signal in list_payload(normalized, "signals")
    ]
    summary = {
        "backfill_count": len(backfill_items),
        "ready_for_confirmation": sum(1 for item in backfill_items if item.get("backfill_status") == "READY_FOR_CONFIRMATION"),
        "needs_primary_source": sum(1 for item in backfill_items if item.get("backfill_status") == "NEEDS_PRIMARY_SOURCE"),
        "needs_manual_review": sum(1 for item in backfill_items if item.get("backfill_status") == "NEEDS_MANUAL_REVIEW"),
        "watch": sum(1 for item in backfill_items if item.get("backfill_status") == "WATCH"),
        "blocked": sum(1 for item in backfill_items if item.get("backfill_status") == "BLOCKED"),
        "eligible_for_topic_activation": sum(1 for item in backfill_items if item.get("eligible_for_topic_activation")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "backfill_items": backfill_items,
        "summary": summary,
        "input_status": {
            "normalized_signal_count": len(list_payload(normalized, "signals")),
            "weak_signal_gate_status": safety_gate.get("gate_status", "UNKNOWN"),
            "connector_evidence_packet_count": (connector_evidence.get("summary") or {}).get("packet_count", 0)
            if isinstance(connector_evidence.get("summary"), dict)
            else 0,
            "hot_material_gate_status": hot_gate.get("gate_status", "UNKNOWN"),
        },
        "warnings": warnings,
        "policy": {
            "metadata_only": True,
            "copyright_safe": True,
            "no_full_text": True,
            "does_not_verify_facts": True,
            "weak_signals_not_hard_evidence": True,
            "no_openclaw_gateway": True,
            "no_openclaw_cron_migration": True,
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
            "status": item.get("backfill_status"),
            "role": item.get("evidence_role"),
            "lane": item.get("lane"),
            "eligible": item.get("eligible_for_topic_activation"),
            "title": compact_text(item.get("title"), 64),
        }
        for item in list_payload(payload, "backfill_items")[:40]
    ]
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings", [])) or "- None."
    return f"""# OpenClaw Signal Evidence Backfill

## Summary

- backfill_count: `{summary.get('backfill_count', 0)}`
- ready_for_confirmation: `{summary.get('ready_for_confirmation', 0)}`
- needs_primary_source: `{summary.get('needs_primary_source', 0)}`
- needs_manual_review: `{summary.get('needs_manual_review', 0)}`
- watch: `{summary.get('watch', 0)}`
- blocked: `{summary.get('blocked', 0)}`
- eligible_for_topic_activation: `{summary.get('eligible_for_topic_activation', 0)}`

## Backfill Items

{markdown_table(rows, ('status', 'role', 'lane', 'eligible', 'title'))}

## Input Warnings

{warnings}

## Boundary

This is metadata-derived backfill planning only. It does not fetch full text, verify claims automatically, start OpenClaw gateway, migrate cron jobs, or turn weak signals into hard evidence.
"""
