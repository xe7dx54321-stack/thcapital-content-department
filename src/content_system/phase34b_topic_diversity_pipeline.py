"""Phase34B Topic Diversity Pipeline v1.

Main pipeline that orchestrates all diversity analysis components:
1. Topic History Memory
2. Topic Similarity Analysis
3. Source/Lane Diversity
4. Competitive Coverage Penalty
5. Differentiated Angle Boost
6. Title Normalization Guard
7. Topic Diversity Scoring
8. Main Topic Selection Reranker
9. Brief Integration
"""

from __future__ import annotations

import json
import yaml
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.topic_history_memory import (
    TopicHistoryReport,
    build_topic_history_memory,
    report_to_dict as history_to_dict,
    write_report as write_history_report,
)
from content_system.topic_similarity import (
    TopicSimilarityReport,
    analyze_topic_similarity,
    report_to_dict as similarity_to_dict,
    write_report as write_similarity_report,
)
from content_system.source_lane_diversity import (
    SourceLaneDiversityReport,
    analyze_source_lane_diversity,
    report_to_dict as source_lane_to_dict,
    write_report as write_source_lane_report,
)
from content_system.competitive_coverage_penalty import (
    CompetitiveCoveragePenaltyReport,
    apply_competitive_penalty,
    report_to_dict as competitive_to_dict,
    write_report as write_competitive_report,
)
from content_system.differentiated_angle_boost import (
    DifferentiatedAngleBoostReport,
    apply_angle_boosts,
    report_to_dict as angle_boost_to_dict,
    write_report as write_angle_boost_report,
)
from content_system.topic_title_normalization_guard import (
    TitleNormalizationReport,
    apply_title_guard,
    report_to_dict as title_guard_to_dict,
    write_report as write_title_guard_report,
)
from content_system.topic_diversity_scoring import (
    TopicDiversityReport,
    build_topic_diversity_report,
    report_to_dict as diversity_to_dict,
    write_report as write_diversity_report,
)
from content_system.main_topic_selection_reranker import (
    TopicRerankingReport,
    rerank_topics,
    report_to_dict as reranking_to_dict,
    write_report as write_reranking_report,
)
from content_system.topic_diversity_brief_integration import (
    BriefIntegrationReport,
    build_diversity_insights,
    report_to_dict as brief_integration_to_dict,
    write_report as write_brief_integration_report,
)

SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class PipelineOutput:
    schema_version: str
    generated_at: str
    run_date: str
    dry_run: bool
    history_report: dict[str, Any]
    similarity_report: dict[str, Any]
    source_lane_report: dict[str, Any]
    competitive_penalty_report: dict[str, Any]
    angle_boost_report: dict[str, Any]
    title_guard_report: dict[str, Any]
    diversity_report: dict[str, Any]
    reranking_report: dict[str, Any]
    brief_integration_report: dict[str, Any]
    outputs: dict[str, str]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class PipelineConfig:
    dry_run: bool = False
    history_window_days: int = 7
    duplicate_similarity_threshold: float = 0.72
    hard_duplicate_threshold: float = 0.88
    output_dir: str = "ignored"
    run_date: str | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def normalize_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return today_token()
    return text.replace("-", "")[:8]


