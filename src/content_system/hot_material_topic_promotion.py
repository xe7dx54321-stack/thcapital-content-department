"""Promote qualified hot materials into connector topic candidates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    topic_root = paths.market_content_root / "03_topic_candidates"
    return {
        "dated_json": topic_root / f"{run_date}__connector-promoted-topic-candidates.json",
        "dated_md": topic_root / f"{run_date}__connector-promoted-topic-candidates.md",
        "latest_json": topic_root / "latest_connector_promoted_topic_candidates.json",
        "latest_md": topic_root / "latest_connector_promoted_topic_candidates.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__connector-promoted-topic-candidates-board.md",
        "board_latest_md": paths.frontstage_root / "latest_connector_promoted_topic_candidates_board.md",
    }


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def topic_type_for(material: dict[str, Any], evidence: dict[str, Any] | None) -> str:
    event_type = str((evidence or {}).get("event_type") or material.get("event_type") or "unknown")
    lane = str(material.get("lane_id") or "")
    if event_type == "paper" or lane == "paper_research":
        return "technical_route_analysis"
    if event_type == "open_source" or lane in {"agent_framework", "open_source"}:
        return "technical_route_analysis"
    if event_type in {"model_release", "product_update"}:
        return "product_strategy_analysis"
    if event_type == "funding":
        return "investment_framework"
    return "news_explainer"


def recommended_content_type(topic_type: str) -> str:
    return {
        "technical_route_analysis": "技术路线解析 / Agent Infra 深度分析",
        "product_strategy_analysis": "产品策略分析 / 公司动态解读",
        "investment_framework": "投资框架 / 创业公司观察",
        "trend_judgment": "趋势判断",
        "company_project_deep_dive": "项目深度拆解",
        "news_explainer": "热点解释器",
    }.get(topic_type, "热点解释器")


def evidence_index(packets: list[dict[str, Any]]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    by_upstream: dict[str, list[dict[str, Any]]] = {}
    by_title: dict[str, list[dict[str, Any]]] = {}
    for packet in packets:
        upstream_id = str(packet.get("upstream_item_id") or "")
        if upstream_id:
            by_upstream.setdefault(upstream_id, []).append(packet)
        title_key = compact_text(packet.get("title"), 120).lower()
        if title_key:
            by_title.setdefault(title_key, []).append(packet)
    return by_upstream, by_title


def match_evidence(material: dict[str, Any], by_upstream: dict[str, list[dict[str, Any]]], by_title: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    connector_item_id = str(material.get("connector_item_id") or "")
    if connector_item_id and connector_item_id in by_upstream:
        return by_upstream[connector_item_id]
    title_key = compact_text(material.get("title"), 120).lower()
    if title_key in by_title:
        return by_title[title_key]
    for key, packets in by_title.items():
        if title_key and (title_key in key or key in title_key):
            return packets
    return []


def strongest_evidence(packets: list[dict[str, Any]]) -> str:
    strengths = [str(item.get("evidence_strength") or "UNKNOWN") for item in packets]
    if "HIGH" in strengths:
        return "HIGH"
    if "MEDIUM" in strengths:
        return "MEDIUM"
    if "LOW" in strengths:
        return "LOW"
    return "LOW"


def promotion_status(gate_item: dict[str, Any], packets: list[dict[str, Any]]) -> tuple[str, list[str], str]:
    decision = str(gate_item.get("gate_decision") or "")
    strength = strongest_evidence(packets)
    weak_signal = any(bool(packet.get("weak_signal_lane")) for packet in packets)
    if decision == "PROMOTE_TO_TOPIC_PIPELINE" and packets and strength in {"HIGH", "MEDIUM"} and not weak_signal:
        return "PROMOTED", [], "Enter content brief path after human source check."
    if decision == "PROMOTE_TO_TOPIC_PIPELINE":
        missing = []
        if not packets:
            missing.append("No connector evidence packet matched this hot material.")
        if strength == "LOW":
            missing.append("Evidence strength is low.")
        if weak_signal:
            missing.append("Weak signal lane needs corroboration before promotion.")
        return "NEEDS_EVIDENCE", missing, "Backfill or attach stronger evidence before brief."
    if decision == "BACKFILL_REQUIRED":
        return "NEEDS_EVIDENCE", ["Hot material quality gate requires backfill."], "Run evidence backfill before topic scoring."
    if decision == "WATCH":
        return "WATCH", [], "Watch for a second source or stronger event signal."
    return "REJECTED", ["Rejected or too weak at hot material quality gate."], "Do not use unless new evidence appears."


def topic_from_material(gate_item: dict[str, Any], material: dict[str, Any], packets: list[dict[str, Any]]) -> dict[str, Any]:
    evidence = packets[0] if packets else None
    status, missing, next_action = promotion_status(gate_item, packets)
    topic_type = topic_type_for(material, evidence)
    evidence_ids = [str(item.get("evidence_id")) for item in packets if item.get("evidence_id")]
    strength = strongest_evidence(packets)
    freshness = str((evidence or {}).get("freshness") or material.get("freshness") or "unknown")
    source_origin = str((evidence or {}).get("source_origin") or "phase27_connector")
    weak_signal = bool((evidence or {}).get("weak_signal_lane", False))
    title = compact_text(material.get("title") or gate_item.get("title"), 180)
    core_angle = compact_text(
        (evidence or {}).get("claim_summary")
        or material.get("why_it_matters")
        or gate_item.get("decision_reason")
        or "Connector metadata suggests a possible content angle; verify before writing.",
        260,
    )
    return {
        "topic_candidate_id": stable_id("conntopic", material.get("material_id") or gate_item.get("material_id"), title),
        "source_material_id": gate_item.get("material_id") or material.get("material_id", ""),
        "evidence_ids": evidence_ids,
        "title": title,
        "topic_type": topic_type,
        "domain_tags": material.get("domain_tags") if isinstance(material.get("domain_tags"), list) else [],
        "why_now": compact_text(material.get("why_it_matters") or gate_item.get("decision_reason"), 220),
        "core_angle": core_angle,
        "evidence_strength": strength,
        "freshness": freshness,
        "recommended_content_type": recommended_content_type(topic_type),
        "promotion_status": status,
        "missing_evidence": missing,
        "next_action": next_action,
        "source_origin": source_origin,
        "weak_signal_lane": weak_signal,
    }


def build_connector_promoted_topic_candidates(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    inputs = {
        "hot_material_quality_gate": paths.logs_root / "latest_hot_material_quality_gate.json",
        "daily_hot_material_pool": paths.market_content_root / "03_topic_candidates" / "latest_daily_hot_material_pool.json",
        "connector_evidence_packets": paths.market_content_root / "03_topic_candidates" / "latest_connector_evidence_packets.json",
        "methodology_topic_scores": paths.market_content_root / "03_topic_candidates" / "latest_methodology_topic_scores.json",
    }
    warnings = warning_for_missing(inputs)
    gate = read_json(inputs["hot_material_quality_gate"])
    pool = read_json(inputs["daily_hot_material_pool"])
    evidence_payload = read_json(inputs["connector_evidence_packets"])
    topic_scores = read_json(inputs["methodology_topic_scores"])

    materials_by_id = {str(item.get("material_id")): item for item in list_payload(pool, "materials")}
    packets = list_payload(evidence_payload, "evidence_packets")
    by_upstream, by_title = evidence_index(packets)
    candidates: list[dict[str, Any]] = []
    for gate_item in list_payload(gate, "items"):
        material_id = str(gate_item.get("material_id") or "")
        material = materials_by_id.get(material_id, {"material_id": material_id, "title": gate_item.get("title"), "lane_id": gate_item.get("lane_id")})
        matched_packets = match_evidence(material, by_upstream, by_title)
        candidates.append(topic_from_material(gate_item, material, matched_packets))

    summary = {
        "candidate_count": len(candidates),
        "promoted": sum(1 for item in candidates if item.get("promotion_status") == "PROMOTED"),
        "needs_evidence": sum(1 for item in candidates if item.get("promotion_status") == "NEEDS_EVIDENCE"),
        "watch": sum(1 for item in candidates if item.get("promotion_status") == "WATCH"),
        "rejected": sum(1 for item in candidates if item.get("promotion_status") == "REJECTED"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "topic_candidates": candidates,
        "summary": summary,
        "input_status": {
            "gate_status": gate.get("gate_status", "UNKNOWN"),
            "material_count": safe_int((pool.get("summary") or {}).get("material_count")) if isinstance(pool.get("summary"), dict) else 0,
            "evidence_packet_count": len(packets),
            "methodology_topic_scores_available": bool(topic_scores),
        },
        "warnings": warnings,
        "policy": {
            "does_not_write_mainline_topic_scores": True,
            "metadata_derived_evidence_only": True,
            "weak_signal_lane_requires_corrobation": True,
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
            "status": item.get("promotion_status"),
            "strength": item.get("evidence_strength"),
            "origin": item.get("source_origin"),
            "title": compact_text(item.get("title"), 78),
            "next": compact_text(item.get("next_action"), 60),
        }
        for item in list_payload(payload, "topic_candidates")[:40]
    ]
    return f"""# Connector Promoted Topic Candidates

## Summary

- candidate_count: `{summary.get('candidate_count', 0)}`
- promoted: `{summary.get('promoted', 0)}`
- needs_evidence: `{summary.get('needs_evidence', 0)}`
- watch: `{summary.get('watch', 0)}`
- rejected: `{summary.get('rejected', 0)}`

## Candidates

{markdown_table(rows, ('status', 'strength', 'origin', 'title', 'next'))}

## Boundary

This is a sidecar promotion queue. It does not overwrite methodology topic scores, drafts, prompts, rules, or content queue artifacts.
"""
