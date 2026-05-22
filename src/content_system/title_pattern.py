"""Title Pattern Extractor v1."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class TitlePattern:
    pattern_id: str
    run_date: str
    pattern_type: str
    title: str
    source_context: str
    confidence: float
    reuse_guidance: str


@dataclass(frozen=True)
class TitlePatternReport:
    schema_version: str
    generated_at: str
    run_date: str
    pattern_count: int
    type_distribution: dict[str, int]
    patterns: tuple[TitlePattern, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def list_payload(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    raw = payload.get(key)
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def make_id(prefix: str, run_date: str, *parts: str) -> str:
    digest = hashlib.sha1("|".join((run_date, *parts)).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{run_date}_{digest}"


def collect_titles(paths: ProjectPaths) -> list[tuple[str, str]]:
    root = paths.market_content_root / "05_draft_packs"
    titles: list[tuple[str, str]] = []
    for item in list_payload(read_json(root / "latest_content_outlines.json"), "outlines"):
        for title in item.get("title_options", []) or []:
            if title:
                titles.append((str(title), "content_outlines.title_options"))
        if item.get("recommended_title"):
            titles.append((str(item.get("recommended_title")), "content_outlines.recommended_title"))
    for item in list_payload(read_json(root / "latest_content_drafts.json"), "drafts"):
        if item.get("recommended_title"):
            titles.append((str(item.get("recommended_title")), "content_drafts.recommended_title"))
    for item in list_payload(read_json(root / "latest_platform_packages.json"), "packages"):
        wechat = item.get("wechat") if isinstance(item.get("wechat"), dict) else {}
        xhs = item.get("xiaohongshu") if isinstance(item.get("xiaohongshu"), dict) else {}
        for title in (wechat.get("title"), xhs.get("title")):
            if title:
                titles.append((str(title), "platform_packages"))
    return list(dict.fromkeys(titles))[:80]


def classify_title(title: str) -> str:
    lower = title.lower()
    if "?" in title or "为什么" in title or "how" in lower:
        return "question" if "?" in title else "how_to" if "how" in lower else "why_now"
    if re.search(r"\b\d+\b|三|五|十", title):
        return "numbered_list"
    if " vs " in lower or "but" in lower or "不是" in title or "而是" in title:
        return "contrast"
    if any(word in lower for word in ("risk", "warning")) or "风险" in title:
        return "risk_warning"
    if any(company in lower for company in ("openai", "google", "nvidia", "meta", "anthropic", "microsoft", "databricks")):
        return "big_company"
    if any(word in lower for word in ("launch", "release", "new", "opportunity", "推出", "发布", "机会")):
        return "new_opportunity"
    if any(word in lower for word in ("trend", "signal", "趋势", "信号")):
        return "trend_signal"
    if any(word in lower for word in ("case", "客户", "案例")):
        return "case_study"
    return "trend_signal"


def build_title_pattern_report(paths: ProjectPaths) -> TitlePatternReport:
    run_date = today_token()
    titles = collect_titles(paths)
    patterns = tuple(
        TitlePattern(
            pattern_id=make_id("tpat", run_date, title),
            run_date=run_date,
            pattern_type=classify_title(title),
            title=title,
            source_context=context,
            confidence=0.72,
            reuse_guidance="Use this title form as a suggestion only; human editor should rewrite for accuracy and tone.",
        )
        for title, context in titles
    )
    distribution: dict[str, int] = {}
    for pattern in patterns:
        distribution[pattern.pattern_type] = distribution.get(pattern.pattern_type, 0) + 1
    warnings = () if titles else ("No titles found for extraction.",)
    return TitlePatternReport(SCHEMA_VERSION, utc_now(), run_date, len(patterns), dict(sorted(distribution.items())), patterns, warnings)


def report_to_dict(report: TitlePatternReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: TitlePatternReport) -> str:
    rows = [
        f"| {idx} | {item.pattern_type} | {item.confidence:.2f} | {item.title.replace('|', '\\|')} |"
        for idx, item in enumerate(report.patterns, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Title Patterns v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Patterns: `{report.pattern_count}`
- Distribution: `{report.type_distribution}`

## Patterns

| # | Type | Confidence | Title |
|---:|---|---:|---|
{chr(10).join(rows) if rows else '| 0 | - | 0 | None |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "08_learning_patterns"
    return {
        "dated_json": root / f"{run_date}__title-patterns.json",
        "dated_md": root / f"{run_date}__title-patterns.md",
        "latest_json": root / "latest_title_patterns.json",
        "latest_md": root / "latest_title_patterns.md",
    }


def write_title_pattern_report(report: TitlePatternReport, paths: ProjectPaths) -> dict[str, Path]:
    paths_by_name = output_paths(paths, report.run_date)
    for path in paths_by_name.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)
    for path in (paths_by_name["dated_json"], paths_by_name["latest_json"]):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (paths_by_name["dated_md"], paths_by_name["latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return paths_by_name
