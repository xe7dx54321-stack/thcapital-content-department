"""Revision Instruction Builder v1."""

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
class RevisionInstruction:
    schema_version: str
    revision_id: str
    review_item_id: str
    package_id: str
    run_date: str
    revision_priority: str
    title_fixes: tuple[str, ...]
    opening_fixes: tuple[str, ...]
    logic_fixes: tuple[str, ...]
    evidence_fixes: tuple[str, ...]
    risk_fixes: tuple[str, ...]
    platform_fixes: dict[str, tuple[str, ...]]
    suggested_editor_prompt: str
    human_note: str
    next_action: str


@dataclass(frozen=True)
class RevisionInstructionReport:
    schema_version: str
    generated_at: str
    run_date: str
    revision_count: int
    instructions: tuple[RevisionInstruction, ...]
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


def load_by_key(path: Path, key: str, id_field: str) -> dict[str, dict[str, Any]]:
    payload = read_json(path)
    raw = payload.get(key)
    if not isinstance(raw, list):
        return {}
    return {str(item.get(id_field)): item for item in raw if isinstance(item, dict)}


def priority_for(decision: dict[str, Any], critic: dict[str, Any]) -> str:
    if decision.get("decision") == "ESCALATE_TO_HUMAN" or critic.get("severity") == "HIGH":
        return "HIGH"
    if decision.get("decision") == "NEEDS_REVISION":
        return "MEDIUM"
    return "LOW"


def build_instruction(decision: dict[str, Any], critic: dict[str, Any], package: dict[str, Any], draft: dict[str, Any], run_date: str) -> RevisionInstruction:
    priority = priority_for(decision, critic)
    must_fix = [str(item) for item in critic.get("must_fix_before_publish", []) if item]
    title_fixes = [item for item in must_fix if "title" in item.lower()] or ["Make the title concrete, evidence-bounded, and less promotional."]
    evidence_fixes = [item for item in must_fix if "evidence" in item.lower() or "source" in item.lower()]
    risk_fixes = [item for item in must_fix if "risk" in item.lower() or "wording" in item.lower()]
    logic_fixes = [str(item) for item in critic.get("logic_concerns", []) if item]
    platform_fixes = {
        "wechat": tuple(["Strengthen section transitions and separate facts from interpretation."]),
        "xiaohongshu": tuple(["Keep the takeaways concise and avoid overclaiming."]),
    }
    next_action = "human_review" if decision.get("decision") == "ESCALATE_TO_HUMAN" else "agent_revise"
    if decision.get("decision") == "HOLD":
        next_action = "hold"
    title = (package.get("wechat") or {}).get("title") or draft.get("recommended_title") or decision.get("package_id")
    return RevisionInstruction(
        schema_version=SCHEMA_VERSION,
        revision_id=make_id("rev", run_date, str(decision.get("review_item_id") or "")),
        review_item_id=str(decision.get("review_item_id") or ""),
        package_id=str(decision.get("package_id") or ""),
        run_date=run_date,
        revision_priority=priority,
        title_fixes=tuple(dict.fromkeys(title_fixes)),
        opening_fixes=("Clarify what happened in the first paragraph before adding interpretation.",),
        logic_fixes=tuple(dict.fromkeys(logic_fixes or ["Make the causal chain explicit: fact -> implication -> risk."])),
        evidence_fixes=tuple(dict.fromkeys(evidence_fixes or ["Check all evidence links and add independent confirmation if evidence count is low."])),
        risk_fixes=tuple(dict.fromkeys(risk_fixes or ["Keep risk disclosure visible and avoid guaranteed outcomes."])),
        platform_fixes=platform_fixes,
        suggested_editor_prompt=f"Revise `{title}` using the judge decision and critic concerns. Preserve evidence links, reduce overclaiming, and keep human review notes visible.",
        human_note=str(decision.get("human_escalation_reason") or ""),
        next_action=next_action,
    )


def build_revision_instruction_report(paths: ProjectPaths) -> RevisionInstructionReport:
    root = paths.market_content_root / "06_review_queue"
    draft_root = paths.market_content_root / "05_draft_packs"
    judge = read_json(root / "latest_judge_gate.json")
    decisions = [item for item in judge.get("decisions", []) if isinstance(item, dict)] if isinstance(judge.get("decisions"), list) else []
    critics = load_by_key(root / "latest_critic_reviews.json", "reviews", "review_item_id")
    packages = load_by_key(draft_root / "latest_platform_packages.json", "packages", "package_id")
    drafts = load_by_key(draft_root / "latest_content_drafts.json", "drafts", "draft_id")
    run_date = str(judge.get("run_date") or datetime.now().strftime("%Y%m%d")).replace("-", "")[:8]
    target_decisions = [item for item in decisions if item.get("decision") in {"NEEDS_REVISION", "ESCALATE_TO_HUMAN"}]
    instructions = []
    for decision in target_decisions:
        package = packages.get(str(decision.get("package_id")), {})
        draft = drafts.get(str(package.get("draft_id")), {})
        instructions.append(build_instruction(decision, critics.get(str(decision.get("review_item_id")), {}), package, draft, run_date))
    warnings = () if decisions else ("No judge decisions available.",)
    return RevisionInstructionReport(SCHEMA_VERSION, utc_now(), run_date, len(instructions), tuple(instructions), warnings)


def report_to_dict(report: RevisionInstructionReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: RevisionInstructionReport) -> str:
    rows = [
        f"| {idx} | {item.revision_priority} | {item.next_action} | {item.package_id} | {len(item.evidence_fixes)} | {len(item.risk_fixes)} |"
        for idx, item in enumerate(report.instructions, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Revision Instructions v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Instructions: `{report.revision_count}`

## Instructions

| # | Priority | Next Action | Package | Evidence Fixes | Risk Fixes |
|---:|---|---|---|---:|---:|
{chr(10).join(rows) if rows else '| 0 | - | - | - | 0 | 0 |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "06_review_queue"
    return {
        "dated_json": root / f"{run_date}__revision-instructions.json",
        "dated_md": root / f"{run_date}__revision-instructions.md",
        "latest_json": root / "latest_revision_instructions.json",
        "latest_md": root / "latest_revision_instructions.md",
    }


def write_revision_instruction_report(report: RevisionInstructionReport, paths: ProjectPaths) -> dict[str, Path]:
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
