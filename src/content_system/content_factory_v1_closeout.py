"""Build the Content Factory v1 closeout report."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, safe_int, today_token, utc_now, write_json_and_markdown


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__content-factory-v1-closeout.json",
        "dated_md": paths.logs_root / f"{run_date}__content-factory-v1-closeout.md",
        "latest_json": paths.logs_root / "latest_content_factory_v1_closeout.json",
        "latest_md": paths.logs_root / "latest_content_factory_v1_closeout.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__content-factory-v1-closeout-board.md",
        "board_latest_md": paths.frontstage_root / "latest_content_factory_v1_closeout_board.md",
    }


def capability_map() -> list[dict[str, str]]:
    return [
        {"phase": "Phase 0-3", "capability": "source health, structured evidence, topic scoring, content production, agent review"},
        {"phase": "Phase 4-8", "capability": "feedback learning, LLM infrastructure, runtime store, cost guard, dry-run publishing"},
        {"phase": "Phase 9-13", "capability": "WeChat workbench, chief editor actions, version review, final candidates, manual publish sessions"},
        {"phase": "Phase 14-18", "capability": "methodology core, methodology generation, live pilots, image planning, WeChat copy packs"},
        {"phase": "Phase 19-21", "capability": "content ops calendar, queue priority, trial protocol, trial records, trial fix pack"},
        {"phase": "Phase 22-24", "capability": "daily ops runner, recurring issue workflow, stable gate, stable trial, quality calibration"},
        {"phase": "Phase 25", "capability": "stable daily ops baseline, operator acceptance, simplified daily command, v1 closeout"},
        {"phase": "Phase 26", "capability": "upstream source coverage audit, hot signal capture, backfill queue, daily hot material pool"},
        {"phase": "Phase 27", "capability": "selected P0 metadata connectors, connector normalization, connector health gate"},
        {"phase": "Phase 28", "capability": "connector evidence enrichment, topic promotion, acquisition-to-content bridge"},
    ]


def build_content_factory_v1_closeout(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    baseline = read_json(paths.logs_root / "latest_stable_daily_ops_baseline.json")
    acceptance = read_json(paths.logs_root / "latest_operator_acceptance_checklist.json")
    stable_ops = read_json(paths.logs_root / "latest_stable_daily_ops.json")
    review = read_json(paths.logs_root / "latest_stable_ops_readiness_review.json")
    quality = read_json(paths.logs_root / "latest_content_quality_calibration.json")
    methodology = read_json(paths.logs_root / "latest_ops_to_methodology_feedback.json")
    evidence = read_json(paths.market_content_root / "03_topic_candidates" / "latest_connector_evidence_packets.json")
    promoted = read_json(paths.market_content_root / "03_topic_candidates" / "latest_connector_promoted_topic_candidates.json")
    bridge = read_json(paths.logs_root / "latest_acquisition_to_content_bridge.json")
    baseline_summary = baseline.get("summary") if isinstance(baseline.get("summary"), dict) else {}
    acceptance_summary = acceptance.get("operator_acceptance_summary") if isinstance(acceptance.get("operator_acceptance_summary"), dict) else {}
    quality_summary = quality.get("summary") if isinstance(quality.get("summary"), dict) else {}
    methodology_summary = methodology.get("summary") if isinstance(methodology.get("summary"), dict) else {}
    evidence_summary = evidence.get("summary") if isinstance(evidence.get("summary"), dict) else {}
    promoted_summary = promoted.get("summary") if isinstance(promoted.get("summary"), dict) else {}
    bridge_summary = bridge.get("summary") if isinstance(bridge.get("summary"), dict) else {}

    blocking = safe_int(baseline_summary.get("blocking_issue_count"))
    baseline_status = str(baseline.get("baseline_status") or "UNKNOWN")
    acceptance_status = str(acceptance.get("acceptance_status") or "UNKNOWN")
    stable_status = str(stable_ops.get("status") or "UNKNOWN")
    if blocking or acceptance_summary.get("fail"):
        v1_status = "NEEDS_FIX"
    elif baseline_status == "READY_FOR_DAILY_OPS" and stable_status == "SUCCESS" and acceptance_status == "ACCEPTABLE_FOR_DAILY_USE":
        v1_status = "CLOSED_READY_FOR_DAILY_OPS"
    elif baseline_status in {"READY_FOR_DAILY_OPS", "ACTIONABLE_WITH_WARNINGS"} and acceptance_status in {"ACCEPTABLE_FOR_DAILY_USE", "ACCEPTABLE_WITH_MANUAL_REVIEW"}:
        v1_status = "CLOSED_WITH_WARNINGS"
    else:
        v1_status = "BLOCKED"

    boundaries = [
        "No automatic publishing.",
        "No WeChat API integration or draft-box creation.",
        "No automatic WeChat backend metric scraping.",
        "No automatic image generation or image model call.",
        "No real image files committed to Git.",
        "No automatic prompt/config/rule mutation.",
        "No mainline article overwrite.",
        "Live mode remains explicitly gated by env, allowlist, key, and cost guard.",
    ]
    known_limitations = [
        f"ready_to_publish remains {((baseline.get('content_quality_status') or {}) if isinstance(baseline.get('content_quality_status'), dict) else {}).get('ready_to_publish', 0)}; content quality still needs human review.",
        f"{quality_summary.get('publish_blocking_quality_issues', 0)} publish-blocking quality issue(s) are currently visible.",
        f"{methodology_summary.get('feedback_count', 0)} methodology feedback item(s) are advisory and not auto-applied.",
        "Manual publishing sessions and post-publish metrics remain operator-entered.",
        "Connector evidence is metadata-derived and still needs human/source review before full article production.",
    ]
    next_phase = [
        "Phase 29：OpenClaw Source Migration & Signal Lane Integration v1",
        "P29-001：OpenClaw Source Inventory Import",
        "P29-002：OpenClaw Source Risk Classification",
        "P29-003：P0/P1 Migration Plan",
        "P29-004：Reddit / YC / TechCrunch / FinSMEs / Newsletter / Chinese Media Metadata Connector",
        "P29-005：Weak Signal Safety Gate",
    ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "v1_status": v1_status,
        "capability_map": capability_map(),
        "daily_use": {
            "recommended_command": "make stable-daily-ops",
            "workbench_entry": "同行资本市场内容系统/11_frontstage/latest_wechat_workbench.html",
            "operator_review_required": True,
            "stable_daily_ops_status": stable_status,
            "baseline_status": baseline_status,
            "operator_acceptance_status": acceptance_status,
        },
        "main_workflow": [
            "Collect sources and evidence.",
            "Score topics and generate methodology-aware content.",
            "Review, rewrite, and promote candidates with human approval.",
            "Prepare WeChat copy pack and visual slots.",
            "Run content ops queue, calendar, trial readiness, and stable daily ops.",
            "Human operator decides any real publishing action.",
        ],
        "content_quality_status": quality_summary,
        "methodology_feedback_status": methodology_summary,
        "acquisition_to_content_status": {
            "evidence_packet_count": evidence_summary.get("packet_count", 0),
            "eligible_for_topic_promotion": evidence_summary.get("eligible_for_topic_promotion", 0),
            "promoted_topic_count": promoted_summary.get("promoted", 0),
            "ready_for_brief": bridge_summary.get("ready_for_brief", 0),
            "needs_evidence": bridge_summary.get("needs_evidence", 0),
        },
        "stable_ops_readiness": {
            "readiness_status": review.get("readiness_status", "UNKNOWN"),
            "summary": review.get("summary") if isinstance(review.get("summary"), dict) else {},
        },
        "boundaries": boundaries,
        "known_limitations": known_limitations,
        "next_phase_recommendations": next_phase,
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    daily = payload.get("daily_use") if isinstance(payload.get("daily_use"), dict) else {}
    capabilities = "\n".join(f"- {item.get('phase')}: {item.get('capability')}" for item in payload.get("capability_map", []))
    workflow = "\n".join(f"{idx}. {item}" for idx, item in enumerate(payload.get("main_workflow", []), 1))
    boundaries = "\n".join(f"- {item}" for item in payload.get("boundaries", []))
    limitations = "\n".join(f"- {item}" for item in payload.get("known_limitations", []))
    next_phase = "\n".join(f"- {item}" for item in payload.get("next_phase_recommendations", []))
    acquisition = payload.get("acquisition_to_content_status") if isinstance(payload.get("acquisition_to_content_status"), dict) else {}
    return f"""# Content Factory v1 Closeout

## Status

- v1_status: `{payload.get('v1_status')}`
- recommended_command: `{daily.get('recommended_command')}`
- workbench_entry: `{daily.get('workbench_entry')}`
- operator_review_required: `{daily.get('operator_review_required')}`
- stable_daily_ops_status: `{daily.get('stable_daily_ops_status')}`

## Capability Map

{capabilities}

## Main Workflow

{workflow}

## Acquisition to Content

- evidence_packet_count: `{acquisition.get('evidence_packet_count', 0)}`
- eligible_for_topic_promotion: `{acquisition.get('eligible_for_topic_promotion', 0)}`
- promoted_topic_count: `{acquisition.get('promoted_topic_count', 0)}`
- ready_for_brief: `{acquisition.get('ready_for_brief', 0)}`
- needs_evidence: `{acquisition.get('needs_evidence', 0)}`

## Boundaries

{boundaries}

## Known Limitations

{limitations}

## Next Phase

{next_phase}
"""
