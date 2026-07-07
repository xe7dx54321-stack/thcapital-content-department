"""Topic Diversity Scoring v1.

Comprehensive diversity scoring that combines:
- Topic similarity penalties
- Source/lane diversity penalties
- Competitive coverage penalties
- Differentiated angle boosts
- Title normalization guards
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class DiversityScoreBreakdown:
    topic_id: str
    title: str
    original_score: float
    recent_topic_duplicate_penalty: float
    same_source_repetition_penalty: float
    same_lane_repetition_penalty: float
    high_competitive_same_angle_penalty: float
    metadata_title_penalty: float
    weak_differentiation_penalty: float
    strong_differentiated_angle_boost: float
    multi_source_support_boost: float
    fresh_undercovered_angle_boost: float
    diversity_adjusted_score: float
    diversity_status: str


@dataclass(frozen=True)
class TopicDiversityReport:
    schema_version: str
    generated_at: str
    run_date: str
    candidate_count: int
    diversity_scores: tuple[DiversityScoreBreakdown, ...]
    avg_original_score: float
    avg_adjusted_score: float
    penalty_count: int
    boost_count: int
    neutral_count: int
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def normalize_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return today_token()
    return text.replace("-", "")[:8]


def calculate_diversity_score(
    candidate: dict[str, Any],
    similarity_report: dict[str, Any] | None = None,
    source_lane_report: dict[str, Any] | None = None,
    competitive_penalty_report: dict[str, Any] | None = None,
    angle_boost_report: dict[str, Any] | None = None,
    title_guard_report: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
) -> DiversityScoreBreakdown:
    default_policy = {
        "penalties": {
            "recent_topic_duplicate": 0.18,
            "same_source_repetition": 0.10,
            "same_lane_repetition": 0.08,
            "high_competitive_same_angle": 0.14,
            "metadata_title": 0.20,
            "weak_differentiation": 0.12,
        },
        "boosts": {
            "strong_differentiated_angle": 0.12,
            "multi_source_support": 0.08,
            "fresh_undercovered_angle": 0.10,
        },
    }
    final_policy = policy or default_policy
    penalties = final_policy.get("penalties", {})
    boosts = final_policy.get("boosts", {})

    original_score = float(candidate.get("score") or candidate.get("topic_score") or 0.0)
    topic_id = str(candidate.get("topic_id") or candidate.get("evidence_id") or "")

    recent_topic_duplicate_penalty = 0.0
    if similarity_report:
        matches = similarity_report.get("similarity_matches", [])
        for match in matches:
            if match.get("topic_id") == topic_id and match.get("is_similar"):
                recent_topic_duplicate_penalty = penalties.get("recent_topic_duplicate", 0.18)
                if match.get("is_hard_duplicate"):
                    recent_topic_duplicate_penalty *= 1.5
                break

    same_source_repetition_penalty = 0.0
    same_lane_repetition_penalty = 0.0
    if source_lane_report:
        source_info = source_lane_report.get("source_lane_info", {})
        candidate_source_id = str(candidate.get("source_id") or "")
        candidate_lane = str(candidate.get("lane") or candidate.get("source_category") or "")

        if candidate_source_id in source_info:
            source_repetition = source_info[candidate_source_id].get("recent_repetition", 0)
            if source_repetition >= 2:
                same_source_repetition_penalty = penalties.get("same_source_repetition", 0.10)
                if source_repetition >= 3:
                    same_source_repetition_penalty *= 1.5

        if candidate_lane in source_info:
            lane_repetition = source_info[candidate_lane].get("recent_repetition", 0)
            if lane_repetition >= 2:
                same_lane_repetition_penalty = penalties.get("same_lane_repetition", 0.08)
                if lane_repetition >= 3:
                    same_lane_repetition_penalty *= 1.5

    high_competitive_same_angle_penalty = 0.0
    if competitive_penalty_report:
        penalties_data = competitive_penalty_report.get("penalties", [])
        for p in penalties_data:
            if p.get("topic_id") == topic_id:
                high_competitive_same_angle_penalty = float(p.get("penalty", 0.0))
                break

    metadata_title_penalty = 0.0
    if title_guard_report:
        guards = title_guard_report.get("guards", [])
        for g in guards:
            if g.get("topic_id") == topic_id and g.get("is_raw_metadata_title"):
                metadata_title_penalty = penalties.get("metadata_title", 0.20)
                break

    weak_differentiation_penalty = 0.0
    strong_differentiated_angle_boost = 0.0
    multi_source_support_boost = 0.0
    fresh_undercovered_angle_boost = 0.0
    if angle_boost_report:
        boosts_data = angle_boost_report.get("boosts", [])
        for b in boosts_data:
            if b.get("topic_id") == topic_id:
                if b.get("boost_type") == "strong_differentiated_angle":
                    strong_differentiated_angle_boost = boosts.get("strong_differentiated_angle", 0.12)
                elif b.get("boost_type") == "multi_source_support":
                    multi_source_support_boost = boosts.get("multi_source_support", 0.08)
                elif b.get("boost_type") == "fresh_undercovered_angle":
                    fresh_undercovered_angle_boost = boosts.get("fresh_undercovered_angle", 0.10)
                elif b.get("boost_type") == "weak_differentiation":
                    weak_differentiation_penalty = penalties.get("weak_differentiation", 0.12)
                break

    total_penalties = (
        recent_topic_duplicate_penalty
        + same_source_repetition_penalty
        + same_lane_repetition_penalty
        + high_competitive_same_angle_penalty
        + metadata_title_penalty
        + weak_differentiation_penalty
    )

    total_boosts = (
        strong_differentiated_angle_boost
        + multi_source_support_boost
        + fresh_undercovered_angle_boost
    )

    diversity_adjusted_score = max(0.0, min(1.0, original_score + total_boosts - total_penalties))

    if total_penalties > total_boosts + 0.05:
        diversity_status = "PENALIZED"
    elif total_boosts > total_penalties + 0.05:
        diversity_status = "BOOSTED"
    else:
        diversity_status = "NEUTRAL"

    return DiversityScoreBreakdown(
        topic_id=topic_id,
        title=str(candidate.get("title") or ""),
        original_score=round(original_score, 4),
        recent_topic_duplicate_penalty=round(recent_topic_duplicate_penalty, 4),
        same_source_repetition_penalty=round(same_source_repetition_penalty, 4),
        same_lane_repetition_penalty=round(same_lane_repetition_penalty, 4),
        high_competitive_same_angle_penalty=round(high_competitive_same_angle_penalty, 4),
        metadata_title_penalty=round(metadata_title_penalty, 4),
        weak_differentiation_penalty=round(weak_differentiation_penalty, 4),
        strong_differentiated_angle_boost=round(strong_differentiated_angle_boost, 4),
        multi_source_support_boost=round(multi_source_support_boost, 4),
        fresh_undercovered_angle_boost=round(fresh_undercovered_angle_boost, 4),
        diversity_adjusted_score=round(diversity_adjusted_score, 4),
        diversity_status=diversity_status,
    )


def build_topic_diversity_report(
    candidates: list[dict[str, Any]],
    run_date: str | None = None,
    similarity_report: dict[str, Any] | None = None,
    source_lane_report: dict[str, Any] | None = None,
    competitive_penalty_report: dict[str, Any] | None = None,
    angle_boost_report: dict[str, Any] | None = None,
    title_guard_report: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
) -> TopicDiversityReport:
    final_run_date = normalize_date(run_date)
    warnings: list[str] = []

    if not candidates:
        warnings.append("No candidates provided for diversity scoring")

    diversity_scores: list[DiversityScoreBreakdown] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        diversity_scores.append(calculate_diversity_score(
            candidate,
            similarity_report,
            source_lane_report,
            competitive_penalty_report,
            angle_boost_report,
            title_guard_report,
            policy,
        ))

    diversity_scores.sort(key=lambda s: -s.diversity_adjusted_score)

    if diversity_scores:
        avg_original = sum(s.original_score for s in diversity_scores) / len(diversity_scores)
        avg_adjusted = sum(s.diversity_adjusted_score for s in diversity_scores) / len(diversity_scores)
    else:
        avg_original = 0.0
        avg_adjusted = 0.0

    penalty_count = sum(1 for s in diversity_scores if s.diversity_status == "PENALIZED")
    boost_count = sum(1 for s in diversity_scores if s.diversity_status == "BOOSTED")
    neutral_count = sum(1 for s in diversity_scores if s.diversity_status == "NEUTRAL")

    return TopicDiversityReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        candidate_count=len(candidates),
        diversity_scores=tuple(diversity_scores),
        avg_original_score=round(avg_original, 4),
        avg_adjusted_score=round(avg_adjusted, 4),
        penalty_count=penalty_count,
        boost_count=boost_count,
        neutral_count=neutral_count,
        warnings=tuple(warnings),
    )


def report_to_dict(report: TopicDiversityReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: TopicDiversityReport) -> str:
    rows = []
    for index, score in enumerate(report.diversity_scores, start=1):
        penalty_str = ""
        if score.recent_topic_duplicate_penalty:
            penalty_str += f" TD{int(score.recent_topic_duplicate_penalty*100)}"
        if score.same_source_repetition_penalty:
            penalty_str += f" SR{int(score.same_source_repetition_penalty*100)}"
        if score.same_lane_repetition_penalty:
            penalty_str += f" LR{int(score.same_lane_repetition_penalty*100)}"
        if score.high_competitive_same_angle_penalty:
            penalty_str += f" CC{int(score.high_competitive_same_angle_penalty*100)}"
        if score.metadata_title_penalty:
            penalty_str += f" MT{int(score.metadata_title_penalty*100)}"
        if score.weak_differentiation_penalty:
            penalty_str += f" WD{int(score.weak_differentiation_penalty*100)}"

        boost_str = ""
        if score.strong_differentiated_angle_boost:
            boost_str += f" DA{int(score.strong_differentiated_angle_boost*100)}"
        if score.multi_source_support_boost:
            boost_str += f" MS{int(score.multi_source_support_boost*100)}"
        if score.fresh_undercovered_angle_boost:
            boost_str += f" FU{int(score.fresh_undercovered_angle_boost*100)}"

        status_color = {
            "PENALIZED": "🔴",
            "BOOSTED": "🟢",
            "NEUTRAL": "⚪",
        }.get(score.diversity_status, "⚪")

        rows.append(
            "| "
            + " | ".join([
                str(index),
                status_color,
                score.diversity_status,
                str(round(score.original_score * 100, 1)) + "%",
                str(round(score.diversity_adjusted_score * 100, 1)) + "%",
                penalty_str or "-",
                boost_str or "-",
                score.title[:50] + "..." if len(score.title) > 50 else score.title,
            ])
            + " |"
        )

    return f"""# Topic Diversity Scoring Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Candidates: `{report.candidate_count}`
