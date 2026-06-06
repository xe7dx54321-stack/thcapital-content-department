"""Run a quality gate over the daily hot material pool."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, quality_score, stable_id


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__hot-material-quality-gate.json",
        "dated_md": paths.logs_root / f"{run_date}__hot-material-quality-gate.md",
        "latest_json": paths.logs_root / "latest_hot_material_quality_gate.json",
        "latest_md": paths.logs_root / "latest_hot_material_quality_gate.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__hot-material-quality-gate-board.md",
        "board_latest_md": paths.frontstage_root / "latest_hot_material_quality_gate_board.md",
    }


def gate_item(material: dict[str, Any]) -> dict[str, Any]:
    material_id = str(material.get("material_id") or stable_id("hotmat", material.get("title")))
    use = str(material.get("recommended_use") or "")
    evidence = str(material.get("evidence_strength") or "UNKNOWN")
    freshness = str(material.get("freshness") or "unknown")
    score = quality_score(material.get("hotness_score"), material.get("content_potential_score"), evidence, freshness)
    risk_flags: list[str] = []
    if evidence in {"LOW", "UNKNOWN"}:
        risk_flags.append("weak_evidence")
    if freshness in {"stale", "unknown"}:
        risk_flags.append("freshness_uncertain")
    if material.get("source_type") == "backfill_task":
        risk_flags.append("backfill_not_completed")
    weak_signal = bool(material.get("weak_signal")) or (
        material.get("source_origin") == "openclaw_migration" and not material.get("can_use_as_hard_evidence")
    )
    if weak_signal:
        risk_flags.append("weak_signal_not_hard_evidence")
    if weak_signal and material.get("evidence_role") in {"manual_only"}:
        decision = "BACKFILL_REQUIRED"
        reason = "OpenClaw migrated manual/weak signal needs confirmation before content use."
        next_action = "Complete manual evidence backfill; do not use as hard evidence."
    elif weak_signal:
        decision = "WATCH"
        reason = "OpenClaw migrated weak signal can indicate attention, but cannot be used as hard evidence."
        next_action = "Confirm with official or authoritative source before topic promotion."
    elif use == "write_now" and score >= 75 and evidence in {"HIGH", "MEDIUM"} and freshness in {"today", "this_week"}:
        decision = "PROMOTE_TO_TOPIC_PIPELINE"
        reason = "Fresh, relevant, and has enough evidence for topic pipeline promotion."
        next_action = "Promote to topic pipeline only after human source check."
    elif use in {"backfill_first"} or evidence in {"LOW", "UNKNOWN"}:
        decision = "BACKFILL_REQUIRED"
        reason = "Signal is potentially useful but needs stronger evidence before writing."
        next_action = "Complete manual backfill and attach source/evidence refs."
    elif use == "develop_topic" or score >= 55:
        decision = "WATCH"
        reason = "Worth developing or watching, but not yet enough for write-now treatment."
        next_action = "Develop evidence packet or wait for stronger signal."
    else:
        decision = "REJECT"
        reason = "Too weak, stale, or generic for the current topic pipeline."
        next_action = "Ignore unless new evidence appears."
    return {
        "material_id": material_id,
        "gate_decision": decision,
        "decision_reason": reason,
        "quality_score": score,
        "risk_flags": risk_flags,
        "required_next_action": next_action,
        "title": material.get("title", ""),
        "lane_id": material.get("lane_id", ""),
        "weak_signal": weak_signal,
        "source_origin": material.get("source_origin", ""),
    }


def build_hot_material_quality_gate(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    pool = read_json(paths.market_content_root / "03_topic_candidates" / "latest_daily_hot_material_pool.json")
    topic_methodology = read_json(repo_root / "config" / "topic_selection_methodology.json")
    article_methodology = read_json(repo_root / "config" / "article_quality_methodology.json")
    audit = read_json(paths.logs_root / "latest_source_coverage_gap_audit.json")

    items = [gate_item(material) for material in list_payload(pool, "materials")]
    weak_supply_reasons: list[str] = []
    if not items:
        weak_supply_reasons.append("No hot materials were available from local artifacts.")
    if len(items) < 3:
        weak_supply_reasons.append("Daily hot material count is below 3.")
    promote = sum(1 for item in items if item.get("gate_decision") == "PROMOTE_TO_TOPIC_PIPELINE")
    backfill = sum(1 for item in items if item.get("gate_decision") == "BACKFILL_REQUIRED")
    high_gaps = safe_int((audit.get("summary") or {}).get("high_severity")) if isinstance(audit.get("summary"), dict) else 0
    if promote == 0:
        weak_supply_reasons.append("No material passed promote-to-topic-pipeline gate.")
    if high_gaps:
        weak_supply_reasons.append(f"{high_gaps} high-severity source coverage gap(s) remain.")
    if not items and not backfill:
        gate_status = "BLOCKED"
    elif weak_supply_reasons and promote == 0:
        gate_status = "WEAK_SUPPLY"
    elif backfill:
        gate_status = "ACTIONABLE"
    else:
        gate_status = "PASS"
    summary = {
        "material_count": len(items),
        "promote_to_topic_pipeline": promote,
        "watch": sum(1 for item in items if item.get("gate_decision") == "WATCH"),
        "backfill_required": backfill,
        "reject": sum(1 for item in items if item.get("gate_decision") == "REJECT"),
        "weak_signal_item_count": sum(1 for item in items if item.get("weak_signal")),
        "weak_signal_watch": sum(1 for item in items if item.get("weak_signal") and item.get("gate_decision") == "WATCH"),
        "weak_signal_backfill_required": sum(
            1 for item in items if item.get("weak_signal") and item.get("gate_decision") == "BACKFILL_REQUIRED"
        ),
        "weak_supply_reasons": weak_supply_reasons,
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "gate_status": gate_status,
        "items": items,
        "summary": summary,
        "methodology_context": {
            "topic_methodology_available": bool(topic_methodology),
            "article_methodology_available": bool(article_methodology),
        },
        "policy": {
            "quality_gate_only": True,
            "does_not_promote_mainline": True,
            "does_not_fetch_external_sources": True,
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
            "decision": item.get("gate_decision"),
            "score": item.get("quality_score"),
            "lane": item.get("lane_id"),
            "title": compact_text(item.get("title"), 80),
            "next": compact_text(item.get("required_next_action"), 80),
        }
        for item in list_payload(payload, "items")[:30]
    ]
    weak = "\n".join(f"- {item}" for item in summary.get("weak_supply_reasons", [])) or "- None."
    return f"""# Hot Material Quality Gate

## Summary

- gate_status: `{payload.get('gate_status')}`
- material_count: `{summary.get('material_count', 0)}`
- promote_to_topic_pipeline: `{summary.get('promote_to_topic_pipeline', 0)}`
- watch: `{summary.get('watch', 0)}`
- backfill_required: `{summary.get('backfill_required', 0)}`
- reject: `{summary.get('reject', 0)}`
- weak_signal_item_count: `{summary.get('weak_signal_item_count', 0)}`
- weak_signal_watch: `{summary.get('weak_signal_watch', 0)}`
- weak_signal_backfill_required: `{summary.get('weak_signal_backfill_required', 0)}`

## Weak Supply Reasons

{weak}

## Gate Items

{markdown_table(rows, ('decision', 'score', 'lane', 'title', 'next'))}

## Boundary

The gate only recommends promotion/watch/backfill/reject. It does not write mainline topic candidates or fetch external sources.
"""
