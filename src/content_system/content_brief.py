"""Content Brief Builder v1.

P2-001 turns Phase 1 high-value candidates into structured editorial briefs.
The builder is deterministic and rule-based: it does not call LLMs, publish
content, or change upstream capture outputs.
"""

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
class ContentBrief:
    schema_version: str
    brief_id: str
    candidate_id: str
    run_date: str
    title: str
    theme: str
    score: float
    score_band: str
    recommended_action: str
    content_type: str
    target_platforms: tuple[str, ...]
    core_claim: str
    why_now: str
    why_it_matters: str
    supporting_evidence: tuple[dict[str, Any], ...]
    missing_info: tuple[str, ...]
    risks: tuple[str, ...]
    suggested_angles: tuple[str, ...]
    audience: str
    editorial_priority: str
    source_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class ContentBriefReport:
    schema_version: str
    generated_at: str
    run_date: str
    brief_count: int
    briefs: tuple[ContentBrief, ...]
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


def normalize_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return today_token()
    return text.replace("-", "")[:8]


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def make_brief_id(run_date: str, candidate_id: str, title: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{candidate_id}|{title}".encode("utf-8")).hexdigest()[:12]
    return f"brief_{run_date}_{digest}"


def content_type_for(candidate: dict[str, Any]) -> str:
    band = str(candidate.get("score_band") or "D")
    action = str(candidate.get("recommended_action") or "")
    if band == "A":
        return "deep_analysis"
    if band == "B":
        return "short_post" if "short" in action else "quick_take"
    if band == "C":
        return "monitor_note"
    return "archive"


def target_platforms_for(content_type: str) -> tuple[str, ...]:
    if content_type == "deep_analysis":
        return ("wechat", "xiaohongshu")
    if content_type in {"short_post", "quick_take"}:
        return ("xiaohongshu", "wechat")
    if content_type == "monitor_note":
        return ("internal",)
    return ()


def editorial_priority_for(band: str) -> str:
    if band == "A":
        return "HIGH"
    if band == "B":
        return "MEDIUM"
    return "LOW"


def core_claim_for(candidate: dict[str, Any]) -> str:
    theme = str(candidate.get("theme") or "该 AI/Agent 信号")
    why = str(candidate.get("why_it_matters") or "")
    if why:
        return f"{theme}：{why}"
    return f"{theme} 是一个值得继续评估的 AI/Agent 内容信号。"


def why_now_for(candidate: dict[str, Any]) -> str:
    evidence_count = safe_int(candidate.get("evidence_count"))
    source_count = safe_int(candidate.get("source_count"))
    return f"当前已有 {evidence_count} 条 evidence、{source_count} 个 source 支撑，适合进入人工编辑前的结构化准备。"


def evidence_items(candidate: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    raw = candidate.get("key_evidence")
    if not isinstance(raw, list):
        return ()
    compact = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        compact.append(
            {
                "evidence_id": item.get("evidence_id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "source_id": item.get("source_id"),
                "source_tier": item.get("source_tier"),
            }
        )
    return tuple(compact)


def missing_info_for(candidate: dict[str, Any], evidence: tuple[dict[str, Any], ...]) -> tuple[str, ...]:
    missing: list[str] = []
    if len(evidence) < 2:
        missing.append("Need more independent evidence before publishing.")
    if safe_int(candidate.get("source_count")) < 2:
        missing.append("Need another source to confirm this signal.")
    return tuple(missing)


def risks_for(candidate: dict[str, Any]) -> tuple[str, ...]:
    risks = ["Rule-based brief; requires human review before publication."]
    raw_risks = candidate.get("risks_missing_info")
    if isinstance(raw_risks, list):
        risks.extend(str(item) for item in raw_risks if item)
    return tuple(dict.fromkeys(risks))


def build_brief(candidate: dict[str, Any], run_date: str) -> ContentBrief:
    candidate_id = str(candidate.get("cluster_id") or f"candidate_{candidate.get('rank', 'unknown')}")
    theme = str(candidate.get("theme") or "Untitled candidate")
    band = str(candidate.get("score_band") or "D")
    content_type = content_type_for(candidate)
    evidence = evidence_items(candidate)
    evidence_ids = tuple(str(item.get("evidence_id")) for item in evidence if item.get("evidence_id"))
    source_ids = tuple(str(item) for item in candidate.get("source_ids", []) if item)
    suggested_angles = tuple(str(item) for item in candidate.get("suggested_angles", []) if item)

    return ContentBrief(
        schema_version=SCHEMA_VERSION,
        brief_id=make_brief_id(run_date, candidate_id, theme),
        candidate_id=candidate_id,
        run_date=run_date,
        title=theme,
        theme=theme,
        score=round(safe_float(candidate.get("total_score")), 2),
        score_band=band,
        recommended_action=str(candidate.get("recommended_action") or "archive"),
        content_type=content_type,
        target_platforms=target_platforms_for(content_type),
        core_claim=core_claim_for(candidate),
        why_now=why_now_for(candidate),
        why_it_matters=str(candidate.get("why_it_matters") or ""),
        supporting_evidence=evidence,
        missing_info=missing_info_for(candidate, evidence),
        risks=risks_for(candidate),
        suggested_angles=suggested_angles,
        audience="AI/Agent builders and investors",
        editorial_priority=editorial_priority_for(band),
        source_ids=source_ids,
        evidence_ids=evidence_ids,
    )


def build_content_brief_report(paths: ProjectPaths, run_date: str | None = None) -> ContentBriefReport:
    input_path = paths.market_content_root / "03_topic_candidates" / "latest_high_value_candidates.json"
    payload = read_json(input_path)
    final_run_date = normalize_date(run_date or payload.get("run_date"))
    raw_candidates = payload.get("candidates")
    candidates = [item for item in raw_candidates if isinstance(item, dict)] if isinstance(raw_candidates, list) else []
    warnings: list[str] = []
    if not input_path.exists():
        warnings.append("latest_high_value_candidates.json not found; run make high-value-candidates first.")
    if not candidates:
        warnings.append("No high-value candidates available for brief generation.")
    briefs = tuple(build_brief(candidate, final_run_date) for candidate in candidates)
    return ContentBriefReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        brief_count=len(briefs),
        briefs=briefs,
        warnings=tuple(warnings),
    )


def report_to_dict(report: ContentBriefReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: ContentBriefReport) -> str:
    rows = []
    detail_sections = []
    for index, brief in enumerate(report.briefs, start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    escape_cell(brief.editorial_priority),
                    escape_cell(brief.score),
                    escape_cell(brief.score_band),
                    escape_cell(brief.content_type),
                    escape_cell(brief.title),
                    escape_cell(", ".join(brief.target_platforms)),
                ]
            )
            + " |"
        )
        evidence_lines = "\n".join(
            f"- `{item.get('source_id')}` {item.get('title')} ({item.get('url') or 'no url'})"
            for item in brief.supporting_evidence
        ) or "- None"
        missing = "\n".join(f"- {item}" for item in brief.missing_info) or "- None"
        risks = "\n".join(f"- {item}" for item in brief.risks) or "- None"
        angles = "\n".join(f"- {item}" for item in brief.suggested_angles) or "- None"
        detail_sections.append(
            f"""### {index}. {brief.title}

- Brief ID: `{brief.brief_id}`
- Content type: `{brief.content_type}`
- Core claim: {brief.core_claim}
- Why now: {brief.why_now}
- Why it matters: {brief.why_it_matters or '待人工补充'}

Supporting evidence:

{evidence_lines}

Suggested angles:

{angles}

Missing info:

{missing}

Risks:

{risks}
"""
        )

    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Content Briefs v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Briefs: `{report.brief_count}`

## Briefs

| # | Priority | Score | Band | Type | Title | Platforms |
|---:|---|---:|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | 0 | D | archive | None | - |'}

## Details

{chr(10).join(detail_sections) if detail_sections else '暂无 brief。'}

## Warnings

{warnings}
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "05_draft_packs"
    return {
        "dated_json": root / f"{run_date}__content-briefs.json",
        "dated_md": root / f"{run_date}__content-briefs.md",
        "latest_json": root / "latest_content_briefs.json",
        "latest_md": root / "latest_content_briefs.md",
    }


def write_content_brief_report(report: ContentBriefReport, paths: ProjectPaths) -> dict[str, Path]:
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
