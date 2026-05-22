"""Rule Update Suggestion v1."""

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
class RuleUpdateSuggestion:
    schema_version: str
    suggestion_id: str
    run_date: str
    target_rule_area: str
    suggestion_type: str
    reason: str
    evidence: tuple[str, ...]
    confidence: float
    proposed_change: str
    auto_apply: bool


@dataclass(frozen=True)
class RuleUpdateSuggestionReport:
    schema_version: str
    generated_at: str
    run_date: str
    suggestion_count: int
    suggestions: tuple[RuleUpdateSuggestion, ...]
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


def list_payload(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    raw = payload.get(key)
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def build_suggestion(run_date: str, area: str, typ: str, reason: str, evidence: list[str], confidence: float, proposed: str) -> RuleUpdateSuggestion:
    return RuleUpdateSuggestion(
        schema_version=SCHEMA_VERSION,
        suggestion_id=make_id("rus", run_date, area, typ, reason[:40]),
        run_date=run_date,
        target_rule_area=area,
        suggestion_type=typ,
        reason=reason,
        evidence=tuple(evidence),
        confidence=round(confidence, 2),
        proposed_change=proposed,
        auto_apply=False,
    )


def build_rule_update_suggestion_report(paths: ProjectPaths) -> RuleUpdateSuggestionReport:
    memory = read_json(paths.market_content_root / "07_publishing" / "review_outcome_memory.json")
    records = list_payload(memory, "records")
    run_date = datetime.now().strftime("%Y%m%d")
    reviewed = [item for item in records if item.get("human_action") not in {None, "", "UNREVIEWED"}]
    suggestions: list[RuleUpdateSuggestion] = []
    warnings: list[str] = []

    if not records:
        warnings.append("No review outcome memory records available.")
        suggestions.append(
            build_suggestion(
                run_date,
                "agent_review",
                "monitor",
                "No review outcome memory yet; keep current rules and collect outcomes.",
                [],
                0.45,
                "Run Phase 4 daily until reviewed outcomes accumulate.",
            )
        )
    elif not reviewed:
        suggestions.append(
            build_suggestion(
                run_date,
                "agent_review",
                "monitor",
                "No human feedback yet; keep current rules and collect more feedback.",
                [f"unreviewed_count={memory.get('summary', {}).get('unreviewed_count', 0)}"],
                0.55,
                "Do not change thresholds until human feedback exists.",
            )
        )
    else:
        revise = [item for item in reviewed if item.get("human_action") == "REVISE"]
        reject = [item for item in reviewed if item.get("human_action") == "REJECT"]
        approve = [item for item in reviewed if item.get("human_action") == "APPROVE"]
        evidence_revise = [item for item in revise if any("evidence" in str(tag).lower() for tag in item.get("feedback_tags", []))]
        if evidence_revise:
            suggestions.append(
                build_suggestion(
                    run_date,
                    "content_quality",
                    "add_check",
                    "Multiple revisions mention evidence issues.",
                    [str(item.get("publishing_candidate_id")) for item in evidence_revise],
                    0.72,
                    "Tighten evidence count or evidence clarity checks before platform packaging.",
                )
            )
        if approve and not reject:
            suggestions.append(
                build_suggestion(
                    run_date,
                    "value_scoring",
                    "monitor",
                    "Approved feedback exists and no reject feedback is present.",
                    [str(item.get("publishing_candidate_id")) for item in approve],
                    0.62,
                    "Keep current scoring weights until a larger sample accumulates.",
                )
            )
        if reject:
            suggestions.append(
                build_suggestion(
                    run_date,
                    "agent_review",
                    "tighten_threshold",
                    "Rejected items indicate current gate may be too permissive.",
                    [str(item.get("publishing_candidate_id")) for item in reject],
                    0.70,
                    "Review Judge Gate approval threshold and critic severity weighting.",
                )
            )
    return RuleUpdateSuggestionReport(SCHEMA_VERSION, utc_now(), run_date, len(suggestions), tuple(suggestions), tuple(warnings))


def report_to_dict(report: RuleUpdateSuggestionReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: RuleUpdateSuggestionReport) -> str:
    rows = [
        f"| {idx} | {item.target_rule_area} | {item.suggestion_type} | {item.confidence:.2f} | {item.reason.replace('|', '\\|')} |"
        for idx, item in enumerate(report.suggestions, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Rule Update Suggestions v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Suggestions: `{report.suggestion_count}`

## Suggestions

| # | Rule Area | Type | Confidence | Reason |
|---:|---|---|---:|---|
{chr(10).join(rows) if rows else '| 0 | - | - | 0 | None |'}

## Policy

- Suggestions are never auto-applied.
- Human review is required before changing scoring or content rules.

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__rule-update-suggestions.json",
        "dated_md": root / f"{run_date}__rule-update-suggestions.md",
        "latest_json": root / "latest_rule_update_suggestions.json",
        "latest_md": root / "latest_rule_update_suggestions.md",
    }


def write_rule_update_suggestion_report(report: RuleUpdateSuggestionReport, paths: ProjectPaths) -> dict[str, Path]:
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
