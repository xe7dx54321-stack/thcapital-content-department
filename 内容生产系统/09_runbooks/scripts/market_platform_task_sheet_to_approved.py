from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
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

from market_business_day import (
    BUSINESS_WINDOW_END,
    BUSINESS_WINDOW_START,
    DAY_MAINLINE_LANE,
    PUBLISH_MODE_DRAFT_ONLY,
    format_cst,
    lane_delivery_deadline,
    lane_selection_scope_default,
)
from market_topic_key_registry import extract_top20_topic_keys
from market_top5_board_utils import top5_board_is_ready, top5_candidate_keys


ROOT = get_project_paths(_REPO_ROOT).legacy_content_root
APPROVED_DIR = ROOT / "04_approved_topics"
LOG_DIR = ROOT / "10_logs"
TZ = ZoneInfo("Asia/Shanghai")
TASK_SECTION_HEADERS = {
    "## 六个主战场任务单",
    "## 三个最重要平台任务单",
}


@dataclass
class Top6Row:
    rank: str
    topic_key: str
    core_judgment: str
    why_write: str
    risk: str


@dataclass
class TaskSlot:
    platform: str
    task_no: str
    topic_key: str
    target_reader: str = "n/a"
    angle: str = "n/a"
    core_point: str = "n/a"
    evidence: str = "n/a"
    source_ref_bundle: str = "n/a"
    visual: str = "n/a"
    fit_reason: str = "n/a"


@dataclass
class TaskSheet:
    path: Path
    date_token: str
    generated_at: str
    input_pack: str
    stage_gate_status: str = "drafting"
    top6: dict[str, Top6Row] = field(default_factory=dict)
    tasks_by_topic: dict[str, list[TaskSlot]] = field(default_factory=dict)
    baijiahao_needed: str = "no"
    baijiahao_reason: str = "n/a"
    baijiahao_carry_text: str = "n/a"


MATERIALIZATION_MODES = {"auto", "premium_all", "continuity_active_only"}
DEFAULT_DELIVERY_LANE = DAY_MAINLINE_LANE
DEFAULT_PUBLISH_MODE = PUBLISH_MODE_DRAFT_ONLY
DEFAULT_SELECTION_SCOPE = lane_selection_scope_default(DEFAULT_DELIVERY_LANE)


FIELD_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
HEADING_RE = re.compile(r"^### `([^`]+)`$")
TASK_RE = re.compile(r"^#### Task (\d+)(?:\s*(?:[（(]([^）)]+)[）)]|[—-]\s*(.+)))?$")
SUBFIELD_RE = re.compile(r"^\s+- `([^`]+)`: ?(.*?)\s*$")
DATE_SUFFIX_RE = re.compile(r"_\d{8}$")


def clean(value: str) -> str:
    return value.strip().strip("`").strip()


def normalized_stage_gate_status(value: str) -> str:
    text = clean(value).lower()
    if "continuity_only" in text:
        return "continuity_only"
    if "premium_pass" in text or "premium_only" in text or text == "pass":
        return "premium_pass"
    if "draft" in text:
        return "drafting"
    return text or "drafting"


def split_refs(raw: str) -> list[str]:
    if not raw or raw == "n/a":
        return []
    parts = [clean(part) for part in raw.split("|")]
    return [part for part in parts if part]


def is_active_task_label(raw_label: str) -> bool:
    label = clean(raw_label)
    if not label:
        return True
    lowered = label.lower()
    if "holdout" in lowered or "不开启" in label or "暂不开启" in label:
        return False
    return True


def strip_date_suffix(topic_key: str) -> str:
    return DATE_SUFFIX_RE.sub("", clean(topic_key))


def resolve_parent_topic_key(topic_key: str, candidate_keys: set[str]) -> str | None:
    normalized = clean(topic_key)
    if normalized in candidate_keys:
        return normalized

    stripped = strip_date_suffix(normalized)
    if stripped in candidate_keys:
        return stripped

    prefix_matches = [key for key in candidate_keys if normalized.startswith(f"{key}_")]
    if prefix_matches:
        return max(prefix_matches, key=len)

    if stripped != normalized:
        prefix_matches = [key for key in candidate_keys if stripped.startswith(f"{key}_")]
        if prefix_matches:
            return max(prefix_matches, key=len)
    return None


