"""WeChat Article Intelligence Extraction v1.

Extracts intelligence from articles including:
- Summary/excerpt
- Entities (companies, products, models, people)
- Angles
- Claims and evidence
- Style patterns
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from content_system.wechat_article_cleaner import CleanedArticle


SCHEMA_VERSION = "v1"

KNOWN_COMPANIES = (
    "OpenAI",
    "Anthropic",
    "Google",
    "DeepMind",
    "NVIDIA",
    "Meta",
    "Microsoft",
    "xAI",
    "Hugging Face",
    "GitHub",
    "Apple",
    "Amazon",
    "AWS",
    "Databricks",
    "Mistral",
    "Cohere",
    "Perplexity",
    "字节跳动",
    "腾讯",
    "阿里巴巴",
    "百度",
    "华为",
    "小米",
    "京东",
)

KNOWN_MODELS = (
    "GPT",
    "Claude",
    "Gemini",
    "Llama",
    "Qwen",
    "DeepSeek",
    "Mistral",
    "Phi",
    "Gemma",
    "Moonshot",
    "GLM",
    "ERNIE",
    "Yuan",
)

KNOWN_PEOPLE = (
    "Sam Altman",
    "Dario Amodei",
    "Jensen Huang",
    "Demis Hassabis",
    "Sundar Pichai",
    "Mark Zuckerberg",
    "Satya Nadella",
    "LeCun",
    "Yann LeCun",
    "Andrej Karpathy",
    "吴恩达",
    "李飞飞",
)

ANGLE_KEYWORDS = {
    "技术深度": ("架构", "原理", "机制", "算法", "模型", "训练", "推理", "优化", "量化", "微调"),
    "商业分析": ("市场", "营收", "利润", "估值", "融资", "投资", "增长", "用户", "付费"),
    "产品对比": ("对比", "vs", "评测", "测评", "对比分析", "竞品", "差异"),
    "行业趋势": ("趋势", "预测", "未来", "发展", "方向", "变化", "演进"),
    "案例研究": ("案例", "实践", "应用", "落地", "客户", "场景", "案例分析"),
    "政策监管": ("政策", "监管", "合规", "法规", "法律", "安全", "治理"),
    "人才招聘": ("招聘", "人才", "团队", "职位", "薪资", "跳槽"),
    "开源社区": ("开源", "GitHub", "社区", "贡献", "开发者", "生态"),
    "数据洞察": ("数据", "指标", "分析", "洞察", "统计", "报告"),
    "风险警示": ("风险", "警告", "问题", "隐患", "挑战", "失败"),
    "未来展望": ("展望", "前景", "机遇", "潜力", "可能性", "机会"),
}


@dataclass(frozen=True)
class IntelligenceEntity:
    entity_type: str
    name: str
    confidence: float


@dataclass(frozen=True)
class IntelligenceClaim:
    claim_text: str
    evidence_text: str
    confidence: float


@dataclass(frozen=True)
class IntelligenceAngle:
    angle_name: str
    confidence: float


@dataclass(frozen=True)
class IntelligencePattern:
    pattern_type: str
    description: str


@dataclass(frozen=True)
class ArticleIntelligence:
    schema_version: str
    entry_id: str
    source_id: str
    title: str
    link: str
    excerpt: str
    entities: tuple[IntelligenceEntity, ...]
    angles: tuple[IntelligenceAngle, ...]
    claims: tuple[IntelligenceClaim, ...]
    patterns: tuple[IntelligencePattern, ...]
    do_not_copy_text: bool = True


@dataclass(frozen=True)
class IntelligenceReport:
    schema_version: str
    generated_at: str
    run_date: str
    input_count: int
    output_count: int
    items: tuple[ArticleIntelligence, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def extract_entities(text: str) -> tuple[IntelligenceEntity, ...]:
    entities: list[IntelligenceEntity] = []
    lowered = text.lower()

    seen: set[tuple[str, str]] = set()

    for company in KNOWN_COMPANIES:
        if company.lower() in lowered and ("company", company) not in seen:
            entities.append(IntelligenceEntity(entity_type="company", name=company, confidence=0.9))
            seen.add(("company", company))

    for model in KNOWN_MODELS:
        if model.lower() in lowered and ("model", model) not in seen:
            entities.append(IntelligenceEntity(entity_type="model", name=model, confidence=0.85))
            seen.add(("model", model))

    for person in KNOWN_PEOPLE:
        if person.lower() in lowered and ("person", person) not in seen:
            entities.append(IntelligenceEntity(entity_type="person", name=person, confidence=0.8))
            seen.add(("person", person))

    return tuple(entities)


def extract_angles(text: str) -> tuple[IntelligenceAngle, ...]:
    angles: list[IntelligenceAngle] = []
    lowered = text.lower()

    for angle_name, keywords in ANGLE_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in lowered)
        if matches > 0:
            confidence = min(0.3 + (matches * 0.15), 0.95)
            angles.append(IntelligenceAngle(angle_name=angle_name, confidence=confidence))

    return tuple(sorted(angles, key=lambda a: -a.confidence))


def extract_claims(text: str) -> tuple[IntelligenceClaim, ...]:
    claims: list[IntelligenceClaim] = []

    claim_patterns = (
        r"(?:声称|宣称|表示|认为|指出|宣布|发布|推出|上线|发布了|推出了|上线了)([^。！？\n]+)",
        r"(?:据|消息|报道|透露|显示|表明|数据显示|研究显示)([^。！？\n]+)",
        r"(?:首次|全球首|国内首|行业首)([^。！？\n]+)",
        r"(?:突破|创新|领先|超越|颠覆|变革)([^。！？\n]+)",
    )

    for pattern in claim_patterns:
        for match in re.finditer(pattern, text):
            claim_text = match.group(1).strip()
            if len(claim_text) >= 10 and len(claim_text) <= 150:
                claims.append(IntelligenceClaim(
                    claim_text=claim_text,
                    evidence_text=text[:200],
                    confidence=0.7,
                ))

    return tuple(claims[:5])


def extract_patterns(text: str) -> tuple[IntelligencePattern, ...]:
    patterns: list[IntelligencePattern] = []

    if re.search(r"(?:\d+[%.％])", text):
        patterns.append(IntelligencePattern(pattern_type="quantitative", description="Contains numerical data/percentage"))

    if re.search(r"(?:例如|比如|举例|如：)", text):
        patterns.append(IntelligencePattern(pattern_type="example_based", description="Uses examples/illustrations"))

    if re.search(r"(?:对比|vs|相比|不同于)", text):
        patterns.append(IntelligencePattern(pattern_type="comparative", description="Uses comparison structure"))

    if re.search(r"(?:首先|其次|再次|最后|第一步|第二步)", text):
        patterns.append(IntelligencePattern(pattern_type="sequential", description="Uses step-by-step structure"))

    if re.search(r"(?:专家|分析师|业内人士|人士认为)", text):
        patterns.append(IntelligencePattern(pattern_type="expert_opinion", description="Cites expert opinions"))

    if re.search(r"(?:数据|统计|报告|调研)", text):
        patterns.append(IntelligencePattern(pattern_type="data_driven", description="Data-driven content"))

    return tuple(patterns)


def extract_intelligence(article: CleanedArticle) -> ArticleIntelligence:
    full_text = article.cleaned_excerpt or " ".join(article.paragraphs)

    entities = extract_entities(full_text)
    angles = extract_angles(full_text)
    claims = extract_claims(full_text)
    patterns = extract_patterns(full_text)

    return ArticleIntelligence(
        schema_version=SCHEMA_VERSION,
        entry_id=article.entry_id,
        source_id=article.source_id,
        title=article.title,
        link=article.link,
        excerpt=full_text[:500],
        entities=entities,
        angles=angles,
        claims=claims,
        patterns=patterns,
        do_not_copy_text=True,
    )


def extract_all_intelligence(articles: tuple[CleanedArticle, ...], run_date: str | None = None) -> IntelligenceReport:
    items: list[ArticleIntelligence] = []
    warnings: list[str] = []

    for article in articles:
        try:
            items.append(extract_intelligence(article))
        except Exception as exc:
            warnings.append(f"Failed to extract intelligence for {article.entry_id}: {exc}")

    return IntelligenceReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date or today_token(),
        input_count=len(articles),
        output_count=len(items),
        items=tuple(items),
        warnings=tuple(warnings),
    )


def report_to_dict(report: IntelligenceReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: IntelligenceReport) -> str:
    rows = []
    for index, item in enumerate(report.items, start=1):
        entities_str = ", ".join(f"{e.name}({e.entity_type})" for e in item.entities[:3]) or "-"
        angles_str = ", ".join(f"{a.angle_name}({int(a.confidence*100)}%)" for a in item.angles[:3]) or "-"
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    item.source_id,
                    str(len(item.entities)),
                    str(len(item.claims)),
                    entities_str,
                    angles_str,
                ]
            )
            + " |"
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"

    return f"""# WeChat Article Intelligence Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Input count: `{report.input_count}`
