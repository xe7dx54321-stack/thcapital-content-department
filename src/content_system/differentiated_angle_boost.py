"""Differentiated Angle Boost v1.

Applies Phase34A differentiated angle recommendations to topic scoring:
- Strong differentiated angle → boost
- Fresh undercovered angle → boost
- Multi-source support → boost
- Weak differentiation → penalty
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "v1"

DIFFERENTIATED_ANGLES = {
    "用户体验角度": {"keywords": ("体验", "用户", "使用", "感受", "交互", "界面"), "description": "从普通用户的实际使用体验出发"},
    "技术实现角度": {"keywords": ("技术", "实现", "架构", "原理", "算法", "机制"), "description": "深入分析技术实现细节和架构设计"},
    "商业价值角度": {"keywords": ("商业", "价值", "市场", "营收", "利润", "商业模式"), "description": "评估商业价值和市场潜力"},
    "行业影响角度": {"keywords": ("行业", "影响", "变革", "颠覆", "重塑", "格局"), "description": "分析对整个行业的深远影响"},
    "对比分析角度": {"keywords": ("对比", "vs", "差异", "优劣", "评测", "对标"), "description": "与竞品或同类产品进行深度对比分析"},
    "历史演进角度": {"keywords": ("历史", "演进", "发展", "历程", "变化", "趋势"), "description": "从历史发展的视角回顾"},
    "未来展望角度": {"keywords": ("未来", "展望", "前景", "机遇", "潜力", "可能"), "description": "展望未来发展方向"},
    "风险警示角度": {"keywords": ("风险", "问题", "挑战", "隐患", "局限", "不足"), "description": "识别潜在风险和挑战"},
    "落地应用角度": {"keywords": ("落地", "应用", "场景", "案例", "实践", "解决方案"), "description": "关注实际落地应用"},
    "生态建设角度": {"keywords": ("生态", "生态系统", "社区", "开发者", "开源", "合作"), "description": "分析产品或技术的生态系统建设"},
    "数据洞察角度": {"keywords": ("数据", "指标", "分析", "洞察", "统计", "报告"), "description": "基于数据和指标进行量化分析"},
    "政策监管角度": {"keywords": ("政策", "监管", "合规", "法规", "法律", "治理"), "description": "分析政策监管环境"},
    "人才招聘角度": {"keywords": ("人才", "招聘", "团队", "职位", "技能", "薪资"), "description": "关注人才需求和招聘市场变化"},
    "投资决策角度": {"keywords": ("投资", "决策", "估值", "融资", "资本", "财务"), "description": "从投资者视角分析投资价值"},
    "教育普及角度": {"keywords": ("教育", "普及", "学习", "培训", "课程", "科普"), "description": "关注技术普及和教育推广"},
}


@dataclass(frozen=True)
class AngleBoost:
    topic_id: str
    title: str
    boost_type: str
    angle_name: str
    confidence: float
    boost_value: float
    description: str


@dataclass(frozen=True)
class DifferentiatedAngleBoostReport:
    schema_version: str
    generated_at: str
    run_date: str
    boosts: tuple[AngleBoost, ...]
    total_boosts: int
    avg_confidence: float
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


def recommend_angles_for_candidate(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    recommendations: list[dict[str, Any]] = []
    text = str(candidate.get("title") or "") + " " + str(candidate.get("summary") or "")
    lowered = text.lower()

    for angle_name, config in DIFFERENTIATED_ANGLES.items():
        matched: list[str] = []
        for keyword in config["keywords"]:
            if keyword in lowered:
                matched.append(keyword)
        if matched:
            confidence = min(0.3 + (len(matched) * 0.12), 0.95)
            recommendations.append({
                "angle_name": angle_name,
                "confidence": confidence,
                "description": config["description"],
                "matched_keywords": matched,
            })

    return sorted(recommendations, key=lambda r: -r["confidence"])


def apply_angle_boosts(
    candidates: list[dict[str, Any]],
    angle_report: dict[str, Any] | None = None,
    run_date: str | None = None,
    strong_angle_threshold: float = 0.70,
    fresh_angle_threshold: float = 0.50,
    weak_differentiation_threshold: float = 0.30,
    strong_boost_score: float = 0.12,
    fresh_boost_score: float = 0.10,
    multi_source_boost_score: float = 0.08,
    weak_penalty_score: float = 0.12,
) -> DifferentiatedAngleBoostReport:
    final_run_date = normalize_date(run_date)
    boosts: list[AngleBoost] = []
    warnings: list[str] = []

    if not candidates:
        warnings.append("No candidates provided for angle boost analysis")

    angle_cache: dict[str, list[dict[str, Any]]] = {}
    if angle_report:
        for r in angle_report.get("reports", []):
            entry_id = str(r.get("entry_id") or "")
            if entry_id:
                angle_cache[entry_id] = [
                    {
                        "angle_name": a.get("angle_name", ""),
                        "confidence": float(a.get("confidence", 0.0)),
                        "description": a.get("description", ""),
                    }
                    for a in r.get("recommended_angles", [])
                ]

    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue

        topic_id = str(candidate.get("topic_id") or candidate.get("evidence_id") or "")
        title = str(candidate.get("title") or "")
        entry_id = str(candidate.get("entry_id") or "")

        angles = angle_cache.get(entry_id)
        if angles is None:
            angles = recommend_angles_for_candidate(candidate)

        source_count = int(candidate.get("source_count") or candidate.get("supporting_sources") or 1)

        if angles:
            top_angle = angles[0]
            confidence = top_angle["confidence"]

            if confidence >= strong_angle_threshold:
                boosts.append(AngleBoost(
                    topic_id=topic_id,
                    title=title,
                    boost_type="strong_differentiated_angle",
                    angle_name=top_angle["angle_name"],
                    confidence=round(confidence, 4),
                    boost_value=round(strong_boost_score, 4),
                    description=top_angle["description"],
                ))
            elif confidence >= fresh_angle_threshold:
                boosts.append(AngleBoost(
                    topic_id=topic_id,
                    title=title,
                    boost_type="fresh_undercovered_angle",
                    angle_name=top_angle["angle_name"],
                    confidence=round(confidence, 4),
                    boost_value=round(fresh_boost_score, 4),
                    description=top_angle["description"],
                ))
            elif confidence <= weak_differentiation_threshold:
                boosts.append(AngleBoost(
                    topic_id=topic_id,
                    title=title,
                    boost_type="weak_differentiation",
                    angle_name=top_angle["angle_name"],
                    confidence=round(confidence, 4),
                    boost_value=-round(weak_penalty_score, 4),
                    description="Weak differentiation detected",
                ))

        if source_count >= 2:
            has_multi_source = False
            for b in boosts:
                if b.topic_id == topic_id and b.boost_type == "multi_source_support":
                    has_multi_source = True
                    break
            if not has_multi_source:
                boosts.append(AngleBoost(
                    topic_id=topic_id,
                    title=title,
                    boost_type="multi_source_support",
                    angle_name="Multi-source",
                    confidence=1.0,
                    boost_value=round(multi_source_boost_score, 4),
                    description=f"Supported by {source_count} sources",
                ))

    boosts.sort(key=lambda b: -b.boost_value)

    if boosts:
        avg_confidence = sum(b.confidence for b in boosts) / len(boosts)
    else:
        avg_confidence = 0.0

    return DifferentiatedAngleBoostReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        boosts=tuple(boosts),
        total_boosts=len(boosts),
        avg_confidence=round(avg_confidence, 4),
        warnings=tuple(warnings),
    )


def report_to_dict(report: DifferentiatedAngleBoostReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: DifferentiatedAngleBoostReport) -> str:
    rows = []
    for index, boost in enumerate(report.boosts, start=1):
        boost_sign = "+" if boost.boost_value > 0 else ""
        status_color = {
            "strong_differentiated_angle": "🟢",
            "fresh_undercovered_angle": "🟡",
            "multi_source_support": "🔵",
            "weak_differentiation": "🔴",
        }.get(boost.boost_type, "⚪")
        rows.append(
            "| "
            + " | ".join([
                str(index),
                status_color,
                boost.boost_type.replace("_", " ").title(),
                boost.angle_name,
                str(int(boost.confidence * 100)) + "%",
                f"{boost_sign}{int(boost.boost_value * 100)}%",
                boost.title[:50] + "..." if len(boost.title) > 50 else boost.title,
            ])
            + " |"
        )

    angle_list = "\n".join(
        f"- **{name}**: {config['description']}"
        for name, config in DIFFERENTIATED_ANGLES.items()
    )

    return f"""# Differentiated Angle Boost Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Total boosts: `{report.total_boosts}`
