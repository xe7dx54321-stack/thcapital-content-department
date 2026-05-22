"""Pattern-to-Brief / Pattern-to-Outline Adapter v1."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class PatternAdapter:
    schema_version: str
    adapter_id: str
    run_date: str
    brief_id: str
    outline_id: str
    recommended_title_patterns: tuple[str, ...]
    recommended_opening_patterns: tuple[str, ...]
    recommended_structure_patterns: tuple[str, ...]
    suggested_brief_improvements: tuple[str, ...]
    suggested_outline_improvements: tuple[str, ...]
    platform_specific_notes: dict[str, tuple[str, ...]]
    auto_apply: bool


@dataclass(frozen=True)
class PatternAdapterReport:
    schema_version: str
    generated_at: str
    run_date: str
    adapter_count: int
    adapters: tuple[PatternAdapter, ...]
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


def by_key(items: list[dict[str, Any]], field: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(field)): item for item in items if item.get(field)}


def pattern_names(items: list[dict[str, Any]], field: str = "pattern_type", limit: int = 3) -> tuple[str, ...]:
    values = []
    for item in items:
        value = str(item.get(field) or item.get("suggested_pattern") or "")
        if value and value not in values:
            values.append(value)
    return tuple(values[:limit])


def build_pattern_adapter_report(paths: ProjectPaths) -> PatternAdapterReport:
    draft_root = paths.market_content_root / "05_draft_packs"
    pattern_root = paths.market_content_root / "08_learning_patterns"
    run_date = today_token()
    briefs = list_payload(read_json(draft_root / "latest_content_briefs.json"), "briefs")
    outlines = by_key(list_payload(read_json(draft_root / "latest_content_outlines.json"), "outlines"), "brief_id")
    title_patterns = list_payload(read_json(pattern_root / "latest_title_patterns.json"), "patterns")
    opening_patterns = list_payload(read_json(pattern_root / "latest_opening_patterns.json"), "patterns")
    structure_patterns = list_payload(read_json(pattern_root / "latest_structure_patterns.json"), "patterns")
    recipes = list_payload(read_json(pattern_root / "latest_content_recipe_suggestions.json"), "suggestions")

    title_names = pattern_names(title_patterns)
    opening_names = pattern_names(opening_patterns)
    structure_names = pattern_names(structure_patterns)
    recipe_notes = tuple(str(item.get("suggested_pattern")) for item in recipes[:3] if item.get("suggested_pattern"))
    adapters: list[PatternAdapter] = []
    for brief in briefs:
        outline = outlines.get(str(brief.get("brief_id")), {})
        brief_id = str(brief.get("brief_id") or "")
        outline_id = str(outline.get("outline_id") or "")
        adapters.append(
            PatternAdapter(
                schema_version=SCHEMA_VERSION,
                adapter_id=make_id("pad", run_date, brief_id, outline_id),
                run_date=run_date,
                brief_id=brief_id,
                outline_id=outline_id,
                recommended_title_patterns=title_names,
                recommended_opening_patterns=opening_names,
                recommended_structure_patterns=structure_names,
                suggested_brief_improvements=(
                    "Add one explicit pattern guidance note to the brief before drafting.",
                    "Use recipe suggestions as optional angle prompts, not automatic rewrites.",
                )
                + recipe_notes[:1],
                suggested_outline_improvements=(
                    "Check whether the outline starts with a concrete event before interpretation.",
                    "Keep evidence expansion and risk section visible.",
                ),
                platform_specific_notes={
                    "wechat": ("Prefer a news-analysis or technical-explainer structure.",),
                    "xiaohongshu": ("Compress into one claim, three takeaways, and one interaction question.",),
                },
                auto_apply=False,
            )
        )
    warnings = () if briefs else ("No content briefs available for pattern adapters.",)
    return PatternAdapterReport(SCHEMA_VERSION, utc_now(), run_date, len(adapters), tuple(adapters), warnings)


def report_to_dict(report: PatternAdapterReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: PatternAdapterReport) -> str:
    rows = [
        f"| {idx} | {item.brief_id} | {item.outline_id} | {', '.join(item.recommended_title_patterns)} | {', '.join(item.recommended_structure_patterns)} |"
        for idx, item in enumerate(report.adapters, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Pattern Adapters v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Adapters: `{report.adapter_count}`

## Adapters

| # | Brief | Outline | Title Patterns | Structure Patterns |
|---:|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | - |'}

## Policy

- Pattern adapters only generate recommendations.
- They do not rewrite briefs or outlines automatically.

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "08_learning_patterns"
    return {
        "dated_json": root / f"{run_date}__pattern-adapters.json",
        "dated_md": root / f"{run_date}__pattern-adapters.md",
        "latest_json": root / "latest_pattern_adapters.json",
        "latest_md": root / "latest_pattern_adapters.md",
    }


def write_pattern_adapter_report(report: PatternAdapterReport, paths: ProjectPaths) -> dict[str, Path]:
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
