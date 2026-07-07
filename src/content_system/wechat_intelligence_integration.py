"""WeChat Intelligence Integration v1.

Integrates WeChat RSS intelligence into topic scoring and content brief.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from content_system.wechat_article_intelligence import ArticleIntelligence, IntelligenceReport
from content_system.wechat_evidence_support import EvidenceSupportReport
from content_system.differentiated_angle_recommender import AngleRecommendationReport


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class WechatTopicScore:
    topic_id: str
    title: str
    source_count: int
    evidence_count: int
    hard_evidence_count: int
    entity_count: int
    angle_count: int
    claim_count: int
    intelligence_score: float
    evidence_score: float
    freshness_score: float
    total_score: float
    score_band: str
    do_not_copy_text: bool = True


@dataclass(frozen=True)
class WechatTopicScoringReport:
    schema_version: str
    generated_at: str
    run_date: str
    topic_count: int
    topics: tuple[WechatTopicScore, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class WechatContentBrief:
    brief_id: str
    topic_id: str
    title: str
    score: float
    score_band: str
    core_claim: str
    why_now: str
    why_it_matters: str
    supporting_evidence: tuple[dict[str, Any], ...]
    suggested_angles: tuple[str, ...]
    entities: tuple[str, ...]
    risks: tuple[str, ...]
    editorial_priority: str
    do_not_copy_text: bool = True


@dataclass(frozen=True)
class WechatBriefReport:
    schema_version: str
    generated_at: str
    run_date: str
    brief_count: int
    briefs: tuple[WechatContentBrief, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def make_topic_id(title: str) -> str:
    digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:12]
    return f"topic_{digest}"


def score_band_for(total_score: float) -> str:
    if total_score >= 80:
        return "A"
    if total_score >= 65:
        return "B"
    if total_score >= 50:
        return "C"
    return "D"


def editorial_priority_for(band: str) -> str:
    if band == "A":
        return "HIGH"
    if band == "B":
        return "MEDIUM"
    return "LOW"


def score_topics(intelligence_report: IntelligenceReport, evidence_report: EvidenceSupportReport) -> WechatTopicScoringReport:
    topics: list[WechatTopicScore] = []
    warnings: list[str] = []

    evidence_map = {e.evidence_id: e for e in evidence_report.evidence_items}

    seen_titles: set[str] = set()

    for item in intelligence_report.items:
        title_norm = item.title.lower().strip()
        if title_norm in seen_titles:
            continue
        seen_titles.add(title_norm)

        related_items = [i for i in intelligence_report.items if title_norm in i.title.lower()]

        source_ids = {i.source_id for i in related_items}
        hard_evidence_count = sum(
            1 for i in related_items
            if evidence_map.get(i.entry_id) is not None and evidence_map[i.entry_id].is_hard_evidence
        )

        total_entities = sum(len(i.entities) for i in related_items)
        total_claims = sum(len(i.claims) for i in related_items)
        total_angles = sum(len(i.angles) for i in related_items)

        intelligence_score = min(
            30.0
            + (len(source_ids) * 5.0)
            + (total_entities * 2.0)
            + (total_claims * 3.0)
            + (total_angles * 1.5),
            100.0
        )

        evidence_score = min(
            30.0
            + (hard_evidence_count * 15.0)
            + ((len(related_items) - hard_evidence_count) * 5.0),
            100.0
        )

        freshness_score = 80.0

        total_score = (intelligence_score * 0.4) + (evidence_score * 0.4) + (freshness_score * 0.2)
        band = score_band_for(total_score)

        topics.append(WechatTopicScore(
            topic_id=make_topic_id(item.title),
            title=item.title,
            source_count=len(source_ids),
            evidence_count=len(related_items),
            hard_evidence_count=hard_evidence_count,
            entity_count=total_entities,
            angle_count=total_angles,
            claim_count=total_claims,
            intelligence_score=round(intelligence_score, 2),
            evidence_score=round(evidence_score, 2),
            freshness_score=round(freshness_score, 2),
            total_score=round(total_score, 2),
            score_band=band,
            do_not_copy_text=True,
        ))

    topics.sort(key=lambda t: -t.total_score)

    return WechatTopicScoringReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=intelligence_report.run_date or today_token(),
        topic_count=len(topics),
        topics=tuple(topics),
        warnings=tuple(warnings),
    )


def build_briefs(scoring_report: WechatTopicScoringReport, intelligence_report: IntelligenceReport, angle_report: AngleRecommendationReport) -> WechatBriefReport:
    briefs: list[WechatContentBrief] = []
    warnings: list[str] = []

    evidence_map = {}
    angle_map = {}

    for topic in scoring_report.topics:
        if topic.score_band == "D":
            continue

        related_items = [i for i in intelligence_report.items if topic.title.lower() in i.title.lower()]
        related_angles = []
        for report in angle_report.reports:
            if topic.title.lower() in report.title.lower():
                related_angles.extend(report.recommended_angles)

        all_claims = []
        all_entities = []
        for item in related_items:
            all_claims.extend(c.claim_text for c in item.claims)
            all_entities.extend(f"{e.name}({e.entity_type})" for e in item.entities)

        supporting_evidence = tuple(
            {
                "evidence_id": item.entry_id,
                "title": item.title,
                "url": item.link,
                "source_id": item.source_id,
            }
            for item in related_items[:5]
        )

        suggested_angles = tuple(a.angle_name for a in related_angles[:5])
        entities = tuple(list(dict.fromkeys(all_entities))[:5])

        risks: list[str] = []
        if topic.hard_evidence_count == 0:
            risks.append("No hard evidence found - needs verification")
        if topic.source_count < 2:
            risks.append("Only one source - consider expanding coverage")
        risks.append("Rule-based brief; requires human review")

        briefs.append(WechatContentBrief(
            brief_id=f"brief_{topic.topic_id}",
            topic_id=topic.topic_id,
            title=topic.title,
            score=topic.total_score,
            score_band=topic.score_band,
            core_claim=all_claims[0] if all_claims else f"{topic.title} is a notable AI/Agent topic",
            why_now=f"{topic.evidence_count} evidence items from {topic.source_count} sources",
            why_it_matters=f"Entities: {', '.join(entities) if entities else 'None'}",
            supporting_evidence=supporting_evidence,
            suggested_angles=suggested_angles,
            entities=entities,
            risks=tuple(risks),
            editorial_priority=editorial_priority_for(topic.score_band),
            do_not_copy_text=True,
        ))

    return WechatBriefReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=scoring_report.run_date,
        brief_count=len(briefs),
        briefs=tuple(briefs),
        warnings=tuple(warnings),
    )


def scoring_report_to_dict(report: WechatTopicScoringReport) -> dict[str, Any]:
    return asdict(report)


def brief_report_to_dict(report: WechatBriefReport) -> dict[str, Any]:
    return asdict(report)


def render_scoring_markdown(report: WechatTopicScoringReport) -> str:
    rows = []
    for index, topic in enumerate(report.topics, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    topic.topic_id,
                    topic.score_band,
                    str(topic.total_score),
                    str(topic.source_count),
                    str(topic.hard_evidence_count),
                    str(topic.entity_count),
                    topic.title[:50] + "..." if len(topic.title) > 50 else topic.title,
                ]
            )
            + " |"
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"

    return f"""# WeChat Topic Scoring Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Topics: `{report.topic_count}`

