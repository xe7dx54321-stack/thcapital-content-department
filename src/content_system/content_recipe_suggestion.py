"""Content Recipe Suggestion v1."""

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
class ContentRecipeSuggestion:
    schema_version: str
    suggestion_id: str
    run_date: str
    recipe_area: str
    target_content_type: str
    target_platform: str
    suggested_pattern: str
    why_useful: str
    example_application: str
    risk_notes: tuple[str, ...]
    auto_apply: bool


@dataclass(frozen=True)
class ContentRecipeSuggestionReport:
    schema_version: str
    generated_at: str
    run_date: str
    suggestion_count: int
    suggestions: tuple[ContentRecipeSuggestion, ...]
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


def suggestion(run_date: str, area: str, content_type: str, platform: str, pattern: str, why: str, example: str) -> ContentRecipeSuggestion:
    return ContentRecipeSuggestion(
        schema_version=SCHEMA_VERSION,
        suggestion_id=make_id("crs", run_date, area, content_type, platform, pattern),
        run_date=run_date,
        recipe_area=area,
        target_content_type=content_type,
        target_platform=platform,
        suggested_pattern=pattern,
        why_useful=why,
        example_application=example,
        risk_notes=("Pattern suggestion only; do not auto-apply.", "Human editor should verify fit and originality."),
        auto_apply=False,
    )


def build_content_recipe_suggestion_report(paths: ProjectPaths) -> ContentRecipeSuggestionReport:
    root = paths.market_content_root / "08_learning_patterns"
    run_date = today_token()
    title_patterns = list_payload(read_json(root / "latest_title_patterns.json"), "patterns")
    opening_patterns = list_payload(read_json(root / "latest_opening_patterns.json"), "patterns")
    structure_patterns = list_payload(read_json(root / "latest_structure_patterns.json"), "patterns")
    suggestions: list[ContentRecipeSuggestion] = []
    if title_patterns:
        pattern = str(title_patterns[0].get("pattern_type") or "why_now")
        suggestions.append(suggestion(run_date, "title", "deep_analysis", "multi", pattern, "Use a proven title framing from recent candidate assets.", "Turn the strongest evidence-backed update into a why-now title."))
    if opening_patterns:
        pattern = str(opening_patterns[0].get("pattern_type") or "news_first")
        suggestions.append(suggestion(run_date, "opening", "deep_analysis", "wechat", pattern, "A concrete opening reduces vague analysis and keeps evidence visible.", "Start with the event, then state why it matters for Agent builders."))
    if structure_patterns:
        pattern = str(structure_patterns[0].get("pattern_type") or "news_analysis")
        suggestions.append(suggestion(run_date, "structure", "deep_analysis", "wechat", pattern, "A stable section sequence helps human editors review quickly.", "Use What happened -> Why it matters -> Evidence -> Risks -> Next watch."))
    suggestions.append(suggestion(run_date, "platform", "short_post", "xiaohongshu", "three_takeaway_card", "Short-form packaging needs concise collection value.", "Convert each brief into one strong claim plus three takeaways and a question."))
    warnings = () if (title_patterns or opening_patterns or structure_patterns) else ("No extracted patterns found; emitted starter recipe suggestions.",)
    return ContentRecipeSuggestionReport(SCHEMA_VERSION, utc_now(), run_date, len(suggestions), tuple(suggestions), warnings)


def report_to_dict(report: ContentRecipeSuggestionReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: ContentRecipeSuggestionReport) -> str:
    rows = [
        f"| {idx} | {item.recipe_area} | {item.target_content_type} | {item.target_platform} | {item.suggested_pattern.replace('|', '\\|')} |"
        for idx, item in enumerate(report.suggestions, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Content Recipe Suggestions v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Suggestions: `{report.suggestion_count}`

## Suggestions

| # | Area | Content Type | Platform | Pattern |
|---:|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | None |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "08_learning_patterns"
    return {
        "dated_json": root / f"{run_date}__content-recipe-suggestions.json",
        "dated_md": root / f"{run_date}__content-recipe-suggestions.md",
        "latest_json": root / "latest_content_recipe_suggestions.json",
        "latest_md": root / "latest_content_recipe_suggestions.md",
    }


def write_content_recipe_suggestion_report(report: ContentRecipeSuggestionReport, paths: ProjectPaths) -> dict[str, Path]:
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
