"""Differentiated Angle Recommender v1.

Recommends at least 11 differentiated angles for article topics.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from content_system.wechat_article_intelligence import ArticleIntelligence


SCHEMA_VERSION = "v1"

DIFFERENTIATED_ANGLES = {
    "用户体验角度": {
        "keywords": ("体验", "用户", "使用", "感受", "交互", "界面", "便捷", "流畅"),
        "description": "从普通用户的实际使用体验出发，关注产品的易用性和感受",
    },
    "技术实现角度": {
        "keywords": ("技术", "实现", "架构", "原理", "算法", "机制", "代码", "底层"),
        "description": "深入分析技术实现细节和架构设计",
    },
    "商业价值角度": {
        "keywords": ("商业", "价值", "市场", "营收", "利润", "商业模式", "变现", "估值"),
        "description": "评估商业价值和市场潜力",
    },
    "行业影响角度": {
        "keywords": ("行业", "影响", "变革", "颠覆", "重塑", "格局", "趋势", "发展"),
        "description": "分析对整个行业的深远影响和格局变化",
    },
    "对比分析角度": {
        "keywords": ("对比", "vs", "差异", "优劣", "评测", "对标", "竞品", "差距"),
        "description": "与竞品或同类产品进行深度对比分析",
    },
    "历史演进角度": {
        "keywords": ("历史", "演进", "发展", "历程", "变化", "趋势", "回顾", "里程碑"),
        "description": "从历史发展的视角回顾技术或产品的演进历程",
    },
    "未来展望角度": {
        "keywords": ("未来", "展望", "前景", "机遇", "潜力", "可能", "预测", "趋势"),
        "description": "展望未来发展方向和可能的演变",
    },
    "风险警示角度": {
        "keywords": ("风险", "问题", "挑战", "隐患", "局限", "不足", "风险点", "警示"),
        "description": "识别潜在风险和挑战",
    },
    "落地应用角度": {
        "keywords": ("落地", "应用", "场景", "案例", "实践", "解决方案", "实施", "部署"),
        "description": "关注实际落地应用和具体使用场景",
    },
    "生态建设角度": {
        "keywords": ("生态", "生态系统", "社区", "开发者", "开源", "合作", "伙伴"),
        "description": "分析产品或技术的生态系统建设",
    },
    "数据洞察角度": {
        "keywords": ("数据", "指标", "分析", "洞察", "统计", "报告", "量化", "实证"),
        "description": "基于数据和指标进行量化分析",
    },
    "政策监管角度": {
        "keywords": ("政策", "监管", "合规", "法规", "法律", "治理", "标准", "规范"),
        "description": "分析政策监管环境和合规要求",
    },
    "人才招聘角度": {
        "keywords": ("人才", "招聘", "团队", "职位", "技能", "薪资", "人才市场"),
        "description": "关注人才需求和招聘市场变化",
    },
    "投资决策角度": {
        "keywords": ("投资", "决策", "估值", "融资", "资本", "财务", "回报", "风险投资"),
        "description": "从投资者视角分析投资价值和决策因素",
    },
    "教育普及角度": {
        "keywords": ("教育", "普及", "学习", "培训", "课程", "科普", "入门", "教程"),
        "description": "关注技术普及和教育推广",
    },
}


@dataclass(frozen=True)
class AngleRecommendation:
    angle_name: str
    confidence: float
    description: str
    matched_keywords: tuple[str, ...]


@dataclass(frozen=True)
class AngleReport:
    schema_version: str
    run_date: str
    entry_id: str
    title: str
    recommended_angles: tuple[AngleRecommendation, ...]
    top_angle: str | None


@dataclass(frozen=True)
class AngleRecommendationReport:
    schema_version: str
    generated_at: str
    run_date: str
    input_count: int
    reports: tuple[AngleReport, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def recommend_angles(intelligence_item: ArticleIntelligence) -> tuple[AngleRecommendation, ...]:
    recommendations: list[AngleRecommendation] = []
    text = intelligence_item.excerpt + " " + intelligence_item.title
    lowered = text.lower()

    for angle_name, config in DIFFERENTIATED_ANGLES.items():
        matched: list[str] = []
        for keyword in config["keywords"]:
            if keyword in lowered:
                matched.append(keyword)

        if matched:
            confidence = min(0.3 + (len(matched) * 0.12), 0.95)
            recommendations.append(AngleRecommendation(
                angle_name=angle_name,
                confidence=confidence,
                description=config["description"],
                matched_keywords=tuple(matched),
            ))

    return tuple(sorted(recommendations, key=lambda a: -a.confidence))


def recommend_all_angles(intelligence_items: tuple[ArticleIntelligence, ...], run_date: str | None = None) -> AngleRecommendationReport:
    reports: list[AngleReport] = []
    warnings: list[str] = []

    for item in intelligence_items:
        try:
            angles = recommend_angles(item)
            top_angle = angles[0].angle_name if angles else None
            reports.append(AngleReport(
                schema_version=SCHEMA_VERSION,
                run_date=run_date or today_token(),
                entry_id=item.entry_id,
                title=item.title,
                recommended_angles=angles,
                top_angle=top_angle,
            ))
        except Exception as exc:
            warnings.append(f"Failed to recommend angles for {item.entry_id}: {exc}")

    return AngleRecommendationReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date or today_token(),
        input_count=len(intelligence_items),
        reports=tuple(reports),
        warnings=tuple(warnings),
    )


def report_to_dict(report: AngleRecommendationReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: AngleRecommendationReport) -> str:
    rows = []
    for index, angle_report in enumerate(report.reports, start=1):
        top_angles = ", ".join(f"{a.angle_name}({int(a.confidence*100)}%)" for a in angle_report.recommended_angles[:3]) or "-"
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    angle_report.entry_id[:20] + "..." if len(angle_report.entry_id) > 20 else angle_report.entry_id,
                    angle_report.title[:50] + "..." if len(angle_report.title) > 50 else angle_report.title,
                    str(len(angle_report.recommended_angles)),
                    top_angles,
                ]
            )
            + " |"
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"

    angle_list = "\n".join(f"- **{name}**: {config['description']}" for name, config in DIFFERENTIATED_ANGLES.items())

    return f"""# Differentiated Angle Recommendation Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Input count: `{report.input_count}`