- Avg confidence: `{round(report.avg_confidence * 100, 1)}%`

## Angle Boosts

| # | Status | Type | Angle | Confidence | Boost | Title |
|---:|---|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | - | - | None |'}

## Available Angles ({len(DIFFERENTIATED_ANGLES)})

{angle_list}

## Warnings

{chr(10).join(f"- {w}" for w in report.warnings) if report.warnings else "- None"}

## Notes

- Strong differentiated angle: confidence >= 0.70 → +12%
- Fresh undercovered angle: confidence >= 0.50 → +10%
- Multi-source support: 2+ sources → +8%
- Weak differentiation: confidence <= 0.30 → -12%
- schema_version: `{SCHEMA_VERSION}`
"""


def write_report(report: DifferentiatedAngleBoostReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = Path(output_path + ".json")
    md_path = Path(output_path + ".md")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(payload + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def load_report(json_path: str) -> DifferentiatedAngleBoostReport | None:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return DifferentiatedAngleBoostReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            boosts=tuple(
                AngleBoost(
                    topic_id=b.get("topic_id", ""),
                    title=b.get("title", ""),
                    boost_type=b.get("boost_type", ""),
                    angle_name=b.get("angle_name", ""),
                    confidence=float(b.get("confidence", 0.0)),
                    boost_value=float(b.get("boost_value", 0.0)),
                    description=b.get("description", ""),
                )
                for b in data.get("boosts", [])
            ),
            total_boosts=int(data.get("total_boosts", 0)),
            avg_confidence=float(data.get("avg_confidence", 0.0)),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None