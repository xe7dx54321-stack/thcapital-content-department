"""Human Exception Queue v1 for rule-based agent review outputs."""

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
class HumanException:
    schema_version: str
    exception_id: str
    review_item_id: str
    package_id: str
    run_date: str
    reason: str
    urgency: str
    estimated_review_minutes: int
    recommended_human_action: str
    context_summary: str
    key_questions_for_human: tuple[str, ...]
    links: dict[str, str]


@dataclass(frozen=True)
class HumanExceptionQueueReport:
    schema_version: str
    generated_at: str
    run_date: str
    exception_count: int
    total_estimated_review_minutes: int
    exceptions: tuple[HumanException, ...]
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


def should_escalate(decision: dict[str, Any], item: dict[str, Any]) -> tuple[bool, str]:
    decision_value = str(decision.get("decision") or "")
    confidence = safe_float(decision.get("confidence"))
    quality_score = safe_float(item.get("quality_score"))
    quality_status = str(item.get("quality_status") or "")
    evidence_count = len(item.get("evidence_ids", []) or [])
    publish_status = str(item.get("publish_status") or "")
    priority = str(item.get("priority") or "")
    risk_level = str(item.get("risk_level") or "")

    if decision_value == "ESCALATE_TO_HUMAN":
        return True, str(decision.get("human_escalation_reason") or decision.get("reasoning") or "Judge gate escalated this item.")
    if priority == "HIGH" and risk_level == "HIGH":
        return True, "High-priority item still has HIGH risk after agent review."
    if confidence and confidence < 0.65:
        return True, "Judge confidence is below 0.65."
    if quality_status == "READY_FOR_HUMAN_REVIEW" and 75 <= quality_score <= 82:
        return True, "Quality score is near the publish threshold."
    if quality_status == "READY_FOR_HUMAN_REVIEW" and publish_status == "READY_FOR_HUMAN_REVIEW" and evidence_count < 2:
        return True, "Publish-ready item has fewer than two evidence items."
    return False, ""


def urgency_for(reason: str, item: dict[str, Any]) -> str:
    if item.get("priority") == "HIGH" or "HIGH risk" in reason:
        return "HIGH"
    if "threshold" in reason or "confidence" in reason:
        return "MEDIUM"
    return "LOW"


def action_for(decision: dict[str, Any], reason: str) -> str:
    if str(decision.get("decision")) == "ESCALATE_TO_HUMAN":
        return "decide_angle"
    if "threshold" in reason:
        return "approve"
    if "evidence" in reason.lower():
        return "request_revision"
    return "request_revision"


def build_exception(
    decision: dict[str, Any],
    item: dict[str, Any],
    package: dict[str, Any],
    revision: dict[str, Any],
    run_date: str,
) -> HumanException:
    escalate, reason = should_escalate(decision, item)
    if not escalate:
        raise ValueError("build_exception called for non-escalated item")
    urgency = urgency_for(reason, item)
    minutes = {"HIGH": 8, "MEDIUM": 5, "LOW": 3}[urgency]
    title = str((package.get("wechat") or {}).get("title") or item.get("title") or decision.get("package_id") or "")
    return HumanException(
        schema_version=SCHEMA_VERSION,
        exception_id=make_id("hex", run_date, str(decision.get("review_item_id") or "")),
        review_item_id=str(decision.get("review_item_id") or ""),
        package_id=str(decision.get("package_id") or ""),
        run_date=run_date,
        reason=reason,
        urgency=urgency,
        estimated_review_minutes=minutes,
        recommended_human_action=action_for(decision, reason),
        context_summary=f"{title} needs human attention because: {reason}",
        key_questions_for_human=(
            "Is the core angle worth keeping for this audience?",
            "Is the evidence strong enough for the claim?",
            "Should this proceed, be revised, or be held?",
        ),
        links={
            "platform_package": str(package.get("package_id") or decision.get("package_id") or ""),
            "judge_decision": str(decision.get("judge_decision_id") or ""),
            "revision_instruction": str(revision.get("revision_id") or ""),
        },
    )


def build_human_exception_queue_report(paths: ProjectPaths) -> HumanExceptionQueueReport:
    root = paths.market_content_root / "06_review_queue"
    draft_root = paths.market_content_root / "05_draft_packs"
    judge = read_json(root / "latest_judge_gate.json")
    decisions = [item for item in judge.get("decisions", []) if isinstance(item, dict)] if isinstance(judge.get("decisions"), list) else []
    items = load_by_key(root / "latest_agent_review_queue.json", "items", "review_item_id")
    revisions = load_by_key(root / "latest_revision_instructions.json", "instructions", "review_item_id")
    packages = load_by_key(draft_root / "latest_platform_packages.json", "packages", "package_id")
    run_date = str(judge.get("run_date") or datetime.now().strftime("%Y%m%d")).replace("-", "")[:8]

    exceptions: list[HumanException] = []
    for decision in decisions:
        item = items.get(str(decision.get("review_item_id")), {})
        should_add, _reason = should_escalate(decision, item)
        if should_add:
            exceptions.append(
                build_exception(
                    decision,
                    item,
                    packages.get(str(decision.get("package_id")), {}),
                    revisions.get(str(decision.get("review_item_id")), {}),
                    run_date,
                )
            )
    warnings = () if decisions else ("No judge decisions available.",)
    return HumanExceptionQueueReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date,
        exception_count=len(exceptions),
        total_estimated_review_minutes=sum(item.estimated_review_minutes for item in exceptions),
        exceptions=tuple(exceptions),
        warnings=warnings,
    )


def report_to_dict(report: HumanExceptionQueueReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: HumanExceptionQueueReport) -> str:
    rows = [
        f"| {idx} | {item.urgency} | {item.estimated_review_minutes} | {item.recommended_human_action} | {item.package_id} | {escape_cell(item.reason)} |"
        for idx, item in enumerate(report.exceptions, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Human Exception Queue v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Human exceptions: `{report.exception_count}`
- Estimated review minutes: `{report.total_estimated_review_minutes}`

## Exceptions

| # | Urgency | Minutes | Recommended Action | Package | Reason |
|---:|---|---:|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | 0 | - | - | None |'}

## Policy

- This queue is intentionally sparse.
- Routine `NEEDS_REVISION` items stay in agent revision flow.
- Only high-risk, high-value, low-confidence, or threshold cases are sent to human review.

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "06_review_queue"
    return {
        "dated_json": root / f"{run_date}__human-exception-queue.json",
        "dated_md": root / f"{run_date}__human-exception-queue.md",
        "latest_json": root / "latest_human_exception_queue.json",
        "latest_md": root / "latest_human_exception_queue.md",
    }


def write_human_exception_queue_report(report: HumanExceptionQueueReport, paths: ProjectPaths) -> dict[str, Path]:
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
