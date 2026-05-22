"""Rule-based topic clustering for Evidence Packet v1."""

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
STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "into",
    "that",
    "this",
    "your",
    "new",
    "how",
    "are",
    "our",
    "you",
    "its",
    "more",
    "openai",
    "google",
    "nvidia",
}


@dataclass(frozen=True)
class TopicCluster:
    schema_version: str
    cluster_id: str
    run_date: str
    theme: str
    primary_event_type: str
    evidence_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    companies: tuple[str, ...]
    products: tuple[str, ...]
    models: tuple[str, ...]
    domain_tags: tuple[str, ...]
    evidence_count: int
    source_count: int
    tier_a_count: int
    why_it_matters: str
    suggested_angles: tuple[str, ...]
    items: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class TopicClusterReport:
    schema_version: str
    generated_at: str
    run_date: str
    evidence_count: int
    cluster_count: int
    clusters: tuple[TopicCluster, ...]
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


def text_tokens(text: str) -> tuple[str, ...]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_+-]{2,}", text.lower())
    return tuple(word for word in words if word not in STOPWORDS)


def entity_set(packet: dict[str, Any]) -> set[str]:
    entities = packet.get("entities")
    if not isinstance(entities, dict):
        return set()
    values: set[str] = set()
    for key in ("companies", "products", "models"):
        raw = entities.get(key)
        if isinstance(raw, list):
            values.update(str(item).lower() for item in raw if item)
    return values


def packet_cluster_key(packet: dict[str, Any]) -> str:
    entities = sorted(entity_set(packet))
    event_type = str(packet.get("event_type") or "unknown")
    if entities:
        return f"entity::{event_type}::{entities[0]}"
    tokens = text_tokens(str(packet.get("title") or ""))
    if tokens:
        return f"token::{event_type}::{tokens[0]}"
    return f"single::{packet.get('evidence_id')}"


def mergeable(packet: dict[str, Any], cluster_items: list[dict[str, Any]]) -> bool:
    current_entities = entity_set(packet)
    if current_entities:
        for item in cluster_items:
            if current_entities & entity_set(item):
                return True
    return False


