"""Normalize OpenClaw metadata connector items into weak/supporting signals."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__normalized-openclaw-signals.json",
        "dated_md": paths.logs_root / f"{run_date}__normalized-openclaw-signals.md",
        "latest_json": paths.logs_root / "latest_normalized_openclaw_signals.json",
        "latest_md": paths.logs_root / "latest_normalized_openclaw_signals.md",
    }


def flatten_items(connector_run: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for connector in list_payload(connector_run, "connectors"):
        connector_type = connector.get("connector_type", "")
        for item in connector.get("items", []) if isinstance(connector.get("items"), list) else []:
            if isinstance(item, dict):
                merged = dict(item)
                merged["connector_type"] = connector_type
                items.append(merged)
    return items


def safety_by_item(gate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("item_id")): item for item in list_payload(gate, "items") if item.get("item_id")}


def signal_from_item(item: dict[str, Any], safety: dict[str, Any]) -> dict[str, Any]:
    decision = str(safety.get("safety_decision") or "MANUAL_REVIEW")
    role = str(item.get("evidence_role") or "weak_signal")
    can_hot = bool(safety.get("can_promote_to_hot_material"))
    if not item.get("url") and decision != "ALLOW_AS_WEAK_SIGNAL":
        can_hot = False
    return {
        "signal_id": stable_id("ocsignal", item.get("item_id"), item.get("url")),
        "source_id": item.get("source_id", ""),
        "source_name": item.get("source_name", ""),
        "title": item.get("title", ""),
        "url": item.get("url", ""),
        "lane": item.get("lane", ""),
        "source_origin": "openclaw_migration",
        "evidence_role": role if role in {"supporting_evidence", "weak_signal", "heat_validation", "manual_only"} else "weak_signal",
        "weak_signal": True,
        "can_use_as_hard_evidence": False,
        "metadata_only": bool(item.get("metadata_only", True)),
        "copyright_safe": bool(item.get("copyright_safe", True)),
        "candidate_for_hot_material_pool": can_hot,
        "required_confirmation": safety.get("required_confirmation", "Confirm with stronger source before content claims."),
    }


def normalize_openclaw_signals(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    connector_path = paths.logs_root / "latest_openclaw_metadata_connector_run.json"
    gate_path = paths.logs_root / "latest_weak_signal_safety_gate.json"
    connector = read_json(connector_path)
    gate = read_json(gate_path)
    safety_map = safety_by_item(gate)
    signals = [signal_from_item(item, safety_map.get(str(item.get("item_id")), {})) for item in flatten_items(connector)]
    summary = {
        "signal_count": len(signals),
        "weak_signal_count": sum(1 for item in signals if item.get("weak_signal")),
        "candidate_for_hot_material_pool": sum(1 for item in signals if item.get("candidate_for_hot_material_pool")),
        "hard_evidence_allowed": sum(1 for item in signals if item.get("can_use_as_hard_evidence")),
    }
    warnings = []
    if not connector_path.exists():
        warnings.append(f"Missing input: {connector_path}")
    if not gate_path.exists():
        warnings.append(f"Missing input: {gate_path}")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "signals": signals,
        "summary": summary,
        "warnings": warnings,
        "policy": {
            "source_origin": "openclaw_migration",
            "metadata_only": True,
            "copyright_safe": True,
            "weak_signals_not_hard_evidence": True,
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
            "candidate": item.get("candidate_for_hot_material_pool"),
            "hard": item.get("can_use_as_hard_evidence"),
            "role": item.get("evidence_role"),
            "lane": item.get("lane"),
            "title": compact_text(item.get("title"), 58),
        }
        for item in list_payload(payload, "signals")[:40]
    ]
    return f"""# Normalized OpenClaw Signals

## Summary

- signal_count: `{summary.get('signal_count', 0)}`
- weak_signal_count: `{summary.get('weak_signal_count', 0)}`
- candidate_for_hot_material_pool: `{summary.get('candidate_for_hot_material_pool', 0)}`
- hard_evidence_allowed: `{summary.get('hard_evidence_allowed', 0)}`

## Signals

{markdown_table(rows, ('candidate', 'hard', 'role', 'lane', 'title'))}

## Boundary

Normalized OpenClaw signals are metadata-only and default to weak/supporting roles. They cannot be used as hard evidence.
"""
