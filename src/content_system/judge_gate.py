"""Rule-based third-party judge gate for Phase 3."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class JudgeDecision:
    schema_version: str
    judge_decision_id: str
    review_item_id: str
    package_id: str
    run_date: str
    agent_role: str
    decision: str
    decision_score: float
    confidence: float
    reasoning: str
    approval_conditions: tuple[str, ...]
    required_revisions: tuple[str, ...]
    human_escalation_reason: str
    risk_level: str
    release_readiness: str
    next_action: str


@dataclass(frozen=True)
class JudgeGateReport:
    schema_version: str
    generated_at: str
    run_date: str
    decision_count: int
    decision_distribution: dict[str, int]
    decisions: tuple[JudgeDecision, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def make_id(prefix: str, run_date: str, *parts: str) -> str:
    digest = hashlib.sha1("|".join((run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def load_by_key(path: Path, key: str, id_field: str) -> dict[str, dict[str, Any]]:
    payload = read_json(path)
    raw = payload.get(key)
    if not isinstance(raw, list):
        return {}
    return {str(item.get(id_field)): item for item in raw if isinstance(item, dict)}


def decision_score(item: dict[str, Any], prop: dict[str, Any], critic: dict[str, Any]) -> float:
    score = safe_float(item.get("quality_score"))
    support = str(prop.get("support_level") or "WEAK")
    severity = str(critic.get("severity") or "HIGH")
    score += {"STRONG": 8, "MODERATE": 3, "WEAK": -8}.get(support, -5)
    score += {"LOW": 8, "MEDIUM": -4, "HIGH": -16}.get(severity, -10)
    if item.get("risk_level") == "LOW":
        score += 5
    elif item.get("risk_level") == "HIGH":
        score -= 10
    return round(max(0.0, min(100.0, score)), 2)


def classify(item: dict[str, Any], prop: dict[str, Any], critic: dict[str, Any], score: float) -> tuple[str, str, str, str]:
    quality = safe_float(item.get("quality_score"))
    quality_status = str(item.get("quality_status") or "")
    support = str(prop.get("support_level") or "WEAK")
    severity = str(critic.get("severity") or "HIGH")
    risk = str(item.get("risk_level") or "HIGH")
    publish = str(item.get("publish_status") or "NOT_READY")
    evidence_count = len(item.get("evidence_ids", []) or [])
    priority = str(item.get("priority") or "LOW")

    if quality < 50 or publish == "HOLD" or not item.get("source_ids") or not item.get("evidence_ids"):
        return "HOLD", "BLOCKED", "hold", "Missing core readiness signals."
    if priority == "HIGH" and severity == "HIGH":
        return "ESCALATE_TO_HUMAN", "NOT_READY", "manual_decision", "High-priority item has high critic severity."
    if quality_status == "READY_FOR_HUMAN_REVIEW" and 75 <= quality <= 82:
        return "ESCALATE_TO_HUMAN", "NOT_READY", "manual_decision", "Quality score is near the publish threshold."
    if quality_status == "READY_FOR_HUMAN_REVIEW" and publish == "READY_FOR_HUMAN_REVIEW" and evidence_count < 2:
        return "ESCALATE_TO_HUMAN", "NOT_READY", "manual_decision", "Publish-ready item has fewer than two evidence items."
    if quality >= 80 and severity == "LOW" and support == "STRONG" and risk == "LOW":
        return "APPROVED_FOR_QUEUE", "READY", "send_to_human_spot_check", "Strong proponent support, low critic severity, and low risk."
    if quality >= 65 and severity in {"MEDIUM", "LOW"}:
        return "NEEDS_REVISION", "NOT_READY", "revise", "Item is viable but requires targeted revision."
    return "HOLD", "BLOCKED", "hold", "Quality and critic signals are not sufficient."


def build_decision(item: dict[str, Any], prop: dict[str, Any], critic: dict[str, Any], run_date: str) -> JudgeDecision:
    score = decision_score(item, prop, critic)
    decision, readiness, next_action, reason = classify(item, prop, critic, score)
    required = tuple(str(x) for x in critic.get("must_fix_before_publish", []) if x)
    conditions = ("Human spot check still required before publication.",) if decision == "APPROVED_FOR_QUEUE" else ()
    confidence = round(min(0.95, (safe_float(prop.get("confidence")) + safe_float(critic.get("confidence"))) / 2 or 0.55), 2)
    if decision == "ESCALATE_TO_HUMAN":
        confidence = min(confidence, 0.72)
    return JudgeDecision(
        schema_version=SCHEMA_VERSION,
        judge_decision_id=make_id("judge", run_date, str(item.get("review_item_id") or "")),
        review_item_id=str(item.get("review_item_id") or ""),
        package_id=str(item.get("package_id") or ""),
        run_date=run_date,
        agent_role="third_party_judge",
        decision=decision,
        decision_score=score,
        confidence=confidence,
        reasoning=reason,
        approval_conditions=conditions,
        required_revisions=required,
        human_escalation_reason=reason if decision == "ESCALATE_TO_HUMAN" else "",
        risk_level=str(item.get("risk_level") or "HIGH"),
        release_readiness=readiness,
        next_action=next_action,
    )


def build_judge_gate_report(paths: ProjectPaths) -> JudgeGateReport:
    root = paths.market_content_root / "06_review_queue"
    queue = read_json(root / "latest_agent_review_queue.json")
    items = [item for item in queue.get("items", []) if isinstance(item, dict)] if isinstance(queue.get("items"), list) else []
    props = load_by_key(root / "latest_proponent_reviews.json", "reviews", "review_item_id")
    critics = load_by_key(root / "latest_critic_reviews.json", "reviews", "review_item_id")
    run_date = str(queue.get("run_date") or datetime.now().strftime("%Y%m%d")).replace("-", "")[:8]
    decisions = tuple(build_decision(item, props.get(str(item.get("review_item_id")), {}), critics.get(str(item.get("review_item_id")), {}), run_date) for item in items)
    distribution: dict[str, int] = {}
    for decision in decisions:
        distribution[decision.decision] = distribution.get(decision.decision, 0) + 1
    warnings = () if items else ("No review queue items available.",)
    return JudgeGateReport(SCHEMA_VERSION, utc_now(), run_date, len(decisions), dict(sorted(distribution.items())), decisions, warnings)


def report_to_dict(report: JudgeGateReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: JudgeGateReport) -> str:
    rows = [
        f"| {idx} | {d.decision} | {d.decision_score:.2f} | {d.confidence:.2f} | {d.risk_level} | {d.next_action} | {escape_cell(d.reasoning)} |"
        for idx, d in enumerate(report.decisions, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Judge Gate v1

> Rule-based third-party judge simulation.

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Decisions: `{report.decision_count}`
- Distribution: `{report.decision_distribution}`

## Decisions

| # | Decision | Score | Confidence | Risk | Next Action | Reasoning |
|---:|---|---:|---:|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | 0 | 0 | - | - | None |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "06_review_queue"
    return {
        "dated_json": root / f"{run_date}__judge-gate.json",
        "dated_md": root / f"{run_date}__judge-gate.md",
        "latest_json": root / "latest_judge_gate.json",
        "latest_md": root / "latest_judge_gate.md",
    }


def write_judge_gate_report(report: JudgeGateReport, paths: ProjectPaths) -> dict[str, Path]:
    paths_by_name = output_paths(paths, report.run_date)
    for path in paths_by_name.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (paths_by_name["dated_json"], paths_by_name["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (paths_by_name["dated_md"], paths_by_name["latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return paths_by_name
