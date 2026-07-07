"""Main Topic Selection Reranker v1.

Performs secondary sorting of main topic candidates after the original topic scoring.
Integrates diversity scores and various penalties/boosts into final ranking.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class RerankedTopic:
    topic_id: str
    title: str
    original_rank: int
    original_score: float
    diversity_adjusted_score: float
    final_rank: int
    rank_change: int
    status: str


@dataclass(frozen=True)
class TopicRerankingReport:
    schema_version: str
    generated_at: str
    run_date: str
    reranked_topics: tuple[RerankedTopic, ...]
    rank_changed_count: int
    avg_rank_change: float
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


def rerank_topics(
    candidates: list[dict[str, Any]],
    diversity_report: dict[str, Any] | None = None,
    run_date: str | None = None,
    original_score_weight: float = 0.6,
    diversity_score_weight: float = 0.4,
) -> TopicRerankingReport:
    final_run_date = normalize_date(run_date)
    warnings: list[str] = []

    if not candidates:
        warnings.append("No candidates provided for reranking")

    original_ranked = sorted(
        enumerate(candidates),
        key=lambda x: -float(x[1].get("score") or x[1].get("topic_score") or 0.0),
    )

    original_rank_map: dict[str, tuple[int, float]] = {}
    for idx, candidate in original_ranked:
        topic_id = str(candidate.get("topic_id") or candidate.get("evidence_id") or "")
        original_rank_map[topic_id] = (idx + 1, float(candidate.get("score") or candidate.get("topic_score") or 0.0))

    diversity_score_map: dict[str, float] = {}
    if diversity_report:
        for score in diversity_report.get("diversity_scores", []):
            topic_id = str(score.get("topic_id", ""))
            diversity_score_map[topic_id] = float(score.get("diversity_adjusted_score", 0.0))

    reranked_with_scores = []
    for idx, candidate in original_ranked:
        topic_id = str(candidate.get("topic_id") or candidate.get("evidence_id") or "")
        title = str(candidate.get("title") or "")
        original_rank, original_score = original_rank_map.get(topic_id, (idx + 1, 0.0))
        diversity_score = diversity_score_map.get(topic_id, original_score)

        final_score = (
            original_score * original_score_weight
            + diversity_score * diversity_score_weight
        )

        reranked_with_scores.append({
            "topic_id": topic_id,
            "title": title,
            "original_rank": original_rank,
            "original_score": original_score,
            "diversity_adjusted_score": diversity_score,
            "final_score": final_score,
        })

    reranked_with_scores.sort(key=lambda x: -x["final_score"])

    final_rank_map: dict[str, int] = {}
    for idx, item in enumerate(reranked_with_scores):
        final_rank_map[item["topic_id"]] = idx + 1

    reranked_topics: list[RerankedTopic] = []
    rank_changes: list[int] = []

    for item in reranked_with_scores:
        topic_id = item["topic_id"]
        original_rank = item["original_rank"]
        final_rank = final_rank_map[topic_id]
        rank_change = original_rank - final_rank
        rank_changes.append(rank_change)

        if rank_change > 0:
            status = "UP"
        elif rank_change < 0:
            status = "DOWN"
        else:
            status = "SAME"

        reranked_topics.append(RerankedTopic(
            topic_id=topic_id,
            title=item["title"],
            original_rank=original_rank,
            original_score=round(item["original_score"], 4),
            diversity_adjusted_score=round(item["diversity_adjusted_score"], 4),
            final_rank=final_rank,
            rank_change=rank_change,
            status=status,
        ))

    rank_changed_count = sum(1 for r in reranked_topics if r.rank_change != 0)
    avg_rank_change = sum(rank_changes) / len(rank_changes) if rank_changes else 0.0

    return TopicRerankingReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        reranked_topics=tuple(reranked_topics),
        rank_changed_count=rank_changed_count,
        avg_rank_change=round(avg_rank_change, 2),
        total_candidates=len(candidates),
        warnings=tuple(warnings),
    )


def report_to_dict(report: TopicRerankingReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: TopicRerankingReport) -> str:
    rows = []
    for topic in report.reranked_topics:
        rank_arrow = "↑" if topic.rank_change > 0 else ("↓" if topic.rank_change < 0 else "→")
        rank_change_str = f"{rank_arrow}{abs(topic.rank_change)}" if topic.rank_change != 0 else "-"
        rows.append(
            "| "
            + " | ".join([
                str(topic.final_rank),
                rank_change_str,
                str(topic.original_rank),
                str(round(topic.original_score * 100, 1)) + "%",
                str(round(topic.diversity_adjusted_score * 100, 1)) + "%",
                topic.title[:60] + "..." if len(topic.title) > 60 else topic.title,
            ])
            + " |"
        )

    return f"""# Main Topic Selection Reranking Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Total candidates: `{report.total_candidates}`
- Rank changed: `{report.rank_changed_count}`
- Avg rank change: `{report.avg_rank_change}`

## Reranked Topics

| Final Rank | Change | Original Rank | Original Score | Diversity Score | Title |
|---:|---|:---:|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | 0 | - | - | None |'}

## Scoring Weights

- Original score weight: 60%
- Diversity score weight: 40%

## Warnings

{chr(10).join(f"- {w}" for w in report.warnings) if report.warnings else "- None"}

## Notes

- Positive rank change means topic moved up (better)
- Negative rank change means topic moved down (worse)
- schema_version: `{SCHEMA_VERSION}`
"""


def write_report(report: TopicRerankingReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = Path(output_path + ".json")
    md_path = Path(output_path + ".md")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(payload + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def load_report(json_path: str) -> TopicRerankingReport | None:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return TopicRerankingReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            reranked_topics=tuple(
                RerankedTopic(
                    topic_id=t.get("topic_id", ""),
                    title=t.get("title", ""),
                    original_rank=int(t.get("original_rank", 0)),
                    original_score=float(t.get("original_score", 0.0)),
                    diversity_adjusted_score=float(t.get("diversity_adjusted_score", 0.0)),
                    final_rank=int(t.get("final_rank", 0)),
                    rank_change=int(t.get("rank_change", 0)),
                    status=t.get("status", "SAME"),
                )
                for t in data.get("reranked_topics", [])
            ),
            rank_changed_count=int(data.get("rank_changed_count", 0)),
            avg_rank_change=float(data.get("avg_rank_change", 0.0)),
            total_candidates=int(data.get("total_candidates", 0)),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None