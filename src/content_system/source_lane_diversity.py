"""Source/Lane Diversity Analysis v1.

Prevents excessive concentration of topics from the same source or lane
over consecutive days.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class SourceLaneInfo:
    source_id: str
    lane: str | None
    recent_repetition: int
    days_consecutive: int
    last_used_date: str
    topic_count_7d: int
    is_over_concentrated: bool


@dataclass(frozen=True)
class SourceLaneDiversityReport:
    schema_version: str
    generated_at: str
    run_date: str
    source_lane_info: tuple[SourceLaneInfo, ...]
    over_concentrated_count: int
    total_sources: int
    total_lanes: int
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


def analyze_source_lane_diversity(
    historical_topics: list[dict[str, Any]],
    run_date: str | None = None,
    max_consecutive_days: int = 2,
    max_7d_count: int = 3,
) -> SourceLaneDiversityReport:
    final_run_date = normalize_date(run_date)
    warnings: list[str] = []

    if not historical_topics:
        warnings.append("No historical topics available for source/lane analysis")

    source_counts: Counter[str] = Counter()
    lane_counts: Counter[str] = Counter()
    source_dates: dict[str, list[str]] = {}
    lane_dates: dict[str, list[str]] = {}

    for topic in historical_topics:
        source_id = str(topic.get("source_id") or "")
        lane = str(topic.get("lane") or topic.get("source_category") or "")
        topic_date = str(topic.get("run_date") or "")

        if source_id:
            source_counts[source_id] += 1
            source_dates.setdefault(source_id, []).append(topic_date)

        if lane:
            lane_counts[lane] += 1
            lane_dates.setdefault(lane, []).append(topic_date)

    def calculate_consecutive_days(dates: list[str]) -> int:
        if not dates:
            return 0
        sorted_dates = sorted(set(dates))
        max_consecutive = 1
        current_consecutive = 1
        for i in range(1, len(sorted_dates)):
            prev = int(sorted_dates[i - 1])
            curr = int(sorted_dates[i])
            if curr - prev == 1:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 1
        return max_consecutive

    source_lane_info: list[SourceLaneInfo] = []

    for source_id, count in source_counts.items():
        dates = source_dates.get(source_id, [])
        consecutive = calculate_consecutive_days(dates)
        last_used = max(dates) if dates else ""
        is_over = consecutive >= max_consecutive_days or count >= max_7d_count
        source_lane_info.append(SourceLaneInfo(
            source_id=source_id,
            lane=None,
            recent_repetition=consecutive,
            days_consecutive=consecutive,
            last_used_date=last_used,
            topic_count_7d=count,
            is_over_concentrated=is_over,
        ))

    for lane, count in lane_counts.items():
        dates = lane_dates.get(lane, [])
        consecutive = calculate_consecutive_days(dates)
        last_used = max(dates) if dates else ""
        is_over = consecutive >= max_consecutive_days or count >= max_7d_count
        source_lane_info.append(SourceLaneInfo(
            source_id="",
            lane=lane,
            recent_repetition=consecutive,
            days_consecutive=consecutive,
            last_used_date=last_used,
            topic_count_7d=count,
            is_over_concentrated=is_over,
        ))

    source_lane_info.sort(key=lambda x: (-x.topic_count_7d, x.source_id or x.lane or ""))

    over_concentrated = sum(1 for info in source_lane_info if info.is_over_concentrated)

    return SourceLaneDiversityReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        source_lane_info=tuple(source_lane_info),
        over_concentrated_count=over_concentrated,
        total_sources=len(source_counts),
        total_lanes=len(lane_counts),
        warnings=tuple(warnings),
    )


def report_to_dict(report: SourceLaneDiversityReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: SourceLaneDiversityReport) -> str:
    source_rows = []
    lane_rows = []
    for info in report.source_lane_info:
        if info.source_id:
            source_rows.append(
                "| "
                + " | ".join([
                    info.source_id,
                    str(info.topic_count_7d),
                    str(info.days_consecutive),
                    info.last_used_date,
                    "⚠️" if info.is_over_concentrated else "-",
                ])
                + " |"
            )
        else:
            lane_rows.append(
                "| "
                + " | ".join([
                    info.lane or "",
                    str(info.topic_count_7d),
                    str(info.days_consecutive),
                    info.last_used_date,
                    "⚠️" if info.is_over_concentrated else "-",
                ])
                + " |"
            )

    return f"""# Source/Lane Diversity Analysis Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Total sources: `{report.total_sources}`
- Total lanes: `{report.total_lanes}`
- Over-concentrated: `{report.over_concentrated_count}`

## Sources

| Source ID | 7d Count | Consecutive | Last Used | Warning |
|---|:---:|:---:|---|---|
{chr(10).join(source_rows) if source_rows else '| - | 0 | 0 | - | - |'}

## Lanes

| Lane | 7d Count | Consecutive | Last Used | Warning |
|---|:---:|:---:|---|---|
{chr(10).join(lane_rows) if lane_rows else '| - | 0 | 0 | - | - |'}

## Warnings

{chr(10).join(f"- {w}" for w in report.warnings) if report.warnings else "- None"}

## Notes

- Over-concentration detected when:
  - Consecutive days >= 2
  - 7-day count >= 3
- schema_version: `{SCHEMA_VERSION}`
"""


def write_report(report: SourceLaneDiversityReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = Path(output_path + ".json")
    md_path = Path(output_path + ".md")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(payload + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def load_report(json_path: str) -> SourceLaneDiversityReport | None:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return SourceLaneDiversityReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            source_lane_info=tuple(
                SourceLaneInfo(
                    source_id=s.get("source_id", ""),
                    lane=s.get("lane"),
                    recent_repetition=int(s.get("recent_repetition", 0)),
                    days_consecutive=int(s.get("days_consecutive", 0)),
                    last_used_date=s.get("last_used_date", ""),
                    topic_count_7d=int(s.get("topic_count_7d", 0)),
                    is_over_concentrated=bool(s.get("is_over_concentrated", False)),
                )
                for s in data.get("source_lane_info", [])
            ),
            over_concentrated_count=int(data.get("over_concentrated_count", 0)),
            total_sources=int(data.get("total_sources", 0)),
            total_lanes=int(data.get("total_lanes", 0)),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None