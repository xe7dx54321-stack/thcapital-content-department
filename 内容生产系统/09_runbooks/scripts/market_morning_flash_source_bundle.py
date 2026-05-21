#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from market_business_day import (
    MORNING_FLASH_WINDOW_END,
    MORNING_FLASH_WINDOW_START,
    business_window,
    day_token,
    format_cst,
    parse_cst,
    timestamp_from_name,
)
from market_topic_radar_brief_builder import parse_fields, parse_packet


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
SOURCE_PACKET_DIR = ROOT / "02_topic_radar" / "source_packets"
OUTPUT_DIR = ROOT / "03_topic_candidates"
NORMALIZE_RE = re.compile(r"[^0-9a-z\u4e00-\u9fff]+")
FIT_KEYWORDS = (
    "ai",
    "agent",
    "agents",
    "model",
    "models",
    "llm",
    "claude",
    "openai",
    "anthropic",
    "gpt",
    "gemma",
    "deepseek",
    "robot",
    "robotics",
    "infra",
    "benchmark",
    "workflow",
    "coding",
    "一人公司",
    "模型",
    "智能体",
    "机器人",
    "算力",
    "推理",
    "端侧",
    "本地",
    "创业",
)
PROMO_OR_META_KEYWORDS = (
    "招聘",
    "作者招聘",
    "申报",
    "榜单",
    "参会",
    "报名",
    "投稿",
    "活动预告",
    "会议议程",
    "征集",
)
MAINSTREAM_PREFIXES = (
    "wechat__jiqizhixin",
    "wechat__liangziwei",
    "wechat__zhidx",
    "web__36kr_ai",
    "web__techcrunch_ai",
    "web__openai_news",
    "web__anthropic_newsroom",
    "web__github_blog",
    "web__theverge_ai",
    "x__",
    "derived__",
)


