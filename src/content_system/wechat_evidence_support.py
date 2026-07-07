"""WeChat Evidence Support Check v1.

Checks evidence support levels. Regular media sources cannot be used as
hard evidence - only official sources qualify.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from content_system.wechat_article_intelligence import ArticleIntelligence


SCHEMA_VERSION = "v1"

HARD_EVIDENCE_SOURCES = {
    "openai",
    "anthropic",
    "google",
    "deepmind",
    "nvidia",
    "microsoft",
    "meta",
    "github",
    "huggingface",
    "arxiv",
    "arxiv.org",
}

MEDIA_SOURCE_KEYWORDS = (
    "媒体",
    "新闻",
    "资讯",
    "报道",
    "blog",
    "公众号",
    "网站",
    "tech",
    "news",
    "media",
)


@dataclass(frozen=True)
class EvidenceSupport:
    evidence_id: str
    source_id: str
    is_official: bool
    is_hard_evidence: bool
    evidence_strength: str
    support_score: float
    reliability_reason: str
    caveats: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceSupportReport:
    schema_version: str
    generated_at: str
    run_date: str
    input_count: int
    hard_evidence_count: int
    soft_evidence_count: int
    unsupported_count: int
    evidence_items: tuple[EvidenceSupport, ...]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def is_official_source(source_id: str, source_label: str) -> bool:
    combined = f"{source_id} {source_label}".lower()
    for official in HARD_EVIDENCE_SOURCES:
        if official.lower() in combined:
            return True
    return False


def is_media_source(source_id: str, source_label: str) -> bool:
    combined = f"{source_id} {source_label}".lower()
    for keyword in MEDIA_SOURCE_KEYWORDS:
        if keyword.lower() in combined:
            return True
    return False


def evaluate_evidence(intelligence_item: ArticleIntelligence, is_official: bool = False) -> EvidenceSupport:
    source_id = intelligence_item.source_id
    source_label = ""

    is_official = is_official or is_official_source(source_id, source_label)
    is_media = is_media_source(source_id, source_label)

    caveats: list[str] = []

    if is_media:
        is_hard_evidence = False
        evidence_strength = "SOFT"
        support_score = 0.3
        reliability_reason = "Regular media source - cannot be used as hard evidence"
        caveats.append("This is a media source, not official documentation")
        caveats.append("Content may contain editorial bias or secondhand reporting")
        caveats.append("Needs cross-verification with official sources")
    elif is_official:
        is_hard_evidence = True
        evidence_strength = "HARD"
        support_score = 0.9
        reliability_reason = "Official source - qualifies as hard evidence"
    else:
        is_hard_evidence = False
        evidence_strength = "WEAK"
        support_score = 0.5
        reliability_reason = "Unknown source type - treat with caution"
        caveats.append("Source type not clearly identified")
        caveats.append("Consider verifying source legitimacy")

    if not intelligence_item.claims:
        support_score *= 0.8
        caveats.append("No explicit claims found in excerpt")

    if len(intelligence_item.entities) == 0:
        support_score *= 0.9
        caveats.append("No identifiable entities in content")

    return EvidenceSupport(
        evidence_id=intelligence_item.entry_id,
        source_id=source_id,
        is_official=is_official,
        is_hard_evidence=is_hard_evidence,
        evidence_strength=evidence_strength,
        support_score=round(support_score, 2),
        reliability_reason=reliability_reason,
        caveats=tuple(caveats),
    )


def evaluate_all_evidence(intelligence_items: tuple[ArticleIntelligence, ...], run_date: str | None = None) -> EvidenceSupportReport:
    evidence_items: list[EvidenceSupport] = []
    warnings: list[str] = []

    for item in intelligence_items:
        try:
            evidence_items.append(evaluate_evidence(item))
        except Exception as exc:
            warnings.append(f"Failed to evaluate evidence for {item.entry_id}: {exc}")

    hard_count = sum(1 for e in evidence_items if e.is_hard_evidence)
    soft_count = sum(1 for e in evidence_items if e.evidence_strength == "SOFT")
    unsupported_count = sum(1 for e in evidence_items if e.evidence_strength == "WEAK")

    return EvidenceSupportReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date or today_token(),
        input_count=len(intelligence_items),
        hard_evidence_count=hard_count,
        soft_evidence_count=soft_count,
        unsupported_count=unsupported_count,
        evidence_items=tuple(evidence_items),
        warnings=tuple(warnings),
    )


def get_hard_evidence(report: EvidenceSupportReport) -> tuple[EvidenceSupport, ...]:
    return tuple(e for e in report.evidence_items if e.is_hard_evidence)


def get_soft_evidence(report: EvidenceSupportReport) -> tuple[EvidenceSupport, ...]:
    return tuple(e for e in report.evidence_items if not e.is_hard_evidence)


def report_to_dict(report: EvidenceSupportReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: EvidenceSupportReport) -> str:
    rows = []
    for index, evidence in enumerate(report.evidence_items, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    evidence.evidence_id[:20] + "..." if len(evidence.evidence_id) > 20 else evidence.evidence_id,
                    evidence.source_id,
                    "YES" if evidence.is_official else "NO",
                    evidence.evidence_strength,
                    str(int(evidence.support_score * 100)) + "%",
                ]
            )
            + " |"
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"

    return f"""# WeChat Evidence Support Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Input count: `{report.input_count}`
- Hard evidence: `{report.hard_evidence_count}`
- Soft evidence: `{report.soft_evidence_count}`
- Unsupported: `{report.unsupported_count}`

## Evidence Items

| # | Evidence ID | Source | Official | Strength | Support |
|---:|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | - | - |'}

## Warnings

{warnings}

## Rules

- **Hard evidence**: Only official sources (OpenAI, Anthropic, Google, NVIDIA, etc.)
- **Soft evidence**: Regular media sources - cannot be used as hard evidence
- **Weak evidence**: Unknown or unverified sources

## Notes

- Regular media sources are explicitly NOT hard evidence.
- Only excerpt-level analysis (no full text).
- do_not_copy_text=True for all evidence items.
"""


def write_report(report: EvidenceSupportReport, output_path: str) -> None:
    import json
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = output_path + ".json"
    md_path = output_path + ".md"

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(payload + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)


def load_report(json_path: str) -> EvidenceSupportReport | None:
    try:
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return EvidenceSupportReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            input_count=int(data.get("input_count", 0)),
            hard_evidence_count=int(data.get("hard_evidence_count", 0)),
            soft_evidence_count=int(data.get("soft_evidence_count", 0)),
            unsupported_count=int(data.get("unsupported_count", 0)),
            evidence_items=tuple(
                EvidenceSupport(
                    evidence_id=e.get("evidence_id", ""),
                    source_id=e.get("source_id", ""),
                    is_official=bool(e.get("is_official", False)),
                    is_hard_evidence=bool(e.get("is_hard_evidence", False)),
                    evidence_strength=e.get("evidence_strength", "WEAK"),
                    support_score=float(e.get("support_score", 0.0)),
                    reliability_reason=e.get("reliability_reason", ""),
                    caveats=tuple(e.get("caveats", [])),
                )
                for e in data.get("evidence_items", [])
            ),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None