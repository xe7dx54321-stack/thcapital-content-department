"""Competitive Coverage Penalty v1.

Integrates Phase34A competitive coverage analysis to apply penalties when:
- High competitor coverage on same topic
- Same angle as competitors
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class CompetitivePenalty:
    topic_id: str
    title: str
    topic_name: str
    competitor_coverage_count: int
    coverage_score: float
    same_angle_risk: bool
    penalty: float
    penalty_reason: str


@dataclass(frozen=True)
class CompetitiveCoveragePenaltyReport:
    schema_version: str
    generated_at: str
    run_date: str
    penalties: tuple[CompetitivePenalty, ...]
    total_penalties: int
    avg_penalty: float
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


def classify_topic(text: str) -> tuple[str, ...]:
    topic_keywords = {
        "LLM/大模型": ("大模型", "LLM", "GPT", "Claude", "Gemini", "Llama", "模型"),
        "Agent/智能体": ("智能体", "Agent", "agents", "多智能体", "自主智能"),
        "AI基础设施": ("算力", "GPU", "NVIDIA", "芯片", "推理", "训练", "云"),
        "AI应用": ("应用", "落地", "场景", "案例", "解决方案"),
        "AI安全": ("安全", "对齐", "伦理", "监管", "合规"),
        "AI创业/投资": ("融资", "创业", "投资", "估值", "独角兽"),
        "AI研究": ("论文", "研究", "arxiv", "发表", "实验"),
        "AI教育": ("教育", "学习", "课程", "培训", "人才"),
        "AI工具": ("工具", "SDK", "API", "平台", "框架"),
        "AI政策": ("政策", "法规", "标准", "治理", "白皮书"),
    }
    topics: list[str] = []
    lowered = text.lower()
    for topic_name, keywords in topic_keywords.items():
        if any(kw.lower() in lowered for kw in keywords):
            topics.append(topic_name)
    return tuple(topics)


def apply_competitive_penalty(
    candidates: list[dict[str, Any]],
    coverage_report: dict[str, Any] | None = None,
    run_date: str | None = None,
    penalty_score: float = 0.14,
    high_coverage_threshold: float = 0.5,
) -> CompetitiveCoveragePenaltyReport:
    final_run_date = normalize_date(run_date)
    penalties: list[CompetitivePenalty] = []
    warnings: list[str] = []

    if not candidates:
        warnings.append("No candidates provided for competitive penalty analysis")

    topic_coverage: dict[str, dict[str, Any]] = {}
    if coverage_report:
        analysis = coverage_report.get("analysis", {})
        for tc in analysis.get("topic_coverage", []):
            topic_coverage[str(tc.get("topic_name", ""))] = {
                "source_count": int(tc.get("source_count", 0)),
                "article_count": int(tc.get("article_count", 0)),
                "coverage_score": float(tc.get("coverage_score", 0.0)),
            }

    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue

        topic_id = str(candidate.get("topic_id") or candidate.get("evidence_id") or "")
        title = str(candidate.get("title") or "")
        angle_type = str(candidate.get("angle_type") or candidate.get("suggested_angle") or "")

        candidate_topics = classify_topic(title)
        if not candidate_topics:
            continue

        max_coverage = 0.0
        max_source_count = 0
        matched_topic = ""

        for topic_name in candidate_topics:
            if topic_name in topic_coverage:
                coverage = topic_coverage[topic_name]
                if coverage["coverage_score"] > max_coverage:
                    max_coverage = coverage["coverage_score"]
                    max_source_count = coverage["source_count"]
                    matched_topic = topic_name

        if max_coverage >= high_coverage_threshold:
            same_angle_risk = angle_type != "" and max_source_count >= 3

            if same_angle_risk:
                penalty_value = penalty_score * 1.5
                reason = f"High coverage ({int(max_coverage*100)}%) + same angle risk"
            else:
                penalty_value = penalty_score
                reason = f"High coverage ({int(max_coverage*100)}%)"

            penalties.append(CompetitivePenalty(
                topic_id=topic_id,
                title=title,
                topic_name=matched_topic,
                competitor_coverage_count=max_source_count,
                coverage_score=round(max_coverage, 4),
                same_angle_risk=same_angle_risk,
                penalty=round(penalty_value, 4),
                penalty_reason=reason,
            ))

    penalties.sort(key=lambda p: -p.penalty)

    if penalties:
        avg_penalty = sum(p.penalty for p in penalties) / len(penalties)
    else:
        avg_penalty = 0.0

    return CompetitiveCoveragePenaltyReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        penalties=tuple(penalties),
        total_penalties=len(penalties),
        avg_penalty=round(avg_penalty, 4),
        warnings=tuple(warnings),
    )


def report_to_dict(report: CompetitiveCoveragePenaltyReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: CompetitiveCoveragePenaltyReport) -> str:
    rows = []
    for index, penalty in enumerate(report.penalties, start=1):
        risk_flag = "🔴 HIGH" if penalty.same_angle_risk else "🟡 MEDIUM"
        rows.append(
            "| "
            + " | ".join([
                str(index),
                risk_flag,
                str(int(penalty.coverage_score * 100)) + "%",
                str(penalty.competitor_coverage_count),
                str(int(penalty.penalty * 100)) + "%",
                penalty.title[:50] + "..." if len(penalty.title) > 50 else penalty.title,
                penalty.penalty_reason,
            ])
            + " |"
        )

    return f"""# Competitive Coverage Penalty Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Total penalties: `{report.total_penalties}`
- Avg penalty: `{round(report.avg_penalty * 100, 1)}%`

## Penalties

| # | Risk | Coverage | Competitors | Penalty | Title | Reason |
|---:|---|---|:---:|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | 0 | - | None | - |'}

## Warnings

{chr(10).join(f"- {w}" for w in report.warnings) if report.warnings else "- None"}

## Notes

- High coverage threshold: >= 50%
- Same angle risk: 3+ competitors covering same topic
- schema_version: `{SCHEMA_VERSION}`
"""


def write_report(report: CompetitiveCoveragePenaltyReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = Path(output_path + ".json")
    md_path = Path(output_path + ".md")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(payload + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def load_report(json_path: str) -> CompetitiveCoveragePenaltyReport | None:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return CompetitiveCoveragePenaltyReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            penalties=tuple(
                CompetitivePenalty(
                    topic_id=p.get("topic_id", ""),
                    title=p.get("title", ""),
                    topic_name=p.get("topic_name", ""),
                    competitor_coverage_count=int(p.get("competitor_coverage_count", 0)),
                    coverage_score=float(p.get("coverage_score", 0.0)),
                    same_angle_risk=bool(p.get("same_angle_risk", False)),
                    penalty=float(p.get("penalty", 0.0)),
                    penalty_reason=p.get("penalty_reason", ""),
                )
                for p in data.get("penalties", [])
            ),
            total_penalties=int(data.get("total_penalties", 0)),
            avg_penalty=float(data.get("avg_penalty", 0.0)),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None