"""WeChat Article Cleaner v1.

Cleans HTML content, removes ads, and preserves paragraph structure while
keeping excerpts only (no full text).
"""

from __future__ import annotations

import html
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from content_system.wechat_rss_ingestion import RssEntry


SCHEMA_VERSION = "v1"

AD_PATTERNS = (
    r"(?i)(?:广告|推广|赞助商|sponsored|advertisement|广告时间|插播广告)",
    r"(?i)(?:关注.*公众号|扫码.*关注|长按.*识别)",
    r"(?i)(?:添加.*微信|微信号|wechat.*id)",
    r"(?i)(?:下载.*App|下载.*应用|点击.*下载)",
    r"(?i)(?:淘宝|京东|拼多多|购物|优惠券|返利)",
    r"(?i)(?:原文链接|阅读原文|查看原文)",
    r"(?i)(?:免责声明|本文.*不构成|投资.*建议)",
)

PRESERVED_TAGS = {"p", "div", "span", "strong", "em", "b", "i", "br"}


@dataclass(frozen=True)
class CleanedArticle:
    schema_version: str
    entry_id: str
    source_id: str
    title: str
    link: str
    cleaned_excerpt: str
    paragraphs: tuple[str, ...]
    ad_removed: bool
    do_not_copy_text: bool = True


@dataclass(frozen=True)
class ArticleCleanerReport:
    schema_version: str
    generated_at: str
    run_date: str
    input_count: int
    output_count: int
    articles: tuple[CleanedArticle, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def remove_html_tags(text: str, preserve: set[str] | None = None) -> str:
    tags_to_preserve = PRESERVED_TAGS if preserve is None else preserve
    pattern = re.compile(r"<(\/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>")

    def replacer(match: re.Match[str]) -> str:
        tag = match.group(2).lower()
        if tag in tags_to_preserve:
            return match.group(0)
        return ""

    return pattern.sub(replacer, text)


def remove_ads(text: str) -> tuple[str, bool]:
    has_ad = False
    for pattern in AD_PATTERNS:
        if re.search(pattern, text):
            has_ad = True
            text = re.sub(pattern, "", text)
    return text, has_ad


def remove_excessive_whitespace(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(<br\s*/?>)\s+", r"\1", text)
    text = re.sub(r"\s+(</p>)", r"\1", text)
    text = re.sub(r"(<p[^>]*>)\s+", r"\1", text)
    return text.strip()


def extract_paragraphs(text: str) -> tuple[str, ...]:
    paragraphs: list[str] = []
    text = remove_html_tags(text, preserve={"p", "br"})

    for para_match in re.finditer(r"<p[^>]*>(.*?)</p>", text, re.DOTALL | re.IGNORECASE):
        para_text = para_match.group(1).strip()
        if para_text:
            paragraphs.append(remove_excessive_whitespace(para_text))

    if not paragraphs:
        for line in re.split(r"<br\s*/?>|\n", text):
            stripped = line.strip()
            if stripped:
                paragraphs.append(stripped)

    return tuple(p for p in paragraphs if len(p) >= 10)


def clean_excerpt(excerpt: str) -> str:
    cleaned = html.unescape(excerpt)
    cleaned = remove_html_tags(cleaned)
    cleaned, _ = remove_ads(cleaned)
    cleaned = remove_excessive_whitespace(cleaned)
    return cleaned


def clean_article(entry: RssEntry) -> CleanedArticle:
    cleaned_text, ad_removed = remove_ads(entry.excerpt)
    cleaned_text = html.unescape(cleaned_text)
    cleaned_text = remove_excessive_whitespace(cleaned_text)
    paragraphs = extract_paragraphs(cleaned_text)

    if not paragraphs:
        paragraphs = (cleaned_text,) if cleaned_text else ()

    return CleanedArticle(
        schema_version=SCHEMA_VERSION,
        entry_id=entry.entry_id,
        source_id=entry.source_id,
        title=entry.title,
        link=entry.link,
        cleaned_excerpt=cleaned_text[:500],
        paragraphs=paragraphs,
        ad_removed=ad_removed,
        do_not_copy_text=True,
    )


def clean_all_articles(entries: tuple[RssEntry, ...], run_date: str | None = None) -> ArticleCleanerReport:
    cleaned: list[CleanedArticle] = []
    warnings: list[str] = []

    for entry in entries:
        try:
            cleaned.append(clean_article(entry))
        except Exception as exc:
            warnings.append(f"Failed to clean {entry.entry_id}: {exc}")

    return ArticleCleanerReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date or today_token(),
        input_count=len(entries),
        output_count=len(cleaned),
        articles=tuple(cleaned),
        warnings=tuple(warnings),
    )


def report_to_dict(report: ArticleCleanerReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: ArticleCleanerReport) -> str:
    rows = []
    for index, article in enumerate(report.articles, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    article.source_id,
                    "AD REMOVED" if article.ad_removed else "clean",
                    str(len(article.paragraphs)),
                    article.title[:50] + "..." if len(article.title) > 50 else article.title,
                ]
            )
            + " |"
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"

    return f"""# WeChat Article Cleaner Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Input count: `{report.input_count}`
- Output count: `{report.output_count}`

## Articles

| # | Source | Status | Paragraphs | Title |
|---:|---|---|:---:|---|
{chr(10).join(rows) if rows else '| 0 | - | - | 0 | None |'}

## Warnings

{warnings}

## Notes

- HTML tags are removed except paragraph structure.
- Ad patterns and promotional content are filtered.
- Only excerpts are cleaned (no full text).
- do_not_copy_text=True for all cleaned articles.
"""


def write_report(report: ArticleCleanerReport, output_path: str) -> None:
    import json
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)


def load_report(json_path: str) -> ArticleCleanerReport | None:
    try:
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return ArticleCleanerReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            input_count=int(data.get("input_count", 0)),
            output_count=int(data.get("output_count", 0)),
            articles=tuple(
                CleanedArticle(
                    schema_version=a.get("schema_version", SCHEMA_VERSION),
                    entry_id=a.get("entry_id", ""),
                    source_id=a.get("source_id", ""),
                    title=a.get("title", ""),
                    link=a.get("link", ""),
                    cleaned_excerpt=a.get("cleaned_excerpt", ""),
                    paragraphs=tuple(a.get("paragraphs", [])),
                    ad_removed=bool(a.get("ad_removed", False)),
                    do_not_copy_text=bool(a.get("do_not_copy_text", True)),
                )
                for a in data.get("articles", [])
            ),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None