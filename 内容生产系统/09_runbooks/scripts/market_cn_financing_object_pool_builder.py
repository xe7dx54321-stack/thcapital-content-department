#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
import textwrap
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from market_topic_capture_round import CN_TZ, LOG_DIR, ROOT, compact_snippet, format_dt, now_cn, slugify, write_text


PACKET_DIR = ROOT / "02_topic_radar" / "source_packets"
RESOLVED_DIR = ROOT / "02_topic_radar" / "asset_chains" / "resolved"
POOL_DIR = ROOT / "02_topic_radar" / "cn_financing_object_pool"
OBJECT_DIR = POOL_DIR / "objects"

DEFAULT_SOURCE_IDS = [
    "web__itjuzi",
    "web__36kr_ai",
    "web__zhidx",
    "web__qbitai_site",
    "web__jiqizhixin_site",
    "web__ifanr_ai",
    "wechat__36kr",
    "wechat__zhidx",
    "wechat__jiqizhixin",
    "wechat__ifanr",
]
FINANCING_KEYWORDS = [
    "融资",
    "获投",
    "领投",
    "参投",
    "战略投资",
    "种子轮",
    "天使轮",
    "pre-seed",
    "pre seed",
    "pre-a",
    "pre a",
    "a轮",
    "b轮",
    "c轮",
    "series a",
    "series b",
    "series c",
    "raises",
    "raised",
    "funding",
    "led by",
    "backed by",
]
ROUND_PATTERNS = [
    r"Pre-Seed(?:\+)?",
    r"Pre-A(?:\+)?轮",
    r"Pre-A(?:\+)?",
    r"种子轮",
    r"天使轮",
    r"A\+\s*轮",
    r"A轮",
    r"B\+\s*轮",
    r"B轮",
    r"C\+\s*轮",
    r"C轮",
    r"D轮",
    r"E轮",
    r"战略融资",
    r"战略投资",
    r"Series [A-F]",
    r"seed funding",
    r"series [a-f] funding",
]
AMOUNT_PATTERNS = [
    r"(?:超|近|逾|约)?\d+(?:\.\d+)?(?:万|千万|亿|亿美元|万元|亿元|美元|人民币)",
    r"(?:数|上)\w{0,6}(?:万|千万|亿)(?:元|美元|人民币)?",
    r"\$\d+(?:\.\d+)?(?:[KMB]| million| billion)?",
    r"\d+(?:\.\d+)?\s*(?:million|billion)\s*(?:USD|usd|dollars)?",
]


@dataclass
class PacketRecord:
    path: Path
    text: str
    fields: dict[str, str]
    distilled_body: str
    normalized_excerpt: str


@dataclass
class ResolutionRecord:
    source_packet_path: str
    entity_name: str
    official_site: str
    official_site_confidence: str
    evidence_links: list[str]


@dataclass
class FinancingObject:
    object_key: str
    object_id: str
    company_name: str
    company_name_confidence: str
    source_packet_path: str
    source_id: str
    source_name: str
    title: str
    published_at: str
    captured_at: str
    event_type: str
    round_guess: str
    amount_guess: str
    investor_guess: str
    official_site: str
    official_site_confidence: str
    verification_status: str
    evidence_links: list[str]
    notes: list[str]
    summary: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build semi-structured CN financing object pool from packets and resolved asset chains.")
    parser.add_argument("--date", help="Logical date in YYYY-MM-DD. Default: today in Asia/Shanghai.")
    parser.add_argument("--source-id", action="append", dest="source_ids", help="Override default source ids. Can repeat.")
    parser.add_argument("--limit", type=int, default=100, help="Max number of packet-derived objects to emit.")
    parser.add_argument("--write", action="store_true", help="Actually write object cards, board, and log.")
    return parser.parse_args()


