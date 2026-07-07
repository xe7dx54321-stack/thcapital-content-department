"""WeChat Style Pattern Extractor v1.

Extracts style patterns from articles, avoiding long text citations.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from content_system.wechat_article_cleaner import CleanedArticle


SCHEMA_VERSION = "v1"

STYLE_PATTERNS = {
    "bullet_list": {
        "pattern": r"(?:^\s*[-*•●○]\s+|\n\s*[-*•●○]\s+)",
        "description": "Uses bullet points",
    },
    "numbered_list": {
        "pattern": r"(?:^\s*\d+\.\s+|\n\s*\d+\.\s+)",
        "description": "Uses numbered lists",
    },
    "quote_block": {
        "pattern": r"(?:“[^”]+”|\"[^\"]+\"|「[^」]+」|『[^』]+』)",
        "description": "Contains quoted content",
    },
    "bold_text": {
        "pattern": r"(?:【[^】]+】|\[[^\]]+\]|\*\*[^\*]+\*\*|__[^_]+__)",
        "description": "Uses bold/emphasis markers",
    },
    "data_table": {
        "pattern": r"(?:\|\s*[\w\u4e00-\u9fff]+\s*\|)",
        "description": "Contains table structure",
    },
    "code_block": {
        "pattern": r"(?:`[^`]+`|```[\s\S]*?```)",
        "description": "Contains code blocks",
    },
    "image_reference": {
        "pattern": r"(?:图片|图\d+|附图|图表|截图)",
        "description": "References images or charts",
    },
    "link_reference": {
        "pattern": r"(?:链接|点击|跳转|查看原文)",
        "description": "References external links",
    },
    "question_lead": {
        "pattern": r"(?:^[？?].*|[？?]$)",
        "description": "Uses questions as lead-in",
    },
    "statistic_usage": {
        "pattern": r"(?:\d+[\.％%]\s*(?:增长|下降|占比|达到)|同比|环比)",
        "description": "Uses statistics and percentages",
    },
    "comparative_structure": {
        "pattern": r"(?:相比之下|与此相反|与之不同|一方面.*另一方面)",
        "description": "Uses comparative structures",
    },
    "cause_effect": {
        "pattern": r"(?:因此|导致|使得|由于|因为.*所以)",
        "description": "Uses cause-effect reasoning",
    },
    "temporal_sequence": {
        "pattern": r"(?:首先|其次|然后|最后|第一步|第二步)",
        "description": "Uses temporal sequence markers",
    },
    "expert_citation": {
        "pattern": r"(?:专家表示|分析师指出|业内人士认为|据.*透露)",
        "description": "Cites expert opinions",
    },
    "conclusion_marker": {
        "pattern": r"(?:综上所述|总而言之|总之|由此可见)",
        "description": "Uses conclusion markers",
    },
}


@dataclass(frozen=True)
class StylePattern:
    pattern_type: str
    description: str
    confidence: float
    match_count: int


@dataclass(frozen=True)
class StyleAnalysis:
    schema_version: str
    entry_id: str
    source_id: str
    title: str
    has_long_citation: bool
    citation_warning: str | None
    patterns: tuple[StylePattern, ...]
    dominant_patterns: tuple[str, ...]


@dataclass(frozen=True)
class StylePatternReport:
    schema_version: str
    generated_at: str
    run_date: str
    input_count: int
    analyses: tuple[StyleAnalysis, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def has_long_citation(text: str, max_length: int = 100) -> tuple[bool, str | None]:
    quote_patterns = [
        r"“([^”]+)”",
        r"\"([^\"]+)\"",
        r"「([^」]+)」",
        r"『([^』]+)』",
        r"> ([^\n]+)",
    ]

    for pattern in quote_patterns:
        for match in re.finditer(pattern, text):
            quote_content = match.group(1).strip()
            if len(quote_content) > max_length:
                return True, f"Long citation found: {quote_content[:50]}..."

    return False, None


def extract_patterns(text: str) -> tuple[StylePattern, ...]:
    patterns: list[StylePattern] = []

    for pattern_type, config in STYLE_PATTERNS.items():
        matches = list(re.finditer(config["pattern"], text))
        if matches:
            confidence = min(0.2 + (len(matches) * 0.08), 0.95)
            patterns.append(StylePattern(
                pattern_type=pattern_type,
                description=config["description"],
                confidence=confidence,
                match_count=len(matches),
            ))

    return tuple(sorted(patterns, key=lambda p: -p.confidence))


def analyze_style(article: CleanedArticle) -> StyleAnalysis:
    text = article.cleaned_excerpt or " ".join(article.paragraphs)

    has_long_cite, cite_warning = has_long_citation(text)
    patterns = extract_patterns(text)
    dominant_patterns = tuple(p.pattern_type for p in patterns[:3])

    return StyleAnalysis(
        schema_version=SCHEMA_VERSION,
        entry_id=article.entry_id,
        source_id=article.source_id,
        title=article.title,
        has_long_citation=has_long_cite,
        citation_warning=cite_warning,
        patterns=patterns,
        dominant_patterns=dominant_patterns,
    )


def analyze_all_styles(articles: tuple[CleanedArticle, ...], run_date: str | None = None) -> StylePatternReport:
    analyses: list[StyleAnalysis] = []
    warnings: list[str] = []

    for article in articles:
        try:
            analyses.append(analyze_style(article))
        except Exception as exc:
            warnings.append(f"Failed to analyze style for {article.entry_id}: {exc}")

    return StylePatternReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date or today_token(),
        input_count=len(articles),
        analyses=tuple(analyses),
        warnings=tuple(warnings),
    )


def report_to_dict(report: StylePatternReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: StylePatternReport) -> str:
    rows = []
    for index, analysis in enumerate(report.analyses, start=1):
        patterns_str = ", ".join(f"{p.pattern_type}({int(p.confidence*100)}%)" for p in analysis.patterns[:3]) or "-"
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    analysis.entry_id[:20] + "..." if len(analysis.entry_id) > 20 else analysis.entry_id,
                    analysis.source_id,
                    "YES" if analysis.has_long_citation else "NO",
                    str(len(analysis.patterns)),
                    patterns_str,
                ]
            )
            + " |"
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"

    pattern_list = "\n".join(f"- **{name}**: {config['description']}" for name, config in STYLE_PATTERNS.items())

    return f"""# WeChat Style Pattern Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Input count: `{report.input_count}`

