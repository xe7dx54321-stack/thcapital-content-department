"""Evidence Packet v1 builders.

P1-003 converts official lane packet items into normalized evidence packets by
rule-based extraction. It intentionally avoids LLM calls, embeddings, new
fetchers, or output-format changes in existing ingestion scripts.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.source_coverage import RUNTIME_TO_REGISTRY_ALIASES
from content_system.sources import SourceConfig, SourceRegistry

SCHEMA_VERSION = "v1"

TIER_AUTHORITY = {
    "A": 0.95,
    "B": 0.80,
    "C": 0.75,
    "D": 0.65,
    "E": 0.50,
}

KNOWN_COMPANIES = (
    "OpenAI",
    "Anthropic",
    "Google",
    "DeepMind",
    "NVIDIA",
    "Meta",
    "Microsoft",
    "Dell",
    "SAP",
    "xAI",
    "Hugging Face",
    "GitHub",
    "Apple",
    "Amazon",
    "AWS",
    "Oracle",
    "Salesforce",
    "Databricks",
    "Mistral",
    "Cohere",
    "Perplexity",
)

KNOWN_MODELS = (
    "GPT",
    "Claude",
    "Gemini",
    "Llama",
    "Nemotron",
    "Codex",
    "Vera",
    "Grok",
    "Qwen",
    "DeepSeek",
    "Mistral",
    "Phi",
    "Gemma",
)

KNOWN_FRAMEWORKS = (
    "API",
    "SDK",
    "MCP",
    "Agent SDK",
    "LangChain",
    "LlamaIndex",
    "PyTorch",
    "TensorRT",
    "CUDA",
    "Kubernetes",
)


@dataclass(frozen=True)
class EvidencePacket:
    schema_version: str
    evidence_id: str
    run_date: str
    source_id: str
    source_label: str
    source_tier: str
    source_category: str
    title: str
    url: str
    published_at: str
    captured_at: str
    summary: str
    raw_text_preview: str
    language: str
    event_type: str
    entities: dict[str, list[str]]
    domain_tags: tuple[str, ...]
    evidence_strength: str
    source_authority_score: float
    freshness_score: float
    technical_substance_score: float
    narrative_potential_score: float
    raw_item: dict[str, Any]


@dataclass(frozen=True)
class EvidencePacketReport:
    schema_version: str
    generated_at: str
    run_date: str
    source_count: int
    evidence_count: int
    evidence_packets: tuple[EvidencePacket, ...]
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


def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def safe_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    text = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def detect_language(text: str) -> str:
    if not text:
        return "unknown"
    zh_count = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    if zh_count >= 4 or zh_count / max(len(text), 1) > 0.12:
        return "zh"
    return "en"


def classify_event_type(text: str) -> str:
    lowered = text.lower()
    rules = (
        ("product_release", ("launch", "release", "announce", "introduce", "unveil", "发布", "推出", "上线")),
        ("research", ("paper", "arxiv", "research", "study", "论文", "研究")),
        ("benchmark", ("benchmark", "eval", "leaderboard", "排行", "测评", "评测")),
        ("model_release", ("model", "weights", "checkpoint", "模型", "权重")),
        ("tooling", ("agent", "workflow", "tool", "sdk", "api", "developer", "agents", "工具", "智能体")),
        ("partnership", ("partner", "collaboration", "alliance", "合作", "伙伴")),
        ("policy", ("policy", "regulation", "safety", "governance", "政策", "监管", "安全")),
        ("funding", ("funding", "raise", "series ", "融资")),
    )
    for event_type, keywords in rules:
        if any(keyword in lowered or keyword in text for keyword in keywords):
            return event_type
    return "unknown"


def unique_matches(text: str, candidates: tuple[str, ...]) -> list[str]:
    found: list[str] = []
    lowered = text.lower()
    for candidate in candidates:
        if candidate.lower() in lowered and candidate not in found:
            found.append(candidate)
    return found


def extract_entities(text: str) -> dict[str, list[str]]:
    products = unique_matches(text, ("Codex", "ChatGPT", "OpenAI API", "Claude Code", "Gemini", "Nemotron", "Vera", "SAP Sapphire"))
    return {
        "companies": unique_matches(text, KNOWN_COMPANIES),
        "products": products,
        "models": unique_matches(text, KNOWN_MODELS),
        "people": unique_matches(text, ("Sam Altman", "Dario Amodei", "Jensen Huang", "Demis Hassabis", "Sundar Pichai")),
        "frameworks": unique_matches(text, KNOWN_FRAMEWORKS),
    }


def domain_tags(text: str, event_type: str) -> tuple[str, ...]:
    lowered = text.lower()
    tags: list[str] = []
    rules = (
        ("agents", ("agent", "agents", "workflow", "智能体")),
        ("models", ("model", "gpt", "claude", "gemini", "llama", "模型")),
        ("infrastructure", ("gpu", "cpu", "inference", "server", "data center", "算力", "推理")),
        ("developer_tools", ("api", "sdk", "codex", "developer", "github", "工具")),
        ("voice", ("voice", "speech", "audio", "transcribe", "语音")),
        ("multimodal", ("vision", "image", "video", "multimodal", "多模态")),
        ("enterprise", ("enterprise", "customer", "business", "企业")),
        ("research", ("research", "paper", "benchmark", "论文")),
        ("safety", ("safety", "policy", "governance", "安全")),
    )
    for tag, keywords in rules:
        if any(keyword in lowered for keyword in keywords):
            tags.append(tag)
    if event_type != "unknown":
        tags.append(event_type)
    return tuple(dict.fromkeys(tags))


def source_for_runtime_id(registry: SourceRegistry, runtime_source_id: str) -> SourceConfig | None:
    return registry.get(runtime_source_id) or registry.get(RUNTIME_TO_REGISTRY_ALIASES.get(runtime_source_id, ""))


def evidence_strength(tier: str, url: str) -> str:
    if tier == "A" and url:
        return "HIGH"
    if tier in {"B", "C"} and url:
        return "MEDIUM"
    return "LOW"


def score_technical(text: str, tags: tuple[str, ...]) -> float:
    lowered = text.lower()
    score = 35.0
    for keyword in ("api", "sdk", "model", "benchmark", "research", "architecture", "inference", "agent", "weights"):
        if keyword in lowered:
            score += 8.0
    if "research" in tags or "infrastructure" in tags:
        score += 8.0
    return min(score, 100.0)


def score_narrative(text: str, tags: tuple[str, ...], event_type: str) -> float:
    score = 35.0
    if event_type in {"product_release", "model_release", "partnership"}:
        score += 20.0
    if "agents" in tags or "enterprise" in tags:
        score += 15.0
    if any(word in text.lower() for word in ("first", "new", "launch", "unveil", "agent", "customer", "enterprise")):
        score += 10.0
    return min(score, 100.0)


def make_evidence_id(run_date: str, source_id: str, title: str, url: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{source_id}|{title}|{url}".encode("utf-8")).hexdigest()[:12]
    safe_source = re.sub(r"[^a-z0-9_]+", "_", source_id.lower()).strip("_") or "source"
    return f"ev_{run_date}_{safe_source}_{digest}"


def packet_path_for_run(paths: ProjectPaths, run_date: str) -> Path:
    return (
        paths.market_content_root
        / "02_topic_radar"
        / "source_packets"
        / f"{run_date}__official_lane"
        / f"{run_date}__packets.json"
    )


def resolve_packet_path(paths: ProjectPaths, run_date: str) -> Path | None:
    direct = packet_path_for_run(paths, run_date)
    if direct.exists():
        return direct
    candidates = sorted(
        (paths.market_content_root / "02_topic_radar" / "source_packets").glob("*official_lane*/*__packets.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_official_packets(paths: ProjectPaths, run_date: str) -> tuple[list[dict[str, Any]], Path | None]:
    packet_path = resolve_packet_path(paths, run_date)
    if packet_path is None:
        return [], None
    payload = read_json(packet_path)
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)], packet_path
    return [], packet_path


def build_evidence_packet(
    *,
    run_date: str,
    source_packet: dict[str, Any],
    raw_item: dict[str, Any],
    registry: SourceRegistry,
) -> EvidencePacket:
    runtime_source_id = str(raw_item.get("_source") or source_packet.get("source_id") or "unknown_source")
    source = source_for_runtime_id(registry, runtime_source_id)
    source_label = str(raw_item.get("label") or source_packet.get("label") or (source.label if source else runtime_source_id))
    source_tier = source.tier if source else "B"
    source_category = source.category if source else "official"

    title = safe_text(raw_item.get("title_text") or raw_item.get("title") or raw_item.get("entity_name") or "")
    url = safe_text(raw_item.get("source_url") or raw_item.get("url") or raw_item.get("link") or "")
    summary = safe_text(raw_item.get("body_snippet") or raw_item.get("summary") or raw_item.get("snippet") or "")
    captured_at = safe_text(raw_item.get("captured_at") or source_packet.get("captured_at") or "")
    published_at = safe_text(raw_item.get("published_at") or raw_item.get("published") or raw_item.get("date") or "")
    combined_text = " ".join(part for part in (title, summary) if part)
    event_type = classify_event_type(combined_text)
    tags = domain_tags(combined_text, event_type)
    entities = extract_entities(combined_text)

    return EvidencePacket(
        schema_version=SCHEMA_VERSION,
        evidence_id=make_evidence_id(run_date, runtime_source_id, title, url),
        run_date=run_date,
        source_id=runtime_source_id,
        source_label=source_label,
        source_tier=source_tier,
        source_category=source_category,
        title=title or "(untitled)",
        url=url,
        published_at=published_at,
        captured_at=captured_at,
        summary=summary,
        raw_text_preview=combined_text[:500],
        language=detect_language(combined_text),
        event_type=event_type,
        entities=entities,
        domain_tags=tags,
        evidence_strength=evidence_strength(source_tier, url),
        source_authority_score=TIER_AUTHORITY.get(source_tier, 0.60),
        freshness_score=90.0 if captured_at or published_at else 60.0,
        technical_substance_score=score_technical(combined_text, tags),
        narrative_potential_score=score_narrative(combined_text, tags, event_type),
        raw_item=raw_item,
    )


def build_evidence_packet_report(
    registry: SourceRegistry,
    paths: ProjectPaths,
    run_date: str | None = None,
) -> EvidencePacketReport:
    manifest = read_json(paths.logs_root / "latest_official_runtime_manifest.json") or {}
    final_run_date = normalize_date(run_date or manifest.get("run_date"))
    source_packets, packet_path = load_official_packets(paths, final_run_date)
    warnings: list[str] = []
    if packet_path is None:
        warnings.append("No official lane source packet JSON found.")
    elif not source_packets:
        warnings.append(f"Official lane packet file has no source packet records: {packet_path.name}")

    evidence: list[EvidencePacket] = []
    for source_packet in source_packets:
        entries = source_packet.get("entries")
        if not isinstance(entries, list):
            continue
        for raw_item in entries:
            if isinstance(raw_item, dict):
                evidence.append(
                    build_evidence_packet(
                        run_date=final_run_date,
                        source_packet=source_packet,
                        raw_item=raw_item,
                        registry=registry,
                    )
                )

    return EvidencePacketReport(
        schema_version=SCHEMA_VERSION,
        generated_at=utc_now(),
        run_date=final_run_date,
        source_count=len(source_packets),
        evidence_count=len(evidence),
        evidence_packets=tuple(evidence),
        warnings=tuple(warnings),
    )


def report_to_dict(report: EvidencePacketReport) -> dict[str, Any]:
    return asdict(report)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: EvidencePacketReport, max_items: int = 80) -> str:
    rows = []
    for index, packet in enumerate(report.evidence_packets[:max_items], start=1):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    escape_cell(packet.source_id),
                    escape_cell(packet.event_type),
                    escape_cell(packet.evidence_strength),
                    escape_cell(packet.title),
                    escape_cell(packet.url),
                ]
            )
            + " |"
        )
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    return f"""# Evidence Packets v1

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Source packets: `{report.source_count}`
- Evidence packets: `{report.evidence_count}`

## Evidence

| # | Source | Event Type | Strength | Title | URL |
|---:|---|---|---|---|---|
{chr(10).join(rows) if rows else '| 0 | - | - | - | None | - |'}

## Warnings

{warnings}

## Notes

- Evidence Packet v1 uses deterministic rules only; no LLM, embeddings, or article generation.
- JSON output preserves the raw item for later traceability.
"""


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "03_topic_candidates"
    return {
        "dated_json": root / f"{run_date}__evidence-packets.json",
        "dated_md": root / f"{run_date}__evidence-packets.md",
        "latest_json": root / "latest_evidence_packets.json",
        "latest_md": root / "latest_evidence_packets.md",
    }


def write_evidence_packet_report(report: EvidencePacketReport, paths: ProjectPaths) -> dict[str, Path]:
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
