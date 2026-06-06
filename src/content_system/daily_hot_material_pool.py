"""Build the daily hot material pool from upstream signals and backfill tasks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, detect_event_type, detect_lane, freshness_from_run_date, markdown_table, stable_id


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    topic_root = paths.market_content_root / "03_topic_candidates"
    return {
        "dated_json": topic_root / f"{run_date}__daily-hot-material-pool.json",
        "dated_md": topic_root / f"{run_date}__daily-hot-material-pool.md",
        "latest_json": topic_root / "latest_daily_hot_material_pool.json",
        "latest_md": topic_root / "latest_daily_hot_material_pool.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__daily-hot-material-pool-board.md",
        "board_latest_md": paths.frontstage_root / "latest_daily_hot_material_pool_board.md",
    }


def evidence_strength_from_refs(refs: Any, source_tier: Any = "") -> str:
    count = len(refs) if isinstance(refs, list) else 0
    if str(source_tier).upper() == "A" and count >= 1:
        return "HIGH"
    if count >= 3:
        return "HIGH"
    if count >= 1:
        return "MEDIUM"
    return "LOW"


def recommended_use(hotness: int, potential: int, evidence_strength: str, freshness: str, source_type: str) -> str:
    if source_type == "backfill_task":
        return "backfill_first"
    if evidence_strength in {"HIGH", "MEDIUM"} and freshness in {"today", "this_week"} and hotness >= 75 and potential >= 70:
        return "write_now"
    if hotness >= 60 or potential >= 65:
        return "develop_topic"
    if freshness == "stale":
        return "hold"
    return "watch"


def material_from_signal(signal: dict[str, Any]) -> dict[str, Any]:
    hotness = safe_int(signal.get("hotness_score"))
    evidence_refs = signal.get("evidence_refs") if isinstance(signal.get("evidence_refs"), list) else []
    evidence_strength = evidence_strength_from_refs(evidence_refs, signal.get("source_tier"))
    potential = min(100, hotness + (10 if signal.get("candidate_for_topic_pool") else 0))
    freshness = str(signal.get("freshness") or "unknown")
    use = recommended_use(hotness, potential, evidence_strength, freshness, "hot_signal")
    origin_source_type = str(signal.get("source_type") or "")
    return {
        "material_id": stable_id("hotmat", "signal", signal.get("signal_id")),
        "title": signal.get("title", ""),
        "source_type": "hot_signal",
        "origin_source_type": origin_source_type,
        "connector_item_id": signal.get("connector_item_id", ""),
        "lane_id": signal.get("lane_id", ""),
        "event_type": signal.get("event_type", "unknown"),
        "domain_tags": signal.get("domain_tags") if isinstance(signal.get("domain_tags"), list) else [],
        "hotness_score": hotness,
        "content_potential_score": potential,
        "evidence_strength": evidence_strength,
        "freshness": freshness,
        "recommended_use": use,
        "why_it_matters": signal.get("why_it_matters", ""),
        "missing_evidence": [] if evidence_strength in {"HIGH", "MEDIUM"} else ["Need confirming evidence before topic promotion."],
        "next_action": {
            "write_now": "Draft topic angle and verify source evidence.",
            "develop_topic": "Expand evidence packet and choose article angle.",
            "watch": "Monitor lane for second source or stronger signal.",
            "backfill_first": "Run manual backfill task before topic scoring.",
            "hold": "Hold unless new evidence appears.",
        }.get(use, "Review manually."),
    }


def material_from_candidate(item: dict[str, Any], run_date: str) -> dict[str, Any]:
    title = str(item.get("theme") or item.get("title") or item.get("cluster_id") or "Untitled topic")
    score = int(min(100, safe_float(item.get("total_score") or item.get("score"))))
    evidence_count = safe_int(item.get("evidence_count"))
    source_count = safe_int(item.get("source_count"))
    evidence_strength = "HIGH" if evidence_count >= 3 and source_count >= 2 else "MEDIUM" if evidence_count else "LOW"
    freshness = freshness_from_run_date(item.get("run_date"), run_date)
    lane_id = detect_lane(title, " ".join(str(source) for source in (item.get("source_ids") or [])))
    use = recommended_use(score, score, evidence_strength, freshness, "topic_candidate")
    return {
        "material_id": stable_id("hotmat", "candidate", item.get("cluster_id") or title),
        "title": compact_text(title, 180),
        "source_type": "topic_candidate",
        "lane_id": lane_id,
        "event_type": detect_event_type(title),
        "domain_tags": [lane_id, str(item.get("score_band") or "").lower()],
        "hotness_score": score,
        "content_potential_score": score,
        "evidence_strength": evidence_strength,
        "freshness": freshness,
        "recommended_use": use,
        "why_it_matters": compact_text(item.get("why_it_matters") or item.get("recommended_action") or "", 240),
        "missing_evidence": item.get("risks_missing_info") if isinstance(item.get("risks_missing_info"), list) else [],
        "next_action": "Use methodology topic score to decide brief/draft path." if use != "hold" else "Hold until fresher evidence appears.",
    }


def material_from_backfill(task: dict[str, Any]) -> dict[str, Any]:
    lane_id = str(task.get("lane_id") or "")
    priority = str(task.get("priority") or "MEDIUM")
    hotness = 55 if priority == "HIGH" else 40
    return {
        "material_id": stable_id("hotmat", "backfill", task.get("task_id")),
        "title": compact_text(task.get("suggested_query") or task.get("reason") or lane_id, 180),
        "source_type": "backfill_task",
        "lane_id": lane_id,
        "event_type": "unknown",
        "domain_tags": [lane_id, "backfill"],
        "hotness_score": hotness,
        "content_potential_score": 50 if priority == "HIGH" else 35,
        "evidence_strength": "UNKNOWN",
        "freshness": "unknown",
        "recommended_use": "backfill_first",
        "why_it_matters": compact_text(task.get("reason"), 220),
        "missing_evidence": ["Backfill task must be completed before topic promotion."],
        "next_action": f"Manual backfill via {task.get('suggested_method')}: {task.get('suggested_query')}",
    }


def build_daily_hot_material_pool(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    hot = read_json(paths.logs_root / "latest_hot_signal_capture.json")
    high_value = read_json(paths.market_content_root / "03_topic_candidates" / "latest_high_value_candidates.json")
    topic_scores = read_json(paths.market_content_root / "03_topic_candidates" / "latest_methodology_topic_scores.json")
    backfill = read_json(paths.logs_root / "latest_fallback_backfill_queue.json")
    runtime = read_json(paths.logs_root / "latest_source_runtime_health.json")

    by_id: dict[str, dict[str, Any]] = {}
    for signal in list_payload(hot, "hot_signals"):
        material = material_from_signal(signal)
        by_id[material["material_id"]] = material
    for candidate in list_payload(high_value, "candidates"):
        material = material_from_candidate(candidate, run_date)
        by_id.setdefault(material["material_id"], material)
    for task in list_payload(backfill, "backfill_tasks"):
        material = material_from_backfill(task)
        by_id[material["material_id"]] = material

    topic_summary = topic_scores.get("summary") if isinstance(topic_scores.get("summary"), dict) else {}
    runtime_missing = safe_int(runtime.get("missing_expected_count"))
    materials = sorted(
        by_id.values(),
        key=lambda item: (
            {"write_now": 0, "develop_topic": 1, "backfill_first": 2, "watch": 3, "hold": 4}.get(str(item.get("recommended_use")), 5),
            -safe_int(item.get("hotness_score")),
        ),
    )
    if len(materials) < 3:
        materials.append(
            {
                "material_id": stable_id("hotmat", "manual_seed", run_date),
                "title": "Manual upstream seed needed",
                "source_type": "manual_seed",
                "lane_id": "official_ai_lab",
                "event_type": "unknown",
                "domain_tags": ["manual_seed"],
                "hotness_score": 0,
                "content_potential_score": 0,
                "evidence_strength": "UNKNOWN",
                "freshness": "unknown",
                "recommended_use": "backfill_first",
                "why_it_matters": "Daily material pool is thin; operator should seed one or more verified URLs before writing.",
                "missing_evidence": ["No sufficient local hot material."],
                "next_action": "Use fallback backfill queue to collect verified upstream source URLs.",
            }
        )
    summary = {
        "material_count": len(materials),
        "write_now": sum(1 for item in materials if item.get("recommended_use") == "write_now"),
        "develop_topic": sum(1 for item in materials if item.get("recommended_use") == "develop_topic"),
        "watch": sum(1 for item in materials if item.get("recommended_use") == "watch"),
        "backfill_first": sum(1 for item in materials if item.get("recommended_use") == "backfill_first"),
        "hold": sum(1 for item in materials if item.get("recommended_use") == "hold"),
        "connector_item_count": sum(1 for item in materials if item.get("origin_source_type") in {"rss_official_blog", "github", "huggingface", "arxiv", "manual_url"}),
        "connector_promote_candidates": sum(
            1
            for item in materials
            if item.get("origin_source_type") in {"rss_official_blog", "github", "huggingface", "arxiv", "manual_url"}
            and item.get("recommended_use") in {"write_now", "develop_topic"}
        ),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "materials": materials,
        "summary": summary,
        "supply_findings": [
            f"methodology_topic_write={topic_summary.get('write', 0)}",
            f"methodology_topic_watch={topic_summary.get('watch', 0)}",
            f"source_runtime_missing_expected={runtime_missing}",
        ],
        "policy": {
            "upstream_supply_only": True,
            "does_not_publish": True,
            "does_not_create_mainline_topics": True,
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
            "use": item.get("recommended_use"),
            "lane": item.get("lane_id"),
            "hotness": item.get("hotness_score"),
            "evidence": item.get("evidence_strength"),
            "title": compact_text(item.get("title"), 80),
        }
        for item in list_payload(payload, "materials")[:30]
    ]
    return f"""# Daily Hot Material Pool

## Summary

- material_count: `{summary.get('material_count', 0)}`
- write_now: `{summary.get('write_now', 0)}`
- develop_topic: `{summary.get('develop_topic', 0)}`
- watch: `{summary.get('watch', 0)}`
- backfill_first: `{summary.get('backfill_first', 0)}`
- hold: `{summary.get('hold', 0)}`
- connector_item_count: `{summary.get('connector_item_count', 0)}`
- connector_promote_candidates: `{summary.get('connector_promote_candidates', 0)}`

## Materials

{markdown_table(rows, ('use', 'lane', 'hotness', 'evidence', 'title'))}

## Boundary

The material pool is upstream supply only. It does not create mainline topic candidates, draft articles, or publish anything.
"""