## Style Analyses

| # | Entry ID | Source | Long Citation | Patterns | Top Patterns |
|---:|---|---|---|:---:|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | 0 | - |'}

## Available Patterns ({len(STYLE_PATTERNS)})

{pattern_list}

## Warnings

{warnings}

## Notes

- Long citations (>100 chars) are flagged for review.
- Pattern extraction is based on excerpt-level analysis only.
- do_not_copy_text=True for all style analyses.
"""


def write_report(report: StylePatternReport, output_path: str) -> None:
    import json
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)


def load_report(json_path: str) -> StylePatternReport | None:
    try:
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return StylePatternReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            input_count=int(data.get("input_count", 0)),
            analyses=tuple(
                StyleAnalysis(
                    schema_version=a.get("schema_version", SCHEMA_VERSION),
                    entry_id=a.get("entry_id", ""),
                    source_id=a.get("source_id", ""),
                    title=a.get("title", ""),
                    has_long_citation=bool(a.get("has_long_citation", False)),
                    citation_warning=a.get("citation_warning"),
                    patterns=tuple(
                        StylePattern(
                            pattern_type=p.get("pattern_type", ""),
                            description=p.get("description", ""),
                            confidence=float(p.get("confidence", 0.0)),
                            match_count=int(p.get("match_count", 0)),
                        )
                        for p in a.get("patterns", [])
                    ),
                    dominant_patterns=tuple(a.get("dominant_patterns", [])),
                )
                for a in data.get("analyses", [])
            ),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None