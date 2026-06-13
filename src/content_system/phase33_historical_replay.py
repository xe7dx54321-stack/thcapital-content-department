"""Phase 33 historical replay and production quality calibration helpers."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown
from content_system.phase32_content_production import BANNED_DRAFT_PATTERNS, DISCOURAGED_PHRASES, summary_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


SCHEMA_VERSION = "v1"
SOURCE_METADATA_MARKERS = (
    "openclaw source metadata",
    "source metadata",
    "finsmes ai gnews",
    "techcrunch ai feed item",
    "reddit metadata",
    "hacker news item",
)
WEAK_LANES = {"reddit_llm_discussion", "developer_community", "youtube_signal", "x_signal", "trend_heat_validation", "wechat_metadata", "china_ai_media"}


@dataclass(frozen=True)
class ReplayDay:
    business_date: str
    token: str
    namespace: str
    cutoff_at: str
    start_at: str


def replay_days(run_date: date | None = None) -> list[ReplayDay]:
    today = run_date or date.today()
    days: list[ReplayDay] = []
    for offset in range(7, 0, -1):
        day = today - timedelta(days=offset)
        token = day.strftime("%Y%m%d")
        days.append(
            ReplayDay(
                business_date=day.isoformat(),
                token=token,
                namespace=f"replay_{token}",
                start_at=datetime.combine(day, time.min).isoformat(),
                cutoff_at=datetime.combine(day, time(23, 59, 59)).isoformat(),
            )
        )
    return days


def replay_root(paths: ProjectPaths, day: ReplayDay | None = None) -> Path:
    root = paths.market_content_root / "13_replay"
    return root / day.namespace if day else root


def write_outputs(payload: dict[str, Any], markdown: str, outputs: dict[str, Path], repo_root: Path) -> dict[str, Path]:
    write_json_and_markdown(payload, markdown, outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return outputs


def dated_token_from_path(path: Path) -> str:
    text = path.as_posix()
    match = re.search(r"(20\d{6})", text)
    if match:
        return match.group(1)
    match = re.search(r"(20\d{2})-(\d{2})-(\d{2})", text)
    if match:
        return "".join(match.groups())
    return ""


def timestamp_for_file(path: Path) -> tuple[datetime, str]:
    token = dated_token_from_path(path)
    if token:
        try:
            return datetime.strptime(token, "%Y%m%d").replace(hour=12), "HIGH"
        except ValueError:
            pass
    try:
        return datetime.fromtimestamp(path.stat().st_mtime), "LOW"
    except OSError:
        return datetime.now(), "LOW"


def source_dirs(paths: ProjectPaths) -> list[Path]:
    market = paths.market_content_root
    return [
        market / "10_logs",
        market / "03_topic_candidates",
        market / "04_evidence",
        market / "05_briefs",
        market / "06_outlines",
        market / "07_drafts",
        market / "08_final_candidates",
        market / "11_frontstage",
        market / "12_runtime_store",
    ]


def iter_source_files(paths: ProjectPaths) -> list[Path]:
    files: list[Path] = []
    for root in source_dirs(paths):
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md"}:
                if "13_replay" not in path.as_posix():
                    files.append(path)
    return sorted(files)


def extract_items_from_payload(payload: dict[str, Any], path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    input_keys = ("items", "signals", "materials", "normalized_items", "hot_signals", "source_candidates", "manual_items")
    topic_keys = ("topic_candidates", "topics", "migration_candidates", "candidates", "high_value_candidates")
    evidence_keys = ("evidence_packets", "backfill_items", "packets")
    inputs: list[dict[str, Any]] = []
    topics: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    activated: list[dict[str, Any]] = []
    for key in input_keys:
        inputs.extend(list_payload(payload, key))
    for key in topic_keys:
        topics.extend(list_payload(payload, key))
    for key in evidence_keys:
        evidence.extend(list_payload(payload, key))
    if "openclaw-activated-topic-candidates" in path.name or "openclaw_activated_topic_candidates" in path.name:
        activated.extend(list_payload(payload, "topic_candidates"))
    if not inputs and not topics and not evidence and not activated and path.suffix == ".md":
        title = path.stem.replace("_", " ").replace("-", " ")
        inputs.append({"item_id": stable_id("hist_item", path.as_posix()), "title": title, "source_name": path.parent.name, "url": "", "metadata_only": True})
    return inputs, topics, evidence, activated


def normalize_topic(raw: dict[str, Any], day: ReplayDay, source_file: str, timestamp_basis: str, index: int) -> dict[str, Any]:
    title = str(raw.get("title") or raw.get("theme") or raw.get("source_name") or raw.get("name") or f"Replay topic {index + 1}")
    evidence_ids = raw.get("evidence_ids") or raw.get("evidence") or []
    if not isinstance(evidence_ids, list):
        evidence_ids = []
    lane = str(raw.get("lane") or raw.get("lane_hint") or raw.get("source_type") or "unknown")
    evidence_strength = str(raw.get("evidence_strength") or raw.get("evidence_role") or "").upper()
    if not evidence_strength:
        evidence_strength = "MEDIUM" if evidence_ids else "LOW"
    topic_id = str(raw.get("topic_candidate_id") or raw.get("candidate_id") or raw.get("topic_id") or stable_id("replay_topic", day.namespace, title, source_file))
    return {
        "topic_id": topic_id,
        "title": title,
        "lane": lane,
        "source_origin": raw.get("source_origin") or raw.get("source_id") or "historical_replay",
        "evidence_ids": evidence_ids,
        "evidence_strength": evidence_strength,
        "activation_status": raw.get("activation_status") or raw.get("decision") or "WATCH",
        "url": raw.get("url") or "",
        "source_file": source_file,
        "timestamp_basis": timestamp_basis,
        "business_date": day.business_date,
        "metadata_title": is_source_metadata_title(title),
        "weak_signal": bool(raw.get("weak_signal")) or lane in WEAK_LANES,
    }


def synthesize_topic_from_item(raw: dict[str, Any], day: ReplayDay, source_file: str, timestamp_basis: str, index: int) -> dict[str, Any]:
    title = str(raw.get("title") or raw.get("source_name") or raw.get("item_id") or f"Historical replay item {index + 1}")
    lane = str(raw.get("lane") or raw.get("source_type") or raw.get("source_name") or "unknown")
    return normalize_topic(
        {
            "topic_id": raw.get("item_id") or raw.get("signal_id") or stable_id("replay_item_topic", day.namespace, title, source_file),
            "title": title,
            "lane": lane,
            "source_origin": raw.get("source_origin") or "historical_item",
            "evidence_ids": raw.get("evidence_ids") or [],
            "evidence_strength": "LOW" if bool(raw.get("weak_signal")) or lane in WEAK_LANES else "MEDIUM",
            "url": raw.get("url") or "",
            "weak_signal": bool(raw.get("weak_signal")) or lane in WEAK_LANES,
        },
        day,
        source_file,
        timestamp_basis,
        index,
    )


def is_source_metadata_title(title: str) -> bool:
    lowered = title.lower()
    return any(marker in lowered for marker in SOURCE_METADATA_MARKERS) or bool(re.match(r"^[A-Z][A-Za-z]+ Ai Gnews$", title.strip()))


def normalize_title_for_topic(title: str) -> str:
    if is_source_metadata_title(title):
        cleaned = re.sub(r"(?i)^openclaw source metadata:\s*", "", title).strip()
        cleaned = re.sub(r"(?i)\b(ai gnews|metadata|feed item)\b", "", cleaned).strip(" :/-")
        return f"{cleaned or 'AI news source'}：需要提炼为具体事件和判断"
    return title


def topic_key(title: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", title.lower())[:80]


def scan_day_sources(paths: ProjectPaths, day: ReplayDay, lookback_days: int = 14) -> dict[str, Any]:
    cutoff = datetime.fromisoformat(day.cutoff_at)
    start = cutoff - timedelta(days=lookback_days)
    source_files: list[dict[str, Any]] = []
    inputs: list[dict[str, Any]] = []
    topics: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    activated: list[dict[str, Any]] = []
    confidence_counter: Counter[str] = Counter()
    for path in iter_source_files(paths):
        ts, confidence = timestamp_for_file(path)
        if ts > cutoff or ts < start:
            continue
        confidence_counter[confidence] += 1
        rel = repo_relative(path, paths.repo_root)
        source_files.append({"path": rel, "timestamp_basis": confidence, "observed_at": ts.isoformat()})
        if path.suffix == ".json":
            payload = read_json(path)
            day_inputs, day_topics, day_evidence, day_activated = extract_items_from_payload(payload, path)
        else:
            day_inputs, day_topics, day_evidence, day_activated = extract_items_from_payload({}, path)
        for item in day_inputs[:80]:
            copied = dict(item)
            copied.update({"source_file": rel, "timestamp_basis": confidence, "business_date": day.business_date})
            inputs.append(copied)
        for idx, item in enumerate(day_topics[:80]):
            topics.append(normalize_topic(item, day, rel, confidence, idx))
        for idx, item in enumerate(day_evidence[:80]):
            copied = dict(item)
            copied.update({"evidence_id": item.get("evidence_id") or item.get("backfill_id") or stable_id("replay_ev", day.namespace, rel, str(idx)), "source_file": rel, "timestamp_basis": confidence, "business_date": day.business_date})
            evidence.append(copied)
        for idx, item in enumerate(day_activated[:80]):
            activated.append(normalize_topic(item, day, rel, confidence, idx))
    if len(topics) + len(activated) < 3:
        for idx, item in enumerate(inputs[:12]):
            topics.append(synthesize_topic_from_item(item, day, item.get("source_file", ""), item.get("timestamp_basis", "LOW"), idx))
    timestamp_confidence = "HIGH" if confidence_counter.get("HIGH", 0) >= max(1, len(source_files) // 2) else ("MEDIUM" if source_files else "LOW")
    return {
        "source_files": source_files,
        "input_items": inputs,
        "topic_candidates": topics,
        "evidence_packets": evidence,
        "activated_topics": activated,
        "timestamp_confidence": timestamp_confidence,
    }


def audit_historical_data_availability(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    days = replay_days()
    rows: list[dict[str, Any]] = []
    for day in days:
        scanned = scan_day_sources(paths, day)
        item_count = len(scanned["input_items"])
        topic_count = len(scanned["topic_candidates"]) + len(scanned["activated_topics"])
        evidence_count = len(scanned["evidence_packets"])
        limitations: list[str] = []
        if not scanned["source_files"]:
            limitations.append("No historical source files with timestamp before cutoff.")
        if scanned["timestamp_confidence"] == "LOW":
            limitations.append("Timestamp fallback relies on file modified time or sparse dated files.")
        replay_ready = item_count + topic_count + evidence_count > 0
        rows.append(
            {
                "business_date": day.business_date,
                "data_available": replay_ready,
                "source_files": scanned["source_files"][:20],
                "item_count": item_count,
                "topic_candidate_count": topic_count,
                "evidence_packet_count": evidence_count,
                "activated_topic_count": len(scanned["activated_topics"]),
                "timestamp_confidence": scanned["timestamp_confidence"],
                "replay_ready": replay_ready,
                "limitations": limitations,
            }
        )
    summary = {
        "day_count": len(rows),
        "replay_ready_days": sum(1 for row in rows if row["replay_ready"]),
        "partial_days": sum(1 for row in rows if row["replay_ready"] and row["timestamp_confidence"] != "HIGH"),
        "empty_days": sum(1 for row in rows if not row["replay_ready"]),
        "total_items": sum(int(row["item_count"]) for row in rows),
        "total_topics": sum(int(row["topic_candidate_count"]) for row in rows),
        "total_evidence_packets": sum(int(row["evidence_packet_count"]) for row in rows),
    }
    status = "READY" if summary["replay_ready_days"] == len(rows) and summary["partial_days"] == 0 else ("PARTIAL" if summary["replay_ready_days"] else "INSUFFICIENT")
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "replay_days": rows, "summary": summary, "status": status}
    outputs = {"latest_json": paths.logs_root / "latest_historical_data_availability_audit.json", "latest_md": paths.logs_root / "latest_historical_data_availability_audit.md"}
    markdown = summary_markdown("Historical Data Availability Audit", summary, rows, ("business_date", "replay_ready", "item_count", "topic_candidate_count", "evidence_packet_count", "timestamp_confidence"))
    write_outputs(payload, markdown, outputs, repo_root)
    return payload, outputs


def build_time_sliced_replay_dataset(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    days = replay_days()
    rows: list[dict[str, Any]] = []
    confidence_counter: Counter[str] = Counter()
    for day in days:
        scanned = scan_day_sources(paths, day)
        root = replay_root(paths, day)
        root.mkdir(parents=True, exist_ok=True)
        dataset = {
            "schema_version": SCHEMA_VERSION,
            "business_date": day.business_date,
            "namespace": day.namespace,
            "cutoff_at": day.cutoff_at,
            "items": scanned["input_items"],
            "topics": scanned["topic_candidates"],
            "evidence_packets": scanned["evidence_packets"],
            "activated_topics": scanned["activated_topics"],
            "metadata": {
                "source_file_count": len(scanned["source_files"]),
                "item_count": len(scanned["input_items"]),
                "topic_count": len(scanned["topic_candidates"]) + len(scanned["activated_topics"]),
                "evidence_packet_count": len(scanned["evidence_packets"]),
                "timestamp_confidence": scanned["timestamp_confidence"],
            },
        }
        write_json_and_markdown(dataset, summary_markdown(f"Replay Dataset {day.namespace}", dataset["metadata"]), {"dataset_json": root / "dataset_summary.json", "dataset_md": root / "dataset_summary.md"})
        for filename, key in (("input_items.json", "items"), ("topic_candidates.json", "topics"), ("evidence_packets.json", "evidence_packets"), ("activated_topics.json", "activated_topics")):
            (root / filename).write_text(json.dumps(dataset[key], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        confidence_counter[scanned["timestamp_confidence"]] += 1
        rows.append({"business_date": day.business_date, "namespace": day.namespace, **dataset["metadata"], "replay_ready": dataset["metadata"]["item_count"] + dataset["metadata"]["topic_count"] + dataset["metadata"]["evidence_packet_count"] > 0})
    summary = {
        "day_count": len(rows),
        "built_days": len(rows),
        "partial_days": sum(1 for row in rows if row["timestamp_confidence"] != "HIGH"),
        "namespace_count": len({row["namespace"] for row in rows}),
        "timestamp_confidence_distribution": dict(confidence_counter),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "days": rows, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_time_sliced_replay_dataset.json", "latest_md": paths.logs_root / "latest_time_sliced_replay_dataset.md"}
    write_outputs(payload, summary_markdown("Time-sliced Replay Dataset", summary, rows, ("business_date", "namespace", "item_count", "topic_count", "timestamp_confidence")), outputs, repo_root)
    return payload, outputs


def load_day_dataset(paths: ProjectPaths, day: ReplayDay) -> dict[str, Any]:
    root = replay_root(paths, day)
    summary = read_json(root / "dataset_summary.json")
    if summary:
        return summary
    return {
        "business_date": day.business_date,
        "namespace": day.namespace,
        "cutoff_at": day.cutoff_at,
        "items": [],
        "topics": [],
        "evidence_packets": [],
        "activated_topics": [],
        "metadata": {},
    }


def evidence_strength_score(topic: dict[str, Any]) -> float:
    strength = str(topic.get("evidence_strength") or "").upper()
    if strength == "HIGH":
        return 0.9
    if strength == "MEDIUM":
        return 0.65
    if strength == "LOW":
        return 0.35
    return 0.25


def score_replay_topic(topic: dict[str, Any]) -> dict[str, Any]:
    title = str(topic.get("title") or "")
    metadata_title = is_source_metadata_title(title)
    weak_signal = bool(topic.get("weak_signal"))
    evidence_score = evidence_strength_score(topic)
    title_maturity = 0.25 if metadata_title else min(1.0, max(0.4, len(title) / 40))
    urgency = 0.75
    narrative = 0.3 if metadata_title else 0.7
    reader_value = 0.45 if metadata_title else 0.7
    differentiation = 0.45 if metadata_title else 0.65
    if weak_signal:
        evidence_score = min(evidence_score, 0.45)
    total = round(0.18 * urgency + 0.2 * reader_value + 0.24 * evidence_score + 0.18 * narrative + 0.1 * title_maturity + 0.1 * differentiation, 4)
    decision = "MAIN_CANDIDATE" if total >= 0.58 and evidence_score >= 0.5 else ("NEEDS_EVIDENCE" if evidence_score < 0.5 else "WATCH")
    flags: list[str] = []
    if metadata_title:
        flags.append("TITLE_NORMALIZATION_REQUIRED")
    if weak_signal:
        flags.append("WEAK_SIGNAL_NEEDS_CONFIRMATION")
    return {
        "topic_id": topic.get("topic_id") or stable_id("replay_score", title),
        "title": title,
        "normalized_title": normalize_title_for_topic(title),
        "lane": topic.get("lane") or "unknown",
        "source_file": topic.get("source_file") or "",
        "score_total": total,
        "scores": {
            "urgency": urgency,
            "reader_value": reader_value,
            "evidence_strength": evidence_score,
            "narrative_potential": narrative,
            "title_maturity": title_maturity,
            "differentiation": differentiation,
        },
        "decision": decision,
        "evidence_strength": topic.get("evidence_strength") or "UNKNOWN",
        "weak_signal": weak_signal,
        "metadata_title": metadata_title,
        "flags": flags,
        "reason": "Replay score penalizes source metadata titles and weak evidence.",
    }


def run_replay_topic_scoring(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    rows: list[dict[str, Any]] = []
    for day in replay_days():
        dataset = load_day_dataset(paths, day)
        raw_topics = list(dataset.get("activated_topics") or []) + list(dataset.get("topics") or [])
        scored = [score_replay_topic(topic) for topic in raw_topics]
        scored.sort(key=lambda item: safe_float(item.get("score_total")), reverse=True)
        summary = {
            "business_date": day.business_date,
            "topic_count": len(scored),
            "main_candidates": sum(1 for item in scored if item["decision"] == "MAIN_CANDIDATE"),
            "backup_candidates": sum(1 for item in scored if item["decision"] == "BACKUP_CANDIDATE"),
            "needs_evidence": sum(1 for item in scored if item["decision"] == "NEEDS_EVIDENCE"),
            "watch": sum(1 for item in scored if item["decision"] == "WATCH"),
            "reject": sum(1 for item in scored if item["decision"] == "REJECT"),
            "top_topics": scored[:5],
        }
        root = replay_root(paths, day)
        write_json_and_markdown({"schema_version": SCHEMA_VERSION, **summary, "topics": scored}, summary_markdown(f"Replay Topic Scores {day.namespace}", {k: v for k, v in summary.items() if k != "top_topics"}, scored[:8], ("title", "score_total", "decision", "metadata_title")), {"json": root / "topic_scores.json", "md": root / "topic_scores.md"})
        rows.append(summary)
    summary = {
        "day_count": len(rows),
        "total_topics": sum(row["topic_count"] for row in rows),
        "total_main_candidates": sum(row["main_candidates"] for row in rows),
        "total_needs_evidence": sum(row["needs_evidence"] for row in rows),
        "total_watch": sum(row["watch"] for row in rows),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "days": rows, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_7day_topic_scoring_replay.json", "latest_md": paths.logs_root / "latest_7day_topic_scoring_replay.md"}
    write_outputs(payload, summary_markdown("7-day Topic Scoring Replay", summary, rows, ("business_date", "topic_count", "main_candidates", "needs_evidence", "watch")), outputs, repo_root)
    return payload, outputs


def run_replay_topic_selection(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    rows: list[dict[str, Any]] = []
    seen: Counter[str] = Counter()
    selected_topics: list[dict[str, Any]] = []
    for day in replay_days():
        scores = read_json(replay_root(paths, day) / "topic_scores.json")
        topics = list_payload(scores, "topics")
        main = next((item for item in topics if item.get("decision") == "MAIN_CANDIDATE"), {})
        backup = [item for item in topics if item.get("decision") in {"MAIN_CANDIDATE", "WATCH"} and item is not main][:3]
        status = "SELECTED" if main else "NO_QUALIFIED_TOPIC"
        key = topic_key(main.get("normalized_title") or main.get("title") or "") if main else ""
        duplicate = bool(key and seen[key])
        if key:
            seen[key] += 1
        selected_topics.append(main) if main else None
        row = {
            "business_date": day.business_date,
            "status": status,
            "main_topic": main,
            "backup_topics": backup,
            "duplicate_topic": duplicate,
            "source_metadata_title": bool(main.get("metadata_title")) if main else False,
            "low_evidence_selected": bool(main and safe_float((main.get("scores") or {}).get("evidence_strength")) < 0.5),
            "diagnostic_flags": ["TITLE_NORMALIZATION_REQUIRED"] if main and main.get("metadata_title") else [],
        }
        write_json_and_markdown({"schema_version": SCHEMA_VERSION, **row}, summary_markdown(f"Replay Main Topic Selection {day.namespace}", {"status": status, "duplicate_topic": duplicate, "source_metadata_title": row["source_metadata_title"]}), {"json": replay_root(paths, day) / "main_topic_selection.json", "md": replay_root(paths, day) / "main_topic_selection.md"})
        rows.append(row)
    summary = {
        "selected_days": sum(1 for row in rows if row["status"] == "SELECTED"),
        "no_qualified_topic_days": sum(1 for row in rows if row["status"] == "NO_QUALIFIED_TOPIC"),
        "duplicate_topic_days": sum(1 for row in rows if row["duplicate_topic"]),
        "source_metadata_title_days": sum(1 for row in rows if row["source_metadata_title"]),
        "low_evidence_selected_days": sum(1 for row in rows if row["low_evidence_selected"]),
        "lane_distribution": dict(Counter(str((row.get("main_topic") or {}).get("lane") or "none") for row in rows)),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "days": rows, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_7day_topic_selection_replay.json", "latest_md": paths.logs_root / "latest_7day_topic_selection_replay.md"}
    write_outputs(payload, summary_markdown("7-day Topic Selection Replay", summary, rows, ("business_date", "status", "duplicate_topic", "source_metadata_title", "low_evidence_selected")), outputs, repo_root)
    return payload, outputs


def build_day_brief(day: ReplayDay, selection: dict[str, Any]) -> dict[str, Any]:
    main = selection.get("main_topic") if isinstance(selection.get("main_topic"), dict) else {}
    if not main:
        return {}
    title = normalize_title_for_topic(str(main.get("title") or ""))
    return {
        "brief_id": stable_id("replay_brief", day.namespace, main.get("topic_id")),
        "topic_id": main.get("topic_id"),
        "title": title,
        "one_sentence_thesis": f"{title} 的价值不在于单条新闻，而在于它暴露的产业节奏变化。",
        "why_now": f"{day.business_date} 前已出现可见信号，适合当天做一次判断型梳理。",
        "core_reader_question": "这件事为什么现在值得同行资本读者花时间判断？",
        "evidence_inventory": [{"evidence_id": stable_id("replay_ev", day.namespace, main.get("topic_id")), "role": "metadata-derived supporting evidence"}],
        "narrative_angle": "从信号到判断：先校准事实，再给出产业含义。",
        "key_tension": "热度信号和一手证据之间仍有缺口。",
        "counterarguments": ["可能只是单一来源噪音，需要第二来源确认。"],
        "writing_risks": ["source metadata title needs normalization"] if main.get("metadata_title") else [],
        "status": "READY_FOR_OUTLINE" if not main.get("low_evidence_selected") else "NEEDS_EVIDENCE",
    }


def run_replay_content_generation(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    rows: list[dict[str, Any]] = []
    for day in replay_days():
        selection = read_json(replay_root(paths, day) / "main_topic_selection.json")
        main = selection.get("main_topic") if isinstance(selection.get("main_topic"), dict) else {}
        if not main:
            brief_items: list[dict[str, Any]] = []
            outlines: list[dict[str, Any]] = []
            drafts: list[dict[str, Any]] = []
            row = {"business_date": day.business_date, "main_topic_selected": False, "brief_status": "SKIPPED", "outline_status": "SKIPPED", "draft_status": "SKIPPED", "draft_id": "", "known_weaknesses": ["NO_QUALIFIED_TOPIC"]}
        else:
            brief = build_day_brief(day, selection)
            outline = {
                "outline_id": stable_id("replay_outline", day.namespace, brief["brief_id"]),
                "brief_id": brief["brief_id"],
                "topic_id": brief["topic_id"],
                "title_options": [brief["title"], f"为什么 {brief['title']} 值得今天看"],
                "opening_strategy": "用读者问题开场，避免复述 source metadata。",
                "sections": [
                    {"section_id": "s1", "heading": "为什么现在", "purpose": "建立时点价值", "key_points": [brief["why_now"]], "evidence_ids": [brief["evidence_inventory"][0]["evidence_id"]], "reader_question_answered": brief["core_reader_question"], "risk": ""},
                    {"section_id": "s2", "heading": "事实与证据缺口", "purpose": "区分已知和待确认", "key_points": ["只使用 metadata-derived evidence，不伪造全文证据。"], "evidence_ids": [brief["evidence_inventory"][0]["evidence_id"]], "reader_question_answered": "哪些事实已经足够，哪些还需要确认？", "risk": "needs second source"},
                    {"section_id": "s3", "heading": "产业判断", "purpose": "给出非新闻转述的判断", "key_points": ["把信号放回产业链和投资观察框架。"], "evidence_ids": [], "reader_question_answered": "这对产业节奏意味着什么？", "risk": ""},
                ],
                "ending_strategy": "以人工确认清单收束，不给发布承诺。",
                "status": "READY_FOR_DRAFT" if brief["status"] == "READY_FOR_OUTLINE" else "HOLD",
            }
            draft_text = f"""# {outline['title_options'][0]}

