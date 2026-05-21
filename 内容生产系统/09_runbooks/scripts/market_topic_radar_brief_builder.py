#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from market_business_day import (
    business_window,
    business_window_status,
    day_token,
    parse_cst,
    timestamp_from_name,
    timestamp_in_business_window,
    window_file_tokens,
)
from market_source_strategy_defs import FUNNEL_LAYERS, infer_funnel_layer


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
SOURCE_PACKET_DIR = ROOT / "02_topic_radar" / "source_packets"
ASSET_CHAIN_DIR = ROOT / "02_topic_radar" / "asset_chains"
TOPIC_CLUSTER_DIR = ROOT / "02_topic_radar" / "topic_clusters"
DEEP_ARTICLE_DIR = ROOT / "02_topic_radar" / "deep_articles"
LOG_DIR = ROOT / "10_logs"


@dataclass
class SourcePacket:
    path: Path
    packet_id: str
    title: str
    source_id: str
    source_type: str
    platform: str
    canonical_url: str
    summary: str
    topic_tags: str
    captured_at: str
    primary_source: str
    verification_status: str
    citation_reliability: str
    heat_hint: str
    funnel_layer_key: str
    funnel_layer_name: str


@dataclass
class AssetChain:
    path: Path
    entity_name: str
    official_site: str
    source_packet_path: str


@dataclass
class TopicCluster:
    path: Path
    cluster_id: str
    title: str
    core_angle: str
    battlefield_type: str
    heat_signals: str
    evidence_signals: str
    market_score: str
    relevance_score: str
    brand_fit_score: str
    timeliness_score: str
    writeability_score: str
    differentiation_angle: str
    reason: str
    packet_ids: list[str]
    primary_source_signals: str
    diffusion_signals: str
    cn_propagation_signals: str
    heat_validation_signals: str
    funnel_coverage_judgment: str
    first_source_score: str
    spread_score: str
    breakout_score: str
    track_fit_score: str
    can_we_win_score: str
    extendability_score: str
    total_score: str
    decision_band: str


@dataclass
class DeepArticle:
    path: Path
    title: str
    source_id: str
    source_packet_path: str
    status: str


KV_RE = re.compile(r"^- `([^`]+)`: ?(.*)$")


