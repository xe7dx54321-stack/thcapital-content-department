"""Head Media Pattern Library v1."""

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
class HeadMediaPattern:
    pattern_id: str
    pattern_type: str
    source_context: str
    pattern_name: str
    pattern_description: str
    example_text: str
    applicable_platforms: tuple[str, ...]
    applicable_content_types: tuple[str, ...]
    strength: str
    reuse_guidance: str
    risk_notes: tuple[str, ...]


@dataclass(frozen=True)
class HeadMediaPatternLibrary:
    schema_version: str
    updated_at: str
    patterns: tuple[HeadMediaPattern, ...]
    summary: dict[str, int]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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


def make_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def strip_md(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[#>*_`\\[\\]]", "", text)).strip()


def collect_examples(paths: ProjectPaths, max_items: int = 30) -> list[dict[str, str]]:
    examples: list[dict[str, str]] = []
    draft_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_content_drafts.json")
    package_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_platform_packages.json")
    outline_payload = read_json(paths.market_content_root / "05_draft_packs" / "latest_content_outlines.json")
    for draft in list_payload(draft_payload, "drafts"):
        body = ((draft.get("wechat_draft") or {}).get("body_markdown") or "")
        examples.append({"context": "latest_content_drafts", "title": str(draft.get("recommended_title") or ""), "body": str(body)})
    for package in list_payload(package_payload, "packages"):
        wechat = package.get("wechat") if isinstance(package.get("wechat"), dict) else {}
        examples.append({"context": "latest_platform_packages", "title": str(wechat.get("title") or ""), "body": str(wechat.get("body_markdown") or "")})
    for outline in list_payload(outline_payload, "outlines"):
        examples.append({"context": "latest_content_outlines", "title": str(outline.get("recommended_title") or ""), "body": json.dumps(outline.get("structure") or [], ensure_ascii=False)})
    return examples[:max_items]


def default_patterns(examples: list[dict[str, str]]) -> list[HeadMediaPattern]:
    first_title = next((item["title"] for item in examples if item.get("title")), "AI/Agent trend signal")
    first_body = next((strip_md(item["body"])[:220] for item in examples if item.get("body")), "Start with the concrete event before interpretation.")
    raw = [
        ("title", "Big company + concrete move", first_title, "Use a recognizable company or model with a concrete action."),
        ("title", "Why now angle", first_title, "Explain why the signal matters today, not as evergreen commentary."),
        ("opening", "News first then interpretation", first_body, "Open with what happened, then move into why it matters."),
        ("opening", "Executive summary hook", first_body, "Summarize the core judgment before evidence expansion."),
        ("structure", "News analysis ladder", "What happened -> why it matters -> evidence -> risks -> next watch", "A stable WeChat structure for AI/Agent official updates."),
        ("structure", "Evidence-first explainer", "Claim -> source evidence -> technical implication -> market implication", "Keep claims bounded by evidence and source authority."),
        ("angle", "Agent workflow relevance", first_title, "Connect product/model updates to agent workflow adoption."),
        ("platform", "Dual-platform package", "WeChat depth + Xiaohongshu concise takeaways", "Prepare long-form analysis and short-form key points together."),
    ]
    patterns: list[HeadMediaPattern] = []
    for pattern_type, name, example, desc in raw:
        patterns.append(
            HeadMediaPattern(
                pattern_id=make_id("pat", pattern_type, name, example[:80]),
                pattern_type=pattern_type,
                source_context="phase2_generated_assets",
                pattern_name=name,
                pattern_description=desc,
                example_text=example,
                applicable_platforms=("wechat", "xiaohongshu") if pattern_type in {"title", "platform"} else ("wechat",),
                applicable_content_types=("deep_analysis", "short_post"),
                strength="MEDIUM",
                reuse_guidance="Use as editorial guidance; do not auto-apply without human review.",
                risk_notes=("Pattern extracted from rule-based/generated assets; validate against real head-media samples later.",),
            )
        )
    return patterns


def summary_for(patterns: list[HeadMediaPattern]) -> dict[str, int]:
    return {
        "pattern_count": len(patterns),
        "title_patterns": sum(1 for item in patterns if item.pattern_type == "title"),
        "opening_patterns": sum(1 for item in patterns if item.pattern_type == "opening"),
        "structure_patterns": sum(1 for item in patterns if item.pattern_type == "structure"),
        "angle_patterns": sum(1 for item in patterns if item.pattern_type == "angle"),
    }


def build_head_media_pattern_library(paths: ProjectPaths) -> HeadMediaPatternLibrary:
    examples = collect_examples(paths)
    patterns = default_patterns(examples)
    warnings = () if examples else ("No generated content examples found; using starter pattern library.",)
    return HeadMediaPatternLibrary(SCHEMA_VERSION, utc_now(), tuple(patterns), summary_for(patterns), warnings)


def library_to_dict(library: HeadMediaPatternLibrary) -> dict[str, Any]:
    return asdict(library)


def render_markdown(library: HeadMediaPatternLibrary) -> str:
    rows = [
        f"| {idx} | {item.pattern_type} | {item.pattern_name} | {item.strength} | {item.pattern_description.replace('|', '\\|')} |"
        for idx, item in enumerate(library.patterns, start=1)
    ]
    warnings = "\n".join(f"- {item}" for item in library.warnings) if library.warnings else "- None"
    return f"""# Head Media Pattern Library v1

## Summary

- Updated at: `{library.updated_at}`
- Pattern count: `{library.summary['pattern_count']}`
- Title patterns: `{library.summary['title_patterns']}`
- Opening patterns: `{library.summary['opening_patterns']}`
- Structure patterns: `{library.summary['structure_patterns']}`
- Angle patterns: `{library.summary['angle_patterns']}`

## Patterns

| # | Type | Name | Strength | Description |
|---:|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | None |'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths) -> dict[str, Path]:
    return {
        "json": paths.market_content_root / "08_learning_patterns" / "head_media_pattern_library.json",
        "md": paths.market_content_root / "08_learning_patterns" / "head_media_pattern_library.md",
        "frontstage": paths.frontstage_root / "head_media_pattern_library_board.md",
    }


def write_head_media_pattern_library(library: HeadMediaPatternLibrary, paths: ProjectPaths) -> dict[str, Path]:
    paths_by_name = output_paths(paths)
    for path in paths_by_name.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(library_to_dict(library), ensure_ascii=False, indent=2)
    markdown = render_markdown(library)
    paths_by_name["json"].write_text(payload + "\n", encoding="utf-8")
    paths_by_name["md"].write_text(markdown, encoding="utf-8")
    paths_by_name["frontstage"].write_text(markdown, encoding="utf-8")
    return paths_by_name
