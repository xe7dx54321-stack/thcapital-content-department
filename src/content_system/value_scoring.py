"""Rule-based value scoring for topic clusters."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths

SCHEMA_VERSION = "v1"
DEFAULT_WEIGHTS = {
    "source_authority": 0.18,
    "freshness": 0.12,
    "novelty": 0.10,
    "strategic_relevance": 0.18,
    "market_impact": 0.14,
    "technical_substance": 0.12,
    "narrative_potential": 0.10,
    "evidence_strength": 0.06,
}


@dataclass(frozen=True)
class ClusterScore:
    schema_version: str
    cluster_id: str
    run_date: str
    theme: str
    total_score: float
    score_band: str
    recommended_action: str
    dimensions: dict[str, float]
    evidence_count: int
    source_count: int
    tier_a_count: int
    source_ids: tuple[str, ...]
    primary_event_type: str
    why_it_matters: str
    suggested_angles: tuple[str, ...]
    items: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class ValueScoreReport:
    schema_version: str
    generated_at: str
    run_date: str
    cluster_count: int
    scored_cluster_count: int
    scores: tuple[ClusterScore, ...]
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


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def load_rules(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "config" / "value_scoring_rules.json"
    payload = read_json(path)
    return payload if payload else {"weights": DEFAULT_WEIGHTS}


def average(values: list[float], default: float = 0.0) -> float:
    return sum(values) / len(values) if values else default


def evidence_strength_value(value: str) -> float:
    return {"HIGH": 95.0, "MEDIUM": 70.0, "LOW": 45.0}.get(value, 40.0)


def keyword_score(text: str, keywords: list[str], base: float = 45.0, step: float = 8.0) -> float:
    lowered = text.lower()
    hits = sum(1 for keyword in keywords if keyword.lower() in lowered)
    return clamp(base + hits * step)


def cluster_dimensions(cluster: dict[str, Any], rules: dict[str, Any]) -> dict[str, float]:
    items = cluster.get("items") if isinstance(cluster.get("items"), list) else []
    source_authority = average([safe_float(item.get("source_authority_score")) * 100 for item in items], 55.0)
    freshness = average([safe_float(item.get("freshness_score")) for item in items], 60.0)
    technical = average([safe_float(item.get("technical_substance_score")) for item in items], 45.0)
    narrative = average([safe_float(item.get("narrative_potential_score")) for item in items], 45.0)
    evidence_strength = average([evidence_strength_value(str(item.get("evidence_strength") or "")) for item in items], 45.0)

    evidence_count = safe_int(cluster.get("evidence_count"))
    source_count = safe_int(cluster.get("source_count"))
    tier_a_count = safe_int(cluster.get("tier_a_count"))
    event_type = str(cluster.get("primary_event_type") or "")
    tags = cluster.get("domain_tags") if isinstance(cluster.get("domain_tags"), list) else []
    theme = str(cluster.get("theme") or "")
    text = " ".join([theme, event_type, " ".join(str(tag) for tag in tags)])

    novelty = clamp(45.0 + min(evidence_count, 5) * 7.0 + min(source_count, 3) * 5.0)
    strategic_relevance = keyword_score(text, list(rules.get("strategic_keywords") or []), base=45.0, step=7.0)
    market_impact = keyword_score(text, list(rules.get("market_keywords") or []), base=42.0, step=8.0)
    if event_type in {"product_release", "model_release", "partnership"}:
        market_impact += 12.0
    if tier_a_count:
        strategic_relevance += min(tier_a_count, 3) * 5.0
        market_impact += min(tier_a_count, 3) * 4.0

    return {
        "source_authority": round(clamp(source_authority), 2),
        "freshness": round(clamp(freshness), 2),
        "novelty": round(clamp(novelty), 2),
        "strategic_relevance": round(clamp(strategic_relevance), 2),
        "market_impact": round(clamp(market_impact), 2),
        "technical_substance": round(clamp(technical), 2),
        "narrative_potential": round(clamp(narrative), 2),
        "evidence_strength": round(clamp(evidence_strength), 2),
    }


def total_score(dimensions: dict[str, float], rules: dict[str, Any]) -> float:
    weights = rules.get("weights") if isinstance(rules.get("weights"), dict) else DEFAULT_WEIGHTS
    score = 0.0
    for key, default_weight in DEFAULT_WEIGHTS.items():
        score += dimensions.get(key, 0.0) * safe_float(weights.get(key, default_weight))
    return round(clamp(score), 2)


def band_and_action(score: float, rules: dict[str, Any]) -> tuple[str, str]:
    bands = rules.get("score_bands") if isinstance(rules.get("score_bands"), dict) else {}
    for band in ("A", "B", "C", "D"):
        config = bands.get(band) if isinstance(bands.get(band), dict) else {}
        minimum = safe_float(config.get("min", {"A": 80, "B": 65, "C": 50, "D": 0}[band]))
        if score >= minimum:
            return band, str(config.get("recommended_action") or {
                "A": "candidate_for_deep_article",
                "B": "candidate_for_short_post",
                "C": "monitor",
                "D": "archive",
            }[band])
    return "D", "archive"


def score_cluster(cluster: dict[str, Any], rules: dict[str, Any], run_date: str) -> ClusterScore:
    dimensions = cluster_dimensions(cluster, rules)
    score = total_score(dimensions, rules)
    band, action = band_and_action(score, rules)
    return ClusterScore(
        schema_version=SCHEMA_VERSION,
        cluster_id=str(cluster.get("cluster_id") or ""),
        run_date=run_date,
        theme=str(cluster.get("theme") or ""),
        total_score=score,
        score_band=band,
        recommended_action=action,
        dimensions=dimensions,
        evidence_count=safe_int(cluster.get("evidence_count")),
        source_count=safe_int(cluster.get("source_count")),
        tier_a_count=safe_int(cluster.get("tier_a_count")),
        source_ids=tuple(str(item) for item in cluster.get("source_ids", []) if item),
        primary_event_type=str(cluster.get("primary_event_type") or "unknown"),
        why_it_matters=str(cluster.get("why_it_matters") or ""),
        suggested_angles=tuple(str(item) for item in cluster.get("suggested_angles", []) if item),
        items=tuple(item for item in cluster.get("items", []) if isinstance(item, dict)),
    )


def build_value_score_report(paths: ProjectPaths, run_date: str | None = None) -> ValueScoreReport:
    input_path = paths.market_content_root / "03_topic_candidates" / "latest_topic_clusters.json"
    payload = read_json(input_path)
    final_run_date = normalize_date(run_date or payload.get("run_date"))
    raw_clusters = payload.get("clusters")
    clusters = [item for item in raw_clusters if isinstance(item, dict)] if isinstance(raw_clusters, list) else []
    rules = load_rules(paths.repo_root)
    warnings: list[str] = []
    if not input_path.exists():
        warnings.append("latest_topic_clusters.json not found; run make topic-clusters first.")
    if not clusters:
        warnings.append("No topic clusters available for scoring.")

    scores = tuple(sorted((score_cluster(cluster, rules, final_run_date) for cluster in clusters), key=lambda item: item.total_score, reverse=True))
    return ValueScoreReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        cluster_count=len(clusters),
        scored_cluster_count=len(scores),
        scores=scores,
        warnings=tuple(warnings),
    )


def report_to_dict(report: ValueScoreReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: ValueScoreReport, max_items: int = 80) -> str:
    rows = []
    for index, score in enumerate(report.scores[:max_items], start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    f"{score.total_score:.2f}",
                    score.score_band,
                    escape_cell(score.theme),
                    score.recommended_action,
                    str(score.evidence_count),
                    escape_cell(", ".join(score.source_ids)),
                ]
            )
            + " |"
        )
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Topic Cluster Scores v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Clusters: `{report.cluster_count}`
- Scored clusters: `{report.scored_cluster_count}`

## Scores

| Rank | Score | Band | Theme | Recommended Action | Evidence | Sources |
|---:|---:|---|---|---|---:|---|
{chr(10).join(rows) if rows else '| 0 | 0 | D | None | archive | 0 | - |'}

## Warnings

{warnings}

## Notes

- Value Scoring v1 is heuristic and rule-based. It is intended for ranking candidates, not final editorial judgment.
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "03_topic_candidates"
    return {
        "dated_json": root / f"{run_date}__topic-cluster-scores.json",
        "dated_md": root / f"{run_date}__topic-cluster-scores.md",
        "latest_json": root / "latest_topic_cluster_scores.json",
        "latest_md": root / "latest_topic_cluster_scores.md",
    }


def write_value_score_report(report: ValueScoreReport, paths: ProjectPaths) -> dict[str, Path]:
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
