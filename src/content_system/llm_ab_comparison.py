"""LLM Agent A/B comparison reports for Phase 7."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, safe_int, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class LLMABComparisonReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    summary: dict[str, Any]
    decision_conflicts: tuple[dict[str, Any], ...]
    critic_differences: tuple[dict[str, Any], ...]
    human_spot_check_items: tuple[dict[str, Any], ...]
    warnings: tuple[str, ...]


def by_key(items: list[dict[str, Any]], field: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(field)): item for item in items if item.get(field)}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__llm-ab-comparison.json",
        "dated_md": paths.logs_root / f"{run_date}__llm-ab-comparison.md",
        "latest_json": paths.logs_root / "latest_llm_ab_comparison.json",
        "latest_md": paths.logs_root / "latest_llm_ab_comparison.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__llm-ab-comparison-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_llm_ab_comparison_board.md",
    }


def build_llm_ab_comparison_report(paths: ProjectPaths) -> LLMABComparisonReport:
    review_root = paths.market_content_root / "06_review_queue"
    log_root = paths.logs_root
    rule_critic = by_key(list_payload(read_json(review_root / "latest_critic_reviews.json"), "reviews"), "review_item_id")
    rule_judge = by_key(list_payload(read_json(review_root / "latest_judge_gate.json"), "decisions"), "review_item_id")
    llm_critic = by_key(list_payload(read_json(review_root / "latest_llm_critic_reviews.json"), "reviews"), "review_item_id")
    llm_judge = by_key(list_payload(read_json(review_root / "latest_llm_judge_gate.json"), "decisions"), "review_item_id")
    llm_prop = list_payload(read_json(review_root / "latest_llm_proponent_reviews.json"), "reviews")
    rewrite = list_payload(read_json(paths.market_content_root / "05_draft_packs" / "latest_llm_rewrite_suggestions.json"), "suggestions")
    run_summary = read_json(log_root / "latest_agent_run_summary.json")
    eval_template = read_json(paths.market_content_root / "07_publishing" / "latest_agent_evaluation_template.json")
    run_date = str(read_json(log_root / "latest_phase6_daily_agent_pipeline.json").get("run_date") or today_token()).replace("-", "")[:8]
    warnings: list[str] = []
    if not rule_judge:
        warnings.append("Rule judge artifact is missing or empty.")
    if not llm_judge:
        warnings.append("LLM judge artifact is missing or empty.")

    decision_conflicts: list[dict[str, Any]] = []
    matched_decisions = 0
    compared_decisions = 0
    human_spot_checks: list[dict[str, Any]] = []
    for review_item_id, llm_item in llm_judge.items():
        rule_item = rule_judge.get(review_item_id, {})
        if not rule_item:
            continue
        compared_decisions += 1
        rule_decision = str(rule_item.get("decision") or "")
        llm_decision = str(llm_item.get("decision") or "")
        comparison = llm_item.get("comparison_to_rule_judge") if isinstance(llm_item.get("comparison_to_rule_judge"), dict) else {}
        matches = rule_decision == llm_decision or bool(comparison.get("matches_rule_decision"))
        if matches:
            matched_decisions += 1
        else:
            conflict = {
                "review_item_id": review_item_id,
                "package_id": llm_item.get("package_id", ""),
                "rule_decision": rule_decision,
                "llm_decision": llm_decision,
                "reason": comparison.get("difference_reason") or "Rule judge and LLM judge differ.",
            }
            decision_conflicts.append(conflict)
            human_spot_checks.append(conflict)
        if comparison.get("requires_human_spot_check"):
            human_spot_checks.append(
                {
                    "review_item_id": review_item_id,
                    "package_id": llm_item.get("package_id", ""),
                    "rule_decision": rule_decision,
                    "llm_decision": llm_decision,
                    "reason": "LLM judge requested human spot check.",
                }
            )

    severity_order = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    critic_differences: list[dict[str, Any]] = []
    for review_item_id, llm_item in llm_critic.items():
        rule_item = rule_critic.get(review_item_id, {})
        if not rule_item:
            continue
        rule_severity = str(rule_item.get("severity") or "")
        llm_severity = str(llm_item.get("severity") or "")
        delta = severity_order.get(llm_severity, 0) - severity_order.get(rule_severity, 0)
        if delta:
            critic_differences.append(
                {
                    "review_item_id": review_item_id,
                    "package_id": llm_item.get("package_id", ""),
                    "rule_severity": rule_severity,
                    "llm_severity": llm_severity,
                    "severity_delta": delta,
                }
            )

    all_llm_items = [*llm_prop, *llm_critic.values(), *llm_judge.values(), *rewrite]
    live_attempted = sum(1 for item in all_llm_items if item.get("live_call_attempted"))
    live_succeeded = sum(1 for item in all_llm_items if item.get("live_call_succeeded"))
    fallback_count = sum(1 for item in all_llm_items if item.get("fallback_used"))
    run_summary_payload = run_summary.get("summary") if isinstance(run_summary.get("summary"), dict) else {}
    decision_match_rate = round(matched_decisions / compared_decisions, 4) if compared_decisions else 0.0
    summary = {
        "rule_vs_llm_decision_compared": compared_decisions,
        "rule_vs_llm_decision_match_count": matched_decisions,
        "rule_vs_llm_decision_match_rate": decision_match_rate,
        "critic_severity_difference_count": len(critic_differences),
        "judge_decision_conflict_count": len(decision_conflicts),
        "rewrite_suggestion_count": len(rewrite),
        "live_attempted_count": live_attempted,
        "live_succeeded_count": live_succeeded,
        "fallback_count": fallback_count,
        "estimated_cost_usd": safe_float(run_summary_payload.get("estimated_cost_usd")),
        "agent_evaluation_count": safe_int(eval_template.get("evaluation_count")),
        "human_spot_check_count": len(human_spot_checks),
        "llm_item_status_distribution": dict(Counter(str(item.get("json_parse_status") or "UNKNOWN") for item in all_llm_items)),
    }
    status = "DEGRADED" if warnings or decision_conflicts else "SUCCESS"
    return LLMABComparisonReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date,
        status=status,
        summary=summary,
        decision_conflicts=tuple(decision_conflicts),
        critic_differences=tuple(critic_differences),
        human_spot_check_items=tuple(human_spot_checks),
        warnings=tuple(warnings),
    )


def render_markdown(report: LLMABComparisonReport) -> str:
    conflicts = "\n".join(
        f"- `{item.get('review_item_id')}`: rule `{item.get('rule_decision')}` vs LLM `{item.get('llm_decision')}` - {item.get('reason')}"
        for item in report.decision_conflicts
    ) or "- None"
    critic_rows = "\n".join(
        f"| {item.get('review_item_id')} | {item.get('rule_severity')} | {item.get('llm_severity')} | {item.get('severity_delta')} |"
        for item in report.critic_differences
    ) or "| - | - | - | 0 |"
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# LLM A/B Comparison v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**
- Decision match rate: `{report.summary.get('rule_vs_llm_decision_match_rate')}`
- Judge conflicts: `{report.summary.get('judge_decision_conflict_count')}`
- Critic severity differences: `{report.summary.get('critic_severity_difference_count')}`
- Rewrite suggestions: `{report.summary.get('rewrite_suggestion_count')}`
- Live attempted: `{report.summary.get('live_attempted_count')}`
- Live succeeded: `{report.summary.get('live_succeeded_count')}`
- Fallback count: `{report.summary.get('fallback_count')}`
- Estimated cost USD: `{report.summary.get('estimated_cost_usd')}`
- Human spot-check items: `{report.summary.get('human_spot_check_count')}`

## Judge Conflicts

{conflicts}

## Critic Severity Differences

| Review Item | Rule Severity | LLM Severity | Delta |
|---|---|---|---:|
{critic_rows}

## Warnings

{warnings}
"""


def write_llm_ab_comparison_report(report: LLMABComparisonReport, paths: ProjectPaths) -> dict[str, Path]:
    outputs = output_paths(paths, report.run_date)
    payload = asdict(report)
    markdown = render_markdown(report)
    return write_json_and_markdown(payload, markdown, outputs)


def report_to_dict(report: LLMABComparisonReport) -> dict[str, Any]:
    return asdict(report)
