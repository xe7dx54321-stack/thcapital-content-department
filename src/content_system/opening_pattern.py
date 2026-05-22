"""Opening Pattern Extractor v1."""

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
class OpeningPattern:
    pattern_id: str
    run_date: str
    pattern_type: str
    opening_text: str
    source_context: str
    confidence: float
    reuse_guidance: str


@dataclass(frozen=True)
class OpeningPatternReport:
    schema_version: str
    generated_at: str
    run_date: str
    pattern_count: int
    type_distribution: dict[str, int]
    patterns: tuple[OpeningPattern, ...]
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


def strip_md(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"[#>*_`\\[\\]]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def first_paragraph(body: str) -> str:
    for part in re.split(r"\n\s*\n", body):
        cleaned = strip_md(part)
        if len(cleaned) > 30 and not cleaned.startswith("核心判断"):
            return cleaned[:400]
    return strip_md(body)[:400]


def collect_openings(paths: ProjectPaths) -> list[tuple[str, str]]:
    root = paths.market_content_root / "05_draft_packs"
    openings: list[tuple[str, str]] = []
    for item in list_payload(read_json(root / "latest_content_drafts.json"), "drafts"):
        body = str((item.get("wechat_draft") or {}).get("body_markdown") or "")
        if body:
            openings.append((first_paragraph(body), "content_drafts.wechat"))
    for item in list_payload(read_json(root / "latest_platform_packages.json"), "packages"):
        body = str((item.get("wechat") or {}).get("body_markdown") or "")
        if body:
            openings.append((first_paragraph(body), "platform_packages.wechat"))
    return [item for item in dict.fromkeys(openings) if item[0]][:50]


def classify_opening(text: str) -> str:
    lower = text.lower()
    if "?" in text or "为什么" in text:
        return "question_hook"
    if re.search(r"\d+|%|倍|万|亿", text):
        return "data_hook"
    if any(word in lower for word in ("problem", "pain", "challenge")) or "问题" in text:
        return "problem_solution"
    if any(word in lower for word in ("but", "however")) or "不是" in text:
        return "contrarian"
    if any(word in lower for word in ("summary", "核心判断")) or "核心判断" in text:
        return "executive_summary"
    if any(word in lower for word in ("trend", "signal")) or "趋势" in text or "信号" in text:
        return "trend_observation"
    if "场景" in text or "当你" in text:
        return "scenario_hook"
    return "news_first"


def build_opening_pattern_report(paths: ProjectPaths) -> OpeningPatternReport:
    run_date = today_token()
    openings = collect_openings(paths)
    patterns = tuple(
        OpeningPattern(
            pattern_id=make_id("opat", run_date, text[:100]),
            run_date=run_date,
            pattern_type=classify_opening(text),
            opening_text=text,
            source_context=context,
            confidence=0.68,
            reuse_guidance="Use as opening guidance only; rewrite manually for final tone.",
        )
        for text, context in openings
    )
    distribution: dict[str, int] = {}
    for pattern in patterns:
        distribution[pattern.pattern_type] = distribution.get(pattern.pattern_type, 0) + 1
    warnings = () if openings else ("No openings found for extraction.",)
    return OpeningPatternReport(SCHEMA_VERSION, utc_now(), run_date, len(patterns), dict(sorted(distribution.items())), patterns, warnings)


def report_to_dict(report: OpeningPatternReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: OpeningPatternReport) -> str:
    rows = [
        f"| {idx} | {item.pattern_type} | {item.confidence:.2f} | {item.opening_text[:120].replace('|', '\\|')} |"
        for idx, item in enumerate(report.patterns, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Opening Patterns v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Patterns: `{report.pattern_count}`
- Distribution: `{report.type_distribution}`

## Patterns

| # | Type | Confidence | Opening Preview |
|---:|---|---:|---|
{chr(10).join(rows) if rows else '| 0 | - | 0 | None |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "08_learning_patterns"
    return {
        "dated_json": root / f"{run_date}__opening-patterns.json",
        "dated_md": root / f"{run_date}__opening-patterns.md",
        "latest_json": root / "latest_opening_patterns.json",
        "latest_md": root / "latest_opening_patterns.md",
    }


def write_opening_pattern_report(report: OpeningPatternReport, paths: ProjectPaths) -> dict[str, Path]:
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
