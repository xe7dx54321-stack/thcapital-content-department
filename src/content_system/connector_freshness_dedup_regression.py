"""Run freshness, dedupe, and traceability regression for connector artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__connector-freshness-dedup-regression.json",
        "dated_md": paths.logs_root / f"{run_date}__connector-freshness-dedup-regression.md",
        "latest_json": paths.logs_root / "latest_connector_freshness_dedup_regression.json",
        "latest_md": paths.logs_root / "latest_connector_freshness_dedup_regression.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__connector-freshness-dedup-regression-board.md",
        "board_latest_md": paths.frontstage_root / "latest_connector_freshness_dedup_regression_board.md",
    }


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def check(check_id: str, status: str, message: str) -> dict[str, str]:
    return {"check_id": check_id, "status": status, "message": message}


def ratio_status(value: float, warn_threshold: float, fail_threshold: float) -> str:
    if value >= fail_threshold:
        return "FAIL"
    if value >= warn_threshold:
        return "WARN"
    return "PASS"


def build_connector_freshness_dedup_regression(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    topic_root = paths.market_content_root / "03_topic_candidates"
    inputs = {
        "normalized_upstream_items": paths.logs_root / "latest_normalized_upstream_items.json",
        "connector_evidence_packets": topic_root / "latest_connector_evidence_packets.json",
        "connector_promoted_topic_candidates": topic_root / "latest_connector_promoted_topic_candidates.json",
        "daily_hot_material_pool": topic_root / "latest_daily_hot_material_pool.json",
        "hot_material_quality_gate": paths.logs_root / "latest_hot_material_quality_gate.json",
    }
    warnings = warning_for_missing(inputs)
    normalized = read_json(inputs["normalized_upstream_items"])
    evidence = read_json(inputs["connector_evidence_packets"])
    promoted = read_json(inputs["connector_promoted_topic_candidates"])
    pool = read_json(inputs["daily_hot_material_pool"])
    gate = read_json(inputs["hot_material_quality_gate"])

    normalized_items = list_payload(normalized, "items")
    evidence_packets = list_payload(evidence, "evidence_packets")
    topic_candidates = list_payload(promoted, "topic_candidates")
    normalized_summary = normalized.get("summary") if isinstance(normalized.get("summary"), dict) else {}

    duplicate_count = safe_int(normalized_summary.get("deduped_count"))
    deduped_count = len(normalized_items)
    input_count = deduped_count + duplicate_count
    duplicate_ratio = round(duplicate_count / input_count, 4) if input_count else 0.0
    freshness_summary = {
        "today": sum(1 for item in evidence_packets if item.get("freshness") == "today"),
        "this_week": sum(1 for item in evidence_packets if item.get("freshness") == "this_week"),
        "stale": sum(1 for item in evidence_packets if item.get("freshness") == "stale"),
        "unknown": sum(1 for item in evidence_packets if item.get("freshness") == "unknown"),
    }
    evidence_count = len(evidence_packets)
    stale_ratio = freshness_summary["stale"] / evidence_count if evidence_count else 0.0
    unknown_ratio = freshness_summary["unknown"] / evidence_count if evidence_count else 0.0

    checks: list[dict[str, str]] = []
    metadata_bad = [item for item in evidence_packets if item.get("metadata_only") is not True]
    checks.append(check("metadata_only", "FAIL" if metadata_bad else "PASS", f"{len(metadata_bad)} evidence packet(s) are not metadata-only."))
    copyright_bad = [item for item in evidence_packets if item.get("copyright_safe") is not True]
    checks.append(check("copyright_safe", "FAIL" if copyright_bad else "PASS", f"{len(copyright_bad)} evidence packet(s) are not copyright-safe."))
    dedupe_status = ratio_status(duplicate_ratio, 0.20, 0.40)
    checks.append(check("dedupe_ratio", dedupe_status, f"duplicate_ratio={duplicate_ratio:.2%}; input={input_count}, deduped={deduped_count}."))
    stale_status = ratio_status(stale_ratio, 0.35, 0.60)
    checks.append(check("stale_ratio", stale_status, f"stale_ratio={stale_ratio:.2%}; stale={freshness_summary['stale']}."))
    unknown_status = ratio_status(unknown_ratio, 0.50, 0.75)
    checks.append(check("unknown_freshness_ratio", unknown_status, f"unknown_ratio={unknown_ratio:.2%}; unknown={freshness_summary['unknown']}."))

    evidence_by_id = {str(item.get("evidence_id")): item for item in evidence_packets}
    promoted_without_evidence = [
        item
        for item in topic_candidates
        if item.get("promotion_status") == "PROMOTED" and not [eid for eid in item.get("evidence_ids", []) if eid in evidence_by_id]
    ]
    checks.append(
        check(
            "promotion_traceability",
            "FAIL" if promoted_without_evidence else "PASS",
            f"{len(promoted_without_evidence)} promoted topic candidate(s) lack traceable evidence.",
        )
    )
    topic_without_url = []
    for candidate in topic_candidates:
        ids = candidate.get("evidence_ids") if isinstance(candidate.get("evidence_ids"), list) else []
        if candidate.get("promotion_status") == "PROMOTED" and not any(evidence_by_id.get(str(eid), {}).get("url") for eid in ids):
            topic_without_url.append(candidate)
    checks.append(check("topic_candidates_have_url", "FAIL" if topic_without_url else "PASS", f"{len(topic_without_url)} promoted topic candidate(s) lack evidence URL."))
    weak_hard = [
        item
        for item in topic_candidates
        if item.get("weak_signal_lane") and item.get("promotion_status") == "PROMOTED"
    ]
    weak_high_evidence = [
        item
        for item in evidence_packets
        if item.get("weak_signal_lane") and item.get("evidence_strength") == "HIGH"
    ]
    checks.append(
        check(
            "weak_signal_lane_not_hard_evidence",
            "FAIL" if weak_hard or weak_high_evidence else "PASS",
            f"{len(weak_hard)} weak-signal promoted topic(s), {len(weak_high_evidence)} weak-signal high evidence packet(s).",
        )
    )

    if any(item.get("status") == "FAIL" for item in checks):
        regression_status = "FAIL"
    elif any(item.get("status") == "WARN" for item in checks):
        regression_status = "WARN"
    else:
        regression_status = "PASS"

    recommendations: list[str] = []
    if duplicate_ratio >= 0.20:
        recommendations.append("Review connector dedupe keys and title normalization before increasing connector volume.")
    if unknown_ratio >= 0.50:
        recommendations.append("Prefer connector endpoints with published_at metadata or add safe date parsing.")
    if promoted_without_evidence:
        recommendations.append("Do not send promoted topics to brief generation until evidence IDs are traceable.")
    if not recommendations:
        recommendations.append("Connector metadata hygiene is acceptable for Phase 28 sidecar promotion.")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "checks": checks,
        "freshness_summary": freshness_summary,
        "dedup_summary": {
            "input_count": input_count,
            "duplicate_count": duplicate_count,
            "deduped_count": deduped_count,
            "duplicate_ratio": duplicate_ratio,
        },
        "regression_status": regression_status,
        "recommendations": recommendations,
        "input_status": {
            "hot_material_count": safe_int((pool.get("summary") or {}).get("material_count")) if isinstance(pool.get("summary"), dict) else 0,
            "quality_gate_status": gate.get("gate_status", "UNKNOWN"),
            "topic_candidate_count": len(topic_candidates),
        },
        "warnings": warnings,
        "policy": {
            "metadata_only": True,
            "copyright_safe": True,
            "no_full_text": True,
            "no_openclaw_migration": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    freshness = payload.get("freshness_summary") if isinstance(payload.get("freshness_summary"), dict) else {}
    dedup = payload.get("dedup_summary") if isinstance(payload.get("dedup_summary"), dict) else {}
    rows = [
        {"check": item.get("check_id"), "status": item.get("status"), "message": compact_text(item.get("message"), 90)}
        for item in list_payload(payload, "checks")
    ]
    recs = "\n".join(f"- {item}" for item in payload.get("recommendations", [])) or "- None."
    return f"""# Connector Freshness and Dedup Regression

## Summary

- regression_status: `{payload.get('regression_status')}`
- today: `{freshness.get('today', 0)}`
- this_week: `{freshness.get('this_week', 0)}`
- stale: `{freshness.get('stale', 0)}`
- unknown: `{freshness.get('unknown', 0)}`
- duplicate_ratio: `{dedup.get('duplicate_ratio', 0.0)}`

## Checks

{markdown_table(rows, ('check', 'status', 'message'))}

## Recommendations

{recs}

## Boundary

Regression checks metadata hygiene only. They do not fetch full text, rewrite source configs, or migrate OpenClaw sources.
"""
