"""WeChat RSS Usage Boundary Gate v1.

Enforces usage boundaries and safety checks for WeChat RSS ingestion.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


SCHEMA_VERSION = "v1"

BOUNDARY_RULES = {
    "no_full_text": {
        "description": "Only excerpts allowed; no full article text extraction",
        "max_length": 500,
    },
    "no_web_scraping": {
        "description": "No additional web page fetching beyond RSS feed",
        "allowed_hosts": {"wechat.rsshub.app", "rsshub.app"},
    },
    "do_not_copy_text": {
        "description": "All content must have do_not_copy_text=True",
    },
    "no_hard_evidence_from_media": {
        "description": "Regular media sources cannot be used as hard evidence",
    },
    "rate_limit": {
        "description": "Max 100 articles per run",
        "max_articles": 100,
    },
    "source_validation": {
        "description": "All sources must be validated and enabled",
    },
}


@dataclass(frozen=True)
class BoundaryCheckResult:
    rule_id: str
    passed: bool
    message: str
    details: dict[str, Any]


@dataclass(frozen=True)
class BoundaryGateReport:
    schema_version: str
    generated_at: str
    run_date: str
    dry_run: bool
    all_passed: bool
    check_results: tuple[BoundaryCheckResult, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def check_no_full_text(articles: Any) -> BoundaryCheckResult:
    max_length = BOUNDARY_RULES["no_full_text"]["max_length"]
    violations = []

    if isinstance(articles, list):
        for index, article in enumerate(articles):
            excerpt = ""
            if isinstance(article, dict):
                excerpt = str(article.get("excerpt", "") or article.get("cleaned_excerpt", ""))
            elif hasattr(article, "excerpt"):
                excerpt = str(article.excerpt)
            elif hasattr(article, "cleaned_excerpt"):
                excerpt = str(article.cleaned_excerpt)

            if len(excerpt) > max_length:
                violations.append(f"Article {index}: excerpt length {len(excerpt)} > {max_length}")

    if violations:
        return BoundaryCheckResult(
            rule_id="no_full_text",
            passed=False,
            message=f"Found {len(violations)} articles with full text (excerpt > {max_length} chars)",
            details={"violations": violations},
        )

    return BoundaryCheckResult(
        rule_id="no_full_text",
        passed=True,
        message="All articles use excerpts only",
        details={"max_length": max_length, "article_count": len(articles) if isinstance(articles, list) else 0},
    )


def check_do_not_copy_text(articles: Any) -> BoundaryCheckResult:
    violations = []

    if isinstance(articles, list):
        for index, article in enumerate(articles):
            do_not_copy = False
            if isinstance(article, dict):
                do_not_copy = bool(article.get("do_not_copy_text", False))
            elif hasattr(article, "do_not_copy_text"):
                do_not_copy = bool(article.do_not_copy_text)

            if not do_not_copy:
                violations.append(f"Article {index}: do_not_copy_text is False")

    if violations:
        return BoundaryCheckResult(
            rule_id="do_not_copy_text",
            passed=False,
            message=f"Found {len(violations)} articles without do_not_copy_text=True",
            details={"violations": violations},
        )

    return BoundaryCheckResult(
        rule_id="do_not_copy_text",
        passed=True,
        message="All articles have do_not_copy_text=True",
        details={"article_count": len(articles) if isinstance(articles, list) else 0},
    )


def check_rate_limit(articles: Any) -> BoundaryCheckResult:
    max_articles = BOUNDARY_RULES["rate_limit"]["max_articles"]
    count = len(articles) if isinstance(articles, list) else 0

    if count > max_articles:
        return BoundaryCheckResult(
            rule_id="rate_limit",
            passed=False,
            message=f"Article count {count} exceeds limit of {max_articles}",
            details={"article_count": count, "max_articles": max_articles},
        )

    return BoundaryCheckResult(
        rule_id="rate_limit",
        passed=True,
        message=f"Article count {count} within limit of {max_articles}",
        details={"article_count": count, "max_articles": max_articles},
    )


def check_no_hard_evidence_from_media(evidence_items: Any) -> BoundaryCheckResult:
    violations = []

    if isinstance(evidence_items, list):
        for index, item in enumerate(evidence_items):
            is_hard = False
            is_media = False

            if isinstance(item, dict):
                is_hard = bool(item.get("is_hard_evidence", False))
                source_id = str(item.get("source_id", ""))
                is_media = any(kw in source_id.lower() for kw in ("media", "news", "资讯", "报道", "公众号"))
            elif hasattr(item, "is_hard_evidence"):
                is_hard = bool(item.is_hard_evidence)
                source_id = str(item.source_id) if hasattr(item, "source_id") else ""
                is_media = any(kw in source_id.lower() for kw in ("media", "news", "资讯", "报道", "公众号"))

            if is_hard and is_media:
                violations.append(f"Evidence {index}: media source marked as hard evidence")

    if violations:
        return BoundaryCheckResult(
            rule_id="no_hard_evidence_from_media",
            passed=False,
            message=f"Found {len(violations)} media sources incorrectly marked as hard evidence",
            details={"violations": violations},
        )

    return BoundaryCheckResult(
        rule_id="no_hard_evidence_from_media",
        passed=True,
        message="No media sources incorrectly marked as hard evidence",
        details={"evidence_count": len(evidence_items) if isinstance(evidence_items, list) else 0},
    )


def check_dry_run_safety(dry_run: bool) -> BoundaryCheckResult:
    if dry_run:
        return BoundaryCheckResult(
            rule_id="dry_run_safety",
            passed=True,
            message="Dry-run mode: no actual HTTP requests will be made",
            details={"dry_run": True},
        )

    return BoundaryCheckResult(
        rule_id="dry_run_safety",
        passed=True,
        message="Live mode: HTTP requests will be made",
        details={"dry_run": False},
    )


def run_boundary_check(
    articles: Any = None,
    evidence_items: Any = None,
    dry_run: bool = False,
    run_date: str | None = None,
) -> BoundaryGateReport:
    check_results: list[BoundaryCheckResult] = []
    warnings: list[str] = []

    check_results.append(check_no_full_text(articles))
    check_results.append(check_do_not_copy_text(articles))
    check_results.append(check_rate_limit(articles))
    check_results.append(check_no_hard_evidence_from_media(evidence_items))
    check_results.append(check_dry_run_safety(dry_run))

    all_passed = all(result.passed for result in check_results)

    if not all_passed:
        failed_rules = [r.rule_id for r in check_results if not r.passed]
        warnings.append(f"Boundary check failed for rules: {', '.join(failed_rules)}")

    return BoundaryGateReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date or today_token(),
        dry_run=dry_run,
        all_passed=all_passed,
        check_results=tuple(check_results),
        warnings=tuple(warnings),
    )


def report_to_dict(report: BoundaryGateReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: BoundaryGateReport) -> dict[str, Any]:
    rows = []
    for result in report.check_results:
        rows.append(
            "| "
            + " | ".join(
                [
                    result.rule_id,
                    "PASS" if result.passed else "FAIL",
                    result.message,
                ]
            )
            + " |"
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"

    return f"""# WeChat RSS Usage Boundary Gate Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Dry run: `{report.dry_run}`