def parse_task_sheet(path: Path) -> TaskSheet:
    lines = path.read_text(encoding="utf-8").splitlines()
    meta: dict[str, str] = {}
    top6: dict[str, Top6Row] = {}
    tasks_by_topic: dict[str, list[TaskSlot]] = {}
    current_platform: str | None = None
    current_task: TaskSlot | None = None
    in_top6 = False
    in_baijiahao = False
    collecting_source_ref_bundle = False
    source_ref_parts: list[str] = []

    def flush_source_ref_bundle() -> None:
        nonlocal collecting_source_ref_bundle, source_ref_parts, current_task
        if collecting_source_ref_bundle and current_task is not None:
            current_task.source_ref_bundle = " | ".join(part for part in source_ref_parts if part) or "n/a"
        collecting_source_ref_bundle = False
        source_ref_parts = []

    for raw_line in lines:
        line = raw_line.rstrip()
        if collecting_source_ref_bundle:
            subfield = SUBFIELD_RE.match(raw_line)
            if subfield and raw_line.startswith("  - "):
                value = clean(subfield.group(2))
                if value:
                    source_ref_parts.append(value)
                continue
            flush_source_ref_bundle()
        if line.startswith("## 全局主池 Top6"):
            in_top6 = True
            in_baijiahao = False
            continue
        if line in TASK_SECTION_HEADERS:
            in_top6 = False
            in_baijiahao = False
            continue
        if line.startswith("## `baijiahao` SEO 镜像层判断"):
            in_top6 = False
            in_baijiahao = True
            current_platform = None
            current_task = None
            continue
        if line.startswith("## Holdout 清单"):
            in_top6 = False
            in_baijiahao = False
            current_platform = None
            current_task = None
            continue

        if not in_top6 and not current_platform and not in_baijiahao:
            match = FIELD_RE.match(line)
            if match:
                meta[clean(match.group(1))] = clean(match.group(2))

        if in_top6 and line.startswith("|") and not line.startswith("|---"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) >= 5 and cells[0] != "rank":
                if len(cells) == 5:
                    core_judgment = clean(cells[2])
                    why_write = clean(cells[3])
                    risk = clean(cells[4])
                elif len(cells) >= 8:
                    core_judgment = clean(cells[5])
                    why_write = clean(cells[2])
                    risk = clean(cells[6])
                else:
                    core_judgment = clean(cells[2])
                    why_write = clean(cells[3])
                    risk = clean(cells[-1])
                row = Top6Row(
                    rank=clean(cells[0]),
                    topic_key=clean(cells[1]),
                    core_judgment=core_judgment,
                    why_write=why_write,
                    risk=risk,
                )
                top6[row.topic_key] = row
            continue

        heading = HEADING_RE.match(line)
        if heading:
            current_platform = clean(heading.group(1))
            current_task = None
            continue

        task_match = TASK_RE.match(line)
        if current_platform and task_match:
            label = task_match.group(2) or task_match.group(3) or ""
            if is_active_task_label(label):
                current_task = TaskSlot(platform=current_platform, task_no=task_match.group(1), topic_key="")
            else:
                current_task = None
            continue

        match = FIELD_RE.match(line)
        if current_platform and current_task and match:
            field_name = clean(match.group(1))
            field_value = clean(match.group(2))
            field_map = {
                "topic_key": "topic_key",
                "目标读者": "target_reader",
                "切入角度": "angle",
                "核心论点": "core_point",
                "证据抓手": "evidence",
                "source_ref_bundle": "source_ref_bundle",
                "视觉建议": "visual",
                "为什么适合该平台": "fit_reason",
            }
            attr = field_map.get(field_name)
            if attr:
                if field_name == "source_ref_bundle":
                    collecting_source_ref_bundle = True
                    source_ref_parts = []
                    setattr(current_task, attr, "n/a")
                    continue
                setattr(current_task, attr, field_value)
                if field_name == "为什么适合该平台" and current_task.topic_key:
                    tasks_by_topic.setdefault(current_task.topic_key, []).append(current_task)
                    current_task = None
            continue

        if in_baijiahao:
            match = FIELD_RE.match(line)
            if match:
                key = clean(match.group(1))
                value = clean(match.group(2))
                if key == "是否需要单独立题":
                    meta["baijiahao_needed"] = value
                elif key == "理由":
                    meta["baijiahao_reason"] = value
                elif key == "承接哪篇主稿更优":
                    meta["baijiahao_carry_text"] = value

    flush_source_ref_bundle()

    date_token = meta.get("date", path.stem.split("__", 1)[0])
    return TaskSheet(
        path=path,
        date_token=date_token.replace("-", ""),
        generated_at=meta.get("generated_at", "n/a"),
        input_pack=meta.get("input_pack", "n/a"),
        stage_gate_status=meta.get("stage_gate_status", "drafting"),
        top6=top6,
        tasks_by_topic=tasks_by_topic,
        baijiahao_needed=meta.get("baijiahao_needed", "no"),
        baijiahao_reason=meta.get("baijiahao_reason", "n/a"),
        baijiahao_carry_text=meta.get("baijiahao_carry_text", "n/a"),
    )


def topic_has_baijiahao(sheet: TaskSheet, topic_key: str) -> bool:
    if sheet.baijiahao_needed.lower() != "yes":
        return False
    parent_key = resolve_parent_topic_key(topic_key, set(sheet.top6.keys())) or topic_key
    return parent_key in sheet.baijiahao_carry_text or topic_key in sheet.baijiahao_carry_text


def choose_title(tasks: list[TaskSlot]) -> str:
    preferred = sorted(tasks, key=lambda item: ("wechat" not in item.platform, item.task_no))
    return preferred[0].angle if preferred else "n/a"


def choose_angle(top6_row: Top6Row | None, tasks: list[TaskSlot]) -> str:
    if top6_row and top6_row.core_judgment:
        return top6_row.core_judgment
    for task in tasks:
        if task.core_point != "n/a":
            return task.core_point
    return tasks[0].angle if tasks else "n/a"


def special_instructions(tasks: list[TaskSlot], include_baijiahao: bool) -> str:
    lines = []
    for task in tasks:
        lines.append(
            f"{task.platform}: 目标读者={task.target_reader}；切入角度={task.angle}；核心论点={task.core_point}；"
            f"证据抓手={task.evidence}；视觉建议={task.visual}"
        )
    if include_baijiahao:
        lines.append("baijiahao: 作为 SEO 镜像层承接主稿，优先保留关键词与搜索型标题。")
    return " | ".join(lines) if lines else "n/a"


def source_refs(sheet: TaskSheet, tasks: list[TaskSlot]) -> list[str]:
    refs: list[str] = []
    for task in tasks:
        refs.extend(split_refs(task.source_ref_bundle))
        if task.evidence and task.evidence != "n/a":
            refs.append(f"evidence_hint::{task.platform}::{task.evidence}")
    if sheet.input_pack and sheet.input_pack != "n/a":
        refs.append(sheet.input_pack)
    refs.append(str(sheet.path))
    deduped: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if ref not in seen:
            seen.add(ref)
            deduped.append(ref)
    return deduped


def selection_bucket(sheet: TaskSheet) -> str:
    return "platform_lock_continuity" if normalized_stage_gate_status(sheet.stage_gate_status) == "continuity_only" else "platform_lock"


def top5_board_path_for_sheet(sheet: TaskSheet) -> Path:
    return ROOT / "03_topic_candidates" / f"{sheet.date_token}__daily-top8-to-top5.md"


def top5_board_status_for_sheet(sheet: TaskSheet) -> str:
    return "ready" if top5_board_is_ready(top5_board_path_for_sheet(sheet)) else "missing"


def lock_truth(sheet: TaskSheet) -> str:
    top5_status = top5_board_status_for_sheet(sheet)
    if normalized_stage_gate_status(sheet.stage_gate_status) == "continuity_only":
        return "fallback_top5_backed" if top5_status == "ready" else "fallback_task_sheet_only"
    return "premium_top5_backed" if top5_status == "ready" else "task_sheet_only_without_top5"


def selection_instruction_text(sheet: TaskSheet) -> str:
    top5_status = top5_board_status_for_sheet(sheet)
    if normalized_stage_gate_status(sheet.stage_gate_status) == "continuity_only":
        if top5_status == "ready":
            return "市场内容系统按 Top5 建议板 + continuity limited task sheet 保底锁题；该对象属于不停产兜底，不应等同 premium pass。"
        return "市场内容系统当前按 continuity limited task sheet 间接锁题保底；当日 Top5 正式建议板缺失，不应对外宣称无需老板拍板。"
    if top5_status == "ready":
        return "市场内容系统按 Top5 建议板 + 平台任务单自动锁题，无需老板中途拍板。"
    return "市场内容系统当前按平台任务单间接锁题推进；当日 Top5 正式建议板缺失，需补齐 Top5 才算自治闭环。"


def platform_selection_reason(sheet: TaskSheet, platforms: list[str]) -> str:
    platform_text = ", ".join(platforms)
    if normalized_stage_gate_status(sheet.stage_gate_status) == "continuity_only":
        return f"该题在 continuity task sheet 中被分配到 {platform_text}，作为不停产兜底槽位进入正式写稿，后续仍需补 premium gate。"
    return f"该题在最终平台任务单中被分配到 {platform_text}，并已通过 stage-gate。"


def brand_fit_judgment(sheet: TaskSheet) -> str:
    if normalized_stage_gate_status(sheet.stage_gate_status) == "continuity_only":
        return "平台任务单 continuity 锁题"
    return "平台任务单终局锁题"


def recommended_reason(sheet: TaskSheet, top6_row: Top6Row | None, angle: str) -> str:
    if top6_row:
        return top6_row.why_write
    if normalized_stage_gate_status(sheet.stage_gate_status) == "continuity_only":
        return f"该题被纳入 continuity limited task sheet，优先保障当天仍有可推进写稿对象。核心角度：{angle}"
    return "平台任务单最终保留并进入正式写稿。"


def why_now_value(sheet: TaskSheet, top6_row: Top6Row | None, tasks: list[TaskSlot], angle: str) -> str:
    if top6_row and top6_row.why_write:
        return top6_row.why_write
    for task in tasks:
        if task.core_point and task.core_point != "n/a":
            return task.core_point
    return recommended_reason(sheet, top6_row, angle)


def platform_hint_value(platforms: list[str]) -> str:
    return ", ".join(platforms) if platforms else "n/a"


def existing_card_for(topic_key: str, date_token: str) -> Path | None:
    matches = sorted(APPROVED_DIR.glob(f"{date_token}_*__{topic_key}__approved-topic.md"))
    return matches[-1] if matches else None


def resolve_materialization_mode(sheet: TaskSheet, requested_mode: str) -> str:
    if requested_mode not in MATERIALIZATION_MODES:
        raise SystemExit(f"Unsupported materialization mode: {requested_mode}")
    if requested_mode == "auto":
        if normalized_stage_gate_status(sheet.stage_gate_status) == "continuity_only":
            return "continuity_active_only"
        return "premium_all"
    return requested_mode


def validate_task_sheet_integrity(
    sheet: TaskSheet,
    materialization_mode: str,
    allow_missing_top5_recovery: bool = False,
) -> None:
    task_topic_keys = set(sheet.tasks_by_topic.keys())
    top6_topic_keys = set(sheet.top6.keys())
    matched_top6_keys = {
        task_key: resolve_parent_topic_key(task_key, top6_topic_keys) for task_key in task_topic_keys
    }

    missing_from_top6 = sorted(task_key for task_key, parent_key in matched_top6_keys.items() if parent_key is None)
    if missing_from_top6:
        raise SystemExit(
            "Platform task sheet invalid: these task slots are not present in Top6: "
            + ", ".join(missing_from_top6)
        )

    if materialization_mode == "premium_all":
        assigned_top6 = {parent_key for parent_key in matched_top6_keys.values() if parent_key}
        unassigned_top6 = sorted(top6_topic_keys - assigned_top6)
        if unassigned_top6:
            raise SystemExit(
                "Platform task sheet invalid: these Top6 topics have no downstream task slots: "
                + ", ".join(unassigned_top6)
            )
    elif materialization_mode == "continuity_active_only" and not task_topic_keys:
        raise SystemExit("Platform task sheet invalid: continuity_active_only mode requires at least one active task slot.")

    top5_board_path = top5_board_path_for_sheet(sheet)
    board_candidate_keys = set(top5_candidate_keys(top5_board_path))
    if not board_candidate_keys:
        if not (
            allow_missing_top5_recovery
            and materialization_mode == "continuity_active_only"
            and normalized_stage_gate_status(sheet.stage_gate_status) == "continuity_only"
        ):
            raise SystemExit(
                f"Top5 board missing usable candidate_key set, cannot materialize approved topics safely: {top5_board_path}"
            )
    else:
        illegal_tasks_against_board = sorted(
            task_key for task_key in task_topic_keys if resolve_parent_topic_key(task_key, board_candidate_keys) is None
        )
        if illegal_tasks_against_board:
            raise SystemExit(
                "Platform task sheet invalid: these active task slot topic_key values are outside the referenced Top5/Holdout board: "
                + ", ".join(illegal_tasks_against_board)
            )

        illegal_top6_against_board = sorted(
            top6_key for top6_key in top6_topic_keys if resolve_parent_topic_key(top6_key, board_candidate_keys) is None
        )
        if illegal_top6_against_board:
            raise SystemExit(
                "Platform task sheet invalid: these Top6 topic_key values are outside the referenced Top5/Holdout board: "
                + ", ".join(illegal_top6_against_board)
            )

    input_pack_path = Path(sheet.input_pack).expanduser()
    top20_topic_keys, _ = extract_top20_topic_keys(input_pack_path)
    if not top20_topic_keys:
        raise SystemExit(
            f"Top20 pack missing usable topic_key set, cannot materialize approved topics safely: {input_pack_path}"
        )

    illegal_tasks = sorted(
        task_key for task_key in task_topic_keys if resolve_parent_topic_key(task_key, top20_topic_keys) is None
    )
    if illegal_tasks:
        raise SystemExit(
            "Platform task sheet invalid: these active task slot topic_key values are outside the referenced Top20 pack: "
            + ", ".join(illegal_tasks)
        )

    if materialization_mode == "premium_all":
        illegal_top6 = sorted(
            top6_key for top6_key in top6_topic_keys if resolve_parent_topic_key(top6_key, top20_topic_keys) is None
        )
        if illegal_top6:
            raise SystemExit(
                "Platform task sheet invalid: these Top6 topic_key values are outside the referenced Top20 pack: "
                + ", ".join(illegal_top6)
            )


def resolve_topic_keys(sheet: TaskSheet, requested_topic_keys: list[str] | None) -> list[str]:
    all_task_keys = sorted(sheet.tasks_by_topic.keys())
    if requested_topic_keys is None:
        return all_task_keys
    missing = sorted(set(requested_topic_keys) - set(all_task_keys))
    if missing:
        raise SystemExit(
            "Requested topic_key values are not active slots in the platform task sheet: " + ", ".join(missing)
        )
    return [topic_key for topic_key in all_task_keys if topic_key in set(requested_topic_keys)]


def build_outputs(
    sheet: TaskSheet,
    topic_keys: list[str],
    approved_by: str,
    approved_at: datetime,
) -> list[tuple[str, Path, str]]:
    outputs: list[tuple[str, Path, str]] = []
    for topic_key in topic_keys:
        path, content = build_card(sheet, topic_key, sheet.tasks_by_topic[topic_key], approved_by, approved_at)
        outputs.append((topic_key, path, content))
    return outputs


def build_card(
    sheet: TaskSheet,
    topic_key: str,
    tasks: list[TaskSlot],
    approved_by: str,
    approved_at: datetime,
) -> tuple[Path, str]:
    parent_key = resolve_parent_topic_key(topic_key, set(sheet.top6.keys()))
    top6_row = sheet.top6.get(parent_key or topic_key)
    platforms = sorted({task.platform for task in tasks})
    if topic_has_baijiahao(sheet, topic_key) and "baijiahao" not in platforms:
        platforms.append("baijiahao")
    top5_board_path = top5_board_path_for_sheet(sheet)
    top5_status = top5_board_status_for_sheet(sheet)
    selection_truth = lock_truth(sheet)

    existing = existing_card_for(topic_key, sheet.date_token)
    if existing is not None:
        path = existing
        topic_id = f"topic__{sheet.date_token}_{approved_at.strftime('%H%M%S')}__{topic_key}"
    else:
        stamp = approved_at.strftime("%Y%m%d_%H%M%S")
        path = APPROVED_DIR / f"{stamp}__{topic_key}__approved-topic.md"
        topic_id = f"topic__{stamp}__{topic_key}"

    title = choose_title(tasks)
    angle = choose_angle(top6_row, tasks)
    refs = source_refs(sheet, tasks)
    logical_date_text = f"{sheet.date_token[:4]}-{sheet.date_token[4:6]}-{sheet.date_token[6:8]}"
    delivery_deadline = format_cst(lane_delivery_deadline(logical_date_text, DEFAULT_DELIVERY_LANE))
    content = "\n".join(
        [
            "# Approved Topic Card",
            "",
            f"- `topic_id`: `{topic_id}`",
            f"- `topic_key`: `{topic_key}`",
            f"- `candidate_id`: `cand__{topic_key}`",
            f"- `title`: `{title}`",
            f"- `approved_angle`: `{angle}`",
            f"- `requested_platforms`: `{', '.join(platforms)}`",
            f"- `special_instructions`: `{special_instructions(tasks, 'baijiahao' in platforms)}`",
            f"- `approved_by`: `{approved_by}`",
            f"- `approved_at`: `{approved_at.strftime('%Y-%m-%d %H:%M:%S CST')}`",
            "- `status`: `approved`",
            f"- `delivery_lane`: `{DEFAULT_DELIVERY_LANE}`",
            f"- `publish_mode`: `{DEFAULT_PUBLISH_MODE}`",
            f"- `delivery_deadline`: `{delivery_deadline}`",
            f"- `selection_scope`: `{DEFAULT_SELECTION_SCOPE}`",
            f"- `business_window_start`: `{BUSINESS_WINDOW_START}`",
            f"- `business_window_end`: `{BUSINESS_WINDOW_END}`",
            "",
            "## Selection Context",
            "",
            f"- `source_board_path`: `{sheet.path}`",
            f"- `source_top20_pack_path`: `{sheet.input_pack}`",
            f"- `source_top5_board_path`: `{top5_board_path}`",
            f"- `source_top5_board_status`: `{top5_status}`",
            f"- `selected_rank`: `{top6_row.rank if top6_row else 'n/a'}`",
            f"- `selection_bucket`: `{selection_bucket(sheet)}`",
            f"- `selection_instruction`: `{selection_instruction_text(sheet)}`",
            f"- `lock_truth`: `{selection_truth}`",
            "- `restored_from_holdout`: `no`",
            "",
            "## Platform Decision",
            "",
            "- `platform_selection_mode`: `platform_task_sheet_lock`",
            "- `platform_bundle`: `explicit_platform_slots`",
            f"- `platform_selection_reason`: `{platform_selection_reason(sheet, platforms)}`",
            "",
            "## Platform Task Notes",
            "",
            *[
                f"- `{task.platform}`｜目标读者：{task.target_reader}｜切入角度：{task.angle}｜核心论点：{task.core_point}｜为什么适合：{task.fit_reason}"
                for task in tasks
            ],
            "",
            "## Carried Judgment",
            "",
            f"- `market_potential`: `{'高' if top6_row and int(top6_row.rank) <= 3 else '中高'}`",
            f"- `brand_fit_judgment`: `{brand_fit_judgment(sheet)}`",
            f"- `recommended_reason`: `{recommended_reason(sheet, top6_row, angle)}`",
            f"- `one_line_judgment`: `{top6_row.core_judgment if top6_row else angle}`",
            f"- `why_now`: `{why_now_value(sheet, top6_row, tasks, angle)}`",
            f"- `platform_hint`: `{platform_hint_value(platforms)}`",
            f"- `risk_note`: `{top6_row.risk if top6_row else 'n/a'}`",
            "",
            "## Source Refs",
            "",
            *[f"- `{ref}`" for ref in refs],
            "",
            "## Next Handoff",
            "",
            f"- `draft_pack_target_dir`: `{ROOT / '05_draft_packs' / topic_key}`",
            "- `next_step`: `approved -> drafting`",
            f"- `draft_scope`: `基于 {angle} 生成 {', '.join(platforms)} 对应的平台草稿，并保留原始 refs、risk note 与平台差异化表达。`",
            "",
        ]
    )
    return path, content


def write_execution_log(
    paths: list[Path],
    task_sheet_path: Path,
    approved_at: datetime,
    materialization_mode: str,
    selected_topic_keys: list[str],
) -> Path:
    stamp = approved_at.strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"{stamp}__platform-lock__approved-topic-bridge.md"
    body = "\n".join(
        [
            "# Platform Lock -> Approved Topic Execution Log",
            "",
            f"- `task_sheet_path`: `{task_sheet_path}`",
            f"- `approved_at`: `{approved_at.strftime('%Y-%m-%d %H:%M:%S CST')}`",
            f"- `materialization_mode`: `{materialization_mode}`",
            f"- `selected_topic_keys`: `{', '.join(selected_topic_keys) if selected_topic_keys else 'none'}`",
            f"- `approved_count`: `{len(paths)}`",
            "",
            "## Outputs",
            "",
            *[f"- `{path}`" for path in paths],
            "",
        ]
    )
    log_path.write_text(body, encoding="utf-8")
    return log_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize approved topics from final platform task sheet")
    parser.add_argument("--task-sheet", required=True, help="Path to platform task sheet")
    parser.add_argument("--approved-by", default="market-editor")
    parser.add_argument("--approved-at", default="")
    parser.add_argument("--mode", default="auto", choices=sorted(MATERIALIZATION_MODES))
    parser.add_argument("--topic-key", action="append", dest="topic_keys", default=[], help="Limit materialization to active slot topic_key values")
    parser.add_argument(
        "--allow-missing-top5-recovery",
        action="store_true",
        help="Allow truthful continuity recovery when Top5 board is missing but continuity limited task sheet is valid.",
    )
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def materialize_task_sheet(
    task_sheet_path: Path,
    approved_by: str,
    approved_at: datetime,
    materialization_mode: str,
    write: bool,
    requested_topic_keys: list[str] | None = None,
    allow_missing_top5_recovery: bool = False,
) -> tuple[list[tuple[str, Path, str]], str, TaskSheet]:
    sheet = parse_task_sheet(task_sheet_path)
    resolved_mode = resolve_materialization_mode(sheet, materialization_mode)
    validate_task_sheet_integrity(sheet, resolved_mode, allow_missing_top5_recovery=allow_missing_top5_recovery)
    topic_keys = resolve_topic_keys(sheet, requested_topic_keys or None)
    outputs = build_outputs(sheet, topic_keys, approved_by, approved_at)
    if not outputs:
        raise SystemExit("No active task slots selected for approved-topic materialization.")
    return outputs, resolved_mode, sheet


def persist_outputs(
    outputs: list[tuple[str, Path, str]],
    sheet: TaskSheet,
    approved_by: str,
    approved_at: datetime,
    task_sheet_path: Path,
    materialization_mode: str,
) -> tuple[list[tuple[str, Path, str]], list[Path], Path]:
    APPROVED_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    actual_outputs: list[tuple[str, Path, str]] = []
    written_paths: list[Path] = []
    for index, (topic_key, path, content) in enumerate(outputs):
        if index:
            shifted_time = approved_at + timedelta(seconds=index)
            path, content = build_card(sheet, topic_key, sheet.tasks_by_topic[topic_key], approved_by, shifted_time)
        path.write_text(content, encoding="utf-8")
        actual_outputs.append((topic_key, path, content))
        written_paths.append(path)

    log_path = write_execution_log(
        written_paths,
        task_sheet_path,
        approved_at,
        materialization_mode,
        [topic_key for topic_key, _, _ in actual_outputs],
    )
    return actual_outputs, written_paths, log_path


def main() -> None:
    args = parse_args()
    task_sheet_path = Path(args.task_sheet).expanduser()
    approved_at = (
        datetime.strptime(args.approved_at, "%Y-%m-%d %H:%M:%S").replace(tzinfo=TZ)
        if args.approved_at
        else datetime.now(TZ)
    )
    outputs, resolved_mode, sheet = materialize_task_sheet(
        task_sheet_path=task_sheet_path,
        approved_by=args.approved_by,
        approved_at=approved_at,
        materialization_mode=args.mode,
        write=args.write,
        requested_topic_keys=args.topic_keys,
        allow_missing_top5_recovery=args.allow_missing_top5_recovery,
    )

    if not args.write:
        for _, path, content in outputs:
            print(f"=== {path} ===")
            print(content)
        return

    actual_outputs, written_paths, log_path = persist_outputs(
        outputs=outputs,
        sheet=sheet,
        approved_by=args.approved_by,
        approved_at=approved_at,
        task_sheet_path=task_sheet_path,
        materialization_mode=resolved_mode,
    )
    print(f"APPROVED_TOPIC_COUNT={len(written_paths)}")
    for _, path, _ in actual_outputs:
        print(path)
    print(f"EXECUTION_LOG={log_path}")


if __name__ == "__main__":
    main()
