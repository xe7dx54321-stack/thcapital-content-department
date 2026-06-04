"""Promote human-approved live rewrite sidecars into candidate rewrite versions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.approved_live_output_promotion import APPROVABLE_DECISIONS, by_key
from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "dated_json": root / f"{run_date}__promoted-live-rewrite-versions.json",
        "dated_md": root / f"{run_date}__promoted-live-rewrite-versions.md",
        "latest_json": root / "latest_promoted_live_rewrite_versions.json",
        "latest_md": root / "latest_promoted_live_rewrite_versions.md",
    }


def build_promotions(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    rewrite_payload = read_json(versions_root / "latest_live_methodology_rewrite_pilot.json")
    comparison_payload = read_json(paths.logs_root / "latest_live_output_quality_comparison.json")
    calibration_payload = read_json(paths.logs_root / "latest_live_calibration_feedback.json")
    rewrites = by_key(list_payload(rewrite_payload, "rewrites"), "live_rewrite_id")
    feedback_by_comparison = by_key(list_payload(calibration_payload, "feedback"), "comparison_id")
    versions: list[dict[str, Any]] = []
    skipped = 0
    for comparison in list_payload(comparison_payload, "comparisons"):
        if comparison.get("comparison_type") != "rewrite":
            continue
        feedback = feedback_by_comparison.get(str(comparison.get("comparison_id") or ""), {})
        decision = str(feedback.get("decision") or "")
        live_rewrite_id = str(comparison.get("live_output_id") or "")
        rewrite = rewrites.get(live_rewrite_id)
        if decision not in APPROVABLE_DECISIONS or not rewrite:
            skipped += 1
            continue
        versions.append(
            {
                "version_id": make_id("plrew", run_date, live_rewrite_id, comparison.get("comparison_id")),
                "source_live_rewrite_id": live_rewrite_id,
                "source_article_id": rewrite.get("source_article_id") or "",
                "source_action_id": rewrite.get("source_action_id") or "",
                "comparison_id": comparison.get("comparison_id") or "",
                "calibration_decision": decision,
                "new_title": rewrite.get("new_title") or "",
                "new_opening": rewrite.get("new_opening") or "",
                "new_body_markdown": rewrite.get("new_body_markdown") or "",
                "methodology_issues_addressed": rewrite.get("methodology_issues_addressed") or [],
                "promotion_reason": feedback.get("human_note") or f"Human calibration decision is {decision}; promote as candidate rewrite sidecar.",
                "do_not_overwrite_original": True,
                "do_not_publish": True,
                "status": "PROMOTED",
            }
        )
    summary = {"version_count": len(versions), "promoted": len(versions), "skipped": skipped}
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "versions": versions,
        "summary": summary,
        "policy": {"sidecar_only": True, "do_not_overwrite_original": True, "do_not_publish": True},
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('version_id')}` | `{item.get('source_live_rewrite_id')}` | `{item.get('source_article_id')}` | `{item.get('calibration_decision')}` | `{item.get('status')}` |"
        for item in list_payload(payload, "versions")
    ) or "| - | - | - | - | No promoted live rewrite versions |"
    return f"""# Promoted Live Rewrite Versions

## Summary

- version_count: `{summary.get('version_count', 0)}`
- promoted: `{summary.get('promoted', 0)}`
- skipped: `{summary.get('skipped', 0)}`
- do_not_overwrite_original: `true`
- do_not_publish: `true`

| Version | Source Live Rewrite | Article | Calibration | Status |
|---|---|---|---|---|
{rows}
"""