def ensure_dirs() -> None:
    POOL_DIR.mkdir(parents=True, exist_ok=True)
    OBJECT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def parse_fields(markdown_text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in markdown_text.splitlines():
        line = line.strip()
        match = re.match(r"- `([^`]+)`: (?:`([^`]*)`|(.*))", line)
        if not match:
            continue
        key = match.group(1).strip()
        value = (match.group(2) if match.group(2) is not None else match.group(3) or "").strip()
        fields[key] = value
    return fields


def extract_section(markdown_text: str, heading: str) -> str:
    lines = markdown_text.splitlines()
    marker = f"## {heading}"
    start_index: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == marker:
            start_index = index + 1
            break
    if start_index is None:
        return ""
    collected: list[str] = []
    for line in lines[start_index:]:
        if line.startswith("## "):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip().strip("`")


def day_token(date_text: str) -> str:
    return datetime.fromisoformat(date_text).strftime("%Y%m%d")


def latest_packet_records(source_ids: list[str]) -> list[PacketRecord]:
    latest_by_key: dict[str, PacketRecord] = {}
    for path in sorted(PACKET_DIR.glob("*__source-packet.md"), key=lambda candidate: candidate.stat().st_mtime, reverse=True):
        text = path.read_text(encoding="utf-8", errors="ignore")
        fields = parse_fields(text)
        source_id = fields.get("source_id", "")
        packet_key = fields.get("packet_key", path.stem)
        if source_ids and source_id not in source_ids:
            continue
        if packet_key in latest_by_key:
            continue
        latest_by_key[packet_key] = PacketRecord(
            path=path,
            text=text,
            fields=fields,
            distilled_body=extract_section(text, "Distilled Body"),
            normalized_excerpt=extract_section(text, "Normalized Excerpt"),
        )
    return list(latest_by_key.values())


def latest_resolution_maps() -> tuple[dict[str, ResolutionRecord], dict[str, ResolutionRecord]]:
    by_packet: dict[str, ResolutionRecord] = {}
    by_entity: dict[str, ResolutionRecord] = {}
    for path in sorted(RESOLVED_DIR.glob("*__asset-resolution.md"), key=lambda candidate: candidate.stat().st_mtime, reverse=True):
        text = path.read_text(encoding="utf-8", errors="ignore")
        fields = parse_fields(text)
        source_packet_path = clean_text(fields.get("source_packet_path", ""))
        entity_name = clean_text(fields.get("entity_name", ""))
        official_site = clean_text(fields.get("official_site", ""))
        if official_site == "unknown":
            official_site = ""
        record = ResolutionRecord(
            source_packet_path=source_packet_path,
            entity_name=entity_name,
            official_site=official_site,
            official_site_confidence=clean_text(fields.get("official_site_confidence", "unknown")),
            evidence_links=extract_urls(text),
        )
        if source_packet_path and source_packet_path not in by_packet:
            by_packet[source_packet_path] = record
        if entity_name:
            lowered = entity_name.lower()
            if lowered not in by_entity:
                by_entity[lowered] = record
    return by_packet, by_entity


def extract_urls(text: str) -> list[str]:
    urls = re.findall(r"https?://[^\s)>`]+", text or "")
    deduped: list[str] = []
    seen: set[str] = set()
    for url in urls:
        cleaned = url.strip().rstrip(".,;")
        if cleaned in seen:
            continue
        seen.add(cleaned)
        deduped.append(cleaned)
    return deduped


def packet_signal_text(packet: PacketRecord) -> str:
    parts = [
        packet.fields.get("title", ""),
        packet.fields.get("summary", ""),
        packet.normalized_excerpt,
        packet.distilled_body,
    ]
    return "\n".join(part for part in parts if part).strip()


def is_financing_relevant(packet: PacketRecord) -> bool:
    if packet.fields.get("source_id") == "web__itjuzi":
        return True
    haystack = packet_signal_text(packet).lower()
    strong_terms = [
        "融资",
        "获投",
        "领投",
        "参投",
        "战略投资",
        "funding",
        "raises",
        "raised",
        "series ",
        "seed",
        "pre-a",
        "a轮",
        "b轮",
        "c轮",
    ]
    if "snapshot" in packet.fields.get("title", "").lower() and not any(term in haystack for term in strong_terms):
        return False
    return any(keyword.lower() in haystack for keyword in FINANCING_KEYWORDS)


def extract_round_guess(text: str) -> str:
    for pattern in ROUND_PATTERNS:
        match = re.search(pattern, text, re.I)
        if match:
            return clean_text(match.group(0))
    return "unknown"


def extract_amount_guess(text: str) -> str:
    for pattern in AMOUNT_PATTERNS:
        match = re.search(pattern, text, re.I)
        if match:
            return clean_text(match.group(0))
    return "unknown"


def extract_investor_guess(text: str) -> str:
    patterns = [
        r"由(?P<value>[^，。；\n]{2,80}?)(?:领投|投资|参投)",
        r"(?:投资方|投资机构)(?:包括|为|有|阵容为)?[:：]?(?P<value>[^。；\n]{2,120})",
        r"(?:led by|backed by|with participation from) (?P<value>[^.\n]{3,140})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if not match:
            continue
        value = clean_text(match.group("value"))
        if value:
            return compact_snippet(value, 120)
    return "unknown"


def clean_company_name(value: str) -> str:
    value = clean_text(value)
    value = re.sub(r"\s*[-—|｜:：].*$", "", value).strip()
    value = value.strip("“”\"'[]【】()（）")
    return value


def extract_company_name(packet: PacketRecord, resolution_by_packet: dict[str, ResolutionRecord], resolution_by_entity: dict[str, ResolutionRecord]) -> tuple[str, str]:
    if packet.fields.get("source_id") == "web__itjuzi":
        return "中国 AI 融资背景板", "high"

    title = clean_text(packet.fields.get("title", ""))
    patterns = [
        r"^(?P<name>[^，。；：:]{2,60}?)(?:宣布完成|连续完成|完成|获|获得|再获|拿下|完成了).{0,36}?(?:融资|投资|天使轮|种子轮|Pre-A|A轮|B轮|C轮)",
        r"^(?P<name>[A-Z][A-Za-z0-9&'./+\- ]{1,80}?)\s+(?:Raises|Raised|Closes|Closed|Secures|Secured)\s+.+?(?:Funding|Series|Seed)",
    ]
    for pattern in patterns:
        match = re.search(pattern, title, re.I)
        if match:
            candidate = clean_company_name(match.group("name"))
            if candidate:
                return candidate, "high"

    packet_resolution = resolution_by_packet.get(str(packet.path))
    if packet_resolution and packet_resolution.entity_name:
        return packet_resolution.entity_name, "medium"

    excerpt = clean_text(packet.normalized_excerpt)
    for pattern in patterns:
        match = re.search(pattern, excerpt, re.I)
        if match:
            candidate = clean_company_name(match.group("name"))
            if candidate:
                return candidate, "medium"

    for entity_name in resolution_by_entity.keys():
        if entity_name and entity_name in title.lower():
            return resolution_by_entity[entity_name].entity_name, "medium"

    fallback = clean_company_name(title[:48])
    return fallback or "unknown company", "low"


def choose_resolution(
    packet: PacketRecord,
    company_name: str,
    resolution_by_packet: dict[str, ResolutionRecord],
    resolution_by_entity: dict[str, ResolutionRecord],
) -> ResolutionRecord | None:
    if str(packet.path) in resolution_by_packet:
        return resolution_by_packet[str(packet.path)]
    if company_name and company_name.lower() in resolution_by_entity:
        return resolution_by_entity[company_name.lower()]
    return None


def make_object_key(packet_key: str, company_name: str) -> str:
    digest = hashlib.md5(f"{packet_key}|{company_name}".encode("utf-8")).hexdigest()[:8]
    return f"{slugify(company_name, 'company')}_{digest}"


def build_macro_report_object(packet: PacketRecord) -> FinancingObject:
    packet_key = packet.fields.get("packet_key", packet.path.stem)
    notes = [
        "IT 桔子 PDF 当前充当公开背景层，不是实时 live database。",
        "它更适合补国内 AI 融资规模、轮次结构、地域分布和子赛道分化结论。",
        "正式 daily event 仍需叠加中文媒体入口、公司公告、官网和工商 / 融资数据库交叉验证。",
    ]
    return FinancingObject(
        object_key=make_object_key(packet_key, "中国 AI 融资背景板"),
        object_id=f"cn_fin_obj_{packet_key}",
        company_name="中国 AI 融资背景板",
        company_name_confidence="high",
        source_packet_path=str(packet.path),
        source_id=packet.fields.get("source_id", ""),
        source_name=packet.fields.get("source_name", ""),
        title=packet.fields.get("title", ""),
        published_at=packet.fields.get("published_at", "unknown"),
        captured_at=packet.fields.get("captured_at", "unknown"),
        event_type="macro_report",
        round_guess="n/a",
        amount_guess="n/a",
        investor_guess="n/a",
        official_site=packet.fields.get("canonical_url", ""),
        official_site_confidence="high",
        verification_status="background-layer",
        evidence_links=extract_urls(packet.text)[:8],
        notes=notes,
        summary="国内 AI 融资背景板已补上，可用于赛道冷热、轮次结构与城市分布判断，但不替代实时融资数据库。",
    )


def build_event_object(
    packet: PacketRecord,
    resolution_by_packet: dict[str, ResolutionRecord],
    resolution_by_entity: dict[str, ResolutionRecord],
) -> FinancingObject:
    packet_key = packet.fields.get("packet_key", packet.path.stem)
    signal_text = packet_signal_text(packet)
    company_name, company_confidence = extract_company_name(packet, resolution_by_packet, resolution_by_entity)
    round_guess = extract_round_guess(signal_text)
    amount_guess = extract_amount_guess(signal_text)
    investor_guess = extract_investor_guess(signal_text)
    resolution = choose_resolution(packet, company_name, resolution_by_packet, resolution_by_entity)
    official_site = resolution.official_site if resolution else ""
    official_site_confidence = resolution.official_site_confidence if resolution else "unknown"
    evidence_links = extract_urls(packet.text)
    if resolution:
        evidence_links = list(dict.fromkeys(evidence_links + resolution.evidence_links))

    notes: list[str] = []
    if packet.fields.get("source_id", "").startswith("wechat__"):
        notes.append("当前来自微信文章入口，适合补中文叙事与公司线索，但仍需回链官网 / 公告。")
    if official_site:
        verification_status = "semi-structured / resolved-official-site"
        notes.append("已命中官网，可继续补工商、团队、产品页与融资沿革。")
    elif round_guess != "unknown" or amount_guess != "unknown":
        verification_status = "semi-structured / packet-only"
        notes.append("已抽出轮次或金额，但官网仍未稳定命中，需要补一跳对象解析。")
    else:
        verification_status = "candidate / weak-structure"
        notes.append("当前只有弱事件线索，还不足以直接升格为高置信融资对象。")

    summary = (
        f"{company_name} 出现在 {packet.fields.get('source_name', packet.fields.get('source_id', 'unknown source'))} 的融资相关入口中；"
        f"当前抽取结果为轮次 {round_guess}、金额 {amount_guess}、投资方 {investor_guess}。"
    )
    return FinancingObject(
        object_key=make_object_key(packet_key, company_name),
        object_id=f"cn_fin_obj_{packet_key}",
        company_name=company_name,
        company_name_confidence=company_confidence,
        source_packet_path=str(packet.path),
        source_id=packet.fields.get("source_id", ""),
        source_name=packet.fields.get("source_name", ""),
        title=packet.fields.get("title", ""),
        published_at=packet.fields.get("published_at", "unknown"),
        captured_at=packet.fields.get("captured_at", "unknown"),
        event_type="funding_event_candidate",
        round_guess=round_guess,
        amount_guess=amount_guess,
        investor_guess=investor_guess,
        official_site=official_site or "unknown",
        official_site_confidence=official_site_confidence,
        verification_status=verification_status,
        evidence_links=evidence_links[:12],
        notes=notes,
        summary=summary,
    )


def render_object_card(obj: FinancingObject, generated_at: datetime) -> str:
    return (
        "# CN Financing Object Card\n\n"
        "## Header\n\n"
        f"- `object_id`: `{obj.object_id}`\n"
        f"- `object_key`: `{obj.object_key}`\n"
        f"- `company_name`: `{obj.company_name}`\n"
        f"- `company_name_confidence`: `{obj.company_name_confidence}`\n"
        f"- `source_packet_path`: `{obj.source_packet_path}`\n"
        f"- `source_id`: `{obj.source_id}`\n"
        f"- `source_name`: `{obj.source_name}`\n"
        f"- `title`: `{obj.title}`\n"
        f"- `published_at`: `{obj.published_at}`\n"
        f"- `captured_at`: `{obj.captured_at}`\n"
        f"- `generated_at`: `{format_dt(generated_at)}`\n"
        f"- `event_type`: `{obj.event_type}`\n"
        f"- `round_guess`: `{obj.round_guess}`\n"
        f"- `amount_guess`: `{obj.amount_guess}`\n"
        f"- `investor_guess`: `{obj.investor_guess}`\n"
        f"- `official_site`: `{obj.official_site}`\n"
        f"- `official_site_confidence`: `{obj.official_site_confidence}`\n"
        f"- `verification_status`: `{obj.verification_status}`\n"
        f"- `evidence_count`: `{len(obj.evidence_links)}`\n\n"
        "## Summary\n\n"
        f"{obj.summary}\n\n"
        "## Evidence Links\n\n"
        f"{render_bullets(obj.evidence_links)}\n\n"
        "## Notes\n\n"
        f"{render_bullets(obj.notes)}\n"
    )


def render_bullets(items: list[str], fallback: str = "- none") -> str:
    if not items:
        return fallback
    return "\n".join(f"- {item}" for item in items)


def render_board(date_text: str, generated_at: datetime, packets_scanned: int, objects: list[FinancingObject]) -> str:
    macro_objects = [obj for obj in objects if obj.event_type == "macro_report"]
    event_objects = [obj for obj in objects if obj.event_type != "macro_report"]
    high_signal = [obj for obj in event_objects if "resolved-official-site" in obj.verification_status]
    weak_signal = [obj for obj in event_objects if obj not in high_signal]

    def render_rows(rows: list[FinancingObject]) -> str:
        if not rows:
            return "| none | none | none | none | none | none | none |"
        lines: list[str] = []
        for obj in rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        obj.company_name,
                        obj.round_guess,
                        obj.amount_guess,
                        obj.investor_guess,
                        obj.official_site,
                        obj.verification_status,
                        obj.source_name,
                    ]
                )
                + " |"
            )
        return "\n".join(lines)

    return textwrap.dedent(
        f"""\
        # 国内融资对象池 Board

        - `logical_date`: `{date_text}`
        - `generated_at`: `{format_dt(generated_at)}`
        - `packets_scanned`: `{packets_scanned}`
        - `macro_reports`: `{len(macro_objects)}`
        - `event_objects`: `{len(event_objects)}`
        - `high_signal_objects`: `{len(high_signal)}`
        - `weak_signal_objects`: `{len(weak_signal)}`

        ## 当前判断

        - `IT 桔子 PDF 背景层已经接入，可稳定补国内 AI 融资结构判断。`
        - `实时 live database 仍未直连打通，因此当前对象池定义为“半结构化对象池”。`
        - `凡是已经命中官网的对象，可继续补工商、团队、产品与融资沿革；未命中官网的对象保留在线索池中。`
        - `{('本轮中文入口里尚未命中高置信实时融资对象，当前以背景层为主。' if not event_objects else '本轮已经命中事件层对象，可继续做官网 / 工商 / 融资沿革补料。')}`

        ## 背景层

        | 对象 | 类型 | 来源 | 发布时间 | 用途 |
        | --- | --- | --- | --- | --- |
        {chr(10).join(f"| {obj.company_name} | {obj.event_type} | {obj.source_name} | {obj.published_at} | 国内 AI 融资背景板 |" for obj in macro_objects) if macro_objects else "| none | none | none | none | none |"}

        ## 高信号对象

        | 公司 | 轮次 | 金额 | 投资方 | 官网 | 验证状态 | 来源 |
        | --- | --- | --- | --- | --- | --- | --- |
        {render_rows(high_signal)}

        ## 弱信号 / 待补对象

        | 公司 | 轮次 | 金额 | 投资方 | 官网 | 验证状态 | 来源 |
        | --- | --- | --- | --- | --- | --- | --- |
        {render_rows(weak_signal)}
        """
    ).strip() + "\n"


def render_log(date_text: str, generated_at: datetime, packets_scanned: int, objects: list[FinancingObject], board_path: Path) -> str:
    return textwrap.dedent(
        f"""\
        # 国内融资对象池构建日志

        - `logical_date`: `{date_text}`
        - `generated_at`: `{format_dt(generated_at)}`
        - `packets_scanned`: `{packets_scanned}`
        - `objects_built`: `{len(objects)}`
        - `board_path`: `{board_path}`

        ## Built Objects

        {render_bullets([f'{obj.company_name}｜{obj.verification_status}｜{obj.source_name}' for obj in objects])}
        """
    ).strip() + "\n"


def main() -> int:
    args = parse_args()
    ensure_dirs()
    generated_at = now_cn()
    logical_date = args.date or generated_at.strftime("%Y-%m-%d")
    source_ids = args.source_ids or DEFAULT_SOURCE_IDS

    resolution_by_packet, resolution_by_entity = latest_resolution_maps()
    packets = latest_packet_records(source_ids)

    objects: list[FinancingObject] = []
    for packet in packets:
        if not is_financing_relevant(packet):
            continue
        if packet.fields.get("source_id") == "web__itjuzi":
            objects.append(build_macro_report_object(packet))
            continue
        objects.append(build_event_object(packet, resolution_by_packet, resolution_by_entity))
        if len([obj for obj in objects if obj.event_type != "macro_report"]) >= args.limit:
            break

    token = day_token(logical_date)
    board_path = POOL_DIR / f"{token}__cn-financing-object-pool-board.md"
    board_text = render_board(logical_date, generated_at, len(packets), objects)
    log_path = LOG_DIR / f"{token}_{generated_at.strftime('%H%M%S')}__cn-financing-object-pool-builder.md"
    log_text = render_log(logical_date, generated_at, len(packets), objects, board_path)

    if args.write:
        for obj in objects:
            card_path = OBJECT_DIR / f"{token}__{obj.object_key}__cn-financing-object.md"
            write_text(card_path, render_object_card(obj, generated_at))
        write_text(board_path, board_text)
        write_text(log_path, log_text)

    print(log_text)
    if args.write:
        print(f"\nBoard written to: {board_path}")
        print(f"Log written to: {log_path}")
        print(f"Object dir: {OBJECT_DIR}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
