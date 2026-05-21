#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_business_day import (
    business_window,
    business_window_status,
    day_token,
    parse_cst,
    timestamp_from_name,
    timestamp_in_business_window,
    window_file_tokens,
)


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
SOURCE_PACKET_DIR = ROOT / "02_topic_radar" / "source_packets"
ASSET_CHAIN_DIR = ROOT / "02_topic_radar" / "asset_chains"
TOPIC_CLUSTER_DIR = ROOT / "02_topic_radar" / "topic_clusters"
DEEP_ARTICLE_DIR = ROOT / "02_topic_radar" / "deep_articles"
LOG_DIR = ROOT / "10_logs"

CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
SUMMARY_LINE_RE = re.compile(r"^- `([^`]+)` → `([^`]+)` → `([^`]+)`$")


@dataclass
class SourcePacket:
    path: Path
    title: str
    source_id: str
    platform: str
    captured_at: str
    canonical_url: str
    primary_source: str
    heat_hint: str


@dataclass
class CaptureSummaryItem:
    source_id: str
    title: str
    packet_path: Path
    exists: bool


@dataclass
class CaptureSummary:
    path: Path
    items: list[CaptureSummaryItem]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a real-file manifest for market content source packets.")
    parser.add_argument("--date", default=datetime.now(CN_TZ).date().isoformat(), help="Requested logical date in YYYY-MM-DD.")
    parser.add_argument("--write", action="store_true", help="Write the manifest into 10_logs.")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def source_packet_ts(path: Path) -> datetime | None:
    fields = parse_fields(path)
    return parse_cst(fields.get("captured_at")) or timestamp_from_name(path)


def asset_chain_ts(path: Path) -> datetime | None:
    fields = parse_fields(path)
    return (
        parse_cst(fields.get("derived_at"))
        or timestamp_from_name(fields.get("source_packet_path"))
        or timestamp_from_name(path)
    )


def topic_cluster_ts(path: Path) -> datetime | None:
    fields = parse_fields(path)
    return parse_cst(fields.get("generated_at")) or timestamp_from_name(path)


def deep_article_ts(path: Path) -> datetime | None:
    fields = parse_fields(path)
    return (
        parse_cst(fields.get("deep_captured_at"))
        or parse_cst(fields.get("rss_captured_at"))
        or timestamp_from_name(fields.get("source_packet_path"))
        or timestamp_from_name(path)
    )


def capture_summary_ts(path: Path) -> datetime | None:
    fields = parse_fields(path)
    return parse_cst(fields.get("run_at")) or timestamp_from_name(path)


def collect_source_packets(requested_date: str) -> list[SourcePacket]:
    packets: list[SourcePacket] = []
    for path in sorted(SOURCE_PACKET_DIR.glob("*__source-packet.md")):
        if not timestamp_in_business_window(source_packet_ts(path), requested_date):
            continue
        fields = parse_fields(path)
        packets.append(
            SourcePacket(
                path=path,
                title=clean(fields.get("title", path.stem)),
                source_id=clean(fields.get("source_id", "n/a")),
                platform=clean(fields.get("platform", "n/a")),
                captured_at=clean(fields.get("captured_at", "n/a")),
                canonical_url=clean(fields.get("canonical_url", "n/a")),
                primary_source=clean(fields.get("primary_source", "n/a")),
                heat_hint=clean(fields.get("heat_hint", "n/a")),
            )
        )
    return packets


def collect_simple_paths(root: Path, requested_date: str, suffix: str, ts_resolver) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.rglob(f"*{suffix}")
        if path.is_file()
        and "template" not in path.name
        and timestamp_in_business_window(ts_resolver(path), requested_date)
    )


def collect_capture_summaries(requested_date: str) -> list[CaptureSummary]:
    summaries: list[CaptureSummary] = []
    for path in sorted(LOG_DIR.glob("*__market-topic-capture-summary.md")):
        if not timestamp_in_business_window(capture_summary_ts(path), requested_date):
            continue
        items: list[CaptureSummaryItem] = []
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            match = SUMMARY_LINE_RE.match(raw_line.strip())
            if not match:
                continue
            source_id, title, packet_path = match.groups()
            if not packet_path.startswith("/Users/apple/Documents/同行资本内容部门/内容生产系统/"):
                continue
            packet = Path(packet_path)
            items.append(
                CaptureSummaryItem(
                    source_id=source_id,
                    title=title,
                    packet_path=packet,
                    exists=packet.exists(),
                )
            )
        summaries.append(CaptureSummary(path=path, items=items))
    return summaries


