"""Capture multi-lane hot signals from existing local upstream artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import LANES, compact_text, detect_event_type, detect_lane, freshness_from_run_date, markdown_table, stable_id, source_items_from_manifest


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__hot-signal-capture.json",
        "dated_md": paths.logs_root / f"{run_date}__hot-signal-capture.md",
        "latest_json": paths.logs_root / "latest_hot_signal_capture.json",
        "latest_md": paths.logs_root / "latest_hot_signal_capture.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__hot-signal-capture-board.md",
        "board_latest_md": paths.frontstage_root / "latest_hot_signal_capture_board.md",
    }


def signal_from_manifest_source(item: dict[str, Any], run_date: str) -> dict[str, Any] | None:
    items_found = safe_int(item.get("items_found") or item.get("items_written"))
    if items_found <= 0 and str(item.get("status", "")).upper() not in {"SUCCESS", "OK"}:
        return None
    source_id = str(item.get("source_id") or item.get("label") or "official_source")
    title = str(item.get("notes") or item.get("label") or source_id)
    lane_id = detect_lane(title, source_id)
    score = min(100, 45 + items_found * 3)
    return {
        "signal_id": stable_id("hsig", "manifest", source_id, title),
        "lane_id": lane_id,
        "title": compact_text(title, 140),
        "source": source_id,
        "source_tier": "A" if "openai" in source_id.lower() or "nvidia" in source_id.lower() else "UNKNOWN",
        "event_type": detect_event_type(title),
        "domain_tags": [lane_id],
        "hotness_score": score,
        "freshness": "today",
        "why_it_matters": f"Official lane observed {items_found} item(s) from {source_id}.",
        "evidence_refs": item.get("artifact_paths") if isinstance(item.get("artifact_paths"), list) else [],
        "candidate_for_topic_pool": score >= 55,
    }


def signal_from_candidate(item: dict[str, Any], current_date: str) -> dict[str, Any]:
    title = str(item.get("theme") or item.get("title") or item.get("cluster_id") or "Untitled signal")
    source_ids = item.get("source_ids") if isinstance(item.get("source_ids"), list) else []
    lane_id = detect_lane(title, " ".join(str(source) for source in source_ids))
    evidence = item.get("key_evidence") if isinstance(item.get("key_evidence"), list) else []
    score = int(min(100, safe_float(item.get("total_score") or item.get("score"))))
    return {
        "signal_id": stable_id("hsig", "candidate", item.get("cluster_id") or title),
        "lane_id": lane_id,
        "title": compact_text(title, 160),
        "source": ", ".join(str(source) for source in source_ids[:3]) or "topic_candidate",
        "source_tier": str((evidence[0] or {}).get("source_tier") or "UNKNOWN") if evidence else "UNKNOWN",
        "event_type": detect_event_type(title),
        "domain_tags": [lane_id, str(item.get("score_band") or "").lower()],
        "hotness_score": score,
        "freshness": freshness_from_run_date(item.get("run_date"), current_date),
        "why_it_matters": compact_text(item.get("why_it_matters") or item.get("recommended_action") or "", 220),
        "evidence_refs": [ev.get("evidence_id") or ev.get("url") for ev in evidence[:5] if isinstance(ev, dict)],
        "candidate_for_topic_pool": item.get("recommended_action") in {"candidate_for_deep_article", "write"} or score >= 70,
    }


def build_hot_signal_capture(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    manifest = read_json(paths.logs_root / "latest_official_runtime_manifest.json")
    source_summary = read_json(paths.logs_root / "latest_daily_source_run_summary.json")
    runtime = read_json(paths.logs_root / "latest_source_runtime_health.json")
    expansion = read_json(paths.logs_root / "latest_high_value_source_expansion_plan.json")
    high_value = read_json(paths.market_content_root / "03_topic_candidates" / "latest_high_value_candidates.json")

    signals: list[dict[str, Any]] = []
    for item in source_items_from_manifest(manifest):
        signal = signal_from_manifest_source(item, run_date)
        if signal:
            signals.append(signal)
    for item in list_payload(high_value, "candidates"):
        signals.append(signal_from_candidate(item, run_date))

    by_lane: dict[str, list[dict[str, Any]]] = {lane["lane_id"]: [] for lane in LANES}
    for signal in signals:
        by_lane.setdefault(str(signal.get("lane_id")), []).append(signal)
    source_candidates = list_payload(expansion, "source_candidates")
    runtime_records = list_payload(runtime, "records")
    lanes: list[dict[str, Any]] = []
    for lane in LANES:
        lane_id = lane["lane_id"]
        lane_signals = sorted(by_lane.get(lane_id, []), key=lambda item: safe_int(item.get("hotness_score")), reverse=True)
        missing_sources = [
            item.get("source_name")
            for item in source_candidates
            if detect_lane(item.get("category", ""), item.get("source_name", "")) == lane_id and "already_configured" not in " ".join(item.get("risk", []))
        ][:5]
        runtime_missing = [
            item.get("source_id")
            for item in runtime_records
            if detect_lane(item.get("category", ""), item.get("source_id", "")) == lane_id and "MISSING" in str(item.get("runtime_status", "")).upper()
        ][:5]
        signal_count = len(lane_signals)
        hotness = max([safe_int(item.get("hotness_score")) for item in lane_signals] or [0])
        if signal_count >= 2:
            status = "ACTIVE"
        elif signal_count == 1:
            status = "WEAK"
        elif missing_sources or runtime_missing:
            status = "MISSING_INPUT"
        else:
            status = "EMPTY"
        lanes.append(
            {
                "lane_id": lane_id,
                "label": lane["label"],
                "status": status,
                "signal_count": signal_count,
                "hotness_score": hotness,
                "top_signals": lane_signals[:5],
                "missing_sources": [item for item in [*missing_sources, *runtime_missing] if item],
                "recommended_backfill": [
                    f"Backfill {lane['label']} with official/rss/github/arxiv/manual query source."
                ]
                if status in {"EMPTY", "MISSING_INPUT", "WEAK"}
                else [],
            }
        )
    summary = {
        "lane_count": len(lanes),
        "active_lanes": sum(1 for item in lanes if item.get("status") == "ACTIVE"),
        "hot_signal_count": len(signals),
        "candidate_for_topic_pool": sum(1 for item in signals if item.get("candidate_for_topic_pool")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "lanes": lanes,
        "hot_signals": sorted(signals, key=lambda item: safe_int(item.get("hotness_score")), reverse=True),
        "summary": summary,
        "input_status": {
            "official_manifest_status": manifest.get("status", "UNKNOWN"),
            "daily_source_summary_status": source_summary.get("status", "UNKNOWN"),
            "source_runtime_health_available": bool(runtime),
            "expansion_plan_available": bool(expansion),
        },
        "policy": {
            "local_artifact_only": True,
            "no_external_fetch": True,
            "no_fabricated_hot_signals": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    lane_rows = [
        {
            "lane": item.get("lane_id"),
            "status": item.get("status"),
            "signals": item.get("signal_count"),
            "hotness": item.get("hotness_score"),
        }
        for item in list_payload(payload, "lanes")
    ]
    signal_rows = [
        {
            "lane": item.get("lane_id"),
            "score": item.get("hotness_score"),
            "freshness": item.get("freshness"),
            "title": compact_text(item.get("title"), 80),
        }
        for item in list_payload(payload, "hot_signals")[:15]
    ]
    return f"""# Multi-lane Hot Signal Capture

## Summary

- lane_count: `{summary.get('lane_count', 0)}`
- active_lanes: `{summary.get('active_lanes', 0)}`
- hot_signal_count: `{summary.get('hot_signal_count', 0)}`
- candidate_for_topic_pool: `{summary.get('candidate_for_topic_pool', 0)}`

## Lanes

{markdown_table(lane_rows, ('lane', 'status', 'signals', 'hotness'))}

## Top Signals

{markdown_table(signal_rows, ('lane', 'score', 'freshness', 'title'))}

## Boundary

Signals are derived from existing local artifacts only. Missing lanes are marked empty or missing input rather than filled with invented external news.
"""