def cluster_packets(evidence_packets: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    clusters: list[list[dict[str, Any]]] = []
    keyed: dict[str, list[dict[str, Any]]] = {}

    for packet in evidence_packets:
        placed = False
        if entity_set(packet):
            for cluster in clusters:
                if mergeable(packet, cluster):
                    cluster.append(packet)
                    placed = True
                    break
        if placed:
            continue

        key = packet_cluster_key(packet)
        if key in keyed:
            keyed[key].append(packet)
            placed = True
        else:
            keyed[key] = [packet]
            clusters.append(keyed[key])

    return clusters


def most_common(values: list[str], default: str = "unknown") -> str:
    counts: dict[str, int] = {}
    for value in values:
        if not value:
            continue
        counts[value] = counts.get(value, 0) + 1
    if not counts:
        return default
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def unique_ordered(values: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


def best_theme(items: list[dict[str, Any]]) -> str:
    ranked = sorted(
        items,
        key=lambda item: (
            float(item.get("source_authority_score") or 0),
            float(item.get("narrative_potential_score") or 0),
            len(str(item.get("title") or "")),
        ),
        reverse=True,
    )
    return str(ranked[0].get("title") or "Untitled cluster") if ranked else "Untitled cluster"


def cluster_id(run_date: str, evidence_ids: tuple[str, ...], theme: str) -> str:
    digest = hashlib.sha1(("|".join(evidence_ids) + theme).encode("utf-8")).hexdigest()[:12]
    return f"tc_{run_date}_{digest}"


def why_it_matters(event_type: str, tier_a_count: int, evidence_count: int, tags: tuple[str, ...]) -> str:
    authority = "一手官方信号" if tier_a_count else "多源信号"
    if event_type in {"product_release", "model_release"}:
        return f"{authority}显示产品/模型方向发生更新，可能影响 AI/Agent 市场叙事和工具采用。"
    if event_type == "partnership":
        return f"{authority}显示生态合作推进，值得观察企业采用和渠道扩散。"
    if event_type == "research":
        return f"{authority}提供研究进展线索，可作为后续技术趋势判断素材。"
    if "agents" in tags:
        return f"{authority}与 Agent 工作流相关，适合进入后续选题观察。"
    return f"{authority}形成 {evidence_count} 条 evidence，可进入候选池继续评分。"


def suggested_angles(event_type: str, tags: tuple[str, ...], companies: tuple[str, ...]) -> tuple[str, ...]:
    lead = companies[0] if companies else "AI 公司"
    angles = [
        f"{lead} 这次更新对 Agent 工作流意味着什么",
        "从产品能力、开发者采用和企业落地三个角度拆解",
    ]
    if event_type in {"model_release", "product_release"}:
        angles.append("对比同类模型/工具，判断是否有真实差异化")
    elif "infrastructure" in tags:
        angles.append("评估算力和推理成本变化对应用层的影响")
    else:
        angles.append("观察后续一周是否出现社区复述和二次传播")
    return tuple(angles)


def build_cluster(run_date: str, items: list[dict[str, Any]]) -> TopicCluster:
    evidence_ids = tuple(str(item.get("evidence_id") or "") for item in items)
    source_ids = unique_ordered([str(item.get("source_id") or "") for item in items])
    event_type = most_common([str(item.get("event_type") or "") for item in items])

    companies: list[str] = []
    products: list[str] = []
    models: list[str] = []
    tags: list[str] = []
    for item in items:
        entities = item.get("entities")
        if isinstance(entities, dict):
            companies.extend(str(value) for value in entities.get("companies", []) if value)
            products.extend(str(value) for value in entities.get("products", []) if value)
            models.extend(str(value) for value in entities.get("models", []) if value)
        raw_tags = item.get("domain_tags")
        if isinstance(raw_tags, list):
            tags.extend(str(value) for value in raw_tags if value)

    company_values = unique_ordered(companies)
    product_values = unique_ordered(products)
    model_values = unique_ordered(models)
    tag_values = unique_ordered(tags)
    theme = best_theme(items)
    tier_a_count = sum(1 for item in items if item.get("source_tier") == "A")
    compact_items = tuple(
        {
            "evidence_id": item.get("evidence_id"),
            "title": item.get("title"),
            "url": item.get("url"),
            "source_id": item.get("source_id"),
            "source_tier": item.get("source_tier"),
            "event_type": item.get("event_type"),
            "source_authority_score": item.get("source_authority_score"),
            "freshness_score": item.get("freshness_score"),
            "technical_substance_score": item.get("technical_substance_score"),
            "narrative_potential_score": item.get("narrative_potential_score"),
            "evidence_strength": item.get("evidence_strength"),
        }
        for item in items
    )

    return TopicCluster(
        schema_version=SCHEMA_VERSION,
        cluster_id=cluster_id(run_date, evidence_ids, theme),
        run_date=run_date,
        theme=theme,
        primary_event_type=event_type,
        evidence_ids=evidence_ids,
        source_ids=source_ids,
        companies=company_values,
        products=product_values,
        models=model_values,
        domain_tags=tag_values,
        evidence_count=len(items),
        source_count=len(source_ids),
        tier_a_count=tier_a_count,
        why_it_matters=why_it_matters(event_type, tier_a_count, len(items), tag_values),
        suggested_angles=suggested_angles(event_type, tag_values, company_values),
        items=compact_items,
    )


def build_topic_cluster_report(paths: ProjectPaths, run_date: str | None = None) -> TopicClusterReport:
    input_path = paths.market_content_root / "03_topic_candidates" / "latest_evidence_packets.json"
    payload = read_json(input_path)
    final_run_date = normalize_date(run_date or payload.get("run_date"))
    raw_packets = payload.get("evidence_packets")
    evidence_packets = [item for item in raw_packets if isinstance(item, dict)] if isinstance(raw_packets, list) else []
    warnings: list[str] = []
    if not input_path.exists():
        warnings.append("latest_evidence_packets.json not found; run make evidence-packets first.")
    if not evidence_packets:
        warnings.append("No evidence packets available for clustering.")

    clusters = tuple(build_cluster(final_run_date, items) for items in cluster_packets(evidence_packets))
    clusters = tuple(sorted(clusters, key=lambda cluster: (-cluster.evidence_count, cluster.theme)))

    return TopicClusterReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        evidence_count=len(evidence_packets),
        cluster_count=len(clusters),
        clusters=clusters,
        warnings=tuple(warnings),
    )


def report_to_dict(report: TopicClusterReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: TopicClusterReport, max_items: int = 80) -> str:
    rows = []
    for index, cluster in enumerate(report.clusters[:max_items], start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    escape_cell(cluster.theme),
                    escape_cell(cluster.primary_event_type),
                    str(cluster.evidence_count),
                    str(cluster.source_count),
                    str(cluster.tier_a_count),
                    escape_cell(", ".join(cluster.source_ids)),
                ]
            )
            + " |"
        )
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Topic Clusters v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Evidence packets: `{report.evidence_count}`
- Topic clusters: `{report.cluster_count}`

## Clusters

| # | Theme | Event Type | Evidence | Sources | Tier A | Source IDs |
|---:|---|---|---:|---:|---:|---|
{chr(10).join(rows) if rows else '| 0 | None | - | 0 | 0 | 0 | - |'}

## Warnings

{warnings}

## Notes

- Topic Cluster v1 uses entity overlap and simple title tokens only; no embeddings or vector DB.
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "03_topic_candidates"
    return {
        "dated_json": root / f"{run_date}__topic-clusters.json",
        "dated_md": root / f"{run_date}__topic-clusters.md",
        "latest_json": root / "latest_topic_clusters.json",
        "latest_md": root / "latest_topic_clusters.md",
    }


def write_topic_cluster_report(report: TopicClusterReport, paths: ProjectPaths) -> dict[str, Path]:
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
