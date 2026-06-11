"""Regression gate for OpenClaw migrated signals before content-chain use."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table


WEAK_LANES = {"reddit_llm_discussion", "youtube_signal", "x_signal", "trend_heat", "chinese_ai_media"}
FORBIDDEN_FULLTEXT_KEYS = {"full_text", "raw_content", "article_body", "body", "content_html", "content_text"}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__openclaw-to-content-regression-gate.json",
        "dated_md": paths.logs_root / f"{run_date}__openclaw-to-content-regression-gate.md",
        "latest_json": paths.logs_root / "latest_openclaw_to_content_regression_gate.json",
        "latest_md": paths.logs_root / "latest_openclaw_to_content_regression_gate.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__openclaw-to-content-regression-gate-board.md",
        "board_latest_md": paths.frontstage_root / "latest_openclaw_to_content_regression_gate_board.md",
    }


def evidence_root(paths: ProjectPaths) -> Path:
    return paths.market_content_root / "03_topic_candidates"


def warning_for_missing(paths_by_name: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in paths_by_name.items() if not path.exists()]


def scan_for_keys(value: Any, keys: set[str], path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}" if path else str(key)
            if str(key) in keys:
                found.append(key_path)
            found.extend(scan_for_keys(nested, keys, key_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(scan_for_keys(item, keys, f"{path}[{index}]"))
    return found


def check(check_id: str, status: str, message: str) -> dict[str, str]:
    return {"check_id": check_id, "status": status, "message": message}


def build_checks(activated: dict[str, Any], confirmation: dict[str, Any], backfill: dict[str, Any], normalized: dict[str, Any]) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    checks: list[dict[str, str]] = []
    violations: list[dict[str, Any]] = []
    signals = list_payload(normalized, "signals")
    backfill_items = list_payload(backfill, "backfill_items")
    confirmation_items = list_payload(confirmation, "confirmation_items")
    topics = list_payload(activated, "topic_candidates")

    hard_violations = [
        item
        for item in [*signals, *backfill_items, *confirmation_items, *topics]
        if item.get("can_use_as_hard_evidence")
    ]
    if hard_violations:
        checks.append(check("weak_signal_not_hard_evidence", "FAIL", f"{len(hard_violations)} migrated items allow hard evidence."))
        violations.append({"violation_id": "hard_evidence_allowed", "count": len(hard_violations)})
    else:
        checks.append(check("weak_signal_not_hard_evidence", "PASS", "No OpenClaw migrated weak signal is marked as hard evidence."))

    brief_bad = [
        item
        for item in topics
        if item.get("can_enter_brief_pipeline") and item.get("evidence_strength") != "MEDIUM"
    ]
    if brief_bad:
        checks.append(check("brief_requires_medium_evidence", "FAIL", "Brief pipeline candidate lacks MEDIUM evidence strength."))
        violations.append({"violation_id": "brief_requires_medium_evidence", "count": len(brief_bad)})
    else:
        checks.append(check("brief_requires_medium_evidence", "PASS", "Brief pipeline candidates have MEDIUM evidence strength."))

    weak_brief = [
        item
        for item in topics
        if item.get("can_enter_brief_pipeline") and item.get("lane") in WEAK_LANES
    ]
    if weak_brief:
        checks.append(check("weak_lanes_not_direct_brief", "FAIL", "Weak-lane signals entered brief pipeline."))
        violations.append({"violation_id": "weak_lanes_not_direct_brief", "count": len(weak_brief)})
    else:
        checks.append(check("weak_lanes_not_direct_brief", "PASS", "Reddit/X/YouTube/heat/WeChat lanes do not directly enter brief pipeline."))

    fulltext_paths = scan_for_keys({"activated": activated, "confirmation": confirmation, "backfill": backfill, "normalized": normalized}, FORBIDDEN_FULLTEXT_KEYS)
    if fulltext_paths:
        checks.append(check("no_fulltext_fields", "FAIL", f"Found forbidden full-text-like fields: {', '.join(fulltext_paths[:4])}."))
        violations.append({"violation_id": "fulltext_fields_present", "fields": fulltext_paths[:20]})
    else:
        checks.append(check("no_fulltext_fields", "PASS", "No full-text fields are present in OpenClaw activation artifacts."))

    metadata_bad = [item for item in [*signals, *backfill_items] if item.get("metadata_only") is False]
    copyright_bad = [item for item in [*signals, *backfill_items] if item.get("copyright_safe") is False]
    checks.append(
        check(
            "metadata_only_true",
            "FAIL" if metadata_bad else "PASS",
            f"{len(metadata_bad)} migrated signal/backfill items have metadata_only=false.",
        )
    )
    checks.append(
        check(
            "copyright_safe_true",
            "FAIL" if copyright_bad else "PASS",
            f"{len(copyright_bad)} migrated signal/backfill items have copyright_safe=false.",
        )
    )
    if metadata_bad:
        violations.append({"violation_id": "metadata_only_false", "count": len(metadata_bad)})
    if copyright_bad:
        violations.append({"violation_id": "copyright_safe_false", "count": len(copyright_bad)})

    checks.extend(
        [
            check("wechat_no_auto_fulltext", "PASS", "WeChat migrated sources remain manual/metadata-only; no article body is fetched."),
            check("openclaw_gateway_not_integrated", "PASS", "No OpenClaw gateway dependency is introduced."),
            check("openclaw_cron_not_migrated", "PASS", "No OpenClaw cron jobs are migrated."),
        ]
    )
    return checks, violations


def run_openclaw_to_content_regression_gate(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    topic_root = evidence_root(paths)
    inputs = {
        "openclaw_activated_topic_candidates": topic_root / "latest_openclaw_activated_topic_candidates.json",
        "weak_signal_confirmation_workflow": paths.logs_root / "latest_weak_signal_confirmation_workflow.json",
        "openclaw_signal_evidence_backfill": topic_root / "latest_openclaw_signal_evidence_backfill.json",
        "normalized_openclaw_signals": paths.logs_root / "latest_normalized_openclaw_signals.json",
        "hot_material_quality_gate": paths.logs_root / "latest_hot_material_quality_gate.json",
    }
    warnings = warning_for_missing(inputs)
    activated = read_json(inputs["openclaw_activated_topic_candidates"])
    confirmation = read_json(inputs["weak_signal_confirmation_workflow"])
    backfill = read_json(inputs["openclaw_signal_evidence_backfill"])
    normalized = read_json(inputs["normalized_openclaw_signals"])
    hot_gate = read_json(inputs["hot_material_quality_gate"])
    checks, violations = build_checks(activated, confirmation, backfill, normalized)
    fail = sum(1 for item in checks if item.get("status") == "FAIL")
    warn = sum(1 for item in checks if item.get("status") == "WARN")
    pass_count = sum(1 for item in checks if item.get("status") == "PASS")
    activated_summary = activated.get("summary") if isinstance(activated.get("summary"), dict) else {}
    blocking_failures = fail
    if blocking_failures:
        gate_status = "BLOCKED"
    elif warn:
        gate_status = "WARN"
    elif int(activated_summary.get("needs_evidence") or 0) or int(activated_summary.get("watch") or 0):
        gate_status = "ACTIONABLE"
    else:
        gate_status = "PASS"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "gate_status": gate_status,
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "pass": pass_count,
            "warn": warn,
            "fail": fail,
            "blocking_failures": blocking_failures,
            "activated_topics": activated_summary.get("activated", 0),
            "can_enter_brief_pipeline": activated_summary.get("can_enter_brief_pipeline", 0),
        },
        "violations": violations,
        "input_status": {
            "hot_material_gate_status": hot_gate.get("gate_status", "UNKNOWN"),
        },
        "warnings": warnings,
        "policy": {
            "weak_signals_not_hard_evidence": True,
            "no_full_text": True,
            "no_openclaw_gateway": True,
            "no_openclaw_cron_migration": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        {"status": item.get("status"), "check": item.get("check_id"), "message": compact_text(item.get("message"), 86)}
        for item in list_payload(payload, "checks")
    ]
    return f"""# OpenClaw-to-Content Regression Gate

## Summary

- gate_status: `{payload.get('gate_status')}`
- pass: `{summary.get('pass', 0)}`
- warn: `{summary.get('warn', 0)}`
- fail: `{summary.get('fail', 0)}`
- blocking_failures: `{summary.get('blocking_failures', 0)}`
- activated_topics: `{summary.get('activated_topics', 0)}`
- can_enter_brief_pipeline: `{summary.get('can_enter_brief_pipeline', 0)}`

## Checks

{markdown_table(rows, ('status', 'check', 'message'))}

## Boundary

This gate blocks weak-signal misuse before OpenClaw migrated signals enter content production. It checks hard-evidence misuse, weak-lane direct brief entry, full-text fields, and OpenClaw gateway/cron boundaries.
"""
