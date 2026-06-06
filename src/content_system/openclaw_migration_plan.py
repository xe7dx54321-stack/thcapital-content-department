"""Build a P0/P1 OpenClaw source migration plan."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


PRIORITY_NAMES = (
    "reddit localllama",
    "reddit claude",
    "reddit chatgpt",
    "yc launches",
    "techcrunch",
    "finsmes",
    "trend hunt",
    "product hunt",
    "deeplearning",
    "latent space",
    "interconnects",
    "simon willison",
    "understanding ai",
    "infoq",
    "36kr",
    "36氪",
    "geekpark",
    "硅星人",
)


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__openclaw-migration-plan.json",
        "dated_md": paths.logs_root / f"{run_date}__openclaw-migration-plan.md",
        "latest_json": paths.logs_root / "latest_openclaw_migration_plan.json",
        "latest_md": paths.logs_root / "latest_openclaw_migration_plan.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__openclaw-migration-plan-board.md",
        "board_latest_md": paths.frontstage_root / "latest_openclaw_migration_plan_board.md",
    }


def connector_type_for(item: dict[str, Any]) -> str:
    lane = str(item.get("lane") or "")
    source_id = str(item.get("source_id") or "").lower()
    role = str(item.get("evidence_role") or "")
    if "reddit" in source_id or lane == "reddit_llm_discussion":
        return "reddit_metadata"
    if lane == "funding_startup":
        return "media_metadata"
    if lane == "builder_research":
        return "newsletter_metadata"
    if lane == "chinese_ai_media" or "wechat" in source_id:
        return "wechat_metadata"
    if lane == "youtube_signal" or source_id.startswith("youtube__"):
        return "youtube_metadata"
    if lane == "x_signal" or source_id.startswith("x__"):
        return "x_metadata"
    if lane == "trend_heat":
        return "trend_heat_metadata"
    if role == "manual_only":
        return "manual_backfill"
    return "media_metadata"


def lane_bucket(connector_type: str, lane: str) -> str:
    if connector_type == "reddit_metadata":
        return "reddit_llm_discussion"
    if connector_type == "media_metadata":
        return "funding_startup" if lane == "funding_startup" else "builder_research"
    if connector_type == "newsletter_metadata":
        return "builder_research"
    if connector_type == "wechat_metadata":
        return "chinese_ai_media"
    return lane


def should_include(item: dict[str, Any]) -> bool:
    priority = str(item.get("migration_priority") or "")
    ingestion = str(item.get("allowed_ingestion") or "")
    source_text = f"{item.get('source_id')} {item.get('source_name')}".lower()
    if priority not in {"P0", "P1"}:
        return False
    if ingestion not in {"metadata_connector", "manual_backfill", "sidecar_inventory_only"}:
        return False
    if any(name in source_text for name in PRIORITY_NAMES):
        return True
    return str(item.get("evidence_role")) in {"supporting_evidence", "weak_signal", "heat_validation", "manual_only"}


def candidate_from_classification(item: dict[str, Any]) -> dict[str, Any]:
    connector_type = connector_type_for(item)
    lane = lane_bucket(connector_type, str(item.get("lane") or "unknown"))
    role = str(item.get("evidence_role") or "manual_only")
    manual_only = role == "manual_only" or connector_type in {"wechat_metadata", "x_metadata", "manual_backfill"}
    safe_now = bool(
        item.get("allowed_ingestion") == "metadata_connector"
        and not item.get("requires_login")
        and not item.get("requires_api_key")
        and connector_type not in {"x_metadata"}
    )
    if connector_type in {"wechat_metadata"}:
        safe_now = True
    return {
        "migration_id": stable_id("ocmig", item.get("source_id"), connector_type),
        "source_id": item.get("source_id", ""),
        "source_name": item.get("source_name", ""),
        "lane": lane,
        "migration_priority": item.get("migration_priority", "P1"),
        "connector_type": connector_type,
        "evidence_role": role if role in {"supporting_evidence", "weak_signal", "heat_validation", "manual_only"} else "manual_only",
        "safe_to_implement_now": safe_now or manual_only,
        "requires_login": bool(item.get("requires_login")),
        "requires_api_key": bool(item.get("requires_api_key")),
        "do_not_fetch_full_text": True,
        "implementation_note": (
            "Metadata connector only; do not use as hard evidence without confirmation."
            if role in {"weak_signal", "heat_validation"}
            else "Manual metadata/backfill only; do not fetch full text."
            if manual_only
            else "Public metadata connector candidate."
        ),
    }


def build_openclaw_migration_plan(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    risk_path = paths.logs_root / "latest_openclaw_source_risk_classification.json"
    inventory_path = paths.logs_root / "latest_openclaw_source_inventory.json"
    expansion_path = paths.logs_root / "latest_high_value_source_expansion_plan.json"
    risk = read_json(risk_path)
    inventory = read_json(inventory_path)
    expansion = read_json(expansion_path)
    candidates = [candidate_from_classification(item) for item in list_payload(risk, "classified_sources") if should_include(item)]
    candidates = sorted(
        candidates,
        key=lambda item: (
            {"P0": 0, "P1": 1, "P2": 2, "P3": 3}.get(str(item.get("migration_priority")), 9),
            str(item.get("connector_type")),
            str(item.get("source_name")),
        ),
    )
    summary = {
        "candidate_count": len(candidates),
        "p0": sum(1 for item in candidates if item.get("migration_priority") == "P0"),
        "p1": sum(1 for item in candidates if item.get("migration_priority") == "P1"),
        "reddit": sum(1 for item in candidates if item.get("connector_type") == "reddit_metadata"),
        "funding_startup": sum(1 for item in candidates if item.get("lane") == "funding_startup"),
        "builder_research": sum(1 for item in candidates if item.get("lane") == "builder_research"),
        "chinese_ai_media": sum(1 for item in candidates if item.get("lane") == "chinese_ai_media"),
        "youtube_signal": sum(1 for item in candidates if item.get("lane") == "youtube_signal"),
        "x_signal": sum(1 for item in candidates if item.get("lane") == "x_signal"),
        "manual_only": sum(1 for item in candidates if item.get("evidence_role") == "manual_only"),
    }
    warnings = []
    for path in (risk_path, inventory_path, expansion_path):
        if not path.exists():
            warnings.append(f"Missing input: {path}")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "migration_candidates": candidates,
        "summary": summary,
        "context": {
            "inventory_source_count": len(list_payload(inventory, "sources")),
            "source_expansion_candidates": len(list_payload(expansion, "source_candidates")),
        },
        "warnings": warnings,
        "policy": {
            "p0_p1_plan_only": True,
            "metadata_only": True,
            "no_cron_migration": True,
            "no_gateway_dependency": True,
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
            "priority": item.get("migration_priority"),
            "connector": item.get("connector_type"),
            "role": item.get("evidence_role"),
            "lane": item.get("lane"),
            "source": compact_text(item.get("source_name"), 48),
        }
        for item in list_payload(payload, "migration_candidates")[:40]
    ]
    return f"""# OpenClaw P0/P1 Migration Plan

## Summary

- candidate_count: `{summary.get('candidate_count', 0)}`
- p0/p1: `{summary.get('p0', 0)}` / `{summary.get('p1', 0)}`
- reddit: `{summary.get('reddit', 0)}`
- funding_startup: `{summary.get('funding_startup', 0)}`
- builder_research: `{summary.get('builder_research', 0)}`
- chinese_ai_media: `{summary.get('chinese_ai_media', 0)}`
- youtube_signal: `{summary.get('youtube_signal', 0)}`
- x_signal: `{summary.get('x_signal', 0)}`
- manual_only: `{summary.get('manual_only', 0)}`

## Migration Candidates

{markdown_table(rows, ('priority', 'connector', 'role', 'lane', 'source'))}

## Boundary

The plan selects low-risk metadata or manual-only candidates. It does not migrate OpenClaw cron jobs, start the gateway, fetch full text, or mutate config/sources.yaml.
"""
