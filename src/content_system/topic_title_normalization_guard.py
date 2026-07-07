"""Topic Title Normalization Guard v1.

Prevents raw metadata titles from directly becoming main topics.
Ensures titles are human-readable and properly normalized.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "v1"

RAW_METADATA_PATTERNS = [
    r"^https?://",
    r"^[a-zA-Z0-9_-]+\.[a-zA-Z]{2,}(/.*)?$",
    r"^[\w-]+@[\w-]+\.[\w.-]+$",
    r"^[0-9a-f]{32,}$",
    r"^[0-9a-f]{64}$",
    r"^[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}",
    r"^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}",
    r"^Untitled$",
    r"^No title$",
    r"^Title$",
    r"^Article$",
    r"^Post$",
    r"^News$",
    r"^\s*$",
]

MIN_TITLE_LENGTH = 5
MAX_TITLE_LENGTH = 200

LOW_QUALITY_INDICATORS = [
    "read more",
    "click here",
    "learn more",
    "continue reading",
    "full article",
    "subscribe now",
    "sign up",
    "free trial",
]


@dataclass(frozen=True)
class TitleGuard:
    topic_id: str
    original_title: str
    normalized_title: str
    is_raw_metadata_title: bool
    is_human_readable: bool
    issues: tuple[str, ...]
    recommendation: str


@dataclass(frozen=True)
class TitleNormalizationReport:
    schema_version: str
    generated_at: str
    run_date: str
    guards: tuple[TitleGuard, ...]
    raw_metadata_count: int
    non_human_readable_count: int
    total_candidates: int
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def normalize_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return today_token()
    return text.replace("-", "")[:8]


def is_raw_metadata(title: str) -> bool:
    title = title.strip()
    if not title:
        return True
    for pattern in RAW_METADATA_PATTERNS:
        if re.match(pattern, title, re.IGNORECASE):
            return True
    return False


def is_human_readable(title: str) -> bool:
    title = title.strip()
    if len(title) < MIN_TITLE_LENGTH:
        return False
    if len(title) > MAX_TITLE_LENGTH:
        return False

    zh_count = sum(1 for char in title if "\u4e00" <= char <= "\u9fff")
    en_count = sum(1 for char in title if "a" <= char.lower() <= "z")
    num_count = sum(1 for char in title if "0" <= char <= "9")

    text_ratio = (zh_count + en_count) / max(len(title), 1)
    if text_ratio < 0.3:
        return False

    lowered = title.lower()
    for indicator in LOW_QUALITY_INDICATORS:
        if indicator in lowered:
            return False

    return True


def normalize_title(title: str) -> str:
    text = title.strip()
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&[a-zA-Z0-9]+;", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\|+", "|", text)
    text = text.strip("| \t\n\r")
    return text


def apply_title_guard(
    candidates: list[dict[str, Any]],
    run_date: str | None = None,
    require_human_readable: bool = True,
    reject_raw_metadata: bool = True,
) -> TitleNormalizationReport:
    final_run_date = normalize_date(run_date)
    guards: list[TitleGuard] = []
    warnings: list[str] = []

    if not candidates:
        warnings.append("No candidates provided for title normalization guard")

    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue

        topic_id = str(candidate.get("topic_id") or candidate.get("evidence_id") or "")
        original_title = str(candidate.get("title") or "")
        normalized_title = normalize_title(original_title)

        issues: list[str] = []
        is_raw = False
        is_readable = True

        if reject_raw_metadata and is_raw_metadata(normalized_title):
            is_raw = True
            issues.append("Raw metadata title detected")

        if require_human_readable and not is_human_readable(normalized_title):
            is_readable = False
            if len(normalized_title) < MIN_TITLE_LENGTH:
                issues.append(f"Title too short ({len(normalized_title)} chars)")
            elif len(normalized_title) > MAX_TITLE_LENGTH:
                issues.append(f"Title too long ({len(normalized_title)} chars)")
            else:
                issues.append("Title not human-readable")

        if issues:
            recommendation = "Rewrite title to be human-readable and descriptive"
        else:
            recommendation = "Title is acceptable"

        guards.append(TitleGuard(
            topic_id=topic_id,
            original_title=original_title,
            normalized_title=normalized_title,
            is_raw_metadata_title=is_raw,
            is_human_readable=is_readable,
            issues=tuple(issues),
            recommendation=recommendation,
        ))

    raw_count = sum(1 for g in guards if g.is_raw_metadata_title)
    non_readable_count = sum(1 for g in guards if not g.is_human_readable)

    return TitleNormalizationReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        guards=tuple(guards),
        raw_metadata_count=raw_count,
        non_human_readable_count=non_readable_count,
        total_candidates=len(candidates),
        warnings=tuple(warnings),
    )


def report_to_dict(report: TitleNormalizationReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: TitleNormalizationReport) -> str:
    rows = []
    for index, guard in enumerate(report.guards, start=1):
        status_color = "✅" if guard.is_human_readable and not guard.is_raw_metadata_title else "❌"
        status_text = "ACCEPTABLE" if guard.is_human_readable and not guard.is_raw_metadata_title else "REJECTED"
        rows.append(
            "| "
            + " | ".join([
                str(index),
                status_color,
                status_text,
                guard.normalized_title[:60] + "..." if len(guard.normalized_title) > 60 else guard.normalized_title,
                ", ".join(guard.issues) if guard.issues else "-",
                guard.recommendation[:40] + "..." if len(guard.recommendation) > 40 else guard.recommendation,
            ])
            + " |"
        )

    return f"""# Title Normalization Guard Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Total candidates: `{report.total_candidates}`
- Raw metadata titles: `{report.raw_metadata_count}`
- Non-human-readable: `{report.non_human_readable_count}`

## Title Checks

| # | Status | Result | Normalized Title | Issues | Recommendation |
|---:|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | None | - | - |'}

## Validation Rules

- Reject raw metadata: URLs, dates, hashes, empty strings
- Minimum title length: {MIN_TITLE_LENGTH} characters
- Maximum title length: {MAX_TITLE_LENGTH} characters
- Require at least 30% text content (Chinese/English)
- Reject low-quality indicators: "read more", "click here", etc.

## Warnings

{chr(10).join(f"- {w}" for w in report.warnings) if report.warnings else "- None"}

## Notes

- schema_version: `{SCHEMA_VERSION}`
"""


def write_report(report: TitleNormalizationReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = Path(output_path + ".json")
    md_path = Path(output_path + ".md")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(payload + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def load_report(json_path: str) -> TitleNormalizationReport | None:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return TitleNormalizationReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            guards=tuple(
                TitleGuard(
                    topic_id=g.get("topic_id", ""),
                    original_title=g.get("original_title", ""),
                    normalized_title=g.get("normalized_title", ""),
                    is_raw_metadata_title=bool(g.get("is_raw_metadata_title", False)),
                    is_human_readable=bool(g.get("is_human_readable", True)),
                    issues=tuple(g.get("issues", [])),
                    recommendation=g.get("recommendation", ""),
                )
                for g in data.get("guards", [])
            ),
            raw_metadata_count=int(data.get("raw_metadata_count", 0)),
            non_human_readable_count=int(data.get("non_human_readable_count", 0)),
            total_candidates=int(data.get("total_candidates", 0)),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None