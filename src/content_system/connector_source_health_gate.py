"""Run regression and health checks over Phase 27 connector outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table


FORBIDDEN_FULL_TEXT_FIELDS = {"body", "content", "full_text", "html", "raw_html", "article_text", "pdf_text"}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__connector-source-health-gate.json",
        "dated_md": paths.logs_root / f"{run_date}__connector-source-health-gate.md",
        "latest_json": paths.logs_root / "latest_connector_source_health_gate.json",
        "latest_md": paths.logs_root / "latest_connector_source_health_gate.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__connector-source-health-gate-board.md",
        "board_latest_md": paths.frontstage_root / "latest_connector_source_health_gate_board.md",
    }


def check(check_id: str, status: str, message: str) -> dict[str, str]:
    return {"check_id": check_id, "status": status, "message": message}


def all_raw_items(rss: dict[str, Any], research: dict[str, Any], manual: dict[str, Any], normalized: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for source in list_payload(rss, "sources"):
        items.extend(list_payload(source, "items"))
    for connector in list_payload(research, "connectors"):
        items.extend(list_payload(connector, "items"))
    items.extend(list_payload(manual, "manual_items"))
    items.extend(list_payload(normalized, "items"))
    return items


def connector_status(connector_type: str, item_count: int, failed_count: int = 0, skipped_count: int = 0, source_count: int = 0) -> dict[str, Any]:
    if source_count <= 0:
        status = "SKIPPED"
        issue = "No selected source for this connector type."
    elif item_count > 0 and failed_count == 0:
        status = "HEALTHY"
        issue = ""
    elif item_count > 0:
        status = "WEAK"
        issue = f"{failed_count} source(s) failed, but connector still produced metadata items."
    elif failed_count and failed_count >= source_count:
        status = "FAILED"
        issue = "All selected sources failed for this connector type."
    elif skipped_count >= source_count:
        status = "SKIPPED"
        issue = "Connector was skipped or left for manual review."
    else:
        status = "WEAK"
        issue = "Connector produced no items."
    return {"connector_type": connector_type, "status": status, "item_count": item_count, "issue": issue}


def build_connector_health(rss: dict[str, Any], research: dict[str, Any], manual: dict[str, Any]) -> list[dict[str, Any]]:
    rss_sources = list_payload(rss, "sources")
    research_connectors = list_payload(research, "connectors")
    manual_items = list_payload(manual, "manual_items")
    by_type: dict[str, list[dict[str, Any]]] = {"github": [], "huggingface": [], "arxiv": []}
    for connector in research_connectors:
        by_type.setdefault(str(connector.get("connector_type") or "unknown"), []).append(connector)
    return [
        connector_status(
            "rss_official_blog",
            sum(safe_int(item.get("item_count")) for item in rss_sources),
            sum(1 for item in rss_sources if item.get("status") == "FAILED"),
            sum(1 for item in rss_sources if item.get("status") == "SKIPPED"),
            len(rss_sources),
        ),
        *[
            connector_status(
                connector_type,
                sum(safe_int(item.get("item_count")) for item in rows),
                sum(1 for item in rows if item.get("status") == "FAILED"),
                sum(1 for item in rows if item.get("status") == "SKIPPED"),
                len(rows),
            )
            for connector_type, rows in by_type.items()
            if connector_type in {"github", "huggingface", "arxiv"}
        ],
        connector_status(
            "manual_url",
            sum(1 for item in manual_items if item.get("status") == "READY_FOR_REVIEW"),
            0,
            0,
            len(manual_items),
        ),
    ]


def build_checks(repo_root: Path, raw_items: list[dict[str, Any]], normalized: dict[str, Any], connector_health: list[dict[str, Any]]) -> list[dict[str, str]]:
    normalized_items = list_payload(normalized, "items")
    checks: list[dict[str, str]] = []
    metadata_bad = [item for item in raw_items if item.get("metadata_only") is False]
    checks.append(
        check(
            "metadata_only",
            "PASS" if not metadata_bad else "FAIL",
            "All connector outputs are metadata_only=true." if not metadata_bad else f"{len(metadata_bad)} item(s) are not metadata-only.",
        )
    )
    copyright_bad = [item for item in raw_items if item.get("copyright_safe") is False]
    checks.append(
        check(
            "copyright_safe",
            "PASS" if not copyright_bad else "FAIL",
            "All connector outputs are marked copyright_safe=true." if not copyright_bad else f"{len(copyright_bad)} item(s) are not copyright-safe.",
        )
    )
    forbidden = [item for item in raw_items if FORBIDDEN_FULL_TEXT_FIELDS.intersection(item.keys())]
    checks.append(
        check(
            "no_full_text_fields",
            "PASS" if not forbidden else "FAIL",
            "No full-text fields are present." if not forbidden else f"{len(forbidden)} item(s) include forbidden full-text fields.",
        )
    )
    missing_url = [item for item in normalized_items if not item.get("url")]
    checks.append(
        check(
            "url_exists",
            "PASS" if not missing_url else "FAIL",
            "Every normalized upstream item has a URL." if not missing_url else f"{len(missing_url)} normalized item(s) missing URL.",
        )
    )
    missing_title = [item for item in normalized_items if not item.get("title")]
    checks.append(
        check(
            "title_exists",
            "PASS" if not missing_title else "FAIL",
            "Every normalized upstream item has a title." if not missing_title else f"{len(missing_title)} normalized item(s) missing title.",
        )
    )
    failed_connectors = [item for item in connector_health if item.get("status") == "FAILED"]
    normalized_count = safe_int((normalized.get("summary") or {}).get("item_count")) if isinstance(normalized.get("summary"), dict) else 0
    checks.append(
        check(
            "single_connector_failure_isolated",
            "PASS" if not failed_connectors else "WARN" if normalized_count else "FAIL",
            "No connector failed." if not failed_connectors else f"{len(failed_connectors)} connector(s) failed; pipeline continues with other metadata items.",
        )
    )
    manual_bad = [
        item for item in raw_items
        if (item.get("source") in {"fallback_backfill_queue", "url_capture_queue"} or item.get("source_type") == "manual_url")
        and item.get("do_not_auto_fetch") is False
    ]
    checks.append(
        check(
            "manual_url_do_not_auto_fetch",
            "PASS" if not manual_bad else "FAIL",
            "Manual URL items remain do_not_auto_fetch=true." if not manual_bad else f"{len(manual_bad)} manual item(s) allow auto fetch.",
        )
    )
    gitignore = (repo_root / ".gitignore").read_text(encoding="utf-8", errors="replace") if (repo_root / ".gitignore").exists() else ""
    required_patterns = ["normalized-upstream-items", "connector-source-health-gate", "phase27-daily-connector-pipeline"]
    missing_patterns = [pattern for pattern in required_patterns if pattern not in gitignore]
    checks.append(
        check(
            "generated_artifacts_ignored",
            "PASS" if not missing_patterns else "WARN",
            "Phase 27 generated artifacts are covered by .gitignore." if not missing_patterns else f"Missing .gitignore pattern(s): {', '.join(missing_patterns)}",
        )
    )
    return checks


def build_connector_source_health_gate(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    rss = read_json(paths.logs_root / "latest_rss_official_blog_connector_run.json")
    research = read_json(paths.logs_root / "latest_lightweight_research_connector_run.json")
    manual = read_json(paths.logs_root / "latest_manual_url_backfill_ingestion.json")
    normalized = read_json(paths.logs_root / "latest_normalized_upstream_items.json")
    connector_health = build_connector_health(rss, research, manual)
    raw_items = all_raw_items(rss, research, manual, normalized)
    checks = build_checks(repo_root, raw_items, normalized, connector_health)
    summary = {
        "check_count": len(checks),
        "pass": sum(1 for item in checks if item.get("status") == "PASS"),
        "warn": sum(1 for item in checks if item.get("status") == "WARN"),
        "fail": sum(1 for item in checks if item.get("status") == "FAIL"),
        "healthy_connectors": sum(1 for item in connector_health if item.get("status") == "HEALTHY"),
        "weak_connectors": sum(1 for item in connector_health if item.get("status") == "WEAK"),
        "failed_connectors": sum(1 for item in connector_health if item.get("status") == "FAILED"),
        "normalized_item_count": safe_int((normalized.get("summary") or {}).get("item_count")) if isinstance(normalized.get("summary"), dict) else 0,
    }
    if summary["fail"] and summary["normalized_item_count"] == 0:
        gate_status = "BLOCKED"
    elif summary["fail"] or summary["failed_connectors"]:
        gate_status = "DEGRADED"
    elif summary["warn"] or summary["weak_connectors"]:
        gate_status = "ACTIONABLE"
    else:
        gate_status = "PASS"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "gate_status": gate_status,
        "checks": checks,
        "connector_health": connector_health,
        "summary": summary,
        "policy": {
            "metadata_only": True,
            "copyright_safe": True,
            "no_full_text": True,
            "manual_url_not_auto_fetched": True,
            "single_connector_failure_isolated": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    check_rows = [
        {
            "check": item.get("check_id"),
            "status": item.get("status"),
            "message": compact_text(item.get("message"), 90),
        }
        for item in list_payload(payload, "checks")
    ]
    health_rows = [
        {
            "connector": item.get("connector_type"),
            "status": item.get("status"),
            "items": item.get("item_count"),
            "issue": compact_text(item.get("issue"), 80),
        }
        for item in list_payload(payload, "connector_health")
    ]
    return f"""# Connector Source Health Gate

## Summary

- gate_status: `{payload.get('gate_status')}`
- check_count: `{summary.get('check_count', 0)}`
- pass: `{summary.get('pass', 0)}`
- warn: `{summary.get('warn', 0)}`
- fail: `{summary.get('fail', 0)}`
- healthy_connectors: `{summary.get('healthy_connectors', 0)}`
- weak_connectors: `{summary.get('weak_connectors', 0)}`
- failed_connectors: `{summary.get('failed_connectors', 0)}`
- normalized_item_count: `{summary.get('normalized_item_count', 0)}`

## Checks

{markdown_table(check_rows, ('check', 'status', 'message'))}

## Connector Health

{markdown_table(health_rows, ('connector', 'status', 'items', 'issue'))}

## Boundary

The health gate verifies connector metadata safety. It does not publish, fetch manual URL bodies, call APIs, or mutate source configuration.
"""