@dataclass(frozen=True)
class Candidate:
    path: Path
    title: str
    source_id: str
    source_name: str
    primary_source: str
    canonical_url: str
    published_at: str
    captured_at: str
    summary: str
    score: int
    reason_tags: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an auditable morning_flash source bundle from the T-1 17:00 -> T 05:00 window.")
    parser.add_argument("--date", default=datetime.now().date().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--min-items", type=int, default=8, help="Minimum selected events required for ready status.")
    parser.add_argument("--max-items", type=int, default=8, help="Maximum selected events.")
    parser.add_argument("--write", action="store_true", help="Write bundle into 03_topic_candidates.")
    parser.add_argument("--strict-ready", action="store_true", help="Exit non-zero when selected items are below min-items.")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def output_path(date_text: str) -> Path:
    return OUTPUT_DIR / f"{day_token(date_text)}__morning-flash-source-bundle.md"


def source_packet_captured_ts(path: Path, fields: dict[str, str]) -> datetime | None:
    return parse_cst(fields.get("captured_at")) or timestamp_from_name(path)


def normalize_key(title: str, canonical_url: str) -> str:
    url = clean(canonical_url, "")
    if url and url != "n/a":
        return url
    normalized = NORMALIZE_RE.sub(" ", clean(title, "").lower()).strip()
    return normalized or clean(title).lower()


def fit_score(text: str) -> int:
    lowered = clean(text, "").lower()
    hits = sum(1 for token in FIT_KEYWORDS if token in lowered)
    if hits >= 3:
        return 3
    if hits >= 1:
        return 2
    return 0


def is_promo_or_meta(text: str) -> bool:
    lowered = clean(text, "").lower()
    return any(token in lowered for token in PROMO_OR_META_KEYWORDS)


def source_quality_score(source_id: str, primary_source: str) -> int:
    score = {"yes": 4, "partial": 3, "no": 1}.get(clean(primary_source, "").lower(), 2)
    if any(source_id.startswith(prefix) for prefix in MAINSTREAM_PREFIXES):
        score += 1
    return score


def freshness_score(published_dt: datetime, end_dt: datetime) -> int:
    age_hours = max((end_dt - published_dt).total_seconds() / 3600.0, 0.0)
    if age_hours <= 6:
        return 4
    if age_hours <= 12:
        return 3
    if age_hours <= 18:
        return 2
    return 1


def selection_status(selected_count: int, min_items: int) -> str:
    if selected_count >= min_items:
        return "ready"
    if selected_count > 0:
        return "under_target"
    return "empty"


def collect_candidates(date_text: str) -> tuple[list[Candidate], list[str], datetime, datetime]:
    start_dt, end_dt = business_window(
        date_text,
        start_hm=MORNING_FLASH_WINDOW_START,
        end_hm=MORNING_FLASH_WINDOW_END,
    )
    deduped: dict[str, Candidate] = {}
    excluded: list[str] = []
    for path in sorted(SOURCE_PACKET_DIR.glob("*__source-packet.md")):
        fields = parse_fields(path)
        captured_dt = source_packet_captured_ts(path, fields)
        if captured_dt is None or not (start_dt <= captured_dt <= end_dt):
            continue
        packet = parse_packet(path)
        text_blob = " ".join([packet.title, packet.summary, packet.topic_tags, packet.heat_hint, packet.source_id])
        if is_promo_or_meta(text_blob):
            excluded.append(f"promo_or_meta | {packet.title} | {path}")
            continue
        fit = fit_score(text_blob)
        if fit <= 0:
            excluded.append(f"not_ai_enough | {packet.title} | {path}")
            continue
        published_at = clean(fields.get("published_at", "n/a"))
        published_dt = parse_cst(published_at)
        if published_dt is None:
            excluded.append(f"published_at_unparseable | {packet.title} | published_at={published_at} | {path}")
            continue
        if not (start_dt <= published_dt <= end_dt):
            excluded.append(f"published_at_outside_window | {packet.title} | published_at={published_at} | {path}")
            continue
        score = fit * 2 + source_quality_score(packet.source_id, packet.primary_source) + freshness_score(published_dt, end_dt)
        tags = ["fit", f"primary={packet.primary_source}", f"published={published_at}"]
        if any(packet.source_id.startswith(prefix) for prefix in MAINSTREAM_PREFIXES):
            tags.append("mainstream_or_primary_lane")
        candidate = Candidate(
            path=path,
            title=packet.title,
            source_id=packet.source_id,
            source_name=clean(fields.get("source_name", packet.source_id)),
            primary_source=packet.primary_source,
            canonical_url=packet.canonical_url,
            published_at=published_at,
            captured_at=clean(fields.get("captured_at", "n/a")),
            summary=packet.summary,
            score=score,
            reason_tags=tuple(tags),
        )
        key = normalize_key(packet.title, packet.canonical_url)
        existing = deduped.get(key)
        if existing is None or candidate.score > existing.score:
            deduped[key] = candidate
    selected = sorted(
        deduped.values(),
        key=lambda item: (
            item.score,
            parse_cst(item.published_at) or datetime.min.replace(tzinfo=start_dt.tzinfo),
            item.title,
        ),
        reverse=True,
    )
    return selected, excluded, start_dt, end_dt


def render_bundle(
    date_text: str,
    selected: list[Candidate],
    excluded: list[str],
    start_dt: datetime,
    end_dt: datetime,
    min_items: int,
    max_items: int,
) -> str:
    chosen = selected[:max_items]
    status = selection_status(len(chosen), min_items)
    lines = [
        "# Morning Flash Source Bundle",
        "",
        f"- `generated_at`: `{format_cst(datetime.now(start_dt.tzinfo))}`",
        f"- `date`: `{date_text}`",
        f"- `selection_status`: `{status}`",
        f"- `business_window_start`: `{format_cst(start_dt)}`",
        f"- `business_window_end`: `{format_cst(end_dt)}`",
        f"- `selected_items`: `{len(chosen)}`",
        f"- `min_items_required`: `{min_items}`",
        f"- `max_items_allowed`: `{max_items}`",
        f"- `excluded_items`: `{len(excluded)}`",
        "",
        "## Policy",
        "",
        "- 只允许从 `captured_at` 落在 `T-1 17:00 -> T 05:00` 的 source packet 中选题。",
        "- `published_at` 必须可解析，且同样落在晨间时间窗内；否则一律视为 stale / 不可审计，禁止写进早报正文。",
        "- 只选 AI / Agent / 模型 / 机器人 / infra / 工作流相关对象；招聘、报名、榜单征集、活动预告等 meta 内容一律排除。",
        "- 后续 approved-topic / draft-pack / wechat.md 只允许使用本 bundle 内对象，不得额外增写 bundle 外历史旧题。",
        "",
        "## Selected Events",
        "",
    ]
    if chosen:
        for index, item in enumerate(chosen, start=1):
            lines.extend(
                [
                    f"### {index}. {item.title}",
                    f"- `source_name`: `{item.source_name}`",
                    f"- `source_id`: `{item.source_id}`",
                    f"- `primary_source`: `{item.primary_source}`",
                    f"- `published_at`: `{item.published_at}`",
                    f"- `captured_at`: `{item.captured_at}`",
                    f"- `canonical_url`: `{item.canonical_url}`",
                    f"- `score`: `{item.score}`",
                    f"- `selection_reason`: `{', '.join(item.reason_tags)}`",
                    f"- `summary`: `{item.summary}`",
                    f"- `source_packet_path`: `{item.path}`",
                    "",
                ]
            )
    else:
        lines.append("- `none`")
        lines.append("")
    lines.extend(
        [
            "## Source Refs",
            "",
        ]
    )
    if chosen:
        lines.extend(f"- `{item.path}`" for item in chosen)
    else:
        lines.append("- `n/a`")
    lines.extend(
        [
            "",
            "## Excluded Samples",
            "",
        ]
    )
    if excluded:
        lines.extend(f"- `{item}`" for item in excluded[:20])
        if len(excluded) > 20:
            lines.append(f"- `... +{len(excluded) - 20} more excluded items`")
    else:
        lines.append("- `none`")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    selected, excluded, start_dt, end_dt = collect_candidates(args.date)
    text = render_bundle(args.date, selected, excluded, start_dt, end_dt, args.min_items, args.max_items)
    chosen_count = min(len(selected), args.max_items)
    status = selection_status(chosen_count, args.min_items)

    if args.write:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        path = output_path(args.date)
        path.write_text(text, encoding="utf-8")
        print(path)
    else:
        print(text)

    if args.strict_ready and status != "ready":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
