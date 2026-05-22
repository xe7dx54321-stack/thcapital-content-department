#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


_REPO_ROOT = None
for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "content_system" / "paths.py").exists():
        _REPO_ROOT = _parent
        sys.path.insert(0, str(_parent / "src"))
        break
if _REPO_ROOT is None:
    raise RuntimeError("Cannot locate repository root")
from content_system.paths import get_project_paths

ROOT = get_project_paths(_REPO_ROOT).legacy_content_root
LOG_DIR = ROOT / "10_logs"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
SCORE_RE = re.compile(r"(?<!\d)(\d+(?:\.\d+)?)\s*/\s*10")
PLATFORM_ALIASES = {
    "wechat": "wechat",
    "weixin": "wechat",
    "微信公众号": "wechat",
    "公众号": "wechat",
    "微信": "wechat",
    "xiaohongshu": "xiaohongshu",
    "小红书": "xiaohongshu",
    "zhihu": "zhihu",
    "知乎": "zhihu",
    "x": "x",
    "twitter": "x",
    "thread": "x",
    "threads": "x",
    "bilibili": "bilibili",
    "b站": "bilibili",
    "b站专栏": "bilibili",
    "toutiao": "toutiao",
    "今日头条": "toutiao",
    "头条": "toutiao",
    "baijiahao": "baijiahao",
    "百家号": "baijiahao",
}
PLATFORM_READY_POSITIVE_TOKENS = (
    "publish-ready",
    "publish ready",
    "已达 publish-ready",
    "已达 publish ready",
    "已达放行",
    "可直接入公众号草稿箱",
    "可直接入草稿箱",
    "可直接发布",
    "可先行",
    "可进入 publish-ops",
    "可进入 publish queue",
    "可发",
)
PLATFORM_READY_NEGATIVE_TOKENS = (
    "rework",
    "返工",
    "待补",
    "待修",
    "不可发",
    "暂不可发",
    "未达",
    "阻断",
    "整改",
    "缺",
    "不足",
)


@dataclass(frozen=True)
class ContentPackVerdict:
    topic_key: str
    path: Path
    generated_at: str
    score_text: str
    score_value: float | None
    raw_status: str
    normalized_status: str
    next_step_allowed: bool | None
    continuity_decision: str
    continuity_output: str
    publish_ready_platforms: tuple[str, ...]
    platform_scores: tuple[tuple[str, float], ...]

    @property
    def requires_rework(self) -> bool:
        return self.normalized_status == "rework"

    @property
    def allows_publish_queue(self) -> bool:
        if self.normalized_status != "pass":
            return False
        if self.score_value is not None and self.score_value < 8:
            return False
        if self.next_step_allowed is False:
            return False
        return True

    @property
    def score_gap_to_premium(self) -> float | None:
        if self.score_value is None:
            return None
        return round(max(0.0, 8.0 - self.score_value), 2)

    @property
    def continuity_lane(self) -> str:
        if self.allows_publish_queue:
            return "premium_pass"
        if self.publish_ready_platforms:
            return "platform_partial_publishable"
        if self.normalized_status == "pass":
            return "blocked_pass"
        if self.requires_rework:
            if self.score_value is None:
                return "rework_unscored"
            if self.score_value >= 7.5:
                return "near_pass_rework"
            if self.score_value >= 6.0:
                return "salvage_rework"
            return "deep_rework"
        if self.normalized_status == "unknown":
            return "awaiting_review"
        return "unknown"

    @property
    def revision_priority_boost(self) -> int:
        if self.allows_publish_queue:
            return 0
        if self.publish_ready_platforms:
            return 60
        if self.score_value is None:
            return 35 if self.normalized_status == "unknown" else 15
        gap = max(0.0, 8.0 - self.score_value)
        if gap <= 0.5:
            return 140
        if gap <= 1.0:
            return 120
        if gap <= 1.5:
            return 95
        if gap <= 2.0:
            return 70
        if gap <= 3.0:
            return 40
        return 15

    @property
    def platform_scores_map(self) -> dict[str, float]:
        return dict(self.platform_scores)

    def platform_score(self, platform: str) -> float | None:
        return self.platform_scores_map.get(normalize_platform_label(platform))

    def allows_publish_queue_for(self, platform: str) -> bool:
        normalized = normalize_platform_label(platform)
        if not normalized:
            return False
        if self.allows_publish_queue:
            return True
        return normalized in self.publish_ready_platforms


def clean(value: str, fallback: str = "") -> str:
    cleaned = re.sub(r"\s+", " ", value or "").strip()
    for marker in ("`", "*", "_"):
        cleaned = cleaned.strip(marker)
    cleaned = cleaned.strip()
    return cleaned or fallback


def parse_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def parse_score_text(fields: dict[str, str], text: str) -> str:
    score = clean(fields.get("score", ""))
    if score:
        return score
    match = SCORE_RE.search(text)
    return match.group(1) if match else ""