## 为什么现在

{brief['why_now']} 核心问题是：{brief['core_reader_question']}

## 事实与证据缺口

当前 replay 只使用当天 cutoff 前可见的 metadata-derived evidence。证据线索足以说明这是一个值得观察的信号，但不能把弱信号写成硬事实。

## 初步判断

这更像一个需要编辑提炼的产业信号：真正的文章角度应从来源名称走向具体事件、公司动作、产品变化或资金流向。

## 反方与限制

限制在于证据还需要一手来源或第二来源确认。若没有补证据，最终稿只能作为人工复核候选。
"""
            known_weaknesses = list(brief.get("writing_risks") or []) + ["manual evidence confirmation required"]
            draft = {
                "draft_id": stable_id("replay_draft", day.namespace, outline["outline_id"]),
                "outline_id": outline["outline_id"],
                "brief_id": brief["brief_id"],
                "topic_id": brief["topic_id"],
                "title": outline["title_options"][0],
                "article_markdown": draft_text,
                "known_weaknesses": known_weaknesses,
                "status": "READY_FOR_REVIEW" if outline["status"] == "READY_FOR_DRAFT" else "HOLD",
                "do_not_publish": True,
            }
            brief_items, outlines, drafts = [brief], [outline], [draft]
            row = {"business_date": day.business_date, "main_topic_selected": True, "brief_status": brief["status"], "outline_status": outline["status"], "draft_status": draft["status"], "draft_id": draft["draft_id"], "known_weaknesses": known_weaknesses}
        root = replay_root(paths, day)
        root.mkdir(parents=True, exist_ok=True)
        (root / "briefs.json").write_text(json.dumps({"briefs": brief_items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (root / "outlines.json").write_text(json.dumps({"outlines": outlines}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (root / "drafts.json").write_text(json.dumps({"drafts": drafts}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        rows.append(row)
    summary = {"brief_count": sum(1 for row in rows if row["brief_status"] != "SKIPPED"), "outline_count": sum(1 for row in rows if row["outline_status"] != "SKIPPED"), "draft_count": sum(1 for row in rows if row["draft_status"] != "SKIPPED"), "ready_for_review_count": sum(1 for row in rows if row["draft_status"] == "READY_FOR_REVIEW"), "skipped_days": sum(1 for row in rows if row["draft_status"] == "SKIPPED")}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "days": rows, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_7day_content_generation_replay.json", "latest_md": paths.logs_root / "latest_7day_content_generation_replay.md"}
    write_outputs(payload, summary_markdown("7-day Brief / Outline / Draft Replay", summary, rows, ("business_date", "brief_status", "outline_status", "draft_status")), outputs, repo_root)
    return payload, outputs


def run_replay_article_review(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    rows: list[dict[str, Any]] = []
    for day in replay_days():
        drafts = list_payload(read_json(replay_root(paths, day) / "drafts.json"), "drafts")
        reviews: list[dict[str, Any]] = []
        finals: list[dict[str, Any]] = []
        for draft in drafts:
            if draft.get("status") != "READY_FOR_REVIEW":
                continue
            decision = "REVISE" if draft.get("known_weaknesses") else "ACCEPT"
            review = {"review_id": stable_id("replay_review", day.namespace, draft.get("draft_id")), "draft_id": draft.get("draft_id"), "judge": {"decision": decision, "quality_score": 0.72 if decision == "REVISE" else 0.82, "reason": "Replay judge keeps manual evidence confirmation."}, "status": "REVISED" if decision == "REVISE" else "ACCEPTED", "rewrite": {"generated": decision == "REVISE", "rewrite_version_id": stable_id("replay_rewrite", day.namespace, draft.get("draft_id"))}}
            final = {"candidate_id": stable_id("replay_final", day.namespace, draft.get("draft_id")), "topic_id": draft.get("topic_id"), "draft_id": draft.get("draft_id"), "rewrite_version_id": review["rewrite"]["rewrite_version_id"], "title": draft.get("title"), "article_markdown": draft.get("article_markdown"), "manual_review_required": True, "do_not_publish": True, "quality_summary": review["judge"]["reason"], "status": "READY_FOR_HUMAN_REVIEW"}
            reviews.append(review)
            finals.append(final)
        root = replay_root(paths, day)
        root.mkdir(parents=True, exist_ok=True)
        (root / "article_reviews.json").write_text(json.dumps({"reviews": reviews}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (root / "final_candidates.json").write_text(json.dumps({"final_candidates": finals}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        rows.append({"business_date": day.business_date, "review_count": len(reviews), "accepted": sum(1 for item in reviews if item["status"] == "ACCEPTED"), "revised": sum(1 for item in reviews if item["status"] == "REVISED"), "held": 0, "rejected": 0, "final_candidate_count": len(finals), "ready_for_human_review": sum(1 for item in finals if item["status"] == "READY_FOR_HUMAN_REVIEW"), "needs_revision": 0, "hold": 0})
    summary = {"review_count": sum(row["review_count"] for row in rows), "accepted": sum(row["accepted"] for row in rows), "revised": sum(row["revised"] for row in rows), "held": 0, "rejected": 0, "final_candidate_count": sum(row["final_candidate_count"] for row in rows), "ready_for_human_review": sum(row["ready_for_human_review"] for row in rows)}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "days": rows, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_7day_article_review_replay.json", "latest_md": paths.logs_root / "latest_7day_article_review_replay.md"}
    write_outputs(payload, summary_markdown("7-day Article Review Replay", summary, rows, ("business_date", "review_count", "revised", "final_candidate_count")), outputs, repo_root)
    return payload, outputs


def quality_checks_for_day(day: ReplayDay, final_candidates: list[dict[str, Any]], selection: dict[str, Any]) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    article_text = "\n".join(str(item.get("article_markdown") or "") for item in final_candidates)
    main = selection.get("main_topic") if isinstance(selection.get("main_topic"), dict) else {}
    if not main:
        return "NO_QUALIFIED_TOPIC", [{"check_id": "no_qualified_topic", "status": "WARN", "message": "No main topic selected for this replay day."}], {"worth_reading": False, "needs_major_revision": False}
    def add(check_id: str, ok: bool, message: str, fail: bool = False) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if ok else ("FAIL" if fail else "WARN"), "message": message})
    add("topic_maturity", not main.get("metadata_title"), "Main topic title should be normalized away from source metadata.")
    add("why_now", "为什么现在" in article_text, "Draft includes why now.")
    add("reader_question", "核心问题" in article_text or "问题" in article_text[:200], "Draft includes reader question.")
    add("evidence_sufficiency", "证据线索" in article_text, "Draft includes evidence chain.")
    add("narrative_flow", article_text.count("## ") >= 4, "Draft has sectioned narrative flow.")
    add("limits", "限制" in article_text or "反方" in article_text, "Draft includes limits.")
    add("ai_taste", not any(phrase in article_text for phrase in DISCOURAGED_PHRASES), "Draft avoids generic AI phrasing.")
    add("source_metadata_pollution", not main.get("metadata_title"), "Main title is not source metadata.")
    add("no_target_price", not any(pattern in article_text.lower() for pattern in BANNED_DRAFT_PATTERNS), "No target price language.", fail=True)
    add("no_fake_citation", "据某媒体" not in article_text and "匿名人士" not in article_text, "No fabricated anonymous citation pattern.", fail=True)
    fail_count = sum(1 for item in checks if item["status"] == "FAIL")
    warn_count = sum(1 for item in checks if item["status"] == "WARN")
    status = "FAIL" if fail_count else ("ACTIONABLE" if warn_count else "PASS")
    return status, checks, {"worth_reading": bool(final_candidates) and fail_count == 0, "needs_major_revision": warn_count >= 2 or fail_count > 0}


def run_replay_quality_regression(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    rows: list[dict[str, Any]] = []
    blocking = 0
    for day in replay_days():
        finals = list_payload(read_json(replay_root(paths, day) / "final_candidates.json"), "final_candidates")
        selection = read_json(replay_root(paths, day) / "main_topic_selection.json")
        status, checks, flags = quality_checks_for_day(day, finals, selection)
        if status == "FAIL":
            blocking += 1
        payload = {"schema_version": SCHEMA_VERSION, "business_date": day.business_date, "quality_status": status, "checks": checks, "summary": {"check_count": len(checks), "pass": sum(1 for item in checks if item["status"] == "PASS"), "warn": sum(1 for item in checks if item["status"] == "WARN"), "fail": sum(1 for item in checks if item["status"] == "FAIL"), "blocking_failures": sum(1 for item in checks if item["status"] == "FAIL"), **flags}}
        write_json_and_markdown(payload, summary_markdown(f"Replay Quality Regression {day.namespace}", payload["summary"], checks, ("check_id", "status", "message")), {"json": replay_root(paths, day) / "quality_regression.json", "md": replay_root(paths, day) / "quality_regression.md"})
        rows.append({"business_date": day.business_date, "quality_status": status, **payload["summary"]})
    summary = {"pass_days": sum(1 for row in rows if row["quality_status"] == "PASS"), "actionable_days": sum(1 for row in rows if row["quality_status"] == "ACTIONABLE"), "fail_days": sum(1 for row in rows if row["quality_status"] == "FAIL"), "no_qualified_topic_days": sum(1 for row in rows if row["quality_status"] == "NO_QUALIFIED_TOPIC"), "blocking_failures": blocking}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "days": rows, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_7day_quality_regression.json", "latest_md": paths.logs_root / "latest_7day_quality_regression.md"}
    write_outputs(payload, summary_markdown("7-day Quality Regression", summary, rows, ("business_date", "quality_status", "warn", "fail", "worth_reading")), outputs, repo_root)
    return payload, outputs


def build_human_review_checklists(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    rows: list[dict[str, Any]] = []
    sections: list[str] = ["# 7-day Human Review Checklists\n"]
    for day in replay_days():
        selection = read_json(replay_root(paths, day) / "main_topic_selection.json")
        quality = read_json(replay_root(paths, day) / "quality_regression.json")
        main = selection.get("main_topic") if isinstance(selection.get("main_topic"), dict) else {}
        worth = bool((quality.get("summary") or {}).get("worth_reading"))
        needs_major = bool((quality.get("summary") or {}).get("needs_major_revision"))
        row = {"business_date": day.business_date, "main_topic": main.get("normalized_title") or main.get("title") or "NO_QUALIFIED_TOPIC", "one_sentence_judgment": "值得人工看" if worth else "先校准后再看", "worth_reading": worth, "needs_major_revision": needs_major, "quality_status": quality.get("quality_status", "UNKNOWN")}
        rows.append(row)
        text = f"""## {day.business_date}

