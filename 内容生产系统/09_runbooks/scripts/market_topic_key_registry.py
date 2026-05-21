#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


TOP20_HEADING_RE = re.compile(r"^###\s+(\d+)\.\s+(.+)$")
FIELD_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
MINISLATE_HEADER_RE = re.compile(r"^##\s+top20_mini_slate", re.I)
MINISLATE_ROW_RE = re.compile(r"^\|\s*[^|]+\|\s*`([^`]+)`\s*\|")


LEGACY_TOP20_TOPIC_KEY_OVERRIDES: dict[str, dict[int, str]] = {
    "20260327": {
        1: "cognitio-labs-food-trace-ai",
        2: "memory-stocks-turboquant-shock",
        3: "anthropic-trump-injunction",
        4: "mistral-voxtral-tts",
        5: "cursor-kimi-vs-claude-open-source",
        6: "lin-junyang-qwen-ai-road",
        7: "revela-dense-retrieval-iclr-oral",
        8: "nothing-phone-ai-app-builder",
        9: "ai-product-kol-overseas-playbook",
        10: "turboquant-llamacpp-benchmarks",
        11: "claude-code-offline-macbook",
        12: "wikipedia-ai-writing-policy",
        13: "gemini-chat-import",
        14: "skills-eat-apps",
        15: "classic-paper-false-ai-generated",
        16: "openai-adult-mode-retreat",
        17: "beipei-ai-companion-less-talk",
        18: "openai-agentic-product-discovery",
        19: "google-live-translation-ios",
        20: "gemini-flash-live-audio",
    },
    "20260328": {
        1: "softbank-openai-ipo-signal",
        2: "kunlun-agi-three-models-2026",
        3: "turboquant-qwen-macbook-air",
        4: "aibuildai-mle-bench-top",
        5: "unsloth-studio-major-update",
        6: "kv-dequant-turboquant-detail",
        7: "stadler-chatgpt-enterprise",
        8: "claude-leak-next-model",
        9: "qwen-ai-taxi-gaode-didi",
        10: "neurips-retreat-ai-governance",
        11: "openai-sora-meta-court-resistance",
        12: "vcs-betting-ai-next-wave-sora-killed",
        13: "hn-claude-folder-anatomy",
        14: "chatgpt-plus-cancellation",
        15: "claude-pro-billing-anomaly",
        16: "gan-style-claude-prompt",
        17: "sk-hynix-ipo-rammageddon",
        18: "yang-zhilin-model-roundtable",
        19: "geekpark-google-matrix-zhiyuan-robot",
        20: "newo-series-a-finsmes",
    },
}


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value or "")
    value = re.sub(r"\s+", " ", value).strip().strip("`").strip("*")
    return value if value else fallback


def parse_fields_from_lines(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in lines:
        match = FIELD_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def top20_token(path: Path) -> str:
    return path.name.split("__", 1)[0]


def legacy_top20_topic_key(token: str, rank: int) -> str:
    return LEGACY_TOP20_TOPIC_KEY_OVERRIDES.get(token, {}).get(rank, "")


def extract_top20_topic_keys(path: Path) -> tuple[set[str], bool]:
    if not path.exists():
        return set(), False

    token = top20_token(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    top_fields = parse_fields_from_lines(lines)
    keys: set[str] = set()
    explicit_found = False
    index = 0

    while index < len(lines):
        match = TOP20_HEADING_RE.match(lines[index].strip())
        if not match:
            index += 1
            continue

        rank = int(match.group(1))
        index += 1
        block: list[str] = []
        while index < len(lines) and not lines[index].startswith("### "):
            block.append(lines[index])
            index += 1

        fields = parse_fields_from_lines(block)
        topic_key = clean(fields.get("topic_key", ""), "")
        if topic_key:
            explicit_found = True
        else:
            topic_key = legacy_top20_topic_key(token, rank)
        if topic_key:
            keys.add(topic_key)

    if keys:
        return keys, explicit_found

    scorecard_path_raw = clean(top_fields.get("scorecard_path", ""), "")
    if scorecard_path_raw:
        scorecard_path = Path(scorecard_path_raw).expanduser()
        scorecard_keys = extract_top20_keys_from_scorecard(scorecard_path)
        if scorecard_keys:
            return scorecard_keys, True

    return keys, explicit_found


def extract_top20_keys_from_scorecard(path: Path) -> set[str]:
    if not path.exists():
        return set()
    lines = path.read_text(encoding="utf-8").splitlines()
    in_minislate = False
    table_started = False
    keys: set[str] = set()
    for raw_line in lines:
        line = raw_line.rstrip()
        if MINISLATE_HEADER_RE.match(line):
            in_minislate = True
            table_started = False
            continue
        if not in_minislate:
            continue
        if line.startswith("## ") and not MINISLATE_HEADER_RE.match(line):
            break
        if not line.strip():
            if table_started:
                break
            continue
        if not line.lstrip().startswith("|"):
            if table_started:
                break
            continue
        table_started = True
        match = MINISLATE_ROW_RE.match(line.strip())
        if not match:
            continue
        topic_key = clean(match.group(1), "")
        if topic_key and not topic_key.startswith("#"):
            keys.add(topic_key)
    return keys