def parse_score_value(score_text: str) -> float | None:
    match = SCORE_RE.search(score_text)
    if match:
        return float(match.group(1))
    cleaned = clean(score_text)
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_generated_at(raw: str, fallback_path: Path) -> datetime:
    value = clean(raw)
    for fmt in ("%Y-%m-%d %H:%M:%S CST", "%Y-%m-%d %H:%M CST", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return datetime.fromtimestamp(fallback_path.stat().st_mtime, tz=CN_TZ)


def normalize_platform_label(raw: str) -> str:
    value = clean(raw, "")
    if not value:
        return ""
    lowered = value.lower()
    lowered = lowered.replace("`", "").strip()
    if lowered in PLATFORM_ALIASES:
        return PLATFORM_ALIASES[lowered]
    if "wechat" in lowered or "微信" in value or "公众号" in value:
        return "wechat"
    if "xiaohongshu" in lowered or "小红书" in value:
        return "xiaohongshu"
    if "zhihu" in lowered or "知乎" in value:
        return "zhihu"
    if lowered == "x" or "thread" in lowered or "twitter" in lowered:
        return "x"
    if "bilibili" in lowered or "b站" in value:
        return "bilibili"
    if "toutiao" in lowered or "头条" in value:
        return "toutiao"
    if "baijiahao" in lowered or "百家号" in value:
        return "baijiahao"
    return ""


def parse_platform_list(raw: str) -> tuple[str, ...]:
    value = clean(raw, "")
    if not value:
        return ()
    normalized: list[str] = []
    for chunk in re.split(r"[,/|，、\s]+", value):
        platform = normalize_platform_label(chunk)
        if platform and platform not in normalized:
            normalized.append(platform)
    return tuple(sorted(normalized))


def platform_row_is_publish_ready(score_value: float | None, readiness_text: str) -> bool:
    lowered = clean(readiness_text, "").lower()
    if any(token in lowered for token in PLATFORM_READY_POSITIVE_TOKENS):
        return True
    if any(token in lowered for token in PLATFORM_READY_NEGATIVE_TOKENS):
        return False
    return score_value is not None and score_value >= 8.0


def parse_platform_breakdown(text: str) -> tuple[tuple[str, ...], tuple[tuple[str, float], ...]]:
    scores: dict[str, float] = {}
    publish_ready: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or line.count("|") < 3:
            continue
        cells = [clean(cell, "") for cell in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        platform = normalize_platform_label(cells[0])
        if not platform:
            continue
        row_score: float | None = None
        for cell in cells[1:]:
            parsed = parse_score_value(cell)
            if parsed is not None:
                row_score = parsed
                break
        if row_score is not None:
            scores[platform] = row_score
        readiness_text = " ".join(cells[2:]) if len(cells) > 2 else ""
        if platform_row_is_publish_ready(row_score, readiness_text):
            publish_ready.add(platform)
    ordered_scores = tuple(sorted(scores.items(), key=lambda item: item[0]))
    ordered_ready = tuple(sorted(publish_ready))
    return ordered_ready, ordered_scores


def parse_explicit_publish_ready_platforms(fields: dict[str, str]) -> tuple[str, ...]:
    return parse_platform_list(fields.get("publish_ready_platforms", ""))


def infer_next_step_allowed(raw: str) -> bool | None:
    value = clean(raw)
    if not value:
        return None
    lowered = value.lower()
    negative_tokens = ("否", "no", "blocked", "阻塞", "打回", "不可", "不允许", "no-op", "rework")
    positive_tokens = ("是", "yes", "allow", "允许", "可进入", "进入 publish-ops", "进入待人工发布", "进入平台仿真池")
    if any(token in lowered for token in negative_tokens):
        return False
    if any(token in lowered for token in positive_tokens):
        return True
    return None


def normalize_status(raw_status: str, score_value: float | None, next_step_allowed: bool | None) -> str:
    lowered = clean(raw_status).lower()
    if lowered:
        negative_tokens = ("rework", "reject", "rejected", "打回", "阻塞", "no-op")
        positive_tokens = ("pass", "approved", "approve", "通过", "放行", "ready")
        if any(token in lowered for token in negative_tokens):
            return "rework"
        if any(token in lowered for token in positive_tokens):
            return "pass"
    if next_step_allowed is True and (score_value is None or score_value >= 8):
        return "pass"
    if next_step_allowed is False:
        return "rework"
    if score_value is not None and score_value < 8:
        return "rework"
    return "unknown"


def inspect_content_pack_scorecard(path: Path, topic_key: str) -> ContentPackVerdict:
    text = path.read_text(encoding="utf-8")
    fields = parse_fields(path)
    score_text = parse_score_text(fields, text)
    score_value = parse_score_value(score_text)
    raw_status = clean(fields.get("status", ""))
    next_step_allowed = infer_next_step_allowed(fields.get("是否进入下一工序", ""))
    normalized_status = normalize_status(raw_status, score_value, next_step_allowed)
    continuity_decision = clean(fields.get("continuity_decision", ""))
    continuity_output = clean(fields.get("continuity_output", ""))
    publish_ready_from_table, platform_scores = parse_platform_breakdown(text)
    explicit_publish_ready = parse_explicit_publish_ready_platforms(fields)
    publish_ready_platforms = tuple(
        sorted({*publish_ready_from_table, *explicit_publish_ready})
    )
    return ContentPackVerdict(
        topic_key=topic_key,
        path=path,
        generated_at=clean(fields.get("generated_at", "")),
        score_text=score_text,
        score_value=score_value,
        raw_status=raw_status,
        normalized_status=normalized_status,
        next_step_allowed=next_step_allowed,
        continuity_decision=continuity_decision,
        continuity_output=continuity_output,
        publish_ready_platforms=publish_ready_platforms,
        platform_scores=platform_scores,
    )


def latest_content_pack_verdict(topic_key: str) -> ContentPackVerdict | None:
    candidates = sorted(LOG_DIR.glob(f"*__{topic_key}__content-pack__stage-gate-scorecard.md"))
    if not candidates:
        return None
    verdicts = [inspect_content_pack_scorecard(path, topic_key) for path in candidates]
    verdicts.sort(
        key=lambda item: (
            parse_generated_at(item.generated_at, item.path),
            item.path.stat().st_mtime,
            item.path.name,
        )
    )
    return verdicts[-1]
