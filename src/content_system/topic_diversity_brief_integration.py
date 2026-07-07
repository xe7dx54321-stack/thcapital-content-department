"""Topic Diversity Brief Integration v1.

Integrates recommended angles and duplication risks into the content brief.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class DiversityInsight:
    topic_id: str
    recommended_angle: str | None
    angle_description: str | None
    angle_confidence: float
    duplication_risk_level: str
    duplication_risk_details: str
    diversity_score: float
    diversity_status: str


@dataclass(frozen=True)
class BriefIntegrationReport:
    schema_version: str
    generated_at: str
    run_date: str
    insights: tuple[DiversityInsight, ...]
    total_topics: int
    topics_with_angle: int
    topics_with_risk: int
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


def build_diversity_insights(
    candidates: list[dict[str, Any]],
    angle_report: dict[str, Any] | None = None,
    similarity_report: dict[str, Any] | None = None,
    diversity_report: dict[str, Any] | None = None,
    run_date: str | None = None,
) -> BriefIntegrationReport:
    final_run_date = normalize_date(run_date)
    insights: list[DiversityInsight] = []
    warnings: list[str] = []

    if not candidates:
        warnings.append("No candidates provided for brief integration")

    angle_map: dict[str, dict[str, Any]] = {}
    if angle_report:
        for b in angle_report.get("boosts", []):
            topic_id = str(b.get("topic_id", ""))
            if b.get("boost_value", 0) > 0:
                angle_map[topic_id] = {
                    "angle_name": b.get("angle_name", ""),
                    "description": b.get("description", ""),
                    "confidence": float(b.get("confidence", 0.0)),
                }

    similarity_map: dict[str, list[dict[str, Any]]] = {}
    if similarity_report:
        for m in similarity_report.get("similarity_matches", []):
            topic_id = str(m.get("topic_id", ""))
            similarity_map.setdefault(topic_id, []).append({
                "similar_to_title": m.get("similar_to_title", ""),
                "similar_to_date": m.get("similar_to_date", ""),
                "combined_score": float(m.get("combined_score", 0.0)),
                "is_hard_duplicate": bool(m.get("is_hard_duplicate", False)),
            })

    diversity_map: dict[str, dict[str, Any]] = {}
    if diversity_report:
        for s in diversity_report.get("diversity_scores", []):
            topic_id = str(s.get("topic_id", ""))
            diversity_map[topic_id] = {
                "score": float(s.get("diversity_adjusted_score", 0.0)),
                "status": s.get("diversity_status", "NEUTRAL"),
            }

    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue

        topic_id = str(candidate.get("topic_id") or candidate.get("evidence_id") or "")

        angle_info = angle_map.get(topic_id, {})
        recommended_angle = angle_info.get("angle_name") or None
        angle_description = angle_info.get("description") or None
        angle_confidence = angle_info.get("confidence", 0.0)

        similar_items = similarity_map.get(topic_id, [])
        if similar_items:
            hard_duplicates = [s for s in similar_items if s.get("is_hard_duplicate")]
            if hard_duplicates:
                risk_level = "HIGH"
                recent = sorted(hard_duplicates, key=lambda x: -x.get("combined_score", 0))[0]
                risk_details = f"硬重复：{recent.get('similar_to_date', '')} 的 \"{recent.get('similar_to_title', '')[:30]}...\" (相似度 {int(recent.get('combined_score', 0)*100)}%)"
            else:
                risk_level = "MEDIUM"
                recent = sorted(similar_items, key=lambda x: -x.get("combined_score", 0))[0]
                risk_details = f"相似选题：{recent.get('similar_to_date', '')} 的 \"{recent.get('similar_to_title', '')[:30]}...\" (相似度 {int(recent.get('combined_score', 0)*100)}%)"
        else:
            risk_level = "LOW"
            risk_details = "无重复风险"

        diversity_info = diversity_map.get(topic_id, {})
        diversity_score = diversity_info.get("score", 0.0)
        diversity_status = diversity_info.get("status", "NEUTRAL")

        insights.append(DiversityInsight(
            topic_id=topic_id,
            recommended_angle=recommended_angle,
            angle_description=angle_description,
            angle_confidence=round(angle_confidence, 4),
            duplication_risk_level=risk_level,
            duplication_risk_details=risk_details,
            diversity_score=round(diversity_score, 4),
            diversity_status=diversity_status,
        ))

    topics_with_angle = sum(1 for i in insights if i.recommended_angle)
    topics_with_risk = sum(1 for i in insights if i.duplication_risk_level != "LOW")

    return BriefIntegrationReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        insights=tuple(insights),
        total_topics=len(candidates),
        topics_with_angle=topics_with_angle,
        topics_with_risk=topics_with_risk,
        warnings=tuple(warnings),
    )


def generate_brief_update(
    insight: DiversityInsight,
    original_brief: dict[str, Any] | None = None,
) -> dict[str, Any]:
    update: dict[str, Any] = {}

    if insight.recommended_angle:
        update["diversity_recommended_angle"] = insight.recommended_angle
        update["diversity_angle_description"] = insight.angle_description or ""
        update["diversity_angle_confidence"] = insight.angle_confidence

    update["diversity_duplication_risk_level"] = insight.duplication_risk_level
    update["diversity_duplication_risk_details"] = insight.duplication_risk_details
    update["diversity_score"] = insight.diversity_score
    update["diversity_status"] = insight.diversity_status

    if original_brief:
        combined = dict(original_brief)
        combined.update(update)
        return combined

    return update


def report_to_dict(report: BriefIntegrationReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: BriefIntegrationReport) -> str:
    rows = []
    for index, insight in enumerate(report.insights, start=1):
        risk_color = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(insight.duplication_risk_level, "⚪")
        angle_str = insight.recommended_angle or "-"
        rows.append(
            "| "
            + " | ".join([
                str(index),
                angle_str,
                str(int(insight.angle_confidence * 100)) + "%",
                risk_color,
                insight.duplication_risk_level,
                str(round(insight.diversity_score * 100, 1)) + "%",
                insight.diversity_status,
            ])
            + " |"
        )

    return f"""# Topic Diversity Brief Integration Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Total topics: `{report.total_topics}`
- Topics with angle: `{report.topics_with_angle}`
- Topics with risk: `{report.topics_with_risk}`

## Diversity Insights

| # | Recommended Angle | Confidence | Risk | Risk Level | Diversity Score | Status |
|---:|---|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | - | - | - |'}

## Warnings

{chr(10).join(f"- {w}" for w in report.warnings) if report.warnings else "- None"}

## Notes

- schema_version: `{SCHEMA_VERSION}`
"""


def write_report(report: BriefIntegrationReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = Path(output_path + ".json")
    md_path = Path(output_path + ".md")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(payload + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def load_report(json_path: str) -> BriefIntegrationReport | None:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return BriefIntegrationReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            insights=tuple(
                DiversityInsight(
                    topic_id=i.get("topic_id", ""),
                    recommended_angle=i.get("recommended_angle"),
                    angle_description=i.get("angle_description"),
                    angle_confidence=float(i.get("angle_confidence", 0.0)),
                    duplication_risk_level=i.get("duplication_risk_level", "LOW"),
                    duplication_risk_details=i.get("duplication_risk_details", ""),
                    diversity_score=float(i.get("diversity_score", 0.0)),
                    diversity_status=i.get("diversity_status", "NEUTRAL"),
                )
                for i in data.get("insights", [])
            ),
            total_topics=int(data.get("total_topics", 0)),
            topics_with_angle=int(data.get("topics_with_angle", 0)),
            topics_with_risk=int(data.get("topics_with_risk", 0)),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None