- Avg original score: `{round(report.avg_original_score * 100, 1)}%`
- Avg adjusted score: `{round(report.avg_adjusted_score * 100, 1)}%`
- Penalized: `{report.penalty_count}`
- Boosted: `{report.boost_count}`
- Neutral: `{report.neutral_count}`

## Diversity Scores

| # | Status | Category | Original | Adjusted | Penalties | Boosts | Title |
|---:|---|---|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | - | - | - | None |'}

## Legend

**Penalties:**
- TD: Recent topic duplicate
- SR: Same source repetition
- LR: Same lane repetition
- CC: High competitive same angle
- MT: Metadata title
- WD: Weak differentiation

**Boosts:**
- DA: Strong differentiated angle
- MS: Multi-source support
- FU: Fresh undercovered angle

## Warnings

{chr(10).join(f"- {w}" for w in report.warnings) if report.warnings else "- None"}

## Notes

- schema_version: `{SCHEMA_VERSION}`
"""


def write_report(report: TopicDiversityReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = Path(output_path + ".json")
    md_path = Path(output_path + ".md")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(payload + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def load_report(json_path: str) -> TopicDiversityReport | None:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return TopicDiversityReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            candidate_count=int(data.get("candidate_count", 0)),
            diversity_scores=tuple(
                DiversityScoreBreakdown(
                    topic_id=s.get("topic_id", ""),
                    title=s.get("title", ""),
                    original_score=float(s.get("original_score", 0.0)),
                    recent_topic_duplicate_penalty=float(s.get("recent_topic_duplicate_penalty", 0.0)),
                    same_source_repetition_penalty=float(s.get("same_source_repetition_penalty", 0.0)),
                    same_lane_repetition_penalty=float(s.get("same_lane_repetition_penalty", 0.0)),
                    high_competitive_same_angle_penalty=float(s.get("high_competitive_same_angle_penalty", 0.0)),
                    metadata_title_penalty=float(s.get("metadata_title_penalty", 0.0)),
                    weak_differentiation_penalty=float(s.get("weak_differentiation_penalty", 0.0)),
                    strong_differentiated_angle_boost=float(s.get("strong_differentiated_angle_boost", 0.0)),
                    multi_source_support_boost=float(s.get("multi_source_support_boost", 0.0)),
                    fresh_undercovered_angle_boost=float(s.get("fresh_undercovered_angle_boost", 0.0)),
                    diversity_adjusted_score=float(s.get("diversity_adjusted_score", 0.0)),
                    diversity_status=s.get("diversity_status", "NEUTRAL"),
                )
                for s in data.get("diversity_scores", [])
            ),
            avg_original_score=float(data.get("avg_original_score", 0.0)),
            avg_adjusted_score=float(data.get("avg_adjusted_score", 0.0)),
            penalty_count=int(data.get("penalty_count", 0)),
            boost_count=int(data.get("boost_count", 0)),
            neutral_count=int(data.get("neutral_count", 0)),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None