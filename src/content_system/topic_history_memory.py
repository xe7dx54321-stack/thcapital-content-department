"""Topic History Memory v1.

Lightweight memory for tracking past N days of selected main topics, backup topics,
and final candidates to support diversity analysis and duplicate detection.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class HistoricalTopic:
    topic_id: str
    title: str
    run_date: str
    topic_type: str
    source_id: str
    lane: str | None
    event_type: str
    angle_type: str | None
    companies: tuple[str, ...]
    products: tuple[str, ...]
    score: float | None
    normalized_title: str


@dataclass(frozen=True)
class TopicHistoryReport:
    schema_version: str
    generated_at: str
    run_date: str
    history_window_days: int
    historical_topics: tuple[HistoricalTopic, ...]
    main_topic_count: int
    backup_topic_count: int
    final_candidate_count: int
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def date_token(days_ago: int) -> str:
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y%m%d")


def normalize_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return today_token()
    return text.replace("-", "")[:8]


def normalize_title(title: str) -> str:
    import re
    text = title.lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def load_historical_topics_from_topic_selection(
    paths: dict[str, Path],
    run_date: str,
) -> list[HistoricalTopic]:
    topics: list[HistoricalTopic] = []
    topic_path = paths.get("topic_selection_json")
    if not topic_path or not topic_path.exists():
        return topics

    data = read_json(topic_path)
    selected = data.get("selected_topics") or data.get("topics")
    if not isinstance(selected, list):
        return topics

    for item in selected:
        if not isinstance(item, dict):
            continue
        topics.append(HistoricalTopic(
            topic_id=str(item.get("topic_id") or item.get("evidence_id") or ""),
            title=str(item.get("title") or ""),
            run_date=run_date,
            topic_type="main",
            source_id=str(item.get("source_id") or ""),
            lane=str(item.get("lane") or item.get("source_category") or None),
            event_type=str(item.get("event_type") or ""),
            angle_type=str(item.get("angle_type") or item.get("suggested_angle") or None),
            companies=tuple(str(c) for c in item.get("companies", []) if c),
            products=tuple(str(p) for p in item.get("products", []) if p),
            score=float(item.get("score") or item.get("topic_score") or 0.0),
            normalized_title=normalize_title(str(item.get("title") or "")),
        ))

    backup = data.get("backup_topics") or data.get("alternatives")
    if isinstance(backup, list):
        for item in backup:
            if not isinstance(item, dict):
                continue
            topics.append(HistoricalTopic(
                topic_id=str(item.get("topic_id") or item.get("evidence_id") or ""),
                title=str(item.get("title") or ""),
                run_date=run_date,
                topic_type="backup",
                source_id=str(item.get("source_id") or ""),
                lane=str(item.get("lane") or item.get("source_category") or None),
                event_type=str(item.get("event_type") or ""),
                angle_type=str(item.get("angle_type") or item.get("suggested_angle") or None),
                companies=tuple(str(c) for c in item.get("companies", []) if c),
                products=tuple(str(p) for p in item.get("products", []) if p),
                score=float(item.get("score") or item.get("topic_score") or 0.0),
                normalized_title=normalize_title(str(item.get("title") or "")),
            ))

    return topics


def load_historical_topics_from_final_candidates(
    paths: dict[str, Path],
    run_date: str,
) -> list[HistoricalTopic]:
    topics: list[HistoricalTopic] = []
    candidate_path = paths.get("final_candidate_json")
    if not candidate_path or not candidate_path.exists():
        return topics

    data = read_json(candidate_path)
    candidates = data.get("final_candidates") or data.get("candidates")
    if not isinstance(candidates, list):
        return candidates

    for item in candidates:
        if not isinstance(item, dict):
            continue
        topics.append(HistoricalTopic(
            topic_id=str(item.get("candidate_id") or item.get("topic_id") or ""),
            title=str(item.get("title") or item.get("topic_title") or ""),
            run_date=run_date,
            topic_type="final_candidate",
            source_id=str(item.get("source_id") or ""),
            lane=str(item.get("lane") or None),
            event_type=str(item.get("event_type") or ""),
            angle_type=str(item.get("angle_type") or None),
            companies=tuple(str(c) for c in item.get("companies", []) if c),
            products=tuple(str(p) for p in item.get("products", []) if p),
            score=float(item.get("score") or 0.0),
            normalized_title=normalize_title(str(item.get("title") or item.get("topic_title") or "")),
        ))

    return topics


def build_topic_history_memory(
    repo_root: Path,
    run_date: str | None = None,
    history_window_days: int = 7,
) -> TopicHistoryReport:
    final_run_date = normalize_date(run_date)
    warnings: list[str] = []
    historical_topics: list[HistoricalTopic] = []

    topic_selection_pattern = "**/{date}__topic-selection*.json"
    final_candidate_pattern = "**/{date}__final-candidate*.json"

    for days_back in range(1, history_window_days + 1):
        date_str = date_token(days_back)
        topic_paths = list(repo_root.glob(topic_selection_pattern.format(date=date_str)))
        candidate_paths = list(repo_root.glob(final_candidate_pattern.format(date=date_str)))

        for topic_path in topic_paths:
            historical_topics.extend(load_historical_topics_from_topic_selection(
                {"topic_selection_json": topic_path}, date_str
            ))

        for candidate_path in candidate_paths:
            historical_topics.extend(load_historical_topics_from_final_candidates(
                {"final_candidate_json": candidate_path}, date_str
            ))

        if not topic_paths and not candidate_paths:
            warnings.append(f"No topic data found for {date_str}")

    return TopicHistoryReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        history_window_days=history_window_days,
        historical_topics=tuple(historical_topics),
        main_topic_count=sum(1 for t in historical_topics if t.topic_type == "main"),
        backup_topic_count=sum(1 for t in historical_topics if t.topic_type == "backup"),
        final_candidate_count=sum(1 for t in historical_topics if t.topic_type == "final_candidate"),
        warnings=tuple(warnings),
    )


def report_to_dict(report: TopicHistoryReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: TopicHistoryReport) -> str:
    rows = []
    for index, topic in enumerate(report.historical_topics, start=1):
        rows.append(
            "| "
            + " | ".join([
                str(index),
                topic.run_date,
                topic.topic_type,
                topic.title[:60] + "..." if len(topic.title) > 60 else topic.title,
                topic.source_id,
                topic.event_type,
                str(topic.score) if topic.score else "-",
            ])
            + " |"
        )

    return f"""# Topic History Memory Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- History window: `{report.history_window_days}` days
