"""Enrich connector metadata into constrained evidence packets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, freshness_from_run_date, markdown_table, stable_id


SOURCE_AUTHORITY = {
    "rss_official_blog": "HIGH",
    "arxiv": "HIGH",
    "github": "MEDIUM",
    "huggingface": "MEDIUM",
    "manual_url": "LOW",
}


def evidence_root(paths: ProjectPaths) -> Path:
    # This project stores evidence-adjacent topic artifacts in 03_topic_candidates.
    return paths.market_content_root / "03_topic_candidates"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = evidence_root(paths)
    return {
        "dated_json": root / f"{run_date}__connector-evidence-packets.json",
        "dated_md": root / f"{run_date}__connector-evidence-packets.md",
        "latest_json": root / "latest_connector_evidence_packets.json",
        "latest_md": root / "latest_connector_evidence_packets.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__connector-evidence-packets-board.md",
        "board_latest_md": paths.frontstage_root / "latest_connector_evidence_packets_board.md",
    }


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def source_origin_for(source_type: str) -> str:
    if source_type == "manual_url":
        return "manual"
    return "phase27_connector"


def evidence_strength(item: dict[str, Any], source_authority: str) -> str:
    summary = compact_text(item.get("summary"), 220)
    title = compact_text(item.get("title"), 220)
    source_type = str(item.get("source_type") or "")
    if source_type == "manual_url":
        return "LOW"
    if not summary:
        return "LOW"
    if source_authority == "HIGH" and len(summary) >= 40:
        return "HIGH"
    if source_authority in {"HIGH", "MEDIUM"} and title:
        return "MEDIUM"
    return "LOW"


def content_relevance(item: dict[str, Any]) -> str:
    lane = str(item.get("lane_id") or "")
    event_type = str(item.get("event_type") or "unknown")
    if lane and lane not in {"social_weak_signal"} and event_type != "unknown":
        return "HIGH"
    if lane or event_type != "unknown":
        return "MEDIUM"
    return "LOW"


def limitations_for(item: dict[str, Any], strength: str) -> list[str]:
    limitations = ["Metadata-derived evidence only; no full text was fetched or retained."]
    if not compact_text(item.get("summary"), 220):
        limitations.append("Title-only metadata; evidence strength cannot be high.")
    if str(item.get("source_type")) == "manual_url":
        limitations.append("Manual URL backfill needs operator confirmation before topic promotion.")
    if strength in {"LOW", "UNKNOWN"}:
        limitations.append("Needs corroborating source or richer metadata before writing.")
    return limitations


def packet_from_item(item: dict[str, Any], run_date: str) -> dict[str, Any]:
    source_type = str(item.get("source_type") or "manual_url")
    source_authority = SOURCE_AUTHORITY.get(source_type, "UNKNOWN")
    strength = evidence_strength(item, source_authority)
    title = compact_text(item.get("title"), 220)
    summary = compact_text(item.get("summary"), 260)
    claim_summary = compact_text(
        f"Metadata indicates a {item.get('event_type') or 'unknown'} signal: {title}. {summary}",
        320,
    )
    freshness = freshness_from_run_date(item.get("published_at") or item.get("fetched_at"), run_date)
    relevance = content_relevance(item)
    metadata_only = bool(item.get("metadata_only", True))
    copyright_safe = bool(item.get("copyright_safe", True))
    eligible = (
        metadata_only
        and copyright_safe
        and bool(item.get("url"))
        and strength in {"HIGH", "MEDIUM"}
        and relevance in {"HIGH", "MEDIUM"}
        and source_type != "manual_url"
    )
    return {
        "evidence_id": stable_id("connev", item.get("upstream_item_id") or item.get("url"), title),
        "upstream_item_id": item.get("upstream_item_id", ""),
        "title": title,
        "url": item.get("url", ""),
        "source_name": item.get("source_name", ""),
        "source_type": source_type,
        "source_origin": source_origin_for(source_type),
        "migration_candidate": False,
        "weak_signal_lane": False,
        "openclaw_candidate_ref": "",
        "source_authority": source_authority,
        "event_type": item.get("event_type", "unknown"),
        "domain_tags": item.get("domain_tags") if isinstance(item.get("domain_tags"), list) else [],
        "claim_summary": claim_summary,
        "evidence_strength": strength,
        "freshness": freshness,
        "content_relevance": relevance,
        "limitations": limitations_for(item, strength),
        "metadata_only": metadata_only,
        "copyright_safe": copyright_safe,
        "eligible_for_topic_promotion": eligible,
    }


def build_connector_evidence_packets(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    inputs = {
        "normalized_upstream_items": paths.logs_root / "latest_normalized_upstream_items.json",
        "connector_source_health_gate": paths.logs_root / "latest_connector_source_health_gate.json",
        "topic_methodology": repo_root / "config" / "topic_selection_methodology.json",
        "article_methodology": repo_root / "config" / "article_quality_methodology.json",
    }
    warnings = warning_for_missing(inputs)
    normalized = read_json(inputs["normalized_upstream_items"])
    health_gate = read_json(inputs["connector_source_health_gate"])
    topic_methodology = read_json(inputs["topic_methodology"])
    article_methodology = read_json(inputs["article_methodology"])

    packets = [packet_from_item(item, run_date) for item in list_payload(normalized, "items")]
    summary = {
        "packet_count": len(packets),
        "high_strength": sum(1 for item in packets if item.get("evidence_strength") == "HIGH"),
        "medium_strength": sum(1 for item in packets if item.get("evidence_strength") == "MEDIUM"),
        "low_strength": sum(1 for item in packets if item.get("evidence_strength") == "LOW"),
        "eligible_for_topic_promotion": sum(1 for item in packets if item.get("eligible_for_topic_promotion")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "evidence_packets": packets,
        "summary": summary,
        "input_status": {
            "normalized_item_count": len(list_payload(normalized, "items")),
            "connector_gate_status": health_gate.get("gate_status", "UNKNOWN"),
            "topic_methodology_available": bool(topic_methodology),
            "article_methodology_available": bool(article_methodology),
        },
        "warnings": warnings,
        "policy": {
            "metadata_only": True,
            "copyright_safe": True,
            "no_full_text": True,
            "metadata_derived_evidence": True,
            "no_openclaw_migration": True,
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
            "strength": item.get("evidence_strength"),
            "eligible": item.get("eligible_for_topic_promotion"),
            "source": item.get("source_type"),
            "freshness": item.get("freshness"),
            "title": compact_text(item.get("title"), 78),
        }
        for item in list_payload(payload, "evidence_packets")[:40]
    ]
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings", [])) or "- None."
    return f"""# Connector Evidence Packets

## Summary

- packet_count: `{summary.get('packet_count', 0)}`
- high_strength: `{summary.get('high_strength', 0)}`
- medium_strength: `{summary.get('medium_strength', 0)}`
- low_strength: `{summary.get('low_strength', 0)}`
- eligible_for_topic_promotion: `{summary.get('eligible_for_topic_promotion', 0)}`

## Evidence Packets

{markdown_table(rows, ('strength', 'eligible', 'source', 'freshness', 'title'))}

## Input Warnings

{warnings}

## Boundary

Evidence packets are derived from connector metadata only. They do not contain full-text captures and must not be treated as complete fact verification.
"""
