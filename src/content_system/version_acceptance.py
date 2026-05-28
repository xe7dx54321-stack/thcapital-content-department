"""Human review and acceptance layer for article versions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
VALID_DECISIONS = {"UNREVIEWED", "ACCEPT", "REJECT", "REVISE_MORE", "DEFER"}


@dataclass(frozen=True)
class VersionAcceptanceResult:
    run_date: str
    decision_count: int
    accepted_count: int
    rejected_count: int
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "dated_json": root / f"{run_date}__version-review-decisions.json",
        "dated_md": root / f"{run_date}__version-review-decisions.md",
        "latest_json": root / "latest_version_review_decisions.json",
        "latest_md": root / "latest_version_review_decisions.md",
        "board_dated_md": paths.frontstage_root / f"{run_date}__version-review-board.md",
        "board_latest_md": paths.frontstage_root / "latest_version_review_board.md",
    }


def accepted_as_for(decision: str) -> str:
    if decision == "ACCEPT":
        return "candidate_final"
    if decision in {"REVISE_MORE", "DEFER"}:
        return "reference_only"
    return "none"


def decision_from_comparison(comparison: dict[str, Any], existing: dict[str, Any] | None = None) -> dict[str, Any]:
    previous = existing or {}
    decision = str(previous.get("decision") or "UNREVIEWED")
    if decision not in VALID_DECISIONS:
        decision = "UNREVIEWED"
    return {
        "decision_id": previous.get("decision_id") or f"vdec_{comparison.get('version_id') or 'version'}",
        "version_id": comparison.get("version_id") or "",
        "comparison_id": comparison.get("comparison_id") or "",
        "source_action_id": comparison.get("source_action_id") or "",
        "source_article_id": comparison.get("source_article_id") or "",
        "decision": decision,
        "human_score": previous.get("human_score"),
        "human_notes": previous.get("human_notes") or "",
        "accepted_as": previous.get("accepted_as") or accepted_as_for(decision),
        "decided_by": previous.get("decided_by") or "human",
        "decided_at": previous.get("decided_at") or "",
        "do_not_publish": True,
        "do_not_overwrite_original": True,
    }


def build_decision_payload(paths: ProjectPaths) -> dict[str, Any]:
    versions_root = paths.market_content_root / "09_workbench_actions" / "versions"
    comparisons_payload = read_json(versions_root / "latest_version_comparison_scores.json")
    existing_payload = read_json(versions_root / "latest_version_review_decisions.json")
    run_date = str(comparisons_payload.get("run_date") or existing_payload.get("run_date") or today_token()).replace("-", "")[:8]
    existing_by_version = {
        str(item.get("version_id")): item
        for item in list_payload(existing_payload, "decisions")
        if item.get("version_id")
    }
    decisions = [
        decision_from_comparison(comparison, existing_by_version.get(str(comparison.get("version_id"))))
        for comparison in list_payload(comparisons_payload, "comparisons")
    ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "decisions": decisions,
    }
    payload["summary"] = summarize(decisions)
    return payload


def summarize(decisions: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "accepted": sum(1 for item in decisions if item.get("decision") == "ACCEPT"),
        "rejected": sum(1 for item in decisions if item.get("decision") == "REJECT"),
        "revise_more": sum(1 for item in decisions if item.get("decision") == "REVISE_MORE"),
        "deferred": sum(1 for item in decisions if item.get("decision") == "DEFER"),
        "unreviewed": sum(1 for item in decisions if item.get("decision") == "UNREVIEWED"),
    }


def set_version_decision(
    payload: dict[str, Any],
    version_id: str,
    decision: str,
    human_score: float | None = None,
    note: str = "",
) -> bool:
    changed = False
    for item in list_payload(payload, "decisions"):
        if item.get("version_id") == version_id:
            item["decision"] = decision
            item["human_score"] = human_score
            item["human_notes"] = note
            item["accepted_as"] = accepted_as_for(decision)
            item["decided_by"] = "human"
            item["decided_at"] = utc_now()
            item["do_not_publish"] = True
            item["do_not_overwrite_original"] = True
            changed = True
    payload["summary"] = summarize(list_payload(payload, "decisions"))
    return changed


def update_version_review(
    paths: ProjectPaths,
    repo_root: Path,
    version_id: str | None = None,
    decision: str | None = None,
    score: float | None = None,
    note: str = "",
) -> tuple[VersionAcceptanceResult, dict[str, Any], bool]:
    payload = build_decision_payload(paths)
    changed = False
    if version_id and decision:
        changed = set_version_decision(payload, version_id, decision, score, note)
    result = write_version_review(payload, paths, repo_root)
    return result, payload, changed


def write_version_review(payload: dict[str, Any], paths: ProjectPaths, repo_root: Path) -> VersionAcceptanceResult:
    run_date = str(payload.get("run_date") or today_token()).replace("-", "")[:8]
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    decisions = list_payload(payload, "decisions")
    return VersionAcceptanceResult(
        run_date,
        len(decisions),
        sum(1 for item in decisions if item.get("decision") == "ACCEPT"),
        sum(1 for item in decisions if item.get("decision") == "REJECT"),
        repo_relative(outputs["latest_json"], repo_root),
        repo_relative(outputs["board_latest_md"], repo_root),
    )


def build_version_review_board(paths: ProjectPaths, repo_root: Path) -> tuple[VersionAcceptanceResult, dict[str, Any]]:
    payload = build_decision_payload(paths)
    return write_version_review(payload, paths, repo_root), payload


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('version_id')}` | `{item.get('decision')}` | `{item.get('human_score') if item.get('human_score') is not None else ''}` | `{item.get('accepted_as')}` | {item.get('human_notes') or ''} |"
        for item in list_payload(payload, "decisions")
    ) or "| - | UNREVIEWED | - | none | No versions to review |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Version Review Board

## Summary

- Run date: `{payload.get('run_date')}`
- Accepted: `{summary.get('accepted', 0)}`
- Rejected: `{summary.get('rejected', 0)}`
- Revise more: `{summary.get('revise_more', 0)}`
- Deferred: `{summary.get('deferred', 0)}`
- Unreviewed: `{summary.get('unreviewed', 0)}`
- Policy: `ACCEPT` does not publish and does not overwrite the original draft.

## Decisions

| Version | Decision | Score | Accepted As | Notes |
|---|---|---:|---|---|
{rows}

## CLI

```bash
python3 scripts/review_article_version.py --accept <version_id> --score 8 --note "标题和开头明显更好"
python3 scripts/review_article_version.py --reject <version_id> --note "改得太营销"
python3 scripts/review_article_version.py --revise-more <version_id> --note "证据还不够"
python3 scripts/review_article_version.py --defer <version_id> --note "明天再看"
```
"""


def score_or_none(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return safe_float(value)
