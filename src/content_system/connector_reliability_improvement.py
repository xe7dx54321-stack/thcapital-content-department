"""Build reliability improvement guidance for selected P0 connectors."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__connector-reliability-improvement.json",
        "dated_md": paths.logs_root / f"{run_date}__connector-reliability-improvement.md",
        "latest_json": paths.logs_root / "latest_connector_reliability_improvement.json",
        "latest_md": paths.logs_root / "latest_connector_reliability_improvement.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__connector-reliability-improvement-board.md",
        "board_latest_md": paths.frontstage_root / "latest_connector_reliability_improvement_board.md",
    }


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def classify_issue_type(status: str, item_count: int, error: str) -> str:
    lowered = error.lower()
    if "rate" in lowered or "429" in lowered:
        return "rate_limited"
    if "parse" in lowered or "xml" in lowered or "json" in lowered:
        return "parse_error"
    if status in {"FAILED"}:
        return "fetch_failed"
    if status in {"EMPTY"} or item_count == 0:
        return "empty_output"
    if status in {"WEAK"}:
        return "weak_output"
    return "unknown"


def severity_for(issue_type: str, status: str, item_count: int) -> str:
    if issue_type in {"fetch_failed", "parse_error", "rate_limited"} and item_count == 0:
        return "HIGH"
    if issue_type in {"empty_output", "weak_output"} or status in {"WEAK", "SKIPPED"}:
        return "MEDIUM"
    return "LOW"


def fallback_for(issue_type: str) -> str:
    if issue_type == "rate_limited":
        return "retry_later"
    if issue_type in {"fetch_failed", "parse_error", "unknown"}:
        return "source_config_review"
    if issue_type in {"empty_output", "weak_output"}:
        return "manual_backfill"
    return "monitor_only"


def connector_issue(
    connector_type: str,
    source_name: str,
    status: str,
    item_count: int,
    error: str = "",
    issue: str = "",
) -> dict[str, Any]:
    issue_type = classify_issue_type(status, item_count, error or issue)
    severity = severity_for(issue_type, status, item_count)
    fallback_action = fallback_for(issue_type)
    safe_to_retry = fallback_action == "retry_later" or (issue_type == "fetch_failed" and not error)
    root_cause = compact_text(error or issue or f"{connector_type} returned {status} with {item_count} item(s).", 220)
    recommended_fix = {
        "retry_later": "Retry once in a later daily run; do not loop or bypass public endpoint limits.",
        "manual_backfill": "Create a manual backfill task or provide one verified URL for operator review.",
        "source_config_review": "Review the public URL/RSS/query configuration as a sidecar note; do not mutate config automatically.",
        "alternative_url": "Suggest an alternative public metadata endpoint for a future config patch.",
        "monitor_only": "Monitor next run; no operator action needed unless repeated.",
    }.get(fallback_action, "Monitor next run.")
    return {
        "issue_id": stable_id("connrel", connector_type, source_name, issue_type, status),
        "connector_type": connector_type,
        "source_name": source_name,
        "severity": severity,
        "issue_type": issue_type,
        "root_cause": root_cause,
        "recommended_fix": recommended_fix,
        "fallback_action": fallback_action,
        "safe_to_auto_retry": safe_to_retry,
        "auto_applied": False,
    }


def build_connector_reliability_improvement(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    inputs = {
        "connector_health_gate": paths.logs_root / "latest_connector_source_health_gate.json",
        "rss_connector_run": paths.logs_root / "latest_rss_official_blog_connector_run.json",
        "lightweight_research_connector_run": paths.logs_root / "latest_lightweight_research_connector_run.json",
        "p0_selection": paths.logs_root / "latest_p0_source_connector_selection.json",
        "source_expansion": paths.logs_root / "latest_high_value_source_expansion_plan.json",
    }
    warnings = warning_for_missing(inputs)
    health_gate = read_json(inputs["connector_health_gate"])
    rss = read_json(inputs["rss_connector_run"])
    research = read_json(inputs["lightweight_research_connector_run"])
    selection = read_json(inputs["p0_selection"])
    expansion = read_json(inputs["source_expansion"])

    issues_by_id: dict[str, dict[str, Any]] = {}
    for source in list_payload(rss, "sources"):
        status = str(source.get("status") or "UNKNOWN").upper()
        count = safe_int(source.get("item_count"))
        if status in {"FAILED", "EMPTY", "SKIPPED"} or count == 0:
            issue = connector_issue(
                "rss_official_blog",
                str(source.get("source_name") or source.get("source_id") or "rss_source"),
                status,
                count,
                str(source.get("error") or ""),
            )
            issues_by_id[issue["issue_id"]] = issue

    for connector in list_payload(research, "connectors"):
        connector_type = str(connector.get("connector_type") or "github")
        status = str(connector.get("status") or "UNKNOWN").upper()
        count = safe_int(connector.get("item_count"))
        if status in {"FAILED", "EMPTY", "SKIPPED"} or count == 0:
            issue = connector_issue(
                connector_type,
                str(connector.get("query_or_source") or connector_type),
                status,
                count,
                str(connector.get("error") or ""),
            )
            issues_by_id[issue["issue_id"]] = issue

    for health in list_payload(health_gate, "connector_health"):
        status = str(health.get("status") or "UNKNOWN").upper()
        count = safe_int(health.get("item_count"))
        if status in {"FAILED", "WEAK", "SKIPPED"}:
            connector_type = str(health.get("connector_type") or "unknown")
            issue = connector_issue(
                connector_type,
                connector_type,
                status,
                count,
                issue=str(health.get("issue") or ""),
            )
            issues_by_id.setdefault(issue["issue_id"], issue)

    selected_count = safe_int((selection.get("summary") or {}).get("selected_count")) if isinstance(selection.get("summary"), dict) else 0
    candidate_count = safe_int((expansion.get("summary") or {}).get("candidate_count")) if isinstance(expansion.get("summary"), dict) else 0
    if selected_count == 0 and candidate_count:
        issue = connector_issue("manual_url", "p0_source_selection", "EMPTY", 0, "No selected P0 connector source was available.")
        issues_by_id[issue["issue_id"]] = issue

    connector_issues = sorted(
        issues_by_id.values(),
        key=lambda item: ({"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(str(item.get("severity")), 3), item.get("connector_type", "")),
    )
    summary = {
        "issue_count": len(connector_issues),
        "high": sum(1 for item in connector_issues if item.get("severity") == "HIGH"),
        "medium": sum(1 for item in connector_issues if item.get("severity") == "MEDIUM"),
        "low": sum(1 for item in connector_issues if item.get("severity") == "LOW"),
        "safe_to_retry": sum(1 for item in connector_issues if item.get("safe_to_auto_retry")),
        "requires_manual": sum(1 for item in connector_issues if not item.get("safe_to_auto_retry")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "connector_issues": connector_issues,
        "reliability_summary": summary,
        "warnings": warnings,
        "policy": {
            "sidecar_only": True,
            "auto_applied": False,
            "no_sources_yaml_mutation": True,
            "no_login_or_paywall_bypass": True,
            "no_openclaw_migration": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("reliability_summary") if isinstance(payload.get("reliability_summary"), dict) else {}
    rows = [
        {
            "severity": item.get("severity"),
            "connector": item.get("connector_type"),
            "source": compact_text(item.get("source_name"), 40),
            "type": item.get("issue_type"),
            "fallback": item.get("fallback_action"),
        }
        for item in list_payload(payload, "connector_issues")[:40]
    ]
    warnings = "\n".join(f"- {item}" for item in payload.get("warnings", [])) or "- None."
    return f"""# P0 Connector Reliability Improvement

## Summary

- issue_count: `{summary.get('issue_count', 0)}`
- high: `{summary.get('high', 0)}`
- medium: `{summary.get('medium', 0)}`
- low: `{summary.get('low', 0)}`
- safe_to_retry: `{summary.get('safe_to_retry', 0)}`
- requires_manual: `{summary.get('requires_manual', 0)}`

## Connector Issues

{markdown_table(rows, ('severity', 'connector', 'source', 'type', 'fallback'))}

## Input Warnings

{warnings}

## Boundary

This report only generates sidecar reliability guidance. It does not mutate `config/sources.yaml`, bypass login/paywalls, fetch full text, or migrate OpenClaw cron/source inventory.
"""
