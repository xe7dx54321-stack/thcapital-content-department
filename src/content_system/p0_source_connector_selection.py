"""Select safe P0 sources for Phase 27 lightweight connectors."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.source_coverage_gap_audit import read_sources_config
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


CONNECTOR_BY_TYPE = {
    "official_blog": "rss_official_blog",
    "rss": "rss_official_blog",
    "github": "github_repo",
    "huggingface": "huggingface_feed",
    "arxiv": "arxiv_keyword",
    "manual_url": "manual_url_backfill",
    "search_query": "arxiv_keyword",
}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__p0-source-connector-selection.json",
        "dated_md": paths.logs_root / f"{run_date}__p0-source-connector-selection.md",
        "latest_json": paths.logs_root / "latest_p0_source_connector_selection.json",
        "latest_md": paths.logs_root / "latest_p0_source_connector_selection.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__p0-source-connector-selection-board.md",
        "board_latest_md": paths.frontstage_root / "latest_p0_source_connector_selection_board.md",
    }


def source_url_lookup(sources: list[dict[str, Any]]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for item in sources:
        label = str(item.get("label") or item.get("source_id") or "").lower()
        source_id = str(item.get("source_id") or "").lower()
        url = str(item.get("primary_url") or "")
        if label:
            lookup[label] = url
        if source_id:
            lookup[source_id] = url
    return lookup


def configured_url_for_candidate(candidate: dict[str, Any], url_lookup: dict[str, str]) -> str:
    name = str(candidate.get("source_name") or "").lower()
    aliases = {
        "openai news": "openai blog",
        "anthropic news": "anthropic news",
        "google deepmind blog": "google deepmind blog",
        "google ai blog": "google ai blog",
        "meta ai blog": "meta ai blog",
        "nvidia ai blog": "nvidia technical blog",
        "hugging face papers": "hugging face daily papers",
        "github trending ai / agent": "github trending ai",
        "arxiv ai / llm / agent queries": "arxiv cs.ai recent",
    }
    return url_lookup.get(aliases.get(name, name), "")


def selection_from_candidate(candidate: dict[str, Any], url_lookup: dict[str, str]) -> dict[str, Any]:
    source_type = str(candidate.get("source_type") or "manual_url")
    method = str(candidate.get("suggested_fetch_method") or "")
    connector_type = CONNECTOR_BY_TYPE.get(source_type) or CONNECTOR_BY_TYPE.get(method) or "manual_url_backfill"
    requires_api = bool(candidate.get("requires_api_key"))
    requires_login = bool(candidate.get("requires_login"))
    risk_flags = candidate.get("risk") if isinstance(candidate.get("risk"), list) else []
    safe_to_fetch = not requires_api and not requires_login and "paywall_or_login" not in risk_flags
    name = str(candidate.get("source_name") or "")
    if source_type == "github" and "Trending" in name:
        connector_type = "github_repo"
    if source_type == "search_query" and "arXiv" not in name:
        safe_to_fetch = False
    implementation_status = "SELECTED" if safe_to_fetch and candidate.get("priority") == "P0" else "SKIPPED"
    if implementation_status == "SKIPPED" and candidate.get("priority") == "P0":
        implementation_status = "FUTURE"
    return {
        "selection_id": stable_id("p0sel", name, connector_type),
        "source_name": name,
        "source_type": source_type if source_type in {"rss", "official_blog", "github", "huggingface", "arxiv", "manual_url"} else "manual_url",
        "category": candidate.get("category", "official_ai_lab"),
        "priority": candidate.get("priority", "P0"),
        "connector_type": connector_type,
        "requires_api_key": requires_api,
        "requires_login": requires_login,
        "safe_to_fetch": safe_to_fetch,
        "expected_value": candidate.get("expected_daily_value", "HIGH"),
        "implementation_status": implementation_status,
        "reason": candidate.get("reason", ""),
        "risk_flags": risk_flags,
        "configured_url": configured_url_for_candidate(candidate, url_lookup),
    }


def build_p0_source_connector_selection(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    expansion = read_json(paths.logs_root / "latest_high_value_source_expansion_plan.json")
    audit = read_json(paths.logs_root / "latest_source_coverage_gap_audit.json")
    sources_path = repo_root / "config" / "sources.yaml"
    configured_sources = read_sources_config(sources_path)
    url_lookup = source_url_lookup(configured_sources)
    candidates = [item for item in list_payload(expansion, "source_candidates") if item.get("priority") == "P0"]
    selected_sources = [selection_from_candidate(item, url_lookup) for item in candidates]
    if not any(item.get("connector_type") == "manual_url_backfill" for item in selected_sources):
        selected_sources.append(
            {
                "selection_id": stable_id("p0sel", "manual_url_backfill", run_date),
                "source_name": "Manual URL Backfill Queue",
                "source_type": "manual_url",
                "category": "open_source",
                "priority": "P0",
                "connector_type": "manual_url_backfill",
                "requires_api_key": False,
                "requires_login": False,
                "safe_to_fetch": True,
                "expected_value": "MEDIUM",
                "implementation_status": "SELECTED",
                "reason": "Manual backfill queue is required when public connectors are weak or blocked.",
                "risk_flags": ["manual_review_required"],
                "configured_url": "",
            }
        )
    selected = [item for item in selected_sources if item.get("implementation_status") == "SELECTED"]
    summary = {
        "selected_count": len(selected),
        "rss_official_blog": sum(1 for item in selected if item.get("connector_type") == "rss_official_blog"),
        "github_repo": sum(1 for item in selected if item.get("connector_type") == "github_repo"),
        "huggingface_feed": sum(1 for item in selected if item.get("connector_type") == "huggingface_feed"),
        "arxiv_keyword": sum(1 for item in selected if item.get("connector_type") == "arxiv_keyword"),
        "manual_url_backfill": sum(1 for item in selected if item.get("connector_type") == "manual_url_backfill"),
        "requires_api_key": sum(1 for item in selected_sources if item.get("requires_api_key")),
        "requires_login": sum(1 for item in selected_sources if item.get("requires_login")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "selected_sources": selected_sources,
        "summary": summary,
        "coverage_gap_summary": audit.get("summary") if isinstance(audit.get("summary"), dict) else {},
        "policy": {
            "no_api_key": True,
            "no_login": True,
            "metadata_only": True,
            "no_sources_yaml_mutation": True,
        },
        "warnings": [f"Missing input: {sources_path}"] if not sources_path.exists() else [],
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        {
            "status": item.get("implementation_status"),
            "source": compact_text(item.get("source_name"), 42),
            "connector": item.get("connector_type"),
            "safe": item.get("safe_to_fetch"),
            "reason": compact_text(item.get("reason"), 80),
        }
        for item in list_payload(payload, "selected_sources")
    ]
    return f"""# P0 Source Connector Selection

## Summary

- selected_count: `{summary.get('selected_count', 0)}`
- rss_official_blog: `{summary.get('rss_official_blog', 0)}`
- github_repo: `{summary.get('github_repo', 0)}`
- huggingface_feed: `{summary.get('huggingface_feed', 0)}`
- arxiv_keyword: `{summary.get('arxiv_keyword', 0)}`
- manual_url_backfill: `{summary.get('manual_url_backfill', 0)}`

## Selected Sources

{markdown_table(rows, ('status', 'source', 'connector', 'safe', 'reason'))}

## Boundary

Selection is sidecar-only and does not mutate `config/sources.yaml`.
"""
