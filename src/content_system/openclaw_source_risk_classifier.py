"""Classify OpenClaw sources by migration risk and evidence role."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__openclaw-source-risk-classification.json",
        "dated_md": paths.logs_root / f"{run_date}__openclaw-source-risk-classification.md",
        "latest_json": paths.logs_root / "latest_openclaw_source_risk_classification.json",
        "latest_md": paths.logs_root / "latest_openclaw_source_risk_classification.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__openclaw-source-risk-classification-board.md",
        "board_latest_md": paths.frontstage_root / "latest_openclaw_source_risk_classification_board.md",
    }


def priority_for(source: dict[str, Any]) -> str:
    source_type = str(source.get("source_type") or "")
    lane = str(source.get("lane_hint") or "")
    source_id = str(source.get("source_id") or "")
    name = str(source.get("source_name") or "")
    haystack = f"{source_id} {name} {lane}".lower()
    if source_id.startswith("openclaw_capability__"):
        return "DO_NOT_MIGRATE"
    if source_type in {"yc", "media", "newsletter"}:
        return "P0" if any(token in haystack for token in ("yc", "techcrunch", "finsmes", "deeplearning", "latent", "interconnects", "simon", "understanding", "infoq")) else "P1"
    if source_type == "reddit":
        return "P0"
    if source_type == "wechat":
        return "P1" if any(token in haystack for token in ("36kr", "36氪", "geek", "机器", "新智元", "zhidx", "guixingren")) else "P2"
    if source_type in {"trend_heat", "youtube"}:
        return "P1"
    if source_type == "x":
        return "P2"
    if source_type == "industry_trial":
        return "P2" if safe_int(source.get("enabled_job_count")) else "P3"
    return "P3"


def classify_source(source: dict[str, Any], config_text: str) -> dict[str, Any]:
    source_id = str(source.get("source_id") or "")
    source_name = str(source.get("source_name") or "")
    source_type = str(source.get("source_type") or "unknown")
    lane = str(source.get("lane_hint") or "unknown")
    priority = priority_for(source)
    configured = source_id in config_text
    if priority == "DO_NOT_MIGRATE":
        return {
            "source_id": source_id,
            "source_name": source_name,
            "lane": lane,
            "migration_priority": "DO_NOT_MIGRATE",
            "risk_level": "BLOCKED",
            "evidence_role": "blocked",
            "allowed_ingestion": "do_not_ingest",
            "requires_login": True,
            "requires_api_key": False,
            "copyright_risk": "HIGH",
            "fact_risk": "HIGH",
            "reason": "OpenClaw capability is explicitly outside current project scope.",
            "migration_note": "Do not migrate gateway, cron, WeChat full-text deep capture, draftbox, publishing, or result backflow.",
        }
    if source_type in {"reddit", "youtube", "trend_heat"}:
        return {
            "source_id": source_id,
            "source_name": source_name,
            "lane": "reddit_llm_discussion" if source_type == "reddit" else lane,
            "migration_priority": priority,
            "risk_level": "MEDIUM",
            "evidence_role": "weak_signal" if source_type != "trend_heat" else "heat_validation",
            "allowed_ingestion": "metadata_connector",
            "requires_login": False,
            "requires_api_key": False,
            "copyright_risk": "LOW",
            "fact_risk": "HIGH",
            "reason": "Useful for attention and weak signal detection, but not reliable as hard evidence.",
            "migration_note": "Allow metadata-only ingestion; require confirmation before content claims.",
        }
    if source_type == "x":
        return {
            "source_id": source_id,
            "source_name": source_name,
            "lane": "x_signal",
            "migration_priority": priority,
            "risk_level": "HIGH",
            "evidence_role": "weak_signal",
            "allowed_ingestion": "sidecar_inventory_only",
            "requires_login": True,
            "requires_api_key": False,
            "copyright_risk": "MEDIUM",
            "fact_risk": "HIGH",
            "reason": "X content commonly requires login/API and is weak signal only.",
            "migration_note": "Do not auto-fetch X; keep as inventory or manual URL only.",
        }
    if source_type == "wechat":
        return {
            "source_id": source_id,
            "source_name": source_name,
            "lane": "chinese_ai_media",
            "migration_priority": priority,
            "risk_level": "HIGH",
            "evidence_role": "manual_only",
            "allowed_ingestion": "manual_backfill",
            "requires_login": False,
            "requires_api_key": False,
            "copyright_risk": "HIGH",
            "fact_risk": "MEDIUM",
            "reason": "Chinese media coverage is valuable, but current project must not deep-crawl WeChat full text.",
            "migration_note": "Use metadata/manual backfill only; never auto-fetch article body or backend data.",
        }
    if source_type in {"yc", "media", "newsletter"}:
        return {
            "source_id": source_id,
            "source_name": source_name,
            "lane": "funding_startup" if source_type in {"yc", "media"} and any(token in source_id.lower() for token in ("yc", "techcrunch", "finsmes")) else "builder_research",
            "migration_priority": priority,
            "risk_level": "LOW" if source_type != "media" else "MEDIUM",
            "evidence_role": "supporting_evidence",
            "allowed_ingestion": "metadata_connector",
            "requires_login": False,
            "requires_api_key": False,
            "copyright_risk": "LOW" if source_type != "media" else "MEDIUM",
            "fact_risk": "MEDIUM",
            "reason": "Public metadata can broaden upstream coverage without full-text capture.",
            "migration_note": "Metadata-only connector candidate." + (" Already present in config/sources.yaml." if configured else ""),
        }
    if source_type == "industry_trial":
        return {
            "source_id": source_id,
            "source_name": source_name,
            "lane": "industry_deep_research",
            "migration_priority": priority,
            "risk_level": "MEDIUM",
            "evidence_role": "manual_only",
            "allowed_ingestion": "manual_backfill",
            "requires_login": False,
            "requires_api_key": False,
            "copyright_risk": "MEDIUM",
            "fact_risk": "MEDIUM",
            "reason": "Valuable for vertical industry research, but should not pollute the daily AI hot material lane.",
            "migration_note": "Keep as P2/P3 manual or later specialized lane.",
        }
    return {
        "source_id": source_id,
        "source_name": source_name,
        "lane": lane,
        "migration_priority": priority,
        "risk_level": "MEDIUM",
        "evidence_role": "manual_only",
        "allowed_ingestion": "manual_backfill",
        "requires_login": False,
        "requires_api_key": False,
        "copyright_risk": "MEDIUM",
        "fact_risk": "MEDIUM",
        "reason": "Unknown source type needs operator review before migration.",
        "migration_note": "Classified conservatively.",
    }


def build_openclaw_source_risk_classification(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    inventory_path = paths.logs_root / "latest_openclaw_source_inventory.json"
    sources_config = repo_root / "config" / "sources.yaml"
    audit_path = paths.logs_root / "latest_source_coverage_gap_audit.json"
    inventory = read_json(inventory_path)
    audit = read_json(audit_path)
    config_text = sources_config.read_text(encoding="utf-8") if sources_config.exists() else ""
    classified = [classify_source(source, config_text) for source in list_payload(inventory, "sources")]
    summary = {
        "source_count": len(classified),
        "p0": sum(1 for item in classified if item.get("migration_priority") == "P0"),
        "p1": sum(1 for item in classified if item.get("migration_priority") == "P1"),
        "p2": sum(1 for item in classified if item.get("migration_priority") == "P2"),
        "p3": sum(1 for item in classified if item.get("migration_priority") == "P3"),
        "do_not_migrate": sum(1 for item in classified if item.get("migration_priority") == "DO_NOT_MIGRATE"),
        "metadata_connector": sum(1 for item in classified if item.get("allowed_ingestion") == "metadata_connector"),
        "manual_backfill": sum(1 for item in classified if item.get("allowed_ingestion") == "manual_backfill"),
        "weak_signal": sum(1 for item in classified if item.get("evidence_role") in {"weak_signal", "heat_validation"}),
        "blocked": sum(1 for item in classified if item.get("risk_level") == "BLOCKED" or item.get("allowed_ingestion") == "do_not_ingest"),
    }
    warnings = []
    if not inventory_path.exists():
        warnings.append(f"Missing input: {inventory_path}")
    if not sources_config.exists():
        warnings.append(f"Missing input: {sources_config}")
    if not audit_path.exists():
        warnings.append(f"Missing input: {audit_path}")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "classified_sources": classified,
        "summary": summary,
        "context": {
            "source_gap_audit_available": bool(audit),
            "config_sources_available": bool(config_text),
        },
        "warnings": warnings,
        "policy": {
            "risk_classification_only": True,
            "does_not_fetch_sources": True,
            "does_not_mutate_config": True,
            "weak_signals_not_hard_evidence": True,
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
            "priority": item.get("migration_priority"),
            "risk": item.get("risk_level"),
            "role": item.get("evidence_role"),
            "ingestion": item.get("allowed_ingestion"),
            "source": compact_text(item.get("source_name"), 52),
        }
        for item in list_payload(payload, "classified_sources")[:48]
    ]
    return f"""# OpenClaw Source Risk Classification

## Summary

- source_count: `{summary.get('source_count', 0)}`
- p0/p1/p2/p3: `{summary.get('p0', 0)}` / `{summary.get('p1', 0)}` / `{summary.get('p2', 0)}` / `{summary.get('p3', 0)}`
- do_not_migrate: `{summary.get('do_not_migrate', 0)}`
- metadata_connector: `{summary.get('metadata_connector', 0)}`
- manual_backfill: `{summary.get('manual_backfill', 0)}`
- weak_signal: `{summary.get('weak_signal', 0)}`
- blocked: `{summary.get('blocked', 0)}`

## Classified Sources

{markdown_table(rows, ('priority', 'risk', 'role', 'ingestion', 'source'))}

## Boundary

Reddit, X, YouTube, trend heat, and WeChat sources are not hard evidence. Login/paywall/full-text/WeChat draftbox or publishing capabilities are blocked from migration.
"""
