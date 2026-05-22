"""Article Structure Pattern Extractor v1."""

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
class StructurePattern:
    pattern_id: str
    run_date: str
    pattern_type: str
    headings: tuple[str, ...]
    source_context: str
    confidence: float
    reuse_guidance: str


@dataclass(frozen=True)
class StructurePatternReport:
    schema_version: str
    generated_at: str
    run_date: str
    pattern_count: int
    type_distribution: dict[str, int]
    patterns: tuple[StructurePattern, ...]
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


def headings_from_markdown(text: str) -> tuple[str, ...]:
    headings = [match.group(1).strip() for match in re.finditer(r"^#{2,3}\s+(.+)$", text, flags=re.M)]
    return tuple(headings[:12])


def collect_structures(paths: ProjectPaths) -> list[tuple[tuple[str, ...], str]]:
    root = paths.market_content_root / "05_draft_packs"
    structures: list[tuple[tuple[str, ...], str]] = []
    for item in list_payload(read_json(root / "latest_content_drafts.json"), "drafts"):
        headings = headings_from_markdown(str((item.get("wechat_draft") or {}).get("body_markdown") or ""))
        if headings:
            structures.append((headings, "content_drafts.wechat"))
    for item in list_payload(read_json(root / "latest_platform_packages.json"), "packages"):
        headings = headings_from_markdown(str((item.get("wechat") or {}).get("body_markdown") or ""))
        if headings:
            structures.append((headings, "platform_packages.wechat"))
    for item in list_payload(read_json(root / "latest_content_outlines.json"), "outlines"):
        raw = item.get("wechat_outline") or item.get("structure") or []
        headings = tuple(str((entry or {}).get("heading") or (entry or {}).get("section") or "") for entry in raw if isinstance(entry, dict))
        if headings:
            structures.append((headings, "content_outlines"))
    return list(dict.fromkeys(structures))[:50]


def classify_structure(headings: tuple[str, ...]) -> str:
    joined = " ".join(headings).lower()
    if any(word in joined for word in ("how", "guide", "工具", "步骤")):
        return "tool_guide"
    if any(word in joined for word in ("technical", "model", "api", "技术", "模型")):
        return "technical_explainer"
    if any(word in joined for word in ("company", "公司", "企业")):
        return "company_breakdown"
    if any(word in joined for word in ("investment", "market", "机会", "风险")):
        return "investment_logic"
    if len(headings) >= 6:
        return "news_analysis"
    if any(word in joined for word in ("case", "案例")):
        return "case_study"
    if re.search(r"\d|三|五", joined):
        return "listicle"
    return "trend_analysis"


def build_structure_pattern_report(paths: ProjectPaths) -> StructurePatternReport:
    run_date = today_token()
    structures = collect_structures(paths)
    patterns = tuple(
        StructurePattern(
            pattern_id=make_id("spat", run_date, "|".join(headings)),
            run_date=run_date,
            pattern_type=classify_structure(headings),
            headings=headings,
            source_context=context,
            confidence=0.70,
            reuse_guidance="Use the section sequence as a structure suggestion only.",
        )
        for headings, context in structures
    )
    distribution: dict[str, int] = {}
    for pattern in patterns:
        distribution[pattern.pattern_type] = distribution.get(pattern.pattern_type, 0) + 1
    warnings = () if structures else ("No article structures found for extraction.",)
    return StructurePatternReport(SCHEMA_VERSION, utc_now(), run_date, len(patterns), dict(sorted(distribution.items())), patterns, warnings)


def report_to_dict(report: StructurePatternReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: StructurePatternReport) -> str:
    rows = [
        f"| {idx} | {item.pattern_type} | {item.confidence:.2f} | {' -> '.join(item.headings[:6]).replace('|', '\\|')} |"
        for idx, item in enumerate(report.patterns, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Structure Patterns v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Patterns: `{report.pattern_count}`
- Distribution: `{report.type_distribution}`

## Patterns

| # | Type | Confidence | Heading Flow |
|---:|---|---:|---|
{chr(10).join(rows) if rows else '| 0 | - | 0 | None |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "08_learning_patterns"
    return {
        "dated_json": root / f"{run_date}__structure-patterns.json",
        "dated_md": root / f"{run_date}__structure-patterns.md",
        "latest_json": root / "latest_structure_patterns.json",
        "latest_md": root / "latest_structure_patterns.md",
    }


def write_structure_pattern_report(report: StructurePatternReport, paths: ProjectPaths) -> dict[str, Path]:
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