- Overall status: `{'PASS' if report.all_passed else 'FAIL'}`

## Boundary Checks

| Rule | Status | Message |
|:---|:---:|---|
{chr(10).join(rows)}

## Warnings

{warnings}

## Boundary Rules Summary

- **no_full_text**: Excerpts only, max 500 characters
- **no_web_scraping**: No additional web page fetching beyond RSS
- **do_not_copy_text**: All articles must have do_not_copy_text=True
- **no_hard_evidence_from_media**: Media sources cannot be hard evidence
- **rate_limit**: Max 100 articles per run

## Notes

- Boundary checks prevent data misuse and compliance violations.
- Failed checks should be resolved before proceeding with content production.
"""


def write_report(report: BoundaryGateReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)


def load_report(json_path: str) -> BoundaryGateReport | None:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return BoundaryGateReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            dry_run=bool(data.get("dry_run", False)),
            all_passed=bool(data.get("all_passed", False)),
            check_results=tuple(
                BoundaryCheckResult(
                    rule_id=r.get("rule_id", ""),
                    passed=bool(r.get("passed", False)),
                    message=r.get("message", ""),
                    details=r.get("details", {}),
                )
                for r in data.get("check_results", [])
            ),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None


def assert_boundaries(report: BoundaryGateReport) -> None:
    if not report.all_passed:
        failed = [r for r in report.check_results if not r.passed]
        messages = "\n".join(f"- {r.rule_id}: {r.message}" for r in failed)
        raise RuntimeError(f"WeChat RSS boundary check failed:\n{messages}")