"""Topic Similarity Analysis v1.

Identifies similar topics and duplicate events based on:
- Title similarity
- Entity overlap (companies, products)
- Event type matching
- Angle type matching
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "v1"

STOPWORDS = {
    "the", "and", "for", "with", "from", "into", "that", "this", "your", "new",
    "how", "are", "our", "you", "its", "more", "openai", "google", "nvidia",
}


@dataclass(frozen=True)
class SimilarityMatch:
    topic_id: str
    candidate_title: str
    similar_to_id: str
    similar_to_title: str
    similar_to_date: str
    title_similarity: float
    normalized_title_similarity: float
    entity_overlap_score: float
    company_overlap_score: float
    event_type_match: bool
    angle_type_match: bool
    combined_score: float
    is_hard_duplicate: bool
    is_similar: bool


@dataclass(frozen=True)
class TopicSimilarityReport:
    schema_version: str
    generated_at: str
    run_date: str
    candidate_count: int
    historical_topic_count: int
    similarity_matches: tuple[SimilarityMatch, ...]
    hard_duplicate_count: int
    similar_count: int
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


def text_tokens(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_+-]{2,}", text.lower())
    return [word for word in words if word not in STOPWORDS]


def jaccard_similarity(set_a: set[str], set_b: set[str]) -> float:
    if not set_a and not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def title_similarity_score(title1: str, title2: str) -> float:
    tokens1 = text_tokens(title1)
    tokens2 = text_tokens(title2)
    if not tokens1 or not tokens2:
        return 0.0
    return jaccard_similarity(set(tokens1), set(tokens2))


def normalized_title_similarity(title1: str, title2: str) -> float:
    norm1 = re.sub(r"[^a-z0-9]", " ", title1.lower()).strip()
    norm2 = re.sub(r"[^a-z0-9]", " ", title2.lower()).strip()
    if not norm1 or not norm2:
        return 0.0
    max_len = max(len(norm1), len(norm2))
    if max_len == 0:
        return 0.0
    return 1.0 - (levenshtein_distance(norm1, norm2) / max_len)


def entity_overlap_score(
    companies1: tuple[str, ...],
    products1: tuple[str, ...],
    companies2: tuple[str, ...],
    products2: tuple[str, ...],
) -> float:
    entities1 = set(c.lower() for c in companies1) | set(p.lower() for p in products1)
    entities2 = set(c.lower() for c in companies2) | set(p.lower() for p in products2)
    return jaccard_similarity(entities1, entities2)


def company_overlap_score(
    companies1: tuple[str, ...],
    companies2: tuple[str, ...],
) -> float:
    set1 = set(c.lower() for c in companies1)
    set2 = set(c.lower() for c in companies2)
    return jaccard_similarity(set1, set2)


def calculate_combined_similarity(
    candidate: dict[str, Any],
    historical: dict[str, Any],
    weights: dict[str, float],
) -> dict[str, float]:
    title_sim = title_similarity_score(
        str(candidate.get("title") or ""),
        str(historical.get("title") or ""),
    )
    norm_title_sim = normalized_title_similarity(
        str(candidate.get("normalized_title") or candidate.get("title") or ""),
        str(historical.get("normalized_title") or historical.get("title") or ""),
    )
    entity_sim = entity_overlap_score(
        tuple(candidate.get("companies", [])),
        tuple(candidate.get("products", [])),
        tuple(historical.get("companies", [])),
        tuple(historical.get("products", [])),
    )
    company_sim = company_overlap_score(
        tuple(candidate.get("companies", [])),
        tuple(historical.get("companies", [])),
    )
    event_match = str(candidate.get("event_type") or "") == str(historical.get("event_type") or "")
    angle_match = str(candidate.get("angle_type") or "") == str(historical.get("angle_type") or "")

    combined = (
        title_sim * weights.get("title_similarity", 0.35)
        + norm_title_sim * weights.get("normalized_title_similarity", 0.25)
        + entity_sim * weights.get("entity_overlap", 0.20)
        + company_sim * weights.get("company_overlap", 0.10)
        + (1.0 if event_match else 0.0) * weights.get("event_type_match", 0.10)
    )

    return {
        "title_similarity": round(title_sim, 4),
        "normalized_title_similarity": round(norm_title_sim, 4),
        "entity_overlap_score": round(entity_sim, 4),
        "company_overlap_score": round(company_sim, 4),
        "event_type_match": event_match,
        "angle_type_match": angle_match,
        "combined_score": round(combined, 4),
    }


def analyze_topic_similarity(
    candidates: list[dict[str, Any]],
    historical_topics: list[dict[str, Any]],
    run_date: str | None = None,
    duplicate_threshold: float = 0.72,
    hard_duplicate_threshold: float = 0.88,
    weights: dict[str, float] | None = None,
) -> TopicSimilarityReport:
    final_run_date = normalize_date(run_date)
    similarity_matches: list[SimilarityMatch] = []
    warnings: list[str] = []

    if not candidates:
        warnings.append("No candidates provided for similarity analysis")
    if not historical_topics:
        warnings.append("No historical topics available for comparison")

    default_weights = {
        "title_similarity": 0.35,
        "normalized_title_similarity": 0.25,
        "entity_overlap": 0.20,
        "company_overlap": 0.10,
        "event_type_match": 0.10,
    }
    final_weights = weights or default_weights

    for candidate in candidates:
        candidate_id = str(candidate.get("topic_id") or candidate.get("evidence_id") or "")
        for historical in historical_topics:
            historical_id = str(historical.get("topic_id") or "")
            if candidate_id == historical_id:
                continue

            sim_scores = calculate_combined_similarity(candidate, historical, final_weights)
            is_hard_duplicate = sim_scores["combined_score"] >= hard_duplicate_threshold
            is_similar = sim_scores["combined_score"] >= duplicate_threshold

            if is_similar:
                similarity_matches.append(SimilarityMatch(
                    topic_id=candidate_id,
                    candidate_title=str(candidate.get("title") or ""),
                    similar_to_id=historical_id,
                    similar_to_title=str(historical.get("title") or ""),
                    similar_to_date=str(historical.get("run_date") or ""),
                    **sim_scores,
                    is_hard_duplicate=is_hard_duplicate,
                    is_similar=is_similar,
                ))

    similarity_matches.sort(key=lambda m: -m.combined_score)

    return TopicSimilarityReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        candidate_count=len(candidates),
        historical_topic_count=len(historical_topics),
        similarity_matches=tuple(similarity_matches),
        hard_duplicate_count=sum(1 for m in similarity_matches if m.is_hard_duplicate),
        similar_count=len(similarity_matches),
        warnings=tuple(warnings),
    )


def report_to_dict(report: TopicSimilarityReport) -> dict[str, Any]:
    return asdict(report)


def render_markdown(report: TopicSimilarityReport) -> str:
    rows = []
    for index, match in enumerate(report.similarity_matches, start=1):
        duplicate_flag = "🔴 HARD" if match.is_hard_duplicate else ("🟡 SIMILAR" if match.is_similar else "")
        rows.append(
            "| "
            + " | ".join([
                str(index),
                duplicate_flag,
                str(round(match.combined_score * 100, 1)) + "%",
                match.candidate_title[:50] + "..." if len(match.candidate_title) > 50 else match.candidate_title,
                match.similar_to_date,
                match.similar_to_title[:50] + "..." if len(match.similar_to_title) > 50 else match.similar_to_title,
                str(round(match.title_similarity * 100, 1)) + "%",
                str(round(match.entity_overlap_score * 100, 1)) + "%",
            ])
            + " |"
        )

    return f"""# Topic Similarity Analysis Report
- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Candidates: `{report.candidate_count}`
- Historical topics: `{report.historical_topic_count}`
- Similar topics: `{report.similar_count}`
- Hard duplicates: `{report.hard_duplicate_count}`

## Similarity Matches

| # | Status | Combined | Candidate | Similar Date | Similar Topic | Title Sim | Entity Overlap |
|---:|---|---|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | None | - | None | - | - |'}

## Warnings

{chr(10).join(f"- {w}" for w in report.warnings) if report.warnings else "- None"}

## Notes

- Hard duplicates: combined score >= 0.88
- Similar topics: combined score >= 0.72
- schema_version: `{SCHEMA_VERSION}`
"""


def write_report(report: TopicSimilarityReport, output_path: str) -> None:
    payload = json.dumps(report_to_dict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    json_path = Path(output_path + ".json")
    md_path = Path(output_path + ".md")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(payload + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")


def load_report(json_path: str) -> TopicSimilarityReport | None:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return TopicSimilarityReport(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            generated_at=data.get("generated_at", ""),
            run_date=data.get("run_date", ""),
            candidate_count=int(data.get("candidate_count", 0)),
            historical_topic_count=int(data.get("historical_topic_count", 0)),
            similarity_matches=tuple(
                SimilarityMatch(
                    topic_id=m.get("topic_id", ""),
                    candidate_title=m.get("candidate_title", ""),
                    similar_to_id=m.get("similar_to_id", ""),
                    similar_to_title=m.get("similar_to_title", ""),
                    similar_to_date=m.get("similar_to_date", ""),
                    title_similarity=float(m.get("title_similarity", 0.0)),
                    normalized_title_similarity=float(m.get("normalized_title_similarity", 0.0)),
                    entity_overlap_score=float(m.get("entity_overlap_score", 0.0)),
                    company_overlap_score=float(m.get("company_overlap_score", 0.0)),
                    event_type_match=bool(m.get("event_type_match", False)),
                    angle_type_match=bool(m.get("angle_type_match", False)),
                    combined_score=float(m.get("combined_score", 0.0)),
                    is_hard_duplicate=bool(m.get("is_hard_duplicate", False)),
                    is_similar=bool(m.get("is_similar", False)),
                )
                for m in data.get("similarity_matches", [])
            ),
            hard_duplicate_count=int(data.get("hard_duplicate_count", 0)),
            similar_count=int(data.get("similar_count", 0)),
            warnings=tuple(data.get("warnings", [])),
        )
    except Exception:
        return None