## Recommended Angles per Article

| # | Entry ID | Title | Angle Count | Top Angles |
|---:|---|---|:---:|---|
{chr(10).join(rows) if rows else '| 0 | - | - | 0 | - |'}

## Available Angles ({len(DIFFERENTIATED_ANGLES)})

{angle_list}

## Warnings

{warnings}

## Notes

- 15 differentiated angles available for recommendation.
- Confidence scores based on keyword matching in excerpt and title.
- Only excerpt-level analysis (no full text).
- do_not_copy_text=True for all recommendations.
"""


def write_report(report: AngleRecommendationReport, output_path: str) -> None:
    import json
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)


def load_report(json_path: str) -> AngleRecommendationReport | None:
    try:
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return AngleRecommendationReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            input_count=int(data.get("input_count", 0)),
            reports=tuple(
                AngleReport(
                    schema_version=r.get("schema_version", SCHEMA_VERSION),
                    run_date=r.get("run_date", ""),
                    entry_id=r.get("entry_id", ""),
                    title=r.get("title", ""),
                    recommended_angles=tuple(
                        AngleRecommendation(
                            angle_name=a.get("angle_name", ""),
                            confidence=float(a.get("confidence", 0.0)),
                            description=a.get("description", ""),
                            matched_keywords=tuple(a.get("matched_keywords", [])),
                        )
                        for a in r.get("recommended_angles", [])
                    ),
                    top_angle=r.get("top_angle"),
                )
                for r in data.get("reports", [])
            ),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None