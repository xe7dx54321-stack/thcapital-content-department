"""Daily high-value candidate pool builder."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class HighValueCandidate:
    rank: int
    cluster_id: str
    run_date: str
    theme: str
    total_score: float
    score_band: str
    recommended_action: str
    evidence_count: int
    source_count: int
    source_ids: tuple[str, ...]
    why_it_matters: str
    suggested_angles: tuple[str, ...]
    key_evidence: tuple[dict[str, Any], ...]
    risks_missing_info: tuple[str, ...]


@dataclass(frozen=True)
class HighValueCandidateReport:
    schema_version: str
    generated_at: str
    run_date: str
    candidate_count: int
    band_counts: dict[str, int]
    total_source_count: int
    candidates: tuple[HighValueCandidate, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def normalize_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return today_token()
    return text.replace("-", "")[:8]


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def key_evidence(items: list[dict[str, Any]], limit: int = 3) -> tuple[dict[str, Any], ...]:
    compact: list[dict[str, Any]] = []
    for item in items[:limit]:
        compact.append(
            {
                "evidence_id": item.get("evidence_id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "source_id": item.get("source_id"),
                "source_tier": item.get("source_tier"),
            }
        )
    return tuple(compact)


def risks_for_score(score: dict[str, Any]) -> tuple[str, ...]:
    risks: list[str] = []
    if safe_int(score.get("source_count")) <= 1:
        risks.append("Single-source signal; needs confirmation before long-form content.")
    if safe_int(score.get("evidence_count")) <= 1:
        risks.append("Only one evidence item in cluster.")
    if str(score.get("score_band")) in {"C", "D"}:
        risks.append("Score band below high-priority threshold.")
    if not risks:
        risks.append("Verify freshness and source context before editorial use.")
    return tuple(risks)


def make_candidate(rank: int, score: dict[str, Any], run_date: str) -> HighValueCandidate:
    items = [item for item in score.get("items", []) if isinstance(item, dict)]
    return HighValueCandidate(
        rank=rank,
        cluster_id=str(score.get("cluster_id") or ""),
        run_date=run_date,
        theme=str(score.get("theme") or ""),
        total_score=round(safe_float(score.get("total_score")), 2),
        score_band=str(score.get("score_band") or "D"),
        recommended_action=str(score.get("recommended_action") or "archive"),
        evidence_count=safe_int(score.get("evidence_count")),
        source_count=safe_int(score.get("source_count")),
        source_ids=tuple(str(item) for item in score.get("source_ids", []) if item),
        why_it_matters=str(score.get("why_it_matters") or ""),
        suggested_angles=tuple(str(item) for item in score.get("suggested_angles", []) if item),
        key_evidence=key_evidence(items),
        risks_missing_info=risks_for_score(score),
    )


def build_high_value_candidate_report(paths: ProjectPaths, run_date: str | None = None) -> HighValueCandidateReport:
    input_path = paths.market_content_root / "03_topic_candidates" / "latest_topic_cluster_scores.json"
    payload = read_json(input_path)
    final_run_date = normalize_date(run_date or payload.get("run_date"))
    raw_scores = payload.get("scores")
    scores = [item for item in raw_scores if isinstance(item, dict)] if isinstance(raw_scores, list) else []
    sorted_scores = sorted(scores, key=lambda item: safe_float(item.get("total_score")), reverse=True)
    selected = [item for item in sorted_scores if item.get("score_band") in {"A", "B"}]
    if not selected and sorted_scores:
        selected = sorted_scores[: min(10, len(sorted_scores))]

    warnings: list[str] = []
    if not input_path.exists():
        warnings.append("latest_topic_cluster_scores.json not found; run make value-scores first.")
    if not scores:
        warnings.append("No scored clusters available.")
    if scores and not any(item.get("score_band") in {"A", "B"} for item in scores):
        warnings.append("No A/B band clusters found; report shows top scored clusters for monitoring.")

    candidates = tuple(make_candidate(index, item, final_run_date) for index, item in enumerate(selected, start=1))
    band_counts: dict[str, int] = {}
    for candidate in candidates:
        band_counts[candidate.score_band] = band_counts.get(candidate.score_band, 0) + 1
    source_ids = {source_id for candidate in candidates for source_id in candidate.source_ids}

    return HighValueCandidateReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        candidate_count=len(candidates),
        band_counts=dict(sorted(band_counts.items())),
        total_source_count=len(source_ids),
        candidates=candidates,
        warnings=tuple(warnings),
    )


def report_to_dict(report: HighValueCandidateReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: HighValueCandidateReport) -> str:
    a_count = report.band_counts.get("A", 0)
    b_count = report.band_counts.get("B", 0)
    rows = []
    detail_sections = []
    for candidate in report.candidates:
        rows.append(
            "| "
            + " | ".join(
                [
                    str(candidate.rank),
                    f"{candidate.total_score:.2f}",
                    candidate.score_band,
                    escape_cell(candidate.theme),
                    candidate.recommended_action,
                    str(candidate.evidence_count),
                    escape_cell(", ".join(candidate.source_ids)),
                ]
            )
            + " |"
        )
        evidence_lines = "\n".join(
            f"- `{item.get('source_id')}` {item.get('title')} ({item.get('url') or 'no url'})"
            for item in candidate.key_evidence
        ) or "- None"
        angles = "\n".join(f"- {item}" for item in candidate.suggested_angles) or "- None"
        risks = "\n".join(f"- {item}" for item in candidate.risks_missing_info) or "- None"
        detail_sections.append(
            f"""### {candidate.rank}. {candidate.theme}

- Score: `{candidate.total_score:.2f}`
- Band: `{candidate.score_band}`
- Recommended action: `{candidate.recommended_action}`
- Why it matters: {candidate.why_it_matters}

Suggested angles:

{angles}

Key evidence:

{evidence_lines}

Risks / missing info:

{risks}
"""
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Daily High-Value Candidates

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Candidates: `{report.candidate_count}`
- A band: `{a_count}`
- B band: `{b_count}`
- Total source count: `{report.total_source_count}`

## Top Candidates

| Rank | Score | Band | Theme | Recommended Action | Evidence Count | Sources |
|---:|---:|---|---|---|---:|---|
{chr(10).join(rows) if rows else '| 0 | 0 | D | None | archive | 0 | - |'}

## Candidate Details

{chr(10).join(detail_sections) if detail_sections else '暂无候选。'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    topic_root = paths.market_content_root / "03_topic_candidates"
    return {
        "dated_json": topic_root / f"{run_date}__high-value-candidates.json",
        "dated_md": topic_root / f"{run_date}__high-value-candidates.md",
        "latest_json": topic_root / "latest_high_value_candidates.json",
        "latest_md": topic_root / "latest_high_value_candidates.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__high-value-candidates-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_high_value_candidates_board.md",
    }


def write_high_value_candidate_report(report: HighValueCandidateReport, paths: ProjectPaths) -> dict[str, Path]:
    paths_by_name = output_paths(paths, report.run_date)
    for path in paths_by_name.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (paths_by_name["dated_json"], paths_by_name["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (
        paths_by_name["dated_md"],
        paths_by_name["latest_md"],
        paths_by_name["frontstage_dated_md"],
        paths_by_name["frontstage_latest_md"],
    ):
        path.write_text(markdown, encoding="utf-8")
    return paths_by_name