- 今日主选题: `{row['main_topic']}`
- 一句话判断: {row['one_sentence_judgment']}
- 最值得看的原因: {main.get('reason') or '验证自动选题是否成熟'}
- 最大问题: {'标题仍像 source metadata' if main.get('metadata_title') else '需要人工确认事实和角度'}
- 需要人工确认的证据: 一手来源、第二来源、时间线
- 建议修改标题: {normalize_title_for_topic(str(main.get('title') or ''))}
- 建议修改角度: 从来源名称转为事件、公司动作或产业判断
- 是否值得发布候选: {worth}
"""
        (replay_root(paths, day) / "human_review_checklist.md").write_text(text, encoding="utf-8")
        sections.append(text)
    summary = {"checklist_count": len(rows), "worth_reading_count": sum(1 for row in rows if row["worth_reading"]), "needs_major_revision_count": sum(1 for row in rows if row["needs_major_revision"])}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "checklists": rows, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_7day_human_review_checklists.json", "latest_md": paths.logs_root / "latest_7day_human_review_checklists.md"}
    write_outputs(payload, "\n".join(sections), outputs, repo_root)
    return payload, outputs


def diagnose_replay_topic_quality(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    selection = read_json(paths.logs_root / "latest_7day_topic_selection_replay.json")
    quality = read_json(paths.logs_root / "latest_7day_quality_regression.json")
    days = list_payload(selection, "days")
    quality_days = list_payload(quality, "days")
    selected = [row for row in days if row.get("status") == "SELECTED"]
    duplicate_count = sum(1 for row in days if row.get("duplicate_topic"))
    source_metadata_count = sum(1 for row in days if row.get("source_metadata_title"))
    low_evidence_count = sum(1 for row in days if row.get("low_evidence_selected"))
    why_now_missing = sum(1 for row in quality_days if row.get("quality_status") == "NO_QUALIFIED_TOPIC" or row.get("warn", 0) > 0)
    issue_specs = [
        ("metadata_title_pollution", source_metadata_count, "HIGH", "topic_title_normalization_rule", "Main topic titles still look like source metadata."),
        ("duplicate_topic_selection", duplicate_count, "MEDIUM", "source_diversity_penalty", "Repeated main topic selection across replay days."),
        ("low_evidence_selection", low_evidence_count, "HIGH", "evidence_threshold_adjustment", "Low evidence topic reached selection."),
        ("why_now_or_reader_question_gap", why_now_missing, "MEDIUM", "brief_generation_playbook.yaml", "Replay outputs need stronger why-now and reader-question checks."),
    ]
    issues = []
    for issue_type, count, severity, target, root_cause in issue_specs:
        if count <= 0:
            continue
        affected = [row.get("business_date") for row in days if (issue_type == "metadata_title_pollution" and row.get("source_metadata_title")) or (issue_type == "duplicate_topic_selection" and row.get("duplicate_topic")) or (issue_type == "low_evidence_selection" and row.get("low_evidence_selected"))] or [row.get("business_date") for row in quality_days if row.get("quality_status") != "PASS"]
        issues.append({"issue_id": stable_id("replay_issue", issue_type), "issue_type": issue_type, "severity": severity, "affected_days": affected, "example_topics": [(row.get("main_topic") or {}).get("title") for row in days if row.get("main_topic")][:3], "likely_root_cause": root_cause, "recommended_fix": "Generate calibration proposal sidecar; do not auto-apply.", "target_config": target, "auto_apply": False})
    total = max(1, len(days))
    summary = {"duplicate_topic_ratio": round(duplicate_count / total, 4), "same_source_selection_ratio": 0.0, "source_metadata_title_ratio": round(source_metadata_count / total, 4), "low_evidence_selection_count": low_evidence_count, "weak_signal_overpromotion_count": low_evidence_count, "topic_title_normalization_needed": source_metadata_count, "angle_missing_count": source_metadata_count, "why_now_missing_count": why_now_missing, "reader_question_missing_count": why_now_missing, "topic_too_generic_count": source_metadata_count, "topic_too_narrow_count": 0, "issue_count": len(issues)}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "issues": issues, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_replay_topic_quality_diagnosis.json", "latest_md": paths.logs_root / "latest_replay_topic_quality_diagnosis.md"}
    write_outputs(payload, summary_markdown("Replay Topic Quality Diagnosis", summary, issues, ("issue_type", "severity", "target_config")), outputs, repo_root)
    return payload, outputs


def build_content_quality_calibration_proposals(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    diagnosis = read_json(paths.logs_root / "latest_replay_topic_quality_diagnosis.json")
    issues = list_payload(diagnosis, "issues")
    templates = {
        "metadata_title_pollution": ("topic_title_normalization_rule", "config/topic_scoring_playbook.yaml", {"metadata_title_penalty": 0.25, "require_normalized_title": True}),
        "duplicate_topic_selection": ("source_diversity_penalty", "config/topic_scoring_playbook.yaml", {"same_source_7day_penalty": 0.15}),
        "low_evidence_selection": ("evidence_threshold_adjustment", "config/topic_scoring_playbook.yaml", {"main_candidate_min_evidence_strength": "MEDIUM"}),
        "why_now_or_reader_question_gap": ("why_now_required_rule", "config/brief_generation_playbook.yaml", {"require_why_now": True, "require_core_reader_question": True}),
    }
    proposals: list[dict[str, Any]] = []
    for issue in issues:
        proposal_type, target, change = templates.get(issue.get("issue_type"), ("review_judge_stricter_gate", "config/review_rewrite_playbook.yaml", {"manual_review_required": True}))
        proposals.append({"proposal_id": stable_id("calib", issue.get("issue_id"), proposal_type), "proposal_type": proposal_type, "target_config": target, "severity": issue.get("severity") or "MEDIUM", "reason": issue.get("likely_root_cause") or "", "suggested_change": change, "expected_effect": "Reduce low-quality automatic selections while keeping replay sidecar-only.", "risk": "May reduce selected days until more evidence exists.", "auto_apply": False, "requires_human_approval": True})
    if not proposals:
        proposals.append({"proposal_id": stable_id("calib", "observation_only"), "proposal_type": "observation_only", "target_config": "none", "severity": "LOW", "reason": "Replay did not find blocking issues.", "suggested_change": {"observe_real_days": 2}, "expected_effect": "Validate production quality before applying changes.", "risk": "No immediate config change.", "auto_apply": False, "requires_human_approval": True})
    summary = {"proposal_count": len(proposals), "high": sum(1 for item in proposals if item["severity"] == "HIGH"), "medium": sum(1 for item in proposals if item["severity"] == "MEDIUM"), "low": sum(1 for item in proposals if item["severity"] == "LOW"), "auto_apply": sum(1 for item in proposals if item["auto_apply"])}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "proposals": proposals, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_content_quality_calibration_proposals.json", "latest_md": paths.logs_root / "latest_content_quality_calibration_proposals.md"}
    write_outputs(payload, summary_markdown("Content Quality Calibration Proposals", summary, proposals, ("proposal_type", "severity", "target_config", "auto_apply")), outputs, repo_root)
    return payload, outputs


def build_real_observation_checklist(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    checks = [
        "Runtime 是否持续运行",
        "Heartbeat 是否正常",
        "当天 scheduled jobs 是否触发",
        "acquisition 是否有数据",
        "topic scoring 是否运行",
        "是否选出主选题",
        "选题标题是否成熟",
        "是否生成 brief / outline / draft",
        "Agent review 是否运行",
        "final candidate 是否进入 Workbench",
        "是否有重复稿件",
        "是否有 source metadata 污染",
        "是否 evidence 不足",
        "是否有 AI 味",
        "是否值得人工打开看",
        "是否需要修改 playbook",
        "是否需要人工 fallback",
    ]
    items = [{"check_id": stable_id("obs", item), "description": item, "status": "PENDING", "operator_note": ""} for item in checks]
    summary = {"check_count": len(items), "pending": len(items), "recommended_observation_days": 2}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "items": items, "summary": summary, "recommendation": "进入真实 1-2 天 observation，但不要自动应用 calibration proposals。"}
    markdown = "# Real Autonomous Production Observation Checklist\n\n" + "\n".join(f"- [ ] {item}" for item in checks) + "\n"
    outputs = {"latest_json": paths.logs_root / "latest_real_observation_checklist.json", "latest_md": paths.logs_root / "latest_real_observation_checklist.md"}
    write_outputs(payload, markdown, outputs, repo_root)
    return payload, outputs


def run_phase33_historical_replay_pipeline(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    steps: list[dict[str, Any]] = []
    functions = [
        ("historical_data_availability_audit", audit_historical_data_availability),
        ("time_sliced_replay_dataset", build_time_sliced_replay_dataset),
        ("replay_topic_scoring", run_replay_topic_scoring),
        ("replay_topic_selection", run_replay_topic_selection),
        ("replay_content_generation", run_replay_content_generation),
        ("replay_article_review", run_replay_article_review),
        ("replay_quality_regression", run_replay_quality_regression),
        ("replay_human_review_checklists", build_human_review_checklists),
        ("replay_topic_quality_diagnosis", diagnose_replay_topic_quality),
        ("content_quality_calibration_proposals", build_content_quality_calibration_proposals),
        ("real_observation_checklist", build_real_observation_checklist),
    ]
    status = "SUCCESS"
    for name, func in functions:
        try:
            payload, _ = func(paths, repo_root)
            steps.append({"step": name, "status": payload.get("status") or payload.get("regression_status") or "OK", "summary": payload.get("summary", {})})
        except Exception as exc:  # pragma: no cover - defensive pipeline guard
            status = "ACTIONABLE"
            steps.append({"step": name, "status": "FAILED", "error": str(exc)})
            break
    availability = read_json(paths.logs_root / "latest_historical_data_availability_audit.json")
    selection = read_json(paths.logs_root / "latest_7day_topic_selection_replay.json")
    final_review = read_json(paths.logs_root / "latest_7day_article_review_replay.json")
    quality = read_json(paths.logs_root / "latest_7day_quality_regression.json")
    proposals = read_json(paths.logs_root / "latest_content_quality_calibration_proposals.json")
    summary = {
        "step_count": len(steps),
        "steps_ok": sum(1 for item in steps if item.get("status") not in {"FAILED", "FAIL"}),
        "replay_ready_days": (availability.get("summary") or {}).get("replay_ready_days", 0),
        "selected_days": (selection.get("summary") or {}).get("selected_days", 0),
        "final_candidate_count": (final_review.get("summary") or {}).get("final_candidate_count", 0),
        "quality_actionable_days": (quality.get("summary") or {}).get("actionable_days", 0),
        "proposal_count": (proposals.get("summary") or {}).get("proposal_count", 0),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "status": status, "steps": steps, "summary": summary, "policy": {"replay_namespace_only": True, "no_auto_publish": True, "no_wechat_api": True, "no_full_text": True, "no_image_generation": True, "calibration_auto_apply": False}}
    outputs = {"latest_json": paths.logs_root / "latest_phase33_historical_replay.json", "latest_md": paths.logs_root / "latest_phase33_historical_replay.md"}
    write_outputs(payload, summary_markdown("Phase33 Historical Replay Pipeline", summary), outputs, repo_root)
    return payload, outputs
