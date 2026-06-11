"""Build a sidecar proposal for future OpenClaw source registry changes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__openclaw-source-registry-proposal.json",
        "dated_md": paths.logs_root / f"{run_date}__openclaw-source-registry-proposal.md",
        "latest_json": paths.logs_root / "latest_openclaw_source_registry_proposal.json",
        "latest_md": paths.logs_root / "latest_openclaw_source_registry_proposal.md",
    }


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def risk_by_source(risk: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("source_id")): item for item in list_payload(risk, "classified_sources") if item.get("source_id")}


def confirmation_promotable_sources(workflow: dict[str, Any]) -> set[str]:
    promotable: set[str] = set()
    for item in list_payload(workflow, "confirmation_items"):
        if item.get("can_promote_to_topic"):
            # Confirmation artifacts keep source name but not source_id; source-level routing stays conservative.
            promotable.add(str(item.get("source_name") or ""))
    return promotable


def registry_action(candidate: dict[str, Any], risk: dict[str, Any], config_text: str, gate_status: str, promotable_names: set[str]) -> tuple[str, str]:
    source_id = str(candidate.get("source_id") or "")
    source_name = str(candidate.get("source_name") or "")
    if source_id in config_text:
        return "DO_NOT_ADD", "Already present or referenced in config/sources.yaml."
    if risk.get("risk_level") == "BLOCKED" or risk.get("allowed_ingestion") == "do_not_ingest":
        return "DO_NOT_ADD", "Blocked by OpenClaw source risk classification."
    if candidate.get("requires_login") or candidate.get("requires_api_key"):
        return "MANUAL_BACKFILL_ONLY", "Requires login or API key; keep outside automated registry."
    if candidate.get("evidence_role") == "manual_only" or candidate.get("connector_type") in {"wechat_metadata", "x_metadata"}:
        return "MANUAL_BACKFILL_ONLY", "Manual-only or account-state-sensitive source; do not enable as connector."
    if candidate.get("evidence_role") in {"weak_signal", "heat_validation"}:
        return "ADD_AS_DISABLED", "Weak/heat signal can be inventoried as disabled metadata source pending confirmation."
    if gate_status == "BLOCKED":
        return "ADD_AS_DISABLED", "Regression gate is blocked; keep candidate disabled until resolved."
    if source_name in promotable_names and candidate.get("migration_priority") == "P0":
        return "ADD_AS_ENABLED", "P0 supporting source with confirmable metadata; safe as future metadata connector proposal."
    return "ADD_AS_DISABLED", "Supporting metadata source candidate; enable only after operator review."


def yaml_snippet(candidate: dict[str, Any], action: str) -> str:
    if action in {"DO_NOT_ADD", "MANUAL_BACKFILL_ONLY"}:
        return ""
    enabled = "true" if action == "ADD_AS_ENABLED" else "false"
    return (
        f"- id: {candidate.get('source_id', '')}\n"
        f"  name: {candidate.get('source_name', '')}\n"
        f"  type: {candidate.get('connector_type', 'metadata')}\n"
        f"  lane: {candidate.get('lane', '')}\n"
        f"  enabled: {enabled}\n"
        "  metadata_only: true\n"
        "  do_not_fetch_full_text: true\n"
    )


def proposal_from_candidate(candidate: dict[str, Any], risk: dict[str, Any], action: str, reason: str) -> dict[str, Any]:
    return {
        "proposal_id": stable_id("ocreg", candidate.get("source_id"), action),
        "source_id": candidate.get("source_id", ""),
        "source_name": candidate.get("source_name", ""),
        "recommended_registry_action": action,
        "lane": candidate.get("lane", ""),
        "source_type": candidate.get("connector_type", ""),
        "evidence_role": candidate.get("evidence_role", "manual_only"),
        "requires_login": bool(candidate.get("requires_login")),
        "requires_api_key": bool(candidate.get("requires_api_key")),
        "risk_level": risk.get("risk_level", "MEDIUM"),
        "reason": reason,
        "proposed_yaml_snippet": yaml_snippet(candidate, action),
        "auto_apply": False,
    }


def build_openclaw_source_registry_proposal(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    inputs = {
        "openclaw_migration_plan": paths.logs_root / "latest_openclaw_migration_plan.json",
        "openclaw_source_risk_classification": paths.logs_root / "latest_openclaw_source_risk_classification.json",
        "openclaw_metadata_connector_run": paths.logs_root / "latest_openclaw_metadata_connector_run.json",
        "weak_signal_confirmation_workflow": paths.logs_root / "latest_weak_signal_confirmation_workflow.json",
        "openclaw_to_content_regression_gate": paths.logs_root / "latest_openclaw_to_content_regression_gate.json",
        "sources_config": repo_root / "config" / "sources.yaml",
    }
    warnings = warning_for_missing(inputs)
    plan = read_json(inputs["openclaw_migration_plan"])
    risk_payload = read_json(inputs["openclaw_source_risk_classification"])
    connectors = read_json(inputs["openclaw_metadata_connector_run"])
    workflow = read_json(inputs["weak_signal_confirmation_workflow"])
    gate = read_json(inputs["openclaw_to_content_regression_gate"])
    config_text = inputs["sources_config"].read_text(encoding="utf-8") if inputs["sources_config"].exists() else ""
    risks = risk_by_source(risk_payload)
    promotable_names = confirmation_promotable_sources(workflow)
    proposals: list[dict[str, Any]] = []
    for candidate in list_payload(plan, "migration_candidates"):
        risk = risks.get(str(candidate.get("source_id") or ""), {})
        action, reason = registry_action(candidate, risk, config_text, str(gate.get("gate_status") or ""), promotable_names)
        proposals.append(proposal_from_candidate(candidate, risk, action, reason))
    summary = {
        "proposal_count": len(proposals),
        "add_as_enabled": sum(1 for item in proposals if item.get("recommended_registry_action") == "ADD_AS_ENABLED"),
        "add_as_disabled": sum(1 for item in proposals if item.get("recommended_registry_action") == "ADD_AS_DISABLED"),
        "manual_backfill_only": sum(1 for item in proposals if item.get("recommended_registry_action") == "MANUAL_BACKFILL_ONLY"),
        "do_not_add": sum(1 for item in proposals if item.get("recommended_registry_action") == "DO_NOT_ADD"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "proposal_items": proposals,
        "summary": summary,
        "input_status": {
            "connector_item_count": (connectors.get("summary") or {}).get("item_count", 0) if isinstance(connectors.get("summary"), dict) else 0,
            "regression_gate_status": gate.get("gate_status", "UNKNOWN"),
        },
        "warnings": warnings,
        "policy": {
            "auto_apply": False,
            "does_not_modify_sources_yaml": True,
            "sidecar_only": True,
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
            "action": item.get("recommended_registry_action"),
            "risk": item.get("risk_level"),
            "role": item.get("evidence_role"),
            "lane": item.get("lane"),
            "source": compact_text(item.get("source_name"), 52),
        }
        for item in list_payload(payload, "proposal_items")[:48]
    ]
    return f"""# OpenClaw Source Registry Proposal

## Summary

- proposal_count: `{summary.get('proposal_count', 0)}`
- add_as_enabled: `{summary.get('add_as_enabled', 0)}`
- add_as_disabled: `{summary.get('add_as_disabled', 0)}`
- manual_backfill_only: `{summary.get('manual_backfill_only', 0)}`
- do_not_add: `{summary.get('do_not_add', 0)}`

## Proposal Items

{markdown_table(rows, ('action', 'risk', 'role', 'lane', 'source'))}

## Boundary

This is a sidecar proposal only. It never modifies config/sources.yaml, never stages YAML snippets as config, and all proposal_items have auto_apply=false.
"""