def load_topic_diversity_policy(repo_root: Path) -> dict[str, Any]:
    policy_path = repo_root / "config" / "topic_diversity_policy.yaml"
    if not policy_path.exists():
        return {}
    try:
        with open(policy_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def load_differentiated_angle_policy(repo_root: Path) -> dict[str, Any]:
    policy_path = repo_root / "config" / "differentiated_angle_policy.yaml"
    if not policy_path.exists():
        return {}
    try:
        with open(policy_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def load_candidates(repo_root: Path, run_date: str) -> list[dict[str, Any]]:
    patterns = [
        f"**/{run_date}__topic-scoring*.json",
        f"**/{run_date}__evidence-packets*.json",
        f"**/latest_evidence_packets.json",
        f"**/latest_topic_scores.json",
    ]
    for pattern in patterns:
        for path in repo_root.glob(pattern):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                packets = data.get("evidence_packets") or data.get("topics") or data.get("candidates")
                if isinstance(packets, list):
                    return packets
            except Exception:
                continue
    return []


def run_pipeline(
    repo_root: Path,
    config: PipelineConfig | None = None,
) -> PipelineOutput:
    final_config = config or PipelineConfig()
    run_date = normalize_date(final_config.run_date)

    topic_policy = load_topic_diversity_policy(repo_root)
    angle_policy = load_differentiated_angle_policy(repo_root)

    output_dir = Path(repo_root) / final_config.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, str] = {}
    warnings: list[str] = []

    candidates = load_candidates(repo_root, run_date)
    if not candidates:
        warnings.append("No candidates found; using sample data for dry-run")
        candidates = [
            {
                "topic_id": "test_001",
                "evidence_id": "test_001",
                "title": "OpenAI发布GPT-5技术细节分析",
                "source_id": "openai",
                "source_category": "official",
                "event_type": "model_release",
                "score": 0.85,
                "companies": ["OpenAI"],
                "products": ["GPT-5"],
                "summary": "OpenAI发布了GPT-5的技术细节，包括新的推理架构和性能提升。",
            },
            {
                "topic_id": "test_002",
                "evidence_id": "test_002",
                "title": "NVIDIA推出新一代GPU加速AI训练",
                "source_id": "nvidia",
                "source_category": "official",
                "event_type": "product_release",
                "score": 0.78,
                "companies": ["NVIDIA"],
                "products": ["H200"],
                "summary": "NVIDIA推出H200 GPU，为AI训练提供更强算力支持。",
            },
            {
                "topic_id": "test_003",
                "evidence_id": "test_003",
                "title": "Anthropic发布Claude 3.5技术更新",
                "source_id": "anthropic",
                "source_category": "official",
                "event_type": "model_release",
                "score": 0.82,
                "companies": ["Anthropic"],
                "products": ["Claude 3.5"],
                "summary": "Anthropic发布Claude 3.5，提升了多模态能力和推理速度。",
            },
        ]

    history_report = build_topic_history_memory(
        repo_root,
        run_date=run_date,
        history_window_days=topic_policy.get("history_window_days", final_config.history_window_days),
    )
    outputs["history"] = str(output_dir / f"{run_date}__topic-history")
    write_history_report(history_report, outputs["history"])

    historical_topics = [
        {
            "topic_id": t.topic_id,
            "title": t.title,
            "run_date": t.run_date,
            "source_id": t.source_id,
            "lane": t.lane,
            "event_type": t.event_type,
            "angle_type": t.angle_type,
            "companies": list(t.companies),
            "products": list(t.products),
            "normalized_title": t.normalized_title,
        }
        for t in history_report.historical_topics
    ]

    similarity_report = analyze_topic_similarity(
        candidates,
        historical_topics,
        run_date=run_date,
        duplicate_threshold=topic_policy.get("duplicate_similarity_threshold", final_config.duplicate_similarity_threshold),
        hard_duplicate_threshold=topic_policy.get("hard_duplicate_threshold", final_config.hard_duplicate_threshold),
        weights=topic_policy.get("similarity_weights"),
    )
    outputs["similarity"] = str(output_dir / f"{run_date}__topic-similarity")
    write_similarity_report(similarity_report, outputs["similarity"])

    source_lane_report = analyze_source_lane_diversity(
        historical_topics,
        run_date=run_date,
    )
    outputs["source_lane"] = str(output_dir / f"{run_date}__source-lane-diversity")
    write_source_lane_report(source_lane_report, outputs["source_lane"])

    competitive_penalty_report = apply_competitive_penalty(
        candidates,
        run_date=run_date,
        penalty_score=topic_policy.get("penalties", {}).get("high_competitive_same_angle", 0.14),
    )
    outputs["competitive_penalty"] = str(output_dir / f"{run_date}__competitive-penalty")
    write_competitive_report(competitive_penalty_report, outputs["competitive_penalty"])

    angle_boost_report = apply_angle_boosts(
        candidates,
        run_date=run_date,
        strong_angle_threshold=angle_policy.get("angle_confidence_thresholds", {}).get("high", 0.75),
        fresh_angle_threshold=angle_policy.get("angle_confidence_thresholds", {}).get("medium", 0.50),
        weak_differentiation_threshold=angle_policy.get("angle_confidence_thresholds", {}).get("low", 0.25),
        strong_boost_score=angle_policy.get("boost_rules", {}).get("strong_differentiated_angle", {}).get("boost_score", 0.12),
        fresh_boost_score=angle_policy.get("boost_rules", {}).get("fresh_undercovered_angle", {}).get("boost_score", 0.10),
        multi_source_boost_score=topic_policy.get("boosts", {}).get("multi_source_support", 0.08),
        weak_penalty_score=angle_policy.get("penalty_rules", {}).get("weak_differentiation", {}).get("penalty_score", 0.12),
    )
    outputs["angle_boost"] = str(output_dir / f"{run_date}__angle-boost")
    write_angle_boost_report(angle_boost_report, outputs["angle_boost"])

    guards_config = topic_policy.get("guards", {})
    title_guard_report = apply_title_guard(
        candidates,
        run_date=run_date,
        require_human_readable=guards_config.get("require_human_readable", True),
        reject_raw_metadata=guards_config.get("reject_raw_metadata_title", True),
    )
    outputs["title_guard"] = str(output_dir / f"{run_date}__title-guard")
    write_title_guard_report(title_guard_report, outputs["title_guard"])

    diversity_report = build_topic_diversity_report(
        candidates,
        run_date=run_date,
        similarity_report=similarity_to_dict(similarity_report),
        source_lane_report=source_lane_to_dict(source_lane_report),
        competitive_penalty_report=competitive_to_dict(competitive_penalty_report),
        angle_boost_report=angle_boost_to_dict(angle_boost_report),
        title_guard_report=title_guard_to_dict(title_guard_report),
        policy={
            "penalties": topic_policy.get("penalties", {}),
            "boosts": topic_policy.get("boosts", {}),
        },
    )
    outputs["diversity"] = str(output_dir / f"{run_date}__topic-diversity")
    write_diversity_report(diversity_report, outputs["diversity"])

    reranking_report = rerank_topics(
        candidates,
        diversity_report=diversity_to_dict(diversity_report),
        run_date=run_date,
    )
    outputs["reranking"] = str(output_dir / f"{run_date}__topic-reranking")
    write_reranking_report(reranking_report, outputs["reranking"])

    brief_integration_report = build_diversity_insights(
        candidates,
        angle_report=angle_boost_to_dict(angle_boost_report),
        similarity_report=similarity_to_dict(similarity_report),
        diversity_report=diversity_to_dict(diversity_report),
        run_date=run_date,
    )
    outputs["brief_integration"] = str(output_dir / f"{run_date}__brief-integration")
    write_brief_integration_report(brief_integration_report, outputs["brief_integration"])

    return PipelineOutput(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=run_date,
        dry_run=final_config.dry_run,
        history_report=history_to_dict(history_report),
        similarity_report=similarity_to_dict(similarity_report),
        source_lane_report=source_lane_to_dict(source_lane_report),
        competitive_penalty_report=competitive_to_dict(competitive_penalty_report),
        angle_boost_report=angle_boost_to_dict(angle_boost_report),
        title_guard_report=title_guard_to_dict(title_guard_report),
        diversity_report=diversity_to_dict(diversity_report),
        reranking_report=reranking_to_dict(reranking_report),
        brief_integration_report=brief_integration_to_dict(brief_integration_report),
        outputs=outputs,
        warnings=tuple(warnings),
    )


def pipeline_to_dict(pipeline: PipelineOutput) -> dict[str, Any]:
    return asdict(pipeline)


def write_pipeline_output(pipeline: PipelineOutput, output_path: str) -> None:
    payload = json.dumps(pipeline_to_dict(pipeline), ensure_ascii=False, indent=2)
    path = Path(output_path + ".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload + "\n", encoding="utf-8")


def render_pipeline_summary(pipeline: PipelineOutput) -> str:
    diversity = pipeline.diversity_report
    reranking = pipeline.reranking_report

    return f"""# Phase34B Topic Diversity Pipeline Summary
- Generated at: `{pipeline.generated_at}`
- Run date: `{pipeline.run_date}`
- Dry run: `{pipeline.dry_run}`
- Schema version: `{SCHEMA_VERSION}`

## Pipeline Outputs

| Component | Output Path |
|---|---|
| Topic History Memory | `{pipeline.outputs.get('history', '-')}.json` |
| Topic Similarity | `{pipeline.outputs.get('similarity', '-')}.json` |
| Source/Lane Diversity | `{pipeline.outputs.get('source_lane', '-')}.json` |
| Competitive Coverage Penalty | `{pipeline.outputs.get('competitive_penalty', '-')}.json` |
| Differentiated Angle Boost | `{pipeline.outputs.get('angle_boost', '-')}.json` |
| Title Normalization Guard | `{pipeline.outputs.get('title_guard', '-')}.json` |
| Topic Diversity Scoring | `{pipeline.outputs.get('diversity', '-')}.json` |
| Main Topic Reranking | `{pipeline.outputs.get('reranking', '-')}.json` |
| Brief Integration | `{pipeline.outputs.get('brief_integration', '-')}.json` |

## Key Metrics

**Diversity Scoring:**
- Candidates: `{diversity.get('candidate_count', 0)}`
- Penalized: `{diversity.get('penalty_count', 0)}`
- Boosted: `{diversity.get('boost_count', 0)}`
- Neutral: `{diversity.get('neutral_count', 0)}`
- Avg original: `{round(diversity.get('avg_original_score', 0) * 100, 1)}%`
- Avg adjusted: `{round(diversity.get('avg_adjusted_score', 0) * 100, 1)}%`

**Reranking:**
- Rank changed: `{reranking.get('rank_changed_count', 0)}`
- Avg rank change: `{reranking.get('avg_rank_change', 0)}`

## Warnings

{chr(10).join(f"- {w}" for w in pipeline.warnings) if pipeline.warnings else "- None"}

## Notes

- All reports written to `ignored/` directory
- No full article text included in outputs
- Cloud mode: RSS/Mac runtime not required
"""