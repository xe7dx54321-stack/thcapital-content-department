"""Competitive Coverage Analysis v1.

Analyzes which topics are covered by competitor sources and identifies coverage gaps.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from content_system.wechat_article_intelligence import ArticleIntelligence


SCHEMA_VERSION = "v1"

COMPETITOR_SOURCES = {
    "jiqizhixin": "机器之心",
    "liangziwei": "量子位",
    "xinzhiyuan": "新智元",
    "zhidongxi": "智东西",
    "36kr": "36氪",
    "qbitai": "QbitAI",
    "aihub": "AIHub",
    "techweb": "TechWeb",
    "ifanr": "爱范儿",
    "pingwest": "品玩",
}

TOPIC_KEYWORDS = {
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


@dataclass(frozen=True)
class TopicCoverage:
    topic_name: str
    source_count: int
    article_count: int
    sources: tuple[str, ...]


@dataclass(frozen=True)
class CoverageGap:
    topic_name: str
    coverage_score: float
    gap_reason: str
    recommended_action: str


@dataclass(frozen=True)
class CompetitiveAnalysis:
    schema_version: str
    run_date: str
    source_count: int
    total_articles: int
    topic_coverage: tuple[TopicCoverage, ...]
    coverage_gaps: tuple[CoverageGap, ...]
    top_competitors: tuple[str, ...]
    coverage_overlap_score: float


@dataclass(frozen=True)
class CoverageAnalysisReport:
    schema_version: str
    generated_at: str
    run_date: str
    analysis: CompetitiveAnalysis
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def classify_topic(text: str) -> tuple[str, ...]:
    topics: list[str] = []
    lowered = text.lower()

    for topic_name, keywords in TOPIC_KEYWORDS.items():
        if any(kw.lower() in lowered for kw in keywords):
            topics.append(topic_name)

    return tuple(topics)


def analyze_coverage(intelligence_items: tuple[ArticleIntelligence, ...], run_date: str | None = None) -> CoverageAnalysisReport:
    warnings: list[str] = []

    topic_sources: dict[str, set[str]] = {}
    topic_articles: dict[str, int] = {}
    source_articles: Counter[str] = Counter()

    for item in intelligence_items:
        source_articles[item.source_id] += 1
        topics = classify_topic(item.excerpt)
        for topic in topics:
            topic_sources.setdefault(topic, set()).add(item.source_id)
            topic_articles[topic] = topic_articles.get(topic, 0) + 1

    topic_coverage: list[TopicCoverage] = []
    for topic_name, sources in topic_sources.items():
        topic_coverage.append(TopicCoverage(
            topic_name=topic_name,
            source_count=len(sources),
            article_count=topic_articles.get(topic_name, 0),
            sources=tuple(sorted(sources)),
        ))

    topic_coverage.sort(key=lambda t: -t.article_count)

    coverage_gaps: list[CoverageGap] = []
    for topic_name, sources in topic_sources.items():
        coverage_score = len(sources) / max(len(COMPETITOR_SOURCES), 1)
        if coverage_score < 0.3:
            coverage_gaps.append(CoverageGap(
                topic_name=topic_name,
                coverage_score=round(coverage_score, 2),
                gap_reason="Low source coverage",
                recommended_action="Increase monitoring for this topic",
            ))
        elif coverage_score < 0.5:
            coverage_gaps.append(CoverageGap(
                topic_name=topic_name,
                coverage_score=round(coverage_score, 2),
                gap_reason="Moderate source coverage",
                recommended_action="Expand source list for this topic",
            ))

    coverage_gaps.sort(key=lambda g: g.coverage_score)

    top_competitors = tuple(
        source for source, count in source_articles.most_common(5)
    )

    total_topics = len(topic_sources)
    max_coverage = max((tc.source_count for tc in topic_coverage), default=1)
    coverage_overlap_score = (
        sum(tc.source_count for tc in topic_coverage) / max(total_topics * len(COMPETITOR_SOURCES), 1)
        if total_topics > 0 else 0.0
    )

    analysis = CompetitiveAnalysis(
        schema_version=SCHEMA_VERSION,
        run_date=run_date or today_token(),
        source_count=len(source_articles),
        total_articles=len(intelligence_items),
        topic_coverage=tuple(topic_coverage),
        coverage_gaps=tuple(coverage_gaps),
        top_competitors=top_competitors,
        coverage_overlap_score=round(coverage_overlap_score, 2),
    )

    return CoverageAnalysisReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date or today_token(),
        analysis=analysis,
        warnings=tuple(warnings),
    )


def report_to_dict(report: CoverageAnalysisReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: CoverageAnalysisReport) -> str:
    analysis = report.analysis

    topic_rows = []
    for index, topic in enumerate(analysis.topic_coverage, start=1):
        topic_rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    topic.topic_name,
                    str(topic.article_count),
                    str(topic.source_count),
                    ", ".join(topic.sources[:3]) + ("..." if len(topic.sources) > 3 else ""),
                ]
            )
            + " |"
        )

    gap_rows = []
    for index, gap in enumerate(analysis.coverage_gaps, start=1):
        gap_rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    gap.topic_name,
                    str(int(gap.coverage_score * 100)) + "%",
                    gap.gap_reason,
                    gap.recommended_action,
                ]
            )
            + " |"
        )

    return f"""# Competitive Coverage Analysis Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Sources: `{analysis.source_count}`
- Total articles: `{analysis.total_articles}`
- Coverage overlap: `{int(analysis.coverage_overlap_score * 100)}%`

## Topic Coverage

| # | Topic | Articles | Sources | Top Sources |
|---:|---|:---:|:---:|---|
{chr(10).join(topic_rows) if topic_rows else '| 0 | - | 0 | 0 | - |'}

## Coverage Gaps

| # | Topic | Coverage | Reason | Recommended Action |
|---:|---|---|---|---|
{chr(10).join(gap_rows) if gap_rows else '| 0 | - | - | - | - |'}

## Top Competitors

{', '.join(analysis.top_competitors) if analysis.top_competitors else '- None'}

## Notes

- Coverage gaps are identified when less than 50% of sources cover a topic.
- Only excerpt-level analysis (no full text).
- do_not_copy_text=True for all analysis results.
"""


def write_report(report: CoverageAnalysisReport, output_path: str) -> None:
    import json
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)


def load_report(json_path: str) -> CoverageAnalysisReport | None:
    try:
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        analysis_data = data.get("analysis", {})
        return CoverageAnalysisReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            analysis=CompetitiveAnalysis(
                schema_version=analysis_data.get("schema_version", SCHEMA_VERSION),
                run_date=analysis_data.get("run_date", ""),
                source_count=int(analysis_data.get("source_count", 0)),
                total_articles=int(analysis_data.get("total_articles", 0)),
                topic_coverage=tuple(
                    TopicCoverage(
                        topic_name=t.get("topic_name", ""),
                        source_count=int(t.get("source_count", 0)),
                        article_count=int(t.get("article_count", 0)),
                        sources=tuple(t.get("sources", [])),
                    )
                    for t in analysis_data.get("topic_coverage", [])
                ),
                coverage_gaps=tuple(
                    CoverageGap(
                        topic_name=g.get("topic_name", ""),
                        coverage_score=float(g.get("coverage_score", 0.0)),
                        gap_reason=g.get("gap_reason", ""),
                        recommended_action=g.get("recommended_action", ""),
                    )
                    for g in analysis_data.get("coverage_gaps", [])
                ),
                top_competitors=tuple(analysis_data.get("top_competitors", [])),
                coverage_overlap_score=float(analysis_data.get("coverage_overlap_score", 0.0)),
            ),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None