LEGACY_PACKET_INFERENCE = [
    (
        re.compile(r"^trend__yc_launches_ai"),
        {
            "source_type": "official_listing",
            "primary_source": "partial",
            "verification_status": "official-platform-listing",
            "citation_reliability": "medium",
            "heat_hint": "newco + launch entrance",
        },
    ),
    (
        re.compile(r"^web__techcrunch_ai"),
        {
            "source_type": "media_feed",
            "primary_source": "no",
            "verification_status": "secondary-report",
            "citation_reliability": "medium",
            "heat_hint": "media entrance",
        },
    ),
    (
        re.compile(r"^web__finsmes_ai_gnews"),
        {
            "source_type": "fallback_media_feed",
            "primary_source": "no",
            "verification_status": "fallback-entry",
            "citation_reliability": "low",
            "heat_hint": "financing entrance + blocked-source fallback",
        },
    ),
    (
        re.compile(r"^trend__trend_hunt_"),
        {
            "source_type": "product_discovery_mirror",
            "primary_source": "no",
            "verification_status": "mirror-signal",
            "citation_reliability": "low",
            "heat_hint": "early signal + product discovery",
        },
    ),
    (
        re.compile(r"^trend__reddit_"),
        {
            "source_type": "community_discussion",
            "primary_source": "no",
            "verification_status": "community-signal",
            "citation_reliability": "low-medium",
            "heat_hint": "high heat + user signal",
        },
    ),
    (
        re.compile(r"^x__"),
        {
            "source_type": "social_signal",
            "primary_source": "partial",
            "verification_status": "social-primary-signal",
            "citation_reliability": "medium",
            "heat_hint": "fast social signal",
        },
    ),
    (
        re.compile(r"^web__openai_news"),
        {
            "source_type": "official_update",
            "primary_source": "yes",
            "verification_status": "primary-source",
            "citation_reliability": "high",
            "heat_hint": "official update",
        },
    ),
    (
        re.compile(r"^trend__github_trending"),
        {
            "source_type": "open_source_trend",
            "primary_source": "partial",
            "verification_status": "official-platform-listing",
            "citation_reliability": "medium",
            "heat_hint": "open-source traction",
        },
    ),
    (
        re.compile(r"^derived__"),
        {
            "source_type": "derived_official_object",
            "primary_source": "yes",
            "verification_status": "primary-source",
            "citation_reliability": "high",
            "heat_hint": "derived primary context",
        },
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build topic radar brief for TH Capital market content system")
    parser.add_argument("--date", default=datetime.now().date().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def list_business_window_files(folder: Path, suffix: str, date_text: str, ts_resolver) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(
        [
            path
            for path in folder.rglob(f"*{suffix}")
            if path.is_file()
            and "template" not in path.name
            and timestamp_in_business_window(ts_resolver(path), date_text)
        ]
    )


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        match = KV_RE.match(line)
        if not match:
            continue
        key, value = match.groups()
        fields[key] = value.strip()
    return fields


def clean(value: str, fallback: str = "n/a") -> str:
    value = value.replace("`", "").strip()
    return value if value else fallback


def infer_packet_field(source_id: str, field_name: str, fallback: str) -> str:
    for pattern, mapping in LEGACY_PACKET_INFERENCE:
        if pattern.search(source_id):
            value = mapping.get(field_name)
            if value:
                return value
    return fallback


def parse_packet(path: Path) -> SourcePacket:
    fields = parse_fields(path)
    source_id = clean(fields.get("source_id", "unknown"))
    source_type = clean(fields.get("source_type", infer_packet_field(source_id, "source_type", "unknown")))
    platform = clean(fields.get("platform", "unknown"))
    verification_status = clean(fields.get("verification_status", infer_packet_field(source_id, "verification_status", "unknown")))
    funnel_layer = infer_funnel_layer(
        source_id,
        source_type=source_type,
        verification_status=verification_status,
        platform=platform,
    )
    return SourcePacket(
        path=path,
        packet_id=clean(fields.get("packet_id", path.stem)),
        title=clean(fields.get("title", path.stem)),
        source_id=source_id,
        source_type=source_type,
        platform=platform,
        canonical_url=clean(fields.get("canonical_url", "n/a")),
        summary=clean(fields.get("summary", "n/a")),
        topic_tags=clean(fields.get("topic_tags", "n/a")),
        captured_at=clean(fields.get("captured_at", "n/a")),
        primary_source=clean(fields.get("primary_source", infer_packet_field(source_id, "primary_source", "unknown"))),
        verification_status=verification_status,
        citation_reliability=clean(fields.get("citation_reliability", infer_packet_field(source_id, "citation_reliability", "unknown"))),
        heat_hint=clean(fields.get("heat_hint", infer_packet_field(source_id, "heat_hint", "unknown"))),
        funnel_layer_key=funnel_layer.key,
        funnel_layer_name=funnel_layer.name,
    )


def parse_asset_chain(path: Path) -> AssetChain:
    fields = parse_fields(path)
    return AssetChain(
        path=path,
        entity_name=clean(fields.get("entity_name", path.stem)),
        official_site=clean(fields.get("official_site", "n/a")),
        source_packet_path=clean(fields.get("source_packet_path", "n/a")),
    )


def parse_cluster(path: Path) -> TopicCluster:
    fields = parse_fields(path)
    packet_ids_raw = fields.get("packet_ids", "")
    packet_ids = [item.strip().strip("`") for item in packet_ids_raw.split(",") if item.strip()]
    return TopicCluster(
        path=path,
        cluster_id=clean(fields.get("cluster_id", path.stem)),
        title=clean(fields.get("title", path.stem)),
        core_angle=clean(fields.get("core_angle", "n/a")),
        battlefield_type=clean(fields.get("battlefield_type", "n/a")),
        heat_signals=clean(fields.get("heat_signals", "n/a")),
        evidence_signals=clean(fields.get("evidence_signals", "n/a")),
        market_score=clean(fields.get("market_score", "n/a")),
        relevance_score=clean(fields.get("relevance_score", "n/a")),
        brand_fit_score=clean(fields.get("brand_fit_score", "n/a")),
        timeliness_score=clean(fields.get("timeliness_score", "n/a")),
        writeability_score=clean(fields.get("writeability_score", "n/a")),
        differentiation_angle=clean(fields.get("differentiation_angle", "n/a")),
        reason=clean(fields.get("Reason", fields.get("reason", "n/a"))),
        packet_ids=packet_ids,
        primary_source_signals=clean(fields.get("primary_source_signals", "n/a")),
        diffusion_signals=clean(fields.get("diffusion_signals", "n/a")),
        cn_propagation_signals=clean(fields.get("cn_propagation_signals", "n/a")),
        heat_validation_signals=clean(fields.get("heat_validation_signals", "n/a")),
        funnel_coverage_judgment=clean(fields.get("funnel_coverage_judgment", "n/a")),
        first_source_score=clean(fields.get("first_source_score", "n/a")),
        spread_score=clean(fields.get("spread_score", "n/a")),
        breakout_score=clean(fields.get("breakout_score", "n/a")),
        track_fit_score=clean(fields.get("track_fit_score", "n/a")),
        can_we_win_score=clean(fields.get("can_we_win_score", "n/a")),
        extendability_score=clean(fields.get("extendability_score", "n/a")),
        total_score=clean(fields.get("total_score", "n/a")),
        decision_band=clean(fields.get("decision_band", "n/a")),
    )


def parse_deep_article(path: Path) -> DeepArticle:
    fields = parse_fields(path)
    return DeepArticle(
        path=path,
        title=clean(fields.get("title", path.stem)),
        source_id=clean(fields.get("source_id", "unknown")),
        source_packet_path=clean(fields.get("source_packet_path", "n/a")),
        status=clean(fields.get("status", "n/a")),
    )


def source_packet_ts(path: Path):
    fields = parse_fields(path)
    return parse_cst(fields.get("captured_at")) or timestamp_from_name(path)


def asset_chain_ts(path: Path):
    fields = parse_fields(path)
    return (
        parse_cst(fields.get("derived_at"))
        or timestamp_from_name(fields.get("source_packet_path"))
        or timestamp_from_name(path)
    )


def topic_cluster_ts(path: Path):
    fields = parse_fields(path)
    return parse_cst(fields.get("generated_at")) or timestamp_from_name(path)


def deep_article_ts(path: Path):
    fields = parse_fields(path)
    return (
        parse_cst(fields.get("deep_captured_at"))
        or parse_cst(fields.get("rss_captured_at"))
        or timestamp_from_name(fields.get("source_packet_path"))
        or timestamp_from_name(path)
    )


def render_funnel_section(packets: list[SourcePacket]) -> list[str]:
    if not packets:
        return ["- `none`"]

    lines: list[str] = []
    for layer_key, layer in FUNNEL_LAYERS.items():
        layer_packets = [packet for packet in packets if packet.funnel_layer_key == layer_key]
        sample_titles = ", ".join(f"`{packet.title}`" for packet in layer_packets[:3]) if layer_packets else "none"
        lines.extend(
            [
                f"- `{layer.key}` / `{layer.name}`",
                f"  - `count`: `{len(layer_packets)}`",
                f"  - `purpose`: {layer.purpose}",
                f"  - `sample_titles`: {sample_titles}",
            ]
        )
    return lines


def build_brief(date_text: str) -> str:
    token = day_token(date_text)
    window_start, window_end = business_window(date_text)

    packet_paths = list_business_window_files(SOURCE_PACKET_DIR, "__source-packet.md", date_text, source_packet_ts)
    asset_paths = list_business_window_files(ASSET_CHAIN_DIR, "__asset-chain.md", date_text, asset_chain_ts)
    cluster_paths = list_business_window_files(TOPIC_CLUSTER_DIR, "__topic-cluster.md", date_text, topic_cluster_ts)
    deep_article_paths = list_business_window_files(DEEP_ARTICLE_DIR, "__deep-article.md", date_text, deep_article_ts)

    packets = [parse_packet(path) for path in packet_paths]
    assets = [parse_asset_chain(path) for path in asset_paths]
    clusters = [parse_cluster(path) for path in cluster_paths]
    deep_articles = [parse_deep_article(path) for path in deep_article_paths]
    verification_mix = Counter(packet.verification_status for packet in packets)
    source_type_mix = Counter(packet.source_type for packet in packets)
    funnel_mix = Counter(packet.funnel_layer_key for packet in packets)
    primary_packets = [packet for packet in packets if packet.primary_source in {"yes", "partial"}]

    referenced_packet_ids = {packet_id for cluster in clusters for packet_id in cluster.packet_ids}
    unclustered_packets = [packet for packet in packets if packet.packet_id not in referenced_packet_ids]

    output_path = ROOT / "03_topic_candidates" / f"{token}__daily-top8-to-top5.md"
    packet_file_tokens = ", ".join(window_file_tokens(packet_paths)) or "none"
    window_status = business_window_status(date_text)

    lines = [
        "# Market Topic Radar Brief",
        "",
        f"- `date`: `{date_text}`",
        f"- `source_scope`: `{window_start.strftime('%Y-%m-%d %H:%M:%S CST')} -> {window_end.strftime('%Y-%m-%d %H:%M:%S CST')}`",
        f"- `business_window_status`: `{window_status}`",
        f"- `source_packet_file_tokens`: `{packet_file_tokens}`",
        f"- `source_packet_count`: `{len(packets)}`",
        f"- `asset_chain_count`: `{len(assets)}`",
        f"- `topic_cluster_count`: `{len(clusters)}`",
        f"- `deep_article_count`: `{len(deep_articles)}`",
        f"- `suggested_output_path`: `{output_path}`",
        "",
        "## Signal Mix",
        "",
        f"- `verification_mix`: {', '.join(f'{key}={value}' for key, value in verification_mix.items()) if verification_mix else 'none'}",
        f"- `source_type_mix`: {', '.join(f'{key}={value}' for key, value in source_type_mix.items()) if source_type_mix else 'none'}",
        f"- `funnel_mix`: {', '.join(f'{key}={funnel_mix.get(key, 0)}' for key in FUNNEL_LAYERS) if funnel_mix else 'none'}",
        f"- `primary_or_partial_source_packets`: `{len(primary_packets)}`",
        "",
        "## Funnel Coverage",
        "",
        *render_funnel_section(packets),
        "",
        "## Open Topic Clusters",
    ]

    if clusters:
        for cluster in clusters:
            lines.extend(
                [
                    f"- `{cluster.title}`",
                    f"  - `battlefield_type`: `{cluster.battlefield_type}`",
                    f"  - `core_angle`: {cluster.core_angle}",
                    f"  - `funnel_coverage_judgment`: {cluster.funnel_coverage_judgment}",
                    f"  - `primary_source_signals`: {cluster.primary_source_signals}",
                    f"  - `diffusion_signals`: {cluster.diffusion_signals}",
                    f"  - `cn_propagation_signals`: {cluster.cn_propagation_signals}",
                    f"  - `heat_validation_signals`: {cluster.heat_validation_signals}",
                    f"  - `heat_signals`: {cluster.heat_signals}",
                    f"  - `evidence_signals`: {cluster.evidence_signals}",
                    f"  - `scores_legacy`: market={cluster.market_score} / relevance={cluster.relevance_score} / brand_fit={cluster.brand_fit_score} / timeliness={cluster.timeliness_score} / writeability={cluster.writeability_score}",
                    f"  - `scores_v2`: first_source={cluster.first_source_score} / spread={cluster.spread_score} / breakout={cluster.breakout_score} / track_fit={cluster.track_fit_score} / can_we_win={cluster.can_we_win_score} / extendability={cluster.extendability_score} / total={cluster.total_score}",
                    f"  - `decision_band`: {cluster.decision_band}",
                    f"  - `differentiation_angle`: {cluster.differentiation_angle}",
                    f"  - `reason`: {cluster.reason}",
                    f"  - `packet_ids`: {', '.join(cluster.packet_ids) or 'none'}",
                    f"  - `path`: `{cluster.path}`",
                ]
            )
    else:
        lines.append("- `none`")

    lines.extend(["", "## Unclustered Packet Seeds"])
    if unclustered_packets:
        for packet in sorted(unclustered_packets, key=lambda item: item.path.name, reverse=True)[:12]:
            lines.extend(
                [
                    f"- `{packet.title}`",
                    f"  - `packet_id`: `{packet.packet_id}`",
                    f"  - `source_id`: `{packet.source_id}`",
                    f"  - `funnel_layer`: `{packet.funnel_layer_key}` / `{packet.funnel_layer_name}`",
                    f"  - `source_type`: `{packet.source_type}`",
                    f"  - `verification_status`: `{packet.verification_status}` / `primary_source`: `{packet.primary_source}`",
                    f"  - `summary`: {packet.summary}",
                    f"  - `heat_hint`: `{packet.heat_hint}`",
                    f"  - `tags`: {packet.topic_tags}",
                    f"  - `canonical_url`: `{packet.canonical_url}`",
                    f"  - `path`: `{packet.path}`",
                ]
            )
    else:
        lines.append("- `none`")

    lines.extend(["", "## Packet Bank"])
    if packets:
        for packet in sorted(packets, key=lambda item: item.path.name, reverse=True)[:20]:
            lines.extend(
                [
                    f"- `{packet.title}` | `{packet.source_id}`",
                    f"  - `packet_id`: `{packet.packet_id}`",
                    f"  - `funnel_layer`: `{packet.funnel_layer_key}` / `{packet.funnel_layer_name}`",
                    f"  - `source_type`: `{packet.source_type}`",
                    f"  - `verification_status`: `{packet.verification_status}` / `primary_source`: `{packet.primary_source}`",
                    f"  - `citation_reliability`: `{packet.citation_reliability}`",
                    f"  - `heat_hint`: `{packet.heat_hint}`",
                    f"  - `summary`: {packet.summary}",
                    f"  - `tags`: {packet.topic_tags}",
                    f"  - `url`: `{packet.canonical_url}`",
                    f"  - `path`: `{packet.path}`",
                ]
            )
    else:
        lines.append("- `none`")

    lines.extend(["", "## Deep Article Bank"])
    if deep_articles:
        for article in sorted(deep_articles, key=lambda item: item.path.name, reverse=True)[:12]:
            lines.extend(
                [
                    f"- `{article.title}` | `{article.source_id}`",
                    f"  - `status`: `{article.status}`",
                    f"  - `source_packet_path`: `{article.source_packet_path}`",
                    f"  - `path`: `{article.path}`",
                ]
            )
    else:
        lines.append("- `none`")

    lines.extend(["", "## Primary / Partial Source Packets"])
    if primary_packets:
        for packet in sorted(primary_packets, key=lambda item: item.path.name, reverse=True)[:12]:
            lines.extend(
                [
                    f"- `{packet.title}` | `{packet.source_id}`",
                    f"  - `funnel_layer`: `{packet.funnel_layer_key}` / `{packet.funnel_layer_name}`",
                    f"  - `verification_status`: `{packet.verification_status}`",
                    f"  - `summary`: {packet.summary}",
                    f"  - `url`: `{packet.canonical_url}`",
                    f"  - `path`: `{packet.path}`",
                ]
            )
    else:
        lines.append("- `none`")

    lines.extend(["", "## Asset Chains"])
    if assets:
        for asset in sorted(assets, key=lambda item: item.path.name, reverse=True)[:12]:
            lines.extend(
                [
                    f"- `{asset.entity_name}`",
                    f"  - `official_site`: `{asset.official_site}`",
                    f"  - `source_packet_path`: `{asset.source_packet_path}`",
                    f"  - `path`: `{asset.path}`",
                ]
            )
    else:
        lines.append("- `none`")

    lines.extend(
        [
            "",
            "## Ranking Checklist",
            "",
            "- `Pass 0`: 先把当天线索聚成 `event cluster`，不要直接对单条 source packet 排名",
            "- `Pass 1`: 按四层漏斗检查事件链是否走通：`L1 原始信源 → L2 技术/产品扩散 → L3 中文传播 → L4 平台热度验证`",
            "- `Pass 2`: 分开写 `heat signal` 和 `evidence signal`；热度高不等于证据强",
            "- `Business-day rule`: input scope must follow `T-1 17:00 -> T 14:30` and may legally include previous-evening files",
            "- `Pass 3`: 用 V2 六维评分：`first_source / spread / breakout / track_fit / can_we_win / extendability`",
            "- `Pass 4`: 再做主战场 / 相邻战场 / 品牌身份重排，但不能机械边缘化高热相邻战场题",
            "- `Primary-source rule`: 只要能补，就优先补 `L1` 原始口径；中文媒体和热榜不能替代官方信源",
            "- `WeChat-study rule`: 微信 deep article 不只是选题入口，也是标题、结构、叙事和钩子复盘素材",
            "- `Why-us rule`: 进入 Top 5 前，必须回答“竞品在说什么 / 我们还能补什么 / 为什么该我们写”",
            "- `Holdout discipline`: dropped 3 must stay visible with restore condition",
            "- `Citation rule`: every recommended topic must keep original links and source packet paths",
            "- `No fake fullness`: if fewer than 8 strong candidates exist, explicitly mark supply gap",
            "",
            "## Required Output",
            "",
            "- 输出 `Top 8 → Top 5` 板子",
            "- Top 5 必须基于 `事件簇` 而不是零散 source packet",
            "- Top 5 必须解释为什么推荐，以及为什么现在写胜率高",
            "- Holdout 3 必须解释为什么能进 Top 8、为什么被放下、能否捞回、捞回角度是什么",
            "- 每个 Top 5 推荐项必须包含：题目 / 一句话判断 / 事件簇键 / 四层漏斗覆盖 / 市场潜力 / heat signal / evidence signal / 品牌贴合度 / 竞品态势 / 为什么该我们写 / 平台发酵 / 原始链接 / 建议切入角度 / 适合平台 / 风险提示",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    brief = build_brief(args.date)
    if args.write:
        out_path = LOG_DIR / f"{day_token(args.date)}__market-topic-radar-brief.md"
        out_path.write_text(brief, encoding="utf-8")
        print(out_path)
        return
    print(brief, end="")


if __name__ == "__main__":
    main()