- Total historical topics: `{len(report.historical_topics)}`
- Main topics: `{report.main_topic_count}`
- Backup topics: `{report.backup_topic_count}`
- Final candidates: `{report.final_candidate_count}`

## Historical Topics

| # | Date | Type | Title | Source | Event Type | Score |
|---:|---|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | None | - | - | - |'}

## Warnings

{chr(10).join(f"- {w}" for w in report.warnings) if report.warnings else "- None"}

## Notes

- Lightweight memory stores only metadata; no full article text.
- Normalized titles used for similarity comparison.
- schema_version: `{SCHEMA_VERSION}`
"""


def write_report(report: TopicHistoryReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = Path(output_path + ".json")
    md_path = Path(output_path + ".md")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(payload + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def load_report(json_path: str) -> TopicHistoryReport | None:
    try:
        data = read_json(Path(json_path))
        return TopicHistoryReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            history_window_days=int(data.get("history_window_days", 7)),
            historical_topics=tuple(
                HistoricalTopic(
                    topic_id=t.get("topic_id", ""),
                    title=t.get("title", ""),
                    run_date=t.get("run_date", ""),
                    topic_type=t.get("topic_type", ""),
                    source_id=t.get("source_id", ""),
                    lane=t.get("lane"),
                    event_type=t.get("event_type", ""),
                    angle_type=t.get("angle_type"),
                    companies=tuple(t.get("companies", [])),
                    products=tuple(t.get("products", [])),
                    score=float(t.get("score")) if t.get("score") is not None else None,
                    normalized_title=t.get("normalized_title", ""),
                )
                for t in data.get("historical_topics", [])
            ),
            main_topic_count=int(data.get("main_topic_count", 0)),
            backup_topic_count=int(data.get("backup_topic_count", 0)),
            final_candidate_count=int(data.get("final_candidate_count", 0)),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None