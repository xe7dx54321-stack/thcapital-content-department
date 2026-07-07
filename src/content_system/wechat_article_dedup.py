"""WeChat Article Deduplication v1.

Deduplicates articles by URL, title, and content similarity.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from content_system.wechat_article_cleaner import CleanedArticle


SCHEMA_VERSION = "v1"

TITLE_SIMILARITY_THRESHOLD = 0.8
CONTENT_SIMILARITY_THRESHOLD = 0.7


@dataclass(frozen=True)
class DedupResult:
    schema_version: str
    entry_id: str
    source_id: str
    title: str
    link: str
    is_duplicate: bool
    duplicate_of: str | None
    duplicate_reason: str | None
    do_not_copy_text: bool = True


@dataclass(frozen=True)
class DedupReport:
    schema_version: str
    generated_at: str
    run_date: str
    input_count: int
    unique_count: int
    duplicate_count: int
    results: tuple[DedupResult, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def jaccard_similarity(a: str, b: str) -> float:
    a_norm = normalize_text(a)
    b_norm = normalize_text(b)

    if not a_norm or not b_norm:
        return 0.0

    a_tokens = set(a_norm.split())
    b_tokens = set(b_norm.split())

    if not a_tokens and not b_tokens:
        return 1.0

    intersection = a_tokens & b_tokens
    union = a_tokens | b_tokens

    return len(intersection) / max(len(union), 1)


def text_hash(text: str) -> str:
    normalized = normalize_text(text)
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]


def url_hash(url: str) -> str:
    normalized = url.lower().strip()
    normalized = re.sub(r"[\?#].*$", "", normalized)
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]


def is_url_duplicate(url: str, seen_urls: set[str]) -> tuple[bool, str | None]:
    h = url_hash(url)
    if h in seen_urls:
        return True, h
    return False, None


def is_title_duplicate(title: str, seen_titles: dict[str, str]) -> tuple[bool, str | None]:
    for existing_hash, existing_title in seen_titles.items():
        if jaccard_similarity(title, existing_title) >= TITLE_SIMILARITY_THRESHOLD:
            return True, existing_hash
    return False, None


def is_content_duplicate(content: str, seen_contents: dict[str, str]) -> tuple[bool, str | None]:
    for existing_hash, existing_content in seen_contents.items():
        if jaccard_similarity(content, existing_content) >= CONTENT_SIMILARITY_THRESHOLD:
            return True, existing_hash
    return False, None


def deduplicate_articles(articles: tuple[CleanedArticle, ...], run_date: str | None = None) -> DedupReport:
    results: list[DedupResult] = []
    warnings: list[str] = []

    seen_urls: set[str] = set()
    seen_titles: dict[str, str] = {}
    seen_contents: dict[str, str] = {}

    for article in articles:
        is_dup = False
        dup_of = None
        dup_reason = None

        url_dup, url_h = is_url_duplicate(article.link, seen_urls)
        if url_dup:
            is_dup = True
            dup_of = url_h
            dup_reason = "url_match"
        else:
            seen_urls.add(url_hash(article.link))

            title_dup, title_h = is_title_duplicate(article.title, seen_titles)
            if title_dup:
                is_dup = True
                dup_of = title_h
                dup_reason = "title_similarity"
            else:
                title_h = text_hash(article.title)
                seen_titles[title_h] = article.title

                content = article.cleaned_excerpt or " ".join(article.paragraphs)
                content_dup, content_h = is_content_duplicate(content, seen_contents)
                if content_dup:
                    is_dup = True
                    dup_of = content_h
                    dup_reason = "content_similarity"
                else:
                    content_h = text_hash(content)
                    seen_contents[content_h] = content

        results.append(
            DedupResult(
                schema_version=SCHEMA_VERSION,
                entry_id=article.entry_id,
                source_id=article.source_id,
                title=article.title,
                link=article.link,
                is_duplicate=is_dup,
                duplicate_of=dup_of,
                duplicate_reason=dup_reason,
                do_not_copy_text=True,
            )
        )

    unique_count = sum(1 for r in results if not r.is_duplicate)
    duplicate_count = sum(1 for r in results if r.is_duplicate)

    return DedupReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date or today_token(),
        input_count=len(articles),
        unique_count=unique_count,
        duplicate_count=duplicate_count,
        results=tuple(results),
        warnings=tuple(warnings),
    )


def get_unique_results(report: DedupReport) -> tuple[DedupResult, ...]:
    return tuple(r for r in report.results if not r.is_duplicate)


def report_to_dict(report: DedupReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: DedupReport) -> str:
    rows = []
    for index, result in enumerate(report.results, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    "DUPLICATE" if result.is_duplicate else "UNIQUE",
                    result.duplicate_reason or "-",
                    result.source_id,
                    result.title[:50] + "..." if len(result.title) > 50 else result.title,
                ]
            )
            + " |"
        )

    return f"""# WeChat Article Deduplication Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Input count: `{report.input_count}`
- Unique: `{report.unique_count}`
- Duplicates: `{report.duplicate_count}`

## Results

| # | Status | Reason | Source | Title |
|---:|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | None |'}

## Notes

- Deduplication checks: URL exact match → Title similarity ({int(TITLE_SIMILARITY_THRESHOLD*100)}%) → Content similarity ({int(CONTENT_SIMILARITY_THRESHOLD*100)}%).
- Only excerpts are compared (no full text).
- do_not_copy_text=True for all results.
"""


def write_report(report: DedupReport, output_path: str) -> None:
    import json
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)


def load_report(json_path: str) -> DedupReport | None:
    try:
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return DedupReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            input_count=int(data.get("input_count", 0)),
            unique_count=int(data.get("unique_count", 0)),
            duplicate_count=int(data.get("duplicate_count", 0)),
            results=tuple(
                DedupResult(
                    schema_version=r.get("schema_version", SCHEMA_VERSION),
                    entry_id=r.get("entry_id", ""),
                    source_id=r.get("source_id", ""),
                    title=r.get("title", ""),
                    link=r.get("link", ""),
                    is_duplicate=bool(r.get("is_duplicate", False)),
                    duplicate_of=r.get("duplicate_of"),
                    duplicate_reason=r.get("duplicate_reason"),
                    do_not_copy_text=bool(r.get("do_not_copy_text", True)),
                )
                for r in data.get("results", [])
            ),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None