#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from market_platform_task_sheet_to_approved import parse_task_sheet
from market_top5_board_utils import top5_board_is_ready

KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
SCORE_RE = re.compile(r"(?<!\d)(\d+(?:\.\d+)?)\s*/\s*10")
TABLE_LINE_RE = re.compile(r"^\|(.+)\|$")
STAGE_FILE_RE = re.compile(
    r"^(?P<token>\d{8})__(?P<stage>top20|platform-task-sheet)__(?P<suffix>redteam-review|stage-gate-scorecard)\.md$"
)
TOP20_HEADING_RE = re.compile(r"^###\s+\d+\.\s+", re.MULTILINE)
TOP20_TOPIC_KEY_RE = re.compile(r"^- `topic_key`:\s*`?([^`\n]+?)`?\s*$", re.MULTILINE)
TOP20_BLANK_TOTAL_RE = re.compile(r"^- `total_candidates_seen`:\s*$", re.MULTILINE)

ACCEPT_LEVELS = {
    "missing": 0,
    "placeholder": 1,
    "materialized": 2,
    "final": 3,
}

STATUS_PLACEHOLDER_VALUES = {
    "pass / rework",
    "yes / no",
    "高 / 中 / 低",
    "接近通过 / 可补强 / 暂不可发",
    "supplement_evidence / expand_validation / rewrite_angle / rewrite_quality / replace_topic",
}
CONTINUITY_DECISION_PLACEHOLDERS = {
    "premium_only / continuity_only / stop_for_truth",
    "pending",
}
CONTINUITY_OUTPUT_PLACEHOLDERS = {
    "none / top20_mini_slate / limited_task_sheet / backlog_publish / carry_rework_backlog",
    "pending",
}

STAGE_ALIASES = {
    "top20": ["top20_pack", "top20_redteam", "top20_score"],
    "platform-task-sheet": ["platform_task", "platform_task_sheet", "platform_redteam", "platform_score"],
}
PATH_ALIAS_REPLACEMENTS = (
    ("__top20_pack__", "__top20__"),
    ("__top20_redteam__", "__top20__"),
    ("__top20_score__", "__top20__"),
    ("__platform_task__", "__platform-task-sheet__"),
    ("__platform_task_sheet__", "__platform-task-sheet__"),
    ("__platform_redteam__", "__platform-task-sheet__"),
    ("__platform_score__", "__platform-task-sheet__"),
)
PACK_TEMPLATE_MARKERS = (
    "<human_readable_title>",
    "重复到 20 条。",
)
PACK_VALID_SECTION_MARKERS = (
    "## 返工说明",
    "## Top20",
    "## HB2",
    "## 返工动作记录",
    "## 返工结论",
    "## 执行摘要",
)
TOP5_REQUIRED_HEADERS = (
    "## Top 5 Recommended",
    "## Holdout 3",
)
PLATFORM_TASK_REQUIRED_HEADERS = (
    "## 全局主池 Top6",
    "## 六个主战场任务单",
    "## 三个最重要平台任务单",
)


def clean(value: str, fallback: str = "") -> str:
    cleaned = re.sub(r"\s+", " ", value or "").strip()
    for marker in ("`", "*", "_"):
        cleaned = cleaned.strip(marker)
    cleaned = cleaned.strip()
    return cleaned or fallback


def canonical_stage_from_path(path: Path) -> str:
    match = STAGE_FILE_RE.match(path.name)
    return match.group("stage") if match else ""


def artifact_alias_paths(path: Path) -> list[Path]:
    match = STAGE_FILE_RE.match(path.name)
    if not match:
        return [path]
    token = match.group("token")
    stage = match.group("stage")
    suffix = match.group("suffix")
    paths = [path]
    for alias in STAGE_ALIASES.get(stage, []):
        alias_path = path.with_name(f"{token}__{alias}__{suffix}.md")
        if alias_path not in paths:
            paths.append(alias_path)
    return paths


def normalize_alias_text(text: str, canonical_path: Path) -> str:
    normalized = text
    for source, target in PATH_ALIAS_REPLACEMENTS:
        normalized = normalized.replace(source, target)
    expected_stage = canonical_stage_from_path(canonical_path)
    if expected_stage:
        normalized = re.sub(
            r"^(- `stage`:)\s*`?.*?`?\s*$",
            rf"\1 `{expected_stage}`",
            normalized,
            flags=re.MULTILINE,
        )
    return normalized


def artifact_mtime(path: Path) -> float:
    return path.stat().st_mtime if path.exists() else 0.0


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        match = KV_RE.match(stripped)
        if not match:
            table_match = TABLE_LINE_RE.match(stripped)
            if not table_match:
                continue
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if len(cells) < 2:
                continue
            key = clean(cells[0])
            value = clean(cells[1])
            if not key or key in {"字段", "值", "项目", "说明", "维度", "评估", "问题项", "类型", "严重度", "后果"}:
                continue
            if set(key) == {"-"}:
                continue
            fields[key] = value
            continue
        key, value = match.groups()
        fields[key] = clean(value)
    return fields


def score_value(text: str, fields: dict[str, str]) -> str:
    score = clean(fields.get("score", ""))
    if score:
        return score
    match = SCORE_RE.search(text)
    return match.group(1) if match else ""


def normalize_continuity_decision(raw: str) -> str:
    lowered = clean(raw, "").lower()
    if not lowered or lowered in CONTINUITY_DECISION_PLACEHOLDERS:
        return ""
    # Only treat the leading decision token as canonical so explanatory notes
    # like "continuity_only（非 truth failure）" do not get misread as truth_stop.
    head = clean(re.split(r"[（(]", lowered, maxsplit=1)[0], "")
    if "premium_only" in head or "premium pass" in head or head == "premium":
        return "premium_only"
    if (
        "continuity_only" in head
        or "pending_replace_topic" in head
        or "replace_topic" in head
        or "mini_slate" in head
        or "limited_task_sheet" in head
        or "carry_rework_backlog" in head
    ):
        return "continuity_only"
    if (
        "stop_for_truth" in head
        or "truth_stop" in head
        or "truth_failure" in head
        or "fatal" in head
        or head in {"事实失真", "方向严重偏离"}
        or "事实失真" in lowered
        or "方向严重偏离" in lowered
    ):
        return "stop_for_truth"
    return lowered


def normalize_continuity_output(raw: str) -> str:
    lowered = clean(raw, "").lower()
    if not lowered or lowered in CONTINUITY_OUTPUT_PLACEHOLDERS:
        return ""
    if "top20_mini_slate" in lowered or "mini slate" in lowered:
        return "top20_mini_slate"
    if "limited_task_sheet" in lowered or "limited task sheet" in lowered:
        return "limited_task_sheet"
    if "backlog_publish" in lowered or "publish continuity backlog" in lowered:
        return "backlog_publish"
    if "carry_rework_backlog" in lowered or "等待" in lowered or "replace_topic" in lowered:
        return "carry_rework_backlog"
    if lowered == "none":
        return "none"
    return lowered


def normalize_scorecard_status(
    raw_status: str,
    score: str,
    next_step: str,
    continuity_decision: str,
) -> str:
    lowered_status = clean(raw_status, "").lower()
    lowered_next = clean(next_step, "").lower()
    normalized_continuity = normalize_continuity_decision(continuity_decision)

    noop_tokens = ("no_op", "no-op", "waiting_on_", "缺前置", "占位")
    truth_tokens = ("stop_for_truth", "truth_stop", "truth_failure", "事实失真", "方向严重偏离")
    pass_tokens = ("pass", "approved", "approve", "通过", "放行", "premium_pass", "freeze_pass", "frozen_pass")
    rework_tokens = (
        "rework",
        "reject",
        "rejected",
        "打回",
        "未通过",
        "gate_open_with_rework",
        "pending_replace_topic",
    )

    if any(token in lowered_status for token in noop_tokens):
        return "no_op"
    if any(token in lowered_status for token in truth_tokens):
        return "truth_stop"
    if any(token in lowered_status for token in pass_tokens):
        return "pass"
    if any(token in lowered_status for token in rework_tokens):
        return "rework"

    if normalized_continuity == "stop_for_truth":
        return "truth_stop"
    if normalized_continuity == "premium_only":
        return "pass"
    if normalized_continuity == "continuity_only":
        return "rework"

    if lowered_next:
        negative_tokens = ("否", "no", "blocked", "阻塞", "打回", "不可", "不允许", "rework", "等待")
        positive_tokens = ("是", "yes", "allow", "允许", "可进入", "进入", "approved", "pass")
        if any(token in lowered_next for token in negative_tokens):
            return "rework"
        if any(token in lowered_next for token in positive_tokens):
            return "pass"

    lowered_score = clean(score, "").lower()
    if lowered_score and lowered_score not in {"待 redteam-review 就绪后复评", "待复评", "pending"}:
        return "rework"
    return "unknown"


def is_blank_or_placeholder(value: str, placeholders: set[str]) -> bool:
    cleaned = clean(value).lower()
    return not cleaned or cleaned in placeholders


def inspect_scorecard(path: Path, text: str, fields: dict[str, str]) -> dict[str, Any]:
    reasons: list[str] = []
    for key in ("date", "stage", "delivery_pack", "redteam_review", "generated_at"):
        if not clean(fields.get(key, "")):
            reasons.append(f"missing:{key}")
    status = clean(fields.get("status", ""))
    score = score_value(text, fields)
    next_step = clean(fields.get("是否进入下一工序", ""))
    rework_mode = clean(fields.get("rework_mode", ""))
    continuity_decision = clean(fields.get("continuity_decision", ""))
    continuity_output = clean(fields.get("continuity_output", ""))
    normalized_status = normalize_scorecard_status(status, score, next_step, continuity_decision)
    normalized_continuity_decision = normalize_continuity_decision(continuity_decision)
    normalized_continuity_output = normalize_continuity_output(continuity_output)
    if "TBD" in text or "pending market-editor approval" in text:
        reasons.append("contains_pending_placeholder")
    if is_blank_or_placeholder(status, STATUS_PLACEHOLDER_VALUES):
        reasons.append("placeholder_status")
    if normalized_status != "no_op" and (not score or "TBD" in score.upper()):
        reasons.append("missing_score")
    if normalized_status != "no_op" and is_blank_or_placeholder(next_step, STATUS_PLACEHOLDER_VALUES):
        reasons.append("missing_next_step")
    if normalized_status == "rework" and is_blank_or_placeholder(rework_mode, STATUS_PLACEHOLDER_VALUES):
        reasons.append("missing_rework_mode")
    if continuity_decision and not normalized_continuity_decision:
        reasons.append("placeholder_continuity_decision")
    if continuity_output and not normalized_continuity_output:
        reasons.append("placeholder_continuity_output")

    if reasons:
        state = "placeholder" if any(item.startswith("missing:") or "placeholder" in item for item in reasons) else "materialized"
    else:
        if normalized_status in {"pass", "rework", "truth_stop"}:
            state = "final"
        elif normalized_status == "no_op":
            state = "materialized"
        else:
            state = "materialized"
    return {
        "path": str(path),
        "kind": "scorecard",
        "state": state,
        "status": status,
        "normalized_status": normalized_status,
        "score": score,
        "continuity_decision": normalized_continuity_decision or continuity_decision,
        "continuity_output": normalized_continuity_output or continuity_output,
        "reasons": reasons,
    }


def inspect_redteam(path: Path, text: str, fields: dict[str, str]) -> dict[str, Any]:
    reasons: list[str] = []
    placeholder_values = {
        "yes / no",
        "repairable / fatal / mixed",
        "repairable / fatal",
        "keep_and_fix / keep_but_deprioritize / replace_only_if_false",
        "supplement_evidence / expand_validation / rewrite_angle / rewrite_quality / replace_topic",
        "no / yes",
    }
    for key in ("date", "stage", "review_target", "generated_at"):
        if not clean(fields.get(key, "")):
            reasons.append(f"missing:{key}")
    for key in ("结论", "是否建议放行", "最危险问题", "默认补救路径"):
        if is_blank_or_placeholder(fields.get(key, ""), placeholder_values):
            reasons.append(f"missing:{key}")
    if is_blank_or_placeholder(fields.get("minimum_verification_done", ""), placeholder_values):
        reasons.append("missing:minimum_verification_done")
    if "## 总评" not in text:
        reasons.append("missing_summary_section")
    state = "placeholder" if reasons else "final"
    return {
        "path": str(path),
        "kind": "redteam",
        "state": state,
        "status": clean(fields.get("是否建议放行", "")),
        "score": "",
        "reasons": reasons,
    }


def inspect_pack(path: Path, text: str, fields: dict[str, str]) -> dict[str, Any]:
    reasons: list[str] = []
    if len(text.strip()) < 400:
        reasons.append("too_short")
    if not any(marker in text for marker in PACK_VALID_SECTION_MARKERS):
        reasons.append("missing_core_sections")
    if not clean(fields.get("date", "")):
        reasons.append("missing:date")
    for marker in PACK_TEMPLATE_MARKERS:
        if marker in text:
            reasons.append(f"template_marker:{marker}")
    if TOP20_BLANK_TOTAL_RE.search(text):
        reasons.append("missing_total_candidates_seen")
    if "## Top20 候选" in text:
        heading_count = len(TOP20_HEADING_RE.findall(text))
        topic_keys = [
            clean(match.group(1), "")
            for match in TOP20_TOPIC_KEY_RE.finditer(text)
            if clean(match.group(1), "")
        ]
        if heading_count <= 1:
            reasons.append("insufficient_candidate_headings")
        if not topic_keys:
            reasons.append("zero_materialized_candidates")
    state = "placeholder" if reasons else "final"
    return {
        "path": str(path),
        "kind": "pack",
        "state": state,
        "status": clean(fields.get("revision", "")),
        "score": "",
        "reasons": reasons,
    }


def inspect_top5_board(path: Path, text: str, fields: dict[str, str]) -> dict[str, Any]:
    reasons: list[str] = []
    if len(text.strip()) < 300:
        reasons.append("too_short")
    for header in TOP5_REQUIRED_HEADERS:
        if header not in text:
            reasons.append(f"missing_section:{header}")
    if not top5_board_is_ready(path):
        reasons.append("zero_materialized_candidates")
    state = "placeholder" if reasons else "final"
    return {
        "path": str(path),
        "kind": "top5_board",
        "state": state,
        "status": clean(fields.get("board_status", "")),
        "score": "",
        "reasons": reasons,
    }


def inspect_platform_task_sheet(path: Path, text: str, fields: dict[str, str]) -> dict[str, Any]:
    reasons: list[str] = []
    if len(text.strip()) < 400:
        reasons.append("too_short")
    for header in PLATFORM_TASK_REQUIRED_HEADERS:
        if header not in text:
            reasons.append(f"missing_section:{header}")
    try:
        sheet = parse_task_sheet(path)
    except Exception as exc:  # pragma: no cover - defensive guard for malformed runtime files.
        reasons.append(f"parse_failed:{exc.__class__.__name__}")
        sheet = None
    if sheet is None or not sheet.top6:
        reasons.append("top6_missing")
    if sheet is None or not sheet.tasks_by_topic:
        reasons.append("zero_active_tasks")
    state = "placeholder" if reasons else "final"
    return {
        "path": str(path),
        "kind": "platform_task_sheet",
        "state": state,
        "status": clean(fields.get("stage_gate_status", "")),
        "score": "",
        "reasons": reasons,
    }


def inspect_artifact(path: Path, kind: str) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(path),
            "kind": kind,
            "state": "missing",
            "status": "",
            "score": "",
            "reasons": ["missing:file"],
        }
    text = path.read_text(encoding="utf-8")
    fields = parse_fields(text)
    if kind == "scorecard":
        return inspect_scorecard(path, text, fields)
    if kind == "redteam":
        return inspect_redteam(path, text, fields)
    if kind == "pack":
        return inspect_pack(path, text, fields)
    if kind == "top5_board":
        return inspect_top5_board(path, text, fields)
    if kind == "platform_task_sheet":
        return inspect_platform_task_sheet(path, text, fields)
    raise ValueError(f"unsupported kind: {kind}")


def inspect_artifact_family(path: Path, kind: str) -> list[dict[str, Any]]:
    inspections: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate in artifact_alias_paths(path):
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        result = inspect_artifact(candidate, kind)
        result["canonical_path"] = str(path)
        result["is_canonical"] = candidate == path
        result["mtime"] = artifact_mtime(candidate)
        inspections.append(result)
    return inspections


def best_artifact_in_family(path: Path, kind: str) -> dict[str, Any]:
    inspections = inspect_artifact_family(path, kind)
    inspections.sort(
        key=lambda item: (
            ACCEPT_LEVELS[item["state"]],
            item["mtime"],
            1 if item["is_canonical"] else 0,
        ),
        reverse=True,
    )
    return inspections[0]


def promote_best_artifact_to_canonical(path: Path, kind: str) -> dict[str, Any]:
    canonical = path.expanduser()
    current = inspect_artifact(canonical, kind)
    best = best_artifact_in_family(canonical, kind)
    result: dict[str, Any] = {
        "canonical_path": str(canonical),
        "kind": kind,
        "promoted": False,
        "source_path": best["path"],
        "source_state": best["state"],
    }
    if best["path"] == str(canonical):
        result["reason"] = "canonical_already_best"
        return result
    if ACCEPT_LEVELS[best["state"]] < ACCEPT_LEVELS["materialized"]:
        result["reason"] = "best_alias_not_materialized"
        return result
    canonical_mtime = artifact_mtime(canonical)
    if ACCEPT_LEVELS[current["state"]] > ACCEPT_LEVELS[best["state"]]:
        result["reason"] = "canonical_state_stronger"
        return result
    if (
        ACCEPT_LEVELS[current["state"]] == ACCEPT_LEVELS[best["state"]]
        and canonical_mtime >= best["mtime"]
    ):
        result["reason"] = "canonical_same_state_newer"
        return result
    source_path = Path(best["path"])
    normalized_text = normalize_alias_text(source_path.read_text(encoding="utf-8"), canonical)
    canonical.parent.mkdir(parents=True, exist_ok=True)
    canonical.write_text(normalized_text, encoding="utf-8")
    result["promoted"] = True
    result["reason"] = "alias_promoted_to_canonical"
    result["canonical_state_after"] = inspect_artifact(canonical, kind)["state"]
    return result


def state_satisfies(current: str, wanted: str) -> bool:
    return ACCEPT_LEVELS[current] >= ACCEPT_LEVELS[wanted]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect whether a stage artifact is still a bootstrap placeholder or is materially complete.")
    parser.add_argument("--path", required=True, help="Artifact path.")
    parser.add_argument("--kind", required=True, choices=["pack", "redteam", "scorecard", "top5_board", "platform_task_sheet"])
    parser.add_argument("--accept-state", choices=["missing", "placeholder", "materialized", "final"], default="final")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = inspect_artifact(Path(args.path).expanduser(), args.kind)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if state_satisfies(result["state"], args.accept_state) else 1


if __name__ == "__main__":
    raise SystemExit(main())