def render_manifest(
    requested_date: str,
    resolution_mode: str,
    source_packets: list[SourcePacket],
    asset_chains: list[Path],
    topic_clusters: list[Path],
    deep_articles: list[Path],
    capture_summaries: list[CaptureSummary],
) -> str:
    generated_at = format_ts(now_cn())
    window_start, window_end = business_window(requested_date)
    file_tokens = ", ".join(window_file_tokens([packet.path for packet in source_packets])) or "none"
    warnings: list[str] = []
    if resolution_mode == "business-window-open":
        warnings.append(
            "business window is still open; do not freeze Top20 or downstream selection before 14:30 CST"
        )
    if resolution_mode == "business-window-empty":
        warnings.append("no source packets found inside the business window; downstream stages should no-op instead of guessing")

    dangling_rows: list[str] = []
    for summary in capture_summaries:
        for item in summary.items:
            if item.exists:
                continue
            dangling_rows.append(
                f"- `summary`: `{summary.path}` | `source`: `{item.source_id}` | `title`: `{item.title}` | `missing_ref`: `{item.packet_path}`"
            )
    if dangling_rows:
        warnings.append(f"detected `{len(dangling_rows)}` dangling capture-summary refs; do not chase them")

    capture_summary_lines: list[str] = []
    for summary in capture_summaries:
        existing_count = sum(1 for item in summary.items if item.exists)
        missing_count = sum(1 for item in summary.items if not item.exists)
        capture_summary_lines.append(
            f"- `{summary.path.name}` | `listed`: `{len(summary.items)}` | `existing_refs`: `{existing_count}` | `dangling_refs`: `{missing_count}`"
        )

    packet_lines = [
        f"- `{packet.source_id}` | `{packet.title}` | `captured_at`: `{packet.captured_at}` | `primary_source`: `{packet.primary_source}` | `path`: `{packet.path}`"
        for packet in reversed(source_packets)
    ]
    asset_chain_lines = [f"- `{path}`" for path in reversed(asset_chains)]
    topic_cluster_lines = [f"- `{path}`" for path in reversed(topic_clusters)]
    deep_article_lines = [f"- `{path}`" for path in reversed(deep_articles)]
    warning_lines = [f"- {warning}" for warning in warnings]

    return (
        "# 同行资本市场内容系统｜真实文件清单\n\n"
        f"- `requested_date`: `{requested_date}`\n"
        f"- `data_token_used`: `{day_token(requested_date)}`\n"
        f"- `resolution_mode`: `{resolution_mode}`\n"
        f"- `business_window_start`: `{format_ts(window_start)}`\n"
        f"- `business_window_end`: `{format_ts(window_end)}`\n"
        f"- `source_packet_file_tokens`: `{file_tokens}`\n"
        f"- `generated_at`: `{generated_at}`\n"
        f"- `source_packets`: `{len(source_packets)}`\n"
        f"- `asset_chains`: `{len(asset_chains)}`\n"
        f"- `topic_clusters`: `{len(topic_clusters)}`\n"
        f"- `deep_articles`: `{len(deep_articles)}`\n"
        f"- `capture_summaries`: `{len(capture_summaries)}`\n\n"
        "## Preflight Warnings\n\n"
        f"{chr(10).join(warning_lines) if warning_lines else '- none'}\n\n"
        "## Capture Summaries\n\n"
        f"{chr(10).join(capture_summary_lines) if capture_summary_lines else '- none'}\n\n"
        "## Real Source Packets\n\n"
        f"{chr(10).join(packet_lines) if packet_lines else '- none'}\n\n"
        "## Real Asset Chains\n\n"
        f"{chr(10).join(asset_chain_lines) if asset_chain_lines else '- none'}\n\n"
        "## Real Topic Clusters\n\n"
        f"{chr(10).join(topic_cluster_lines) if topic_cluster_lines else '- none'}\n\n"
        "## Real Deep Articles\n\n"
        f"{chr(10).join(deep_article_lines) if deep_article_lines else '- none'}\n\n"
        "## Dangling Capture-Summary Refs\n\n"
        f"{chr(10).join(dangling_rows) if dangling_rows else '- none'}\n"
    )


def default_output_path(requested_date: str) -> Path:
    return LOG_DIR / f"{day_token(requested_date)}__market-source-manifest.md"


def main() -> int:
    args = parse_args()
    requested_date = args.date

    source_packets = collect_source_packets(requested_date)
    asset_chains = collect_simple_paths(ASSET_CHAIN_DIR, requested_date, "__asset-chain.md", asset_chain_ts)
    topic_clusters = collect_simple_paths(TOPIC_CLUSTER_DIR, requested_date, "__topic-cluster.md", topic_cluster_ts)
    deep_articles = collect_simple_paths(DEEP_ARTICLE_DIR, requested_date, "__deep-article.md", deep_article_ts)
    capture_summaries = collect_capture_summaries(requested_date)
    if business_window_status(requested_date) == "open":
        resolution_mode = "business-window-open"
    elif source_packets:
        resolution_mode = "business-window"
    else:
        resolution_mode = "business-window-empty"

    output = render_manifest(
        requested_date=requested_date,
        resolution_mode=resolution_mode,
        source_packets=source_packets,
        asset_chains=asset_chains,
        topic_clusters=topic_clusters,
        deep_articles=deep_articles,
        capture_summaries=capture_summaries,
    )
    print(output)

    if args.write:
        out_path = default_output_path(requested_date)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"\nManifest written to: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