## Topics

| # | Topic ID | Band | Score | Sources | Hard Evidence | Entities | Title |
|---:|---|---|---:|:---:|:---:|:---:|---|
{chr(10).join(rows) if rows else '| 0 | - | D | 0 | 0 | 0 | 0 | - |'}

## Warnings

{warnings}

## Notes

- Intelligence score: sources + entities + claims + angles
- Evidence score: hard evidence + soft evidence
- Freshness score: fixed at 80 for WeChat RSS
- do_not_copy_text=True for all topics.
"""


def render_brief_markdown(report: WechatBriefReport) -> str:
    rows = []
    for index, brief in enumerate(report.briefs, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    brief.brief_id,
                    brief.editorial_priority,
                    brief.score_band,
                    str(brief.score),
                    brief.title[:50] + "..." if len(brief.title) > 50 else brief.title,
                ]
            )
            + " |"
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"

    return f"""# WeChat Content Brief Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Briefs: `{report.brief_count}`

## Briefs

| # | Brief ID | Priority | Band | Score | Title |
|---:|---|---|---|---:|---|
{chr(10).join(rows) if rows else '| 0 | - | LOW | D | 0 | - |'}

## Warnings

{warnings}

## Notes

- Briefs generated for score bands A, B, and C only.
- Rule-based generation; requires human review.
- do_not_copy_text=True for all briefs.
"""


def write_scoring_report(report: WechatTopicScoringReport, output_path: str) -> None:
    payload = json.dumps(scoring_report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_scoring_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)


def write_brief_report(report: WechatBriefReport, output_path: str) -> None:
    payload = json.dumps(brief_report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_brief_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)