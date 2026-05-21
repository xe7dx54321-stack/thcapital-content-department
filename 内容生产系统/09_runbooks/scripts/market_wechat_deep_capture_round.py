#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from market_business_day import day_token, path_in_business_window, text_timestamp_in_business_window
from market_wechat_source_defs import WECHAT_SOURCE_TARGETS


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
PACKET_DIR = ROOT / "02_topic_radar" / "source_packets"
DEEP_DIR = ROOT / "02_topic_radar" / "deep_articles"
DEEP_RAW_DIR = DEEP_DIR / "raw"
LOG_DIR = ROOT / "10_logs"
STATE_DIR = LOG_DIR / "runtime_state"
STATE_PATH = STATE_DIR / "market_wechat_deep_capture_state.json"

OPENCLAW_ROOT = Path("/Users/apple/.openclaw")
X_READER_BIN = Path.home() / "bin" / "x-reader"
INBOX_PATH_CANDIDATES = [
    OPENCLAW_ROOT / "unified_inbox.json",
    OPENCLAW_ROOT / "workspace-data" / "unified_inbox.json",
]
EXPORT_ROOT_CANDIDATES = [
    OPENCLAW_ROOT / "wechat_exports",
    OPENCLAW_ROOT / "workspace-data" / "wechat_exports",
]

CN_TZ = ZoneInfo("Asia/Shanghai")
WECHAT_SOURCE_IDS = [str(target["source_id"]) for target in WECHAT_SOURCE_TARGETS]
BAD_CAPTURE_PATTERNS = [
    "weixin official accounts platform",
    "parameter error",
    "this page maybe not yet fully loaded",
]
UI_NOISE_PATTERNS = [
    "关闭",
    "更多",
    "赞赏",
    "微信扫一扫赞赏作者",
    "喜欢作者",
    "其它金额",
    "返回",
    "名称已清空",
    "轻点两下取消赞",
    "轻点两下取消在看",
]
STOP_CAPTURE_PATTERNS = [
    "关闭",
    "微信扫一扫赞赏作者",
    "赞赏金额",
    "轻点两下取消赞",
    "轻点两下取消在看",
]


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_dt(value: datetime) -> str:
    return value.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def logical_date_token(logical_date: str) -> str:
    return day_token(logical_date)


def parse_iso_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=CN_TZ)
    return parsed.astimezone(CN_TZ)


def ensure_dirs() -> None:
    for path in [PACKET_DIR, DEEP_DIR, DEEP_RAW_DIR, LOG_DIR, STATE_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def save_state(state: dict[str, Any]) -> None:
    write_text(STATE_PATH, json.dumps(state, ensure_ascii=False, indent=2))


def slugify(value: str, fallback: str = "item") -> str:
    normalized = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "_", value.strip().lower())
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or fallback


def compact_text(value: str, limit: int = 240) -> str:
    text = re.sub(r"\s+", " ", value or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def parse_packet_field(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^- `{re.escape(field)}`: `(.*)`$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def load_packet_info(packet_path: Path) -> dict[str, Any] | None:
    text = packet_path.read_text(encoding="utf-8")
    source_id = parse_packet_field(text, "source_id")
    canonical_url = parse_packet_field(text, "canonical_url")
    if not source_id or not canonical_url:
        return None
    return {
        "packet_path": str(packet_path),
        "packet_key": parse_packet_field(text, "packet_key") or packet_path.stem,
        "source_id": source_id,
        "source_name": parse_packet_field(text, "source_name") or source_id,
        "canonical_url": canonical_url,
        "title": parse_packet_field(text, "title") or packet_path.stem,
        "published_at": parse_packet_field(text, "published_at") or "",
        "captured_at": parse_packet_field(text, "captured_at") or "",
    }


def list_candidate_packets(
    logical_date: str,
    source_ids: list[str],
    explicit_packet_paths: list[str] | None = None,
) -> list[dict[str, Any]]:
    candidates: list[Path] = []
    if explicit_packet_paths:
        candidates.extend(Path(item).expanduser() for item in explicit_packet_paths)
    else:
        candidates.extend(sorted(PACKET_DIR.glob("*__source-packet.md")))

    latest_by_url: dict[str, dict[str, Any]] = {}
    source_id_set = set(source_ids)
    for packet_path in candidates:
        if not packet_path.exists():
            continue
        packet = load_packet_info(packet_path)
        if packet is None:
            continue
        if not explicit_packet_paths and not (
            text_timestamp_in_business_window(str(packet.get("captured_at") or ""), logical_date)
            or path_in_business_window(packet_path, logical_date)
        ):
            continue
        source_id = str(packet["source_id"])
        if source_id not in source_id_set:
            continue
        url = str(packet["canonical_url"]).strip()
        if "mp.weixin.qq.com" not in url:
            continue
        existing = latest_by_url.get(url)
        if existing is None or Path(existing["packet_path"]).name < packet_path.name:
            latest_by_url[url] = packet
    return sorted(latest_by_url.values(), key=lambda row: Path(str(row["packet_path"])).name)


def parse_keyed_line(output: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}=(.+)$", output)
    return match.group(1).strip() if match else None


def load_inbox_records(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return loaded if isinstance(loaded, list) else []


def select_latest_inbox_record(records: list[dict[str, Any]], url: str, started_at: datetime) -> dict[str, Any] | None:
    matches = [row for row in records if str(row.get("url") or "").strip() == url]
    if not matches:
        return None

    def sort_key(row: dict[str, Any]) -> tuple[int, str]:
        fetched = parse_iso_dt(str(row.get("fetched_at") or ""))
        is_recent = 1 if fetched and fetched >= started_at - timedelta(minutes=5) else 0
        return (is_recent, str(row.get("fetched_at") or ""))

    matches.sort(key=sort_key)
    return matches[-1]


def find_export_path(output: str, url: str, started_at: datetime) -> Path | None:
    export_path = parse_keyed_line(output, "export")
    if export_path:
        path = Path(export_path).expanduser()
        if path.exists():
            return path

    candidate_dates = [(started_at - timedelta(days=offset)).strftime("%Y-%m-%d") for offset in range(0, 3)]
    for root in EXPORT_ROOT_CANDIDATES:
        for date_str in candidate_dates:
            date_dir = root / date_str
            if not date_dir.exists():
                continue
            for export_file in sorted(date_dir.glob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
                try:
                    snippet = export_file.read_text(encoding="utf-8")[:1200]
                except UnicodeDecodeError:
                    continue
                if url in snippet:
                    return export_file
    return None


def extract_export_body(export_text: str) -> str:
    lines = export_text.splitlines()
    if not lines:
        return ""
    start_index = 0
    for index, line in enumerate(lines):
        if line.startswith("- Fetched:"):
            start_index = index + 1
            break
    while start_index < len(lines) and not lines[start_index].strip():
        start_index += 1
    body = "\n".join(lines[start_index:]).strip()
    return body


def clean_body(text: str) -> str:
    cleaned_lines: list[str] = []
    blank_open = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if cleaned_lines and not blank_open:
                cleaned_lines.append("")
            blank_open = True
            continue
        blank_open = False
        if line.startswith("![image]("):
            continue
        if line.startswith("URL Source:") or line.startswith("Markdown Content:"):
            continue
        if any(pattern in line for pattern in STOP_CAPTURE_PATTERNS):
            break
        if any(pattern in line for pattern in UI_NOISE_PATTERNS) and len(line) <= 24:
            continue
        cleaned_lines.append(line)
    cleaned = "\n".join(cleaned_lines).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def assess_capture_quality(title: str, raw_export_body: str, normalized_body: str, command_output: str, return_code: int) -> tuple[str, list[str], int]:
    lowered = " ".join([title, raw_export_body, normalized_body, command_output]).lower()
    notes: list[str] = []
    ui_noise_hits = sum(lowered.count(pattern.lower()) for pattern in UI_NOISE_PATTERNS)

    if return_code != 0:
        notes.append("x-reader 返回非 0 状态码，需要人工复核。")
        return "failed", notes, ui_noise_hits
    if any(pattern in lowered for pattern in BAD_CAPTURE_PATTERNS):
        notes.append("抓取结果出现公众号参数错误或页面未完整加载痕迹。")
        return "failed", notes, ui_noise_hits

    best_len = max(len(raw_export_body), len(normalized_body))
    if best_len >= 180:
        if ui_noise_hits:
            notes.append("正文已抓回，但包含少量微信页面控件噪音，可用于学习素材复盘。")
        else:
            notes.append("正文结构完整，可直接进入学习素材池。")
        return "full_text", notes, ui_noise_hits
    if best_len >= 80:
        notes.append("正文抓回较短，建议人工抽检是否原文确实较短。")
        return "partial", notes, ui_noise_hits
    notes.append("正文长度异常偏短，建议重跑或人工检查。")
    return "failed", notes, ui_noise_hits


def count_paragraphs(text: str) -> int:
    return len([chunk for chunk in text.split("\n\n") if chunk.strip()])


def count_images(text: str) -> int:
    return len(re.findall(r"!\[image\]\(", text))


def render_deep_article(
    packet: dict[str, Any],
    deep_capture_id: str,
    deep_captured_at: datetime,
    body_completeness: str,
    quality_notes: list[str],
    raw_export_char_count: int,
    normalized_char_count: int,
    paragraph_count: int,
    image_count: int,
    ui_noise_hits: int,
    original_export_path: Path | None,
    raw_copy_path: Path,
    normalized_body_path: Path,
    command_output_path: Path,
    best_body_excerpt: str,
) -> str:
    quality_lines = "\n".join(f"- {note}" for note in quality_notes) or "- none"
    return (
        "# WeChat Deep Article\n\n"
        "## Header\n\n"
        f"- `deep_capture_id`: `{deep_capture_id}`\n"
        f"- `source_packet_key`: `{packet['packet_key']}`\n"
        f"- `source_packet_path`: `{packet['packet_path']}`\n"
        f"- `source_id`: `{packet['source_id']}`\n"
        f"- `source_name`: `{packet['source_name']}`\n"
        f"- `canonical_url`: `{packet['canonical_url']}`\n"
        f"- `title`: `{packet['title']}`\n"
        f"- `published_at`: `{packet['published_at']}`\n"
        f"- `rss_captured_at`: `{packet['captured_at']}`\n"
        f"- `deep_captured_at`: `{format_dt(deep_captured_at)}`\n"
        f"- `extraction_method`: `x-reader`\n"
        f"- `status`: `{body_completeness}`\n\n"
        "## Capture Assessment\n\n"
        f"- `body_completeness`: `{body_completeness}`\n"
        f"- `raw_export_char_count`: `{raw_export_char_count}`\n"
        f"- `normalized_char_count`: `{normalized_char_count}`\n"
        f"- `paragraph_count`: `{paragraph_count}`\n"
        f"- `image_count`: `{image_count}`\n"
        f"- `ui_noise_hits`: `{ui_noise_hits}`\n"
        f"{quality_lines}\n\n"
        "## Trace Paths\n\n"
        f"- `x_reader_export_path`: `{original_export_path or 'not_found'}`\n"
        f"- `raw_export_copy_path`: `{raw_copy_path}`\n"
        f"- `normalized_body_path`: `{normalized_body_path}`\n"
        f"- `command_output_path`: `{command_output_path}`\n\n"
        "## Suggested Uses\n\n"
        "- 学头部号的切题角度、结构组织、段落推进与转折方式\n"
        "- 做内容复盘专题，分析为什么这篇内容在公众号里可能拿到结果\n"
        "- 从同一事件里重构新的切入点，而不是简单复述原文\n\n"
        "## Best-Available Body Excerpt\n\n"
        f"{best_body_excerpt if best_body_excerpt else '_empty_'}\n"
    )


def render_summary_log(
    run_at: datetime,
    logical_date: str,
    write_mode: bool,
    processed_sources: list[str],
    new_articles: list[dict[str, str]],
    skipped_urls: list[dict[str, str]],
    errors: list[str],
) -> str:
    new_article_lines = "\n".join(
        f"- `{row['source_id']}` → `{row['title']}` → `{row['deep_article_path']}`" for row in new_articles
    )
    skipped_lines = "\n".join(
        f"- `{row['source_id']}` → `{row['title']}` → `{row['canonical_url']}`" for row in skipped_urls
    )
    error_lines = "\n".join(f"- {error}" for error in errors)
    return (
        "# 同行资本市场内容系统｜微信公众号全文深抓轮\n\n"
        f"- `run_at`: `{format_dt(run_at)}`\n"
        f"- `logical_date`: `{logical_date}`\n"
        f"- `write_mode`: `{str(write_mode).lower()}`\n"
        f"- `sources`: `{', '.join(processed_sources)}`\n"
        f"- `new_deep_articles`: `{len(new_articles)}`\n"
        f"- `skipped_existing`: `{len(skipped_urls)}`\n"
        f"- `errors`: `{len(errors)}`\n\n"
        "## New Deep Articles\n\n"
        f"{new_article_lines if new_article_lines else '- none'}\n\n"
        "## Skipped Existing\n\n"
        f"{skipped_lines if skipped_lines else '- none'}\n\n"
        "## Errors\n\n"
        f"{error_lines if error_lines else '- none'}\n"
    )


def run_x_reader_capture(url: str, timeout_seconds: int) -> tuple[int, str]:
    completed = subprocess.run(
        [str(X_READER_BIN), url],
        cwd=str(OPENCLAW_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    combined_output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part).strip()
    return completed.returncode, combined_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deep-capture WeChat full text for the market content system.")
    parser.add_argument("--date", help="Logical date in YYYY-MM-DD. Default: today in Asia/Shanghai.")
    parser.add_argument("--source-id", action="append", dest="source_ids", help="WeChat source id to deep-capture. Can repeat.")
    parser.add_argument("--packet-path", action="append", dest="packet_paths", help="Explicit packet path to deep-capture. Can repeat.")
    parser.add_argument("--timeout-seconds", type=int, default=120, help="Per-article x-reader timeout.")
    parser.add_argument("--write", action="store_true", help="Actually write deep articles, logs, and state.")
    parser.add_argument("--force", action="store_true", help="Ignore existing deep-capture state and recapture URLs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    run_at = now_cn()
    logical_date = args.date or run_at.strftime("%Y-%m-%d")
    selected_source_ids = args.source_ids or WECHAT_SOURCE_IDS

    state = load_json(STATE_PATH, {"urls": {}})
    state.setdefault("urls", {})

    candidates = list_candidate_packets(logical_date, selected_source_ids, args.packet_paths)
    new_articles: list[dict[str, str]] = []
    skipped_urls: list[dict[str, str]] = []
    errors: list[str] = []

    if not X_READER_BIN.exists():
        error = f"x-reader not found: {X_READER_BIN}"
        print(error)
        return 1

    for packet in candidates:
        url = str(packet["canonical_url"]).strip()
        state_row = state["urls"].get(url)
        if state_row and not args.force:
            skipped_urls.append(
                {
                    "source_id": str(packet["source_id"]),
                    "title": str(packet["title"]),
                    "canonical_url": url,
                }
            )
            continue

        started_at = now_cn()
        try:
            return_code, command_output = run_x_reader_capture(url, args.timeout_seconds)
        except subprocess.TimeoutExpired:
            errors.append(f"{packet['source_id']}: timeout while capturing {url}")
            continue
        except Exception as exc:
            errors.append(f"{packet['source_id']}: {type(exc).__name__}: {exc}")
            continue

        inbox_path = None
        parsed_inbox = parse_keyed_line(command_output, "inbox")
        if parsed_inbox:
            candidate = Path(parsed_inbox).expanduser()
            if candidate.exists():
                inbox_path = candidate
        if inbox_path is None:
            inbox_path = next((path for path in INBOX_PATH_CANDIDATES if path.exists()), None)

        inbox_records = load_inbox_records(inbox_path)
        inbox_record = select_latest_inbox_record(inbox_records, url, started_at)
        export_path = find_export_path(command_output, url, started_at)

        export_text = export_path.read_text(encoding="utf-8") if export_path and export_path.exists() else ""
        export_body = extract_export_body(export_text)
        normalized_body = clean_body(str((inbox_record or {}).get("content") or export_body))
        body_completeness, quality_notes, ui_noise_hits = assess_capture_quality(
            str(packet["title"]),
            export_body,
            normalized_body,
            command_output,
            return_code,
        )

        if body_completeness == "failed":
            errors.append(f"{packet['source_id']}: failed to deep-capture {url}")
            continue

        deep_captured_at = now_cn()
        timestamp = f"{logical_date_token(logical_date)}_{deep_captured_at.strftime('%H%M%S')}"
        slug = slugify(str(packet["title"]), "wechat_article")
        raw_copy_path = DEEP_RAW_DIR / f"{timestamp}__{slug}__xreader-raw.md"
        normalized_body_path = DEEP_RAW_DIR / f"{timestamp}__{slug}__normalized-body.md"
        command_output_path = DEEP_RAW_DIR / f"{timestamp}__{slug}__command-output.txt"
        deep_article_path = DEEP_DIR / f"{timestamp}__{slug}__deep-article.md"
        deep_capture_id = f"deep_{timestamp}_{slug}"

        raw_to_write = export_text or normalized_body
        write_text(raw_copy_path, raw_to_write)
        write_text(normalized_body_path, normalized_body or export_body)
        write_text(command_output_path, command_output or "(no command output)")

        best_body_excerpt = clean_body(export_body or normalized_body)
        best_body_excerpt = best_body_excerpt[:6000].strip()
        deep_article_text = render_deep_article(
            packet=packet,
            deep_capture_id=deep_capture_id,
            deep_captured_at=deep_captured_at,
            body_completeness=body_completeness,
            quality_notes=quality_notes,
            raw_export_char_count=len(export_body),
            normalized_char_count=len(normalized_body),
            paragraph_count=count_paragraphs(normalized_body or export_body),
            image_count=count_images(export_text),
            ui_noise_hits=ui_noise_hits,
            original_export_path=export_path,
            raw_copy_path=raw_copy_path,
            normalized_body_path=normalized_body_path,
            command_output_path=command_output_path,
            best_body_excerpt=best_body_excerpt,
        )
        if args.write:
            write_text(deep_article_path, deep_article_text)
            state["urls"][url] = {
                "title": str(packet["title"]),
                "source_id": str(packet["source_id"]),
                "source_packet_path": str(packet["packet_path"]),
                "deep_article_path": str(deep_article_path),
                "raw_copy_path": str(raw_copy_path),
                "normalized_body_path": str(normalized_body_path),
                "body_completeness": body_completeness,
                "deep_captured_at": format_dt(deep_captured_at),
            }
        new_articles.append(
            {
                "source_id": str(packet["source_id"]),
                "title": str(packet["title"]),
                "deep_article_path": str(deep_article_path) if args.write else f"(dry-run) {deep_article_path.name}",
            }
        )

    summary_log = render_summary_log(run_at, logical_date, args.write, selected_source_ids, new_articles, skipped_urls, errors)
    print(summary_log)

    if args.write:
        save_state(state)
        summary_path = LOG_DIR / f"{logical_date_token(logical_date)}_{run_at.strftime('%H%M%S')}__market-wechat-deep-capture-summary.md"
        write_text(summary_path, summary_log)
        print(f"\nSummary log written to: {summary_path}")
        print(f"State file updated: {STATE_PATH}")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