- Output count: `{report.output_count}`

## Intelligence Items

| # | Source | Entities | Claims | Top Entities | Top Angles |
|---:|---|:---:|:---:|---|---|
{chr(10).join(rows) if rows else '| 0 | - | 0 | 0 | - | - |'}

## Warnings

{warnings}

## Notes

- Entities: companies, models, people.
- Angles: 11 predefined angle categories with confidence scores.
- Claims: Rule-based extraction from claim patterns.
- Patterns: structural patterns like quantitative, example-based, etc.
- Only excerpts are analyzed (no full text).
- do_not_copy_text=True for all intelligence items.
"""


def write_report(report: IntelligenceReport, output_path: str) -> None:
    import json
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)


def load_report(json_path: str) -> IntelligenceReport | None:
    try:
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return IntelligenceReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            input_count=int(data.get("input_count", 0)),
            output_count=int(data.get("output_count", 0)),
            items=tuple(
                ArticleIntelligence(
                    schema_version=i.get("schema_version", SCHEMA_VERSION),
                    entry_id=i.get("entry_id", ""),
                    source_id=i.get("source_id", ""),
                    title=i.get("title", ""),
                    link=i.get("link", ""),
                    excerpt=i.get("excerpt", ""),
                    entities=tuple(
                        IntelligenceEntity(
                            entity_type=e.get("entity_type", ""),
                            name=e.get("name", ""),
                            confidence=float(e.get("confidence", 0.0)),
                        )
                        for e in i.get("entities", [])
                    ),
                    angles=tuple(
                        IntelligenceAngle(
                            angle_name=a.get("angle_name", ""),
                            confidence=float(a.get("confidence", 0.0)),
                        )
                        for a in i.get("angles", [])
                    ),
                    claims=tuple(
                        IntelligenceClaim(
                            claim_text=c.get("claim_text", ""),
                            evidence_text=c.get("evidence_text", ""),
                            confidence=float(c.get("confidence", 0.0)),
                        )
                        for c in i.get("claims", [])
                    ),
                    patterns=tuple(
                        IntelligencePattern(
                            pattern_type=p.get("pattern_type", ""),
                            description=p.get("description", ""),
                        )
                        for p in i.get("patterns", [])
                    ),
                    do_not_copy_text=bool(i.get("do_not_copy_text", True)),
                )
                for i in data.get("items", [])
            ),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None