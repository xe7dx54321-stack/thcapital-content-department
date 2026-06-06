"""Bridge connector-promoted topics into daily content operations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__acquisition-to-content-bridge.json",
        "dated_md": paths.logs_root / f"{run_date}__acquisition-to-content-bridge.md",
        "latest_json": paths.logs_root / "latest_acquisition_to_content_bridge.json",
        "latest_md": paths.logs_root / "latest_acquisition_to_content_bridge.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__acquisition-to-content-bridge-board.md",
        "board_latest_md": paths.frontstage_root / "latest_acquisition_to_content_bridge_board.md",
    }


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def bridge_status(candidate: dict[str, Any]) -> tuple[str, str, str]:
    status = str(candidate.get("promotion_status") or "")
    if status == "PROMOTED":
        return (
            "READY_FOR_BRIEF",
            "content_brief",
            "有新的上游选题可进入 brief 生产；先做人工 source check，再进入 brief/outline。",
        )
    if status == "NEEDS_EVIDENCE":
        return (
            "NEEDS_EVIDENCE",
            "evidence_backfill",
            "有上游选题需要补证据；先完成证据 backfill，再考虑 brief。",
        )
    if status == "WATCH":
        return ("WATCH", "watch", "继续观察，等待第二来源、更新版本或更强事件信号。")
    return ("REJECTED", "watch", "暂不进入内容生产，除非后续出现新证据。")


def build_bridge_item(candidate: dict[str, Any], evidence_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    status, step, action = bridge_status(candidate)
    evidence_ids = [str(item) for item in candidate.get("evidence_ids", []) if str(item) in evidence_by_id]
    title = compact_text(candidate.get("title"), 180)
    why = compact_text(candidate.get("core_angle") or candidate.get("why_now") or "", 260)
    return {
        "bridge_item_id": stable_id("bridge", candidate.get("topic_candidate_id"), title),
        "topic_candidate_id": candidate.get("topic_candidate_id", ""),
        "title": title,
        "bridge_status": status,
        "recommended_pipeline_step": step,
        "evidence_ids": evidence_ids,
        "why_it_matters": why,
        "operator_action": action,
        "source_origin": candidate.get("source_origin", "phase27_connector"),
        "weak_signal_lane": bool(candidate.get("weak_signal_lane", False)),
    }


def build_acquisition_to_content_bridge(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    topic_root = paths.market_content_root / "03_topic_candidates"
    inputs = {
        "connector_promoted_topic_candidates": topic_root / "latest_connector_promoted_topic_candidates.json",
        "connector_evidence_packets": topic_root / "latest_connector_evidence_packets.json",
        "content_queue_priority": paths.market_content_root / "07_publishing" / "latest_content_queue_priority.json",
        "stable_daily_ops": paths.logs_root / "latest_stable_daily_ops.json",
        "methodology_topic_scores": topic_root / "latest_methodology_topic_scores.json",
    }
    warnings = warning_for_missing(inputs)
    promoted = read_json(inputs["connector_promoted_topic_candidates"])
    evidence = read_json(inputs["connector_evidence_packets"])
    queue = read_json(inputs["content_queue_priority"])
    stable = read_json(inputs["stable_daily_ops"])
    topic_scores = read_json(inputs["methodology_topic_scores"])

    evidence_by_id = {str(item.get("evidence_id")): item for item in list_payload(evidence, "evidence_packets")}
    bridge_items = [build_bridge_item(candidate, evidence_by_id) for candidate in list_payload(promoted, "topic_candidates")]
    summary = {
        "bridge_item_count": len(bridge_items),
        "ready_for_brief": sum(1 for item in bridge_items if item.get("bridge_status") == "READY_FOR_BRIEF"),
        "needs_evidence": sum(1 for item in bridge_items if item.get("bridge_status") == "NEEDS_EVIDENCE"),
        "watch": sum(1 for item in bridge_items if item.get("bridge_status") == "WATCH"),
        "rejected": sum(1 for item in bridge_items if item.get("bridge_status") == "REJECTED"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "bridge_items": bridge_items,
        "summary": summary,
        "operator_actions": [
            "有新的上游选题可进入 brief 生产。" if summary["ready_for_brief"] else "暂无 READY_FOR_BRIEF 的上游选题。",
            "有上游选题需要补证据。" if summary["needs_evidence"] else "暂无需要补证据的上游 promoted topic。",
        ],
        "input_status": {
            "content_queue_items": safe_int((queue.get("summary") or {}).get("item_count")) if isinstance(queue.get("summary"), dict) else 0,
            "stable_daily_ops_status": stable.get("status", "UNKNOWN"),
            "methodology_topic_scores_available": bool(topic_scores),
        },
        "warnings": warnings,
        "policy": {
            "sidecar_only": True,
            "does_not_create_briefs": True,
            "does_not_overwrite_content_queue": True,
            "metadata_derived_evidence_only": True,
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
            "status": item.get("bridge_status"),
            "step": item.get("recommended_pipeline_step"),
            "origin": item.get("source_origin"),
            "title": compact_text(item.get("title"), 78),
            "action": compact_text(item.get("operator_action"), 70),
        }
        for item in list_payload(payload, "bridge_items")[:40]
    ]
    return f"""# Acquisition-to-Content Bridge

## Summary

- bridge_item_count: `{summary.get('bridge_item_count', 0)}`
- ready_for_brief: `{summary.get('ready_for_brief', 0)}`
- needs_evidence: `{summary.get('needs_evidence', 0)}`
- watch: `{summary.get('watch', 0)}`
- rejected: `{summary.get('rejected', 0)}`

## Bridge Items

{markdown_table(rows, ('status', 'step', 'origin', 'title', 'action'))}

## Boundary

The bridge tells the operator what can move toward brief/evidence backfill. It does not create briefs, drafts, publish sessions, or overwrite the main content queue.
"""
