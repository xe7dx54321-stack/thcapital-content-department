"""Gate migrated OpenClaw weak signals before hot-material use."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__weak-signal-safety-gate.json",
        "dated_md": paths.logs_root / f"{run_date}__weak-signal-safety-gate.md",
        "latest_json": paths.logs_root / "latest_weak_signal_safety_gate.json",
        "latest_md": paths.logs_root / "latest_weak_signal_safety_gate.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__weak-signal-safety-gate-board.md",
        "board_latest_md": paths.frontstage_root / "latest_weak_signal_safety_gate_board.md",
    }


def flatten_items(connector_run: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for connector in list_payload(connector_run, "connectors"):
        connector_type = connector.get("connector_type", "")
        status = connector.get("status", "")
        for item in connector.get("items", []) if isinstance(connector.get("items"), list) else []:
            if isinstance(item, dict):
                merged = dict(item)
                merged["connector_type"] = connector_type
                merged["connector_status"] = status
                items.append(merged)
    return items


def classification_by_source(risk: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("source_id")): item for item in list_payload(risk, "classified_sources") if item.get("source_id")}


def safety_for(item: dict[str, Any], classification: dict[str, Any]) -> dict[str, Any]:
    source_name = str(item.get("source_name") or "")
    lane = str(item.get("lane") or classification.get("lane") or "")
    connector_type = str(item.get("connector_type") or "")
    role = str(item.get("evidence_role") or classification.get("evidence_role") or "")
    weak = bool(item.get("weak_signal")) or role in {"weak_signal", "heat_validation", "manual_only"} or connector_type in {
        "reddit_metadata",
        "youtube_metadata",
        "x_metadata",
        "trend_heat_metadata",
        "wechat_metadata",
    }
    risk_flags: list[str] = []
    if weak:
        risk_flags.append("weak_signal_not_hard_evidence")
    if role == "manual_only" or connector_type == "wechat_metadata":
        decision = "MANUAL_REVIEW"
        can_hot = False
        confirmation = "Manual source review required; do not auto-fetch WeChat or full text."
        risk_flags.append("manual_only")
    elif connector_type in {"reddit_metadata", "youtube_metadata", "trend_heat_metadata"}:
        decision = "REQUIRE_CONFIRMATION"
        can_hot = True
        confirmation = "Confirm with official or authoritative source before using in content."
    elif connector_type == "x_metadata":
        decision = "MANUAL_REVIEW"
        can_hot = False
        confirmation = "X source requires manual review; do not auto-fetch login/account-state content."
        risk_flags.append("login_or_api_risk")
    elif classification.get("allowed_ingestion") == "do_not_ingest" or classification.get("risk_level") == "BLOCKED":
        decision = "BLOCK"
        can_hot = False
        confirmation = "Blocked by OpenClaw source risk classification."
        risk_flags.append("blocked_source")
    else:
        decision = "ALLOW_AS_WEAK_SIGNAL"
        can_hot = True
        confirmation = "Use as supporting signal only; attach stronger evidence before claims."
    return {
        "item_id": item.get("item_id", ""),
        "source_name": source_name,
        "lane": lane,
        "weak_signal": True,
        "safety_decision": decision,
        "can_promote_to_hot_material": can_hot,
        "can_use_as_hard_evidence": False,
        "required_confirmation": confirmation,
        "risk_flags": risk_flags,
    }


def run_weak_signal_safety_gate(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    connector_path = paths.logs_root / "latest_openclaw_metadata_connector_run.json"
    risk_path = paths.logs_root / "latest_openclaw_source_risk_classification.json"
    connector = read_json(connector_path)
    risk = read_json(risk_path)
    class_map = classification_by_source(risk)
    items = [safety_for(item, class_map.get(str(item.get("source_id")), {})) for item in flatten_items(connector)]
    summary = {
        "item_count": len(items),
        "allow_as_weak_signal": sum(1 for item in items if item.get("safety_decision") == "ALLOW_AS_WEAK_SIGNAL"),
        "require_confirmation": sum(1 for item in items if item.get("safety_decision") == "REQUIRE_CONFIRMATION"),
        "manual_review": sum(1 for item in items if item.get("safety_decision") == "MANUAL_REVIEW"),
        "blocked": sum(1 for item in items if item.get("safety_decision") == "BLOCK"),
        "hard_evidence_allowed": sum(1 for item in items if item.get("can_use_as_hard_evidence")),
    }
    if summary["blocked"]:
        gate_status = "BLOCKED"
    elif summary["manual_review"] or summary["require_confirmation"]:
        gate_status = "ACTIONABLE"
    elif items:
        gate_status = "PASS"
    else:
        gate_status = "WARN"
    warnings = []
    if not connector_path.exists():
        warnings.append(f"Missing input: {connector_path}")
    if not risk_path.exists():
        warnings.append(f"Missing input: {risk_path}")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "gate_status": gate_status,
        "items": items,
        "summary": summary,
        "warnings": warnings,
        "policy": {
            "weak_signals_not_hard_evidence": True,
            "reddit_x_youtube_trend_wechat_not_hard_evidence": True,
            "no_full_text": True,
            "no_login_or_paywall_bypass": True,
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
            "decision": item.get("safety_decision"),
            "hard": item.get("can_use_as_hard_evidence"),
            "lane": item.get("lane"),
            "source": compact_text(item.get("source_name"), 58),
        }
        for item in list_payload(payload, "items")[:40]
    ]
    return f"""# Weak Signal Safety Gate

## Summary

- gate_status: `{payload.get('gate_status')}`
- item_count: `{summary.get('item_count', 0)}`
- allow_as_weak_signal: `{summary.get('allow_as_weak_signal', 0)}`
- require_confirmation: `{summary.get('require_confirmation', 0)}`
- manual_review: `{summary.get('manual_review', 0)}`
- blocked: `{summary.get('blocked', 0)}`
- hard_evidence_allowed: `{summary.get('hard_evidence_allowed', 0)}`

## Items

{markdown_table(rows, ('decision', 'hard', 'lane', 'source'))}

## Boundary

OpenClaw migrated Reddit, X, YouTube, heat, and WeChat signals default to weak/supporting roles and cannot be used as hard evidence.
"""
