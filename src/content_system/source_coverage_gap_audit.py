"""Audit upstream source coverage gaps for Phase 26."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import LANES, compact_text, detect_lane, list_dicts, markdown_table, source_items_from_manifest, stable_id


EXPECTED_AREAS: tuple[dict[str, str], ...] = (
    {"area": "official_ai_lab", "label": "AI official sources"},
    {"area": "model_release", "label": "Model company updates"},
    {"area": "agent_framework", "label": "Agent frameworks and products"},
    {"area": "open_source", "label": "Open source projects / GitHub / Hugging Face"},
    {"area": "papers", "label": "Papers / arXiv / Papers with Code"},
    {"area": "funding", "label": "Funding / startups / VC"},
    {"area": "china_media", "label": "Chinese technology media"},
    {"area": "developer_community", "label": "Developer communities / HN / Product Hunt"},
    {"area": "social_signal", "label": "Weak social signals / X / Reddit"},
    {"area": "ai_infra", "label": "AI infra / compute / chips / optical interconnect"},
    {"area": "global_media", "label": "Global technology media"},
)


AREA_TO_LANE = {
    "papers": "paper_research",
    "funding": "funding_startup",
    "china_media": "china_ai_media",
    "social_signal": "social_weak_signal",
    "global_media": "global_ai_media",
}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__source-coverage-gap-audit.json",
        "dated_md": paths.logs_root / f"{run_date}__source-coverage-gap-audit.md",
        "latest_json": paths.logs_root / "latest_source_coverage_gap_audit.json",
        "latest_md": paths.logs_root / "latest_source_coverage_gap_audit.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__source-coverage-gap-audit-board.md",
        "board_latest_md": paths.frontstage_root / "latest_source_coverage_gap_audit_board.md",
    }


def read_sources_config(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        payload = yaml.safe_load(text) or {}
        sources = payload.get("sources")
        if isinstance(sources, list):
            return [item for item in sources if isinstance(item, dict)]
    except Exception:
        pass
    sources: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- source_id:"):
            if current:
                sources.append(current)
            current = {"source_id": stripped.split(":", 1)[1].strip().strip('"')}
        elif current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip().strip('"')
    if current:
        sources.append(current)
    return sources


def lane_presence_from_sources(sources: list[dict[str, Any]], runtime_records: list[dict[str, Any]], manifest_sources: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    presence = {lane["lane_id"]: {"configured": 0, "observed": 0, "missing": 0, "stale": 0} for lane in LANES}
    for item in sources:
        text = " ".join(str(item.get(key, "")) for key in ("source_id", "label", "category", "notes", "primary_url"))
        lane_id = detect_lane(text, item.get("source_id", ""))
        presence.setdefault(lane_id, {"configured": 0, "observed": 0, "missing": 0, "stale": 0})["configured"] += 1
    for item in runtime_records:
        text = " ".join(str(item.get(key, "")) for key in ("source_id", "label", "category", "runtime_reason"))
        lane_id = detect_lane(text, item.get("source_id", ""))
        status = str(item.get("runtime_status") or item.get("status") or "").upper()
        if status in {"SUCCESS", "OK", "OBSERVED", "ACTIVE"} or safe_int(item.get("evidence_count")) or safe_int(item.get("artifact_count")):
            presence.setdefault(lane_id, {"configured": 0, "observed": 0, "missing": 0, "stale": 0})["observed"] += 1
        elif "MISSING" in status:
            presence.setdefault(lane_id, {"configured": 0, "observed": 0, "missing": 0, "stale": 0})["missing"] += 1
        elif "STALE" in status:
            presence.setdefault(lane_id, {"configured": 0, "observed": 0, "missing": 0, "stale": 0})["stale"] += 1
    for item in manifest_sources:
        text = " ".join(str(item.get(key, "")) for key in ("source_id", "label", "notes"))
        lane_id = detect_lane(text, item.get("source_id", ""))
        if str(item.get("status", "")).upper() in {"SUCCESS", "OK"} or safe_int(item.get("items_written")) or safe_int(item.get("items_found")):
            presence.setdefault(lane_id, {"configured": 0, "observed": 0, "missing": 0, "stale": 0})["observed"] += 1
    return presence


def build_source_coverage_gap_audit(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    source_config = repo_root / "config" / "sources.yaml"
    sources = read_sources_config(source_config)
    runtime = read_json(paths.logs_root / "latest_source_runtime_health.json")
    source_summary = read_json(paths.logs_root / "latest_daily_source_run_summary.json")
    manifest = read_json(paths.logs_root / "latest_official_runtime_manifest.json")
    high_value = read_json(paths.market_content_root / "03_topic_candidates" / "latest_high_value_candidates.json")
    topic_scores = read_json(paths.market_content_root / "03_topic_candidates" / "latest_methodology_topic_scores.json")
    stable_ops = read_json(paths.logs_root / "latest_stable_daily_ops.json")

    runtime_records = list_dicts(runtime.get("records"))
    manifest_sources = source_items_from_manifest(manifest)
    enabled_sources = [item for item in sources if item.get("enabled", True) not in {False, "false", "False"}]
    observed_sources = safe_int(runtime.get("observed_count") or source_summary.get("observed_sources"))
    missing_expected = safe_int(runtime.get("missing_expected_count") or source_summary.get("missing_expected"))
    stale_sources = sum(1 for item in runtime_records if "STALE" in str(item.get("runtime_status", "")).upper())
    high_value_count = safe_int(high_value.get("candidate_count") or len(list_dicts(high_value.get("candidates"))))
    topic_summary = topic_scores.get("summary") if isinstance(topic_scores.get("summary"), dict) else {}
    topic_count = safe_int(topic_summary.get("topic_count") or len(list_dicts(topic_scores.get("topics"))))
    presence = lane_presence_from_sources(sources, runtime_records, manifest_sources)

    coverage_gaps: list[dict[str, Any]] = []
    for area in EXPECTED_AREAS:
        lane_id = AREA_TO_LANE.get(area["area"], area["area"])
        lane = presence.get(lane_id, {"configured": 0, "observed": 0, "missing": 0, "stale": 0})
        evidence = [
            f"configured={lane.get('configured', 0)}",
            f"observed={lane.get('observed', 0)}",
            f"missing={lane.get('missing', 0)}",
            f"stale={lane.get('stale', 0)}",
        ]
        if lane.get("configured", 0) == 0:
            severity = "HIGH"
            impact = "missed_global_signal"
            description = f"{area['label']} has no configured source lane."
        elif lane.get("observed", 0) == 0:
            severity = "HIGH" if lane_id in {"official_ai_lab", "agent_framework", "open_source", "paper_research", "ai_infra"} else "MEDIUM"
            impact = "no_daily_hot_material"
            description = f"{area['label']} is configured but produced no observed runtime signal."
        elif lane.get("missing", 0) or lane.get("stale", 0):
            severity = "MEDIUM"
            impact = "weak_topic_pool"
            description = f"{area['label']} has missing or stale runtime evidence."
        else:
            severity = "LOW"
            impact = "low_evidence_density" if high_value_count < 5 else "none"
            description = f"{area['label']} has some current coverage."
        if severity != "LOW" or high_value_count < 5 or topic_count < 5:
            coverage_gaps.append(
                {
                    "gap_id": stable_id("gap", area["area"], description),
                    "area": area["area"],
                    "severity": severity,
                    "description": description,
                    "evidence": evidence,
                    "impact_on_content": impact,
                    "recommended_action": "Add or repair source lane, then route to hot signal capture and backfill queue.",
                }
            )

    if topic_count < 5 or high_value_count < 5:
        coverage_gaps.append(
            {
                "gap_id": stable_id("gap", "topic_supply", topic_count, high_value_count),
                "area": "developer_community",
                "severity": "HIGH" if high_value_count == 0 else "MEDIUM",
                "description": "Daily topic supply is thin relative to downstream content ops needs.",
                "evidence": [f"topic_output_count={topic_count}", f"high_value_candidate_count={high_value_count}"],
                "impact_on_content": "weak_topic_pool",
                "recommended_action": "Use backfill queue for P0 lanes before treating downstream queue as exhausted.",
            }
        )

    source_health_findings = [
        {
            "source_id": item.get("source_id", ""),
            "status": item.get("runtime_status") or item.get("status") or "UNKNOWN",
            "reason": compact_text(item.get("runtime_reason") or item.get("error_message") or "", 180),
        }
        for item in runtime_records[:20]
    ]
    topic_supply_findings = [
        f"topic_output_count={topic_count}",
        f"high_value_candidate_count={high_value_count}",
        f"stable_daily_ops_status={stable_ops.get('status', 'UNKNOWN')}",
    ]
    summary = {
        "gap_count": len(coverage_gaps),
        "high_severity": sum(1 for item in coverage_gaps if item.get("severity") == "HIGH"),
        "medium_severity": sum(1 for item in coverage_gaps if item.get("severity") == "MEDIUM"),
        "low_severity": sum(1 for item in coverage_gaps if item.get("severity") == "LOW"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "coverage_summary": {
            "configured_sources": len(sources),
            "enabled_sources": len(enabled_sources),
            "observed_sources": observed_sources,
            "missing_expected_sources": missing_expected,
            "stale_sources": stale_sources,
            "topic_output_count": topic_count,
            "high_value_candidate_count": high_value_count,
        },
        "coverage_gaps": coverage_gaps,
        "source_health_findings": source_health_findings,
        "topic_supply_findings": topic_supply_findings,
        "summary": summary,
        "warnings": [
            f"Missing input: {path}"
            for path in (
                source_config,
                paths.logs_root / "latest_source_runtime_health.json",
                paths.logs_root / "latest_daily_source_run_summary.json",
                paths.logs_root / "latest_official_runtime_manifest.json",
            )
            if not path.exists()
        ],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    coverage = payload.get("coverage_summary") if isinstance(payload.get("coverage_summary"), dict) else {}
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        {
            "area": item.get("area"),
            "severity": item.get("severity"),
            "impact": item.get("impact_on_content"),
            "description": compact_text(item.get("description"), 90),
        }
        for item in list_dicts(payload.get("coverage_gaps"))
    ]
    return f"""# Source Coverage Gap Audit

## Summary

- configured_sources: `{coverage.get('configured_sources', 0)}`
- enabled_sources: `{coverage.get('enabled_sources', 0)}`
- observed_sources: `{coverage.get('observed_sources', 0)}`
- missing_expected_sources: `{coverage.get('missing_expected_sources', 0)}`
- stale_sources: `{coverage.get('stale_sources', 0)}`
- topic_output_count: `{coverage.get('topic_output_count', 0)}`
- high_value_candidate_count: `{coverage.get('high_value_candidate_count', 0)}`
- gap_count: `{summary.get('gap_count', 0)}`
- high_severity: `{summary.get('high_severity', 0)}`

## Coverage Gaps

{markdown_table(rows, ('area', 'severity', 'impact', 'description'))}

## Boundary

This report audits local source coverage only. It does not fetch external sources, bypass logins, or change `config/sources.yaml`.
"""
