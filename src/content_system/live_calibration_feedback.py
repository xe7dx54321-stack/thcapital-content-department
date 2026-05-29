"""Human calibration feedback for Phase 16 live pilot comparisons."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION, make_id
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__live-calibration-feedback.json",
        "dated_md": paths.logs_root / f"{run_date}__live-calibration-feedback.md",
        "latest_json": paths.logs_root / "latest_live_calibration_feedback.json",
        "latest_md": paths.logs_root / "latest_live_calibration_feedback.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__live-calibration-board.md",
        "board_latest_md": paths.frontstage_root / "latest_live_calibration_board.md",
    }


def summary_for(feedback: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "feedback_count": len(feedback),
        "accept_live": sum(1 for item in feedback if item.get("decision") == "ACCEPT_LIVE"),
        "reject_live": sum(1 for item in feedback if item.get("decision") == "REJECT_LIVE"),
        "merge": sum(1 for item in feedback if item.get("decision") == "MERGE"),
        "defer": sum(1 for item in feedback if item.get("decision") == "DEFER"),
    }


def build_payload(paths: ProjectPaths) -> dict[str, Any]:
    run_date = today_token()
    existing = read_json(paths.logs_root / "latest_live_calibration_feedback.json")
    feedback = list_payload(existing, "feedback")
    comparison_payload = read_json(paths.logs_root / "latest_live_output_quality_comparison.json")
    comparisons = list_payload(comparison_payload, "comparisons")
    known_ids = {str(item.get("comparison_id")) for item in feedback}
    for comparison in comparisons:
        comparison_id = str(comparison.get("comparison_id") or "")
        if comparison_id and comparison_id not in known_ids:
            feedback.append(
                {
                    "feedback_id": make_id("lcf", run_date, comparison_id),
                    "comparison_id": comparison_id,
                    "decision": "DEFER",
                    "human_note": "",
                    "suggested_prompt_adjustment": "",
                    "suggested_methodology_adjustment": "",
                    "auto_apply": False,
                }
            )
    return {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "feedback": feedback, "summary": summary_for(feedback), "policy": {"auto_apply": False}}


def update_feedback(paths: ProjectPaths, comparison_id: str, decision: str, note: str) -> tuple[dict[str, Any], dict[str, Path]]:
    payload = build_payload(paths)
    run_date = str(payload.get("run_date") or today_token())
    feedback = list_payload(payload, "feedback")
    matched = False
    for item in feedback:
        if item.get("comparison_id") == comparison_id:
            item["decision"] = decision
            item["human_note"] = note
            matched = True
    if not matched:
        feedback.append(
            {
                "feedback_id": make_id("lcf", run_date, comparison_id),
                "comparison_id": comparison_id,
                "decision": decision,
                "human_note": note,
                "suggested_prompt_adjustment": "",
                "suggested_methodology_adjustment": "",
                "auto_apply": False,
            }
        )
    payload["feedback"] = feedback
    payload["summary"] = summary_for(feedback)
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def build_live_calibration_board(paths: ProjectPaths) -> tuple[dict[str, Any], dict[str, Path]]:
    payload = build_payload(paths)
    run_date = str(payload.get("run_date") or today_token())
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    def escape_cell(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    rows = "\n".join(
        f"| `{item.get('feedback_id')}` | `{item.get('comparison_id')}` | `{item.get('decision')}` | {escape_cell(item.get('human_note') or '')} |"
        for item in list_payload(payload, "feedback")
    ) or "| - | - | - | - |"
    return f"""# Live Calibration Board

## Summary

- feedback_count: `{summary.get('feedback_count', 0)}`
- accept_live: `{summary.get('accept_live', 0)}`
- reject_live: `{summary.get('reject_live', 0)}`
- merge: `{summary.get('merge', 0)}`
- defer: `{summary.get('defer', 0)}`
- auto_apply: `false`

| Feedback | Comparison | Decision | Note |
|---|---|---|---|
{rows}
"""
