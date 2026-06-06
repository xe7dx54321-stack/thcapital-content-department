"""Build a high-value source expansion plan for Phase 26."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import P0_SOURCE_CANDIDATES, P1_SOURCE_CANDIDATES, compact_text, list_dicts, markdown_table, stable_id


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__high-value-source-expansion-plan.json",
        "dated_md": paths.logs_root / f"{run_date}__high-value-source-expansion-plan.md",
        "latest_json": paths.logs_root / "latest_high_value_source_expansion_plan.json",
        "latest_md": paths.logs_root / "latest_high_value_source_expansion_plan.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__high-value-source-expansion-plan-board.md",
        "board_latest_md": paths.frontstage_root / "latest_high_value_source_expansion_plan_board.md",
    }


def configured_source_names(sources_yaml: Path) -> set[str]:
    if not sources_yaml.exists():
        return set()
    text = sources_yaml.read_text(encoding="utf-8").lower()
    return {token for token in ("openai", "anthropic", "deepmind", "google", "meta", "nvidia", "hugging", "github", "arxiv") if token in text}


def candidate_payload(candidate: dict[str, Any], configured_tokens: set[str]) -> dict[str, Any]:
    name = str(candidate.get("source_name", ""))
    already_configured = any(token in name.lower() for token in configured_tokens)
    risk = candidate.get("risk") if isinstance(candidate.get("risk"), list) else []
    if already_configured:
        risk = [*risk, "already_configured_check_runtime"]
    return {
        "candidate_id": stable_id("src_candidate", name, candidate.get("priority")),
        "source_name": name,
        "source_type": candidate.get("source_type", "manual_url"),
        "category": candidate.get("category", "global_media"),
        "priority": candidate.get("priority", "P2"),
        "reason": candidate.get("reason", ""),
        "suggested_fetch_method": candidate.get("suggested_fetch_method", "manual_url"),
        "requires_api_key": bool(candidate.get("requires_api_key", False)),
        "requires_login": bool(candidate.get("requires_login", False)),
        "estimated_reliability": candidate.get("estimated_reliability", "MEDIUM"),
        "expected_daily_value": "HIGH" if candidate.get("priority") == "P0" else "MEDIUM",
        "risk": risk,
        "implementation_note": (
            "Prefer dry-run connector or manifest-backed ingestion. Do not bypass login/paywall."
            if candidate.get("suggested_fetch_method") != "none_yet"
            else "Future planning only."
        ),
    }


def build_high_value_source_expansion_plan(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    audit = read_json(paths.logs_root / "latest_source_coverage_gap_audit.json")
    configured_tokens = configured_source_names(repo_root / "config" / "sources.yaml")
    gaps = list_dicts(audit.get("coverage_gaps"))
    high_gap_areas = {str(item.get("area")) for item in gaps if item.get("severity") == "HIGH"}
    candidates = [candidate_payload(item, configured_tokens) for item in (*P0_SOURCE_CANDIDATES, *P1_SOURCE_CANDIDATES)]

    if "funding" in high_gap_areas:
        candidates.append(
            candidate_payload(
                {
                    "source_name": "Funding AI search query pack",
                    "source_type": "search_query",
                    "category": "funding",
                    "priority": "P2",
                    "reason": "Funding coverage gap requires manual query-driven backfill before connector work.",
                    "suggested_fetch_method": "search_query",
                    "requires_api_key": False,
                    "estimated_reliability": "LOW",
                },
                configured_tokens,
            )
        )
    if "social_signal" in high_gap_areas:
        candidates.append(
            candidate_payload(
                {
                    "source_name": "X / Reddit AI weak signal watchlist",
                    "source_type": "social_signal",
                    "category": "developer_community",
                    "priority": "P3",
                    "reason": "Weak signals are useful but should stay manual until safety and noise controls exist.",
                    "suggested_fetch_method": "manual_url",
                    "requires_api_key": False,
                    "estimated_reliability": "LOW",
                    "risk": ["high_noise", "manual_verification_required"],
                },
                configured_tokens,
            )
        )

    priority_counts = {priority: sum(1 for item in candidates if item.get("priority") == priority) for priority in ("P0", "P1", "P2", "P3")}
    summary = {
        "candidate_count": len(candidates),
        "p0": priority_counts["P0"],
        "p1": priority_counts["P1"],
        "p2": priority_counts["P2"],
        "p3": priority_counts["P3"],
        "api_required": sum(1 for item in candidates if item.get("requires_api_key")),
        "no_api_required": sum(1 for item in candidates if not item.get("requires_api_key")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "source_candidates": candidates,
        "summary": summary,
        "policy": {
            "plan_only": True,
            "do_not_change_sources_yaml": True,
            "do_not_bypass_login_or_paywall": True,
            "api_keys_not_required_by_default": True,
        },
        "warnings": [
            "Missing source coverage audit; expansion defaults to static P0/P1 recommendation set."
            if not audit
            else ""
        ],
    }
    payload["warnings"] = [item for item in payload["warnings"] if item]
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        {
            "priority": item.get("priority"),
            "source": item.get("source_name"),
            "category": item.get("category"),
            "method": item.get("suggested_fetch_method"),
            "reason": compact_text(item.get("reason"), 80),
        }
        for item in list_dicts(payload.get("source_candidates"))[:30]
    ]
    return f"""# High-value Source Expansion Plan

## Summary

- candidate_count: `{summary.get('candidate_count', 0)}`
- p0: `{summary.get('p0', 0)}`
- p1: `{summary.get('p1', 0)}`
- p2: `{summary.get('p2', 0)}`
- p3: `{summary.get('p3', 0)}`
- api_required: `{summary.get('api_required', 0)}`
- no_api_required: `{summary.get('no_api_required', 0)}`

## Candidates

{markdown_table(rows, ('priority', 'source', 'category', 'method', 'reason'))}

## Boundary

This is a plan only. It does not modify `config/sources.yaml`, call APIs, bypass logins, or create paid-source dependencies.
"""
