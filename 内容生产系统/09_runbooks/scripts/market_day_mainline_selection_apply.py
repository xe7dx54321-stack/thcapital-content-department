#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
SELECTION_STATE_DIR = ROOT / "11_frontstage" / "_selection_state"
APPROVED_BUILDER = ROOT / "09_runbooks" / "scripts" / "market_approved_topic_builder.py"
DRAFT_PACK_BUILDER = ROOT / "09_runbooks" / "scripts" / "market_draft_pack_builder.py"
CONTENT_POLISH_BUILDER = ROOT / "09_runbooks" / "scripts" / "market_content_polish_builder.py"
WECHAT_BRIDGE_ENQUEUE = ROOT / "09_runbooks" / "scripts" / "market_wechat_bridge_enqueue.py"
CN_TZ = ZoneInfo("Asia/Shanghai")
DAY_MAINLINE_DEFAULT_PICK_HM = "18:00"
DAY_MAINLINE_DRAFTBOX_DEADLINE_HM = "19:00"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply founder/default day_mainline pick and trigger downstream draft flow.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical day in YYYY-MM-DD.")
    parser.add_argument("--pick-rank", type=int, help="Explicit candidate rank to pick.")
    parser.add_argument("--pick-candidate-key", default="", help="Explicit candidate key to pick.")
    parser.add_argument("--reply-text", default="", help="Raw founder reply text, e.g. 选第1个.")
    parser.add_argument("--auto-default-if-overdue", action="store_true", help="If no explicit pick and now>=18:00, default to first recommended.")
    parser.add_argument("--approved-by", default="market-editor", help="Recorder for approved_topic.")
    parser.add_argument("--write", action="store_true", help="Persist selection and run downstream steps.")
    parser.add_argument("--skip-downstream", action="store_true", help="Only materialize approved topic, skip draft/polish/bridge.")
    return parser.parse_args()


def clean(value: str | None, fallback: str = "") -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().strip("`") or fallback


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def parse_hm(raw: str) -> tuple[int, int]:
    hour, minute = [int(part) for part in raw.split(":", 1)]
    return hour, minute


def lane_dt(date_text: str, hm: str) -> datetime:
    target_day = date.fromisoformat(date_text)
    hour, minute = parse_hm(hm)
    return datetime(target_day.year, target_day.month, target_day.day, hour, minute, tzinfo=CN_TZ)


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def state_path_for(date_text: str) -> Path:
    return SELECTION_STATE_DIR / f"{day_token(date_text)}__day-mainline-founder-pick-state.json"


def load_state(date_text: str) -> dict:
    path = state_path_for(date_text)
    if not path.exists():
        raise SystemExit(f"Selection state not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(date_text: str, payload: dict) -> Path:
    path = state_path_for(date_text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def parse_reply_rank(reply_text: str) -> int | None:
    text = clean(reply_text, "")
    if not text:
        return None
    match = re.search(r"第\s*(\d+)\s*个", text)
    if match:
        return int(match.group(1))
    match = re.search(r"(?:选|用|做)\s*(\d+)", text)
    if match:
        return int(match.group(1))
    return None


def candidate_from_state(payload: dict, pick_rank: int | None, pick_key: str, reply_text: str, auto_default: bool) -> tuple[dict, str]:
    recommended = payload.get("recommended_cards") or []
    holdouts = payload.get("holdout_cards") or []
    cards = recommended + holdouts
    by_rank = {int(card["rank"]): card for card in cards}
    by_key = {clean(card["candidate_key"]): card for card in cards}

    if pick_rank is not None:
        if pick_rank not in by_rank:
            raise SystemExit(f"Requested rank not present in selection state: {pick_rank}")
        return by_rank[pick_rank], f"founder_manual_pick:rank={pick_rank}"

    normalized_key = clean(pick_key, "")
    if normalized_key:
        if normalized_key not in by_key:
            raise SystemExit(f"Requested candidate_key not present in selection state: {normalized_key}")
        return by_key[normalized_key], f"founder_manual_pick:key={normalized_key}"

    parsed_rank = parse_reply_rank(reply_text)
    if parsed_rank is not None:
        if parsed_rank not in by_rank:
            raise SystemExit(f"Reply mentioned rank={parsed_rank}, but it is not present in selection state.")
        return by_rank[parsed_rank], f"founder_reply:{clean(reply_text)}"

    if auto_default and datetime.now(CN_TZ) >= lane_dt(payload["date"], DAY_MAINLINE_DEFAULT_PICK_HM):
        first = next(iter(recommended), None)
        if first is None:
            raise SystemExit("No recommended candidate available for default pick.")
        return first, "default_first_after_1800"

    raise SystemExit("No explicit founder pick found, and default-first condition has not opened yet.")


def run_command(command: list[str]) -> list[str]:
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def latest_path_from_stdout(lines: list[str], suffix: str) -> str:
    for line in reversed(lines):
        if line.endswith(suffix):
            return line
    return ""


def extract_markdown_field(path: str, field: str) -> str:
    if not clean(path, ""):
        return ""
    file_path = Path(path).expanduser().resolve()
    if not file_path.exists():
        return ""
    pattern = re.compile(rf"^- `{re.escape(field)}`: ?`?(.*?)`?$")
    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw_line.strip())
        if match:
            return clean(match.group(1), "")
    return ""


def materialize_approved_topic(card: dict, state: dict, approved_by: str, write: bool) -> str:
    if not APPROVED_BUILDER.exists():
        raise SystemExit(f"Approved-topic builder missing: {APPROVED_BUILDER}")
    selection_instruction = (
        f"白天线创始人拍板：{state.get('selected_reason', 'manual_pick')}；"
        f"若 18:00 前未回复则默认 Top1；本轮目标是在 19:00 前把成品稿同时落到微信草稿箱与飞书云文档。"
    )
    command = [
        "python3",
        str(APPROVED_BUILDER),
        "--board-path",
        clean(state.get("board_path"), ""),
        "--rank",
        str(card["rank"]),
        "--approved-angle",
        clean(card["approved_angle"], card["topic_line"]),
        "--special-instructions",
        clean(card["special_instructions"], ""),
        "--selection-instruction",
        selection_instruction,
        "--approved-by",
        approved_by,
        "--approved-at",
        datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "--delivery-lane",
        "day_mainline",
        "--publish-mode",
        "draft_only",
        "--delivery-deadline",
        format_ts(lane_dt(state["date"], DAY_MAINLINE_DRAFTBOX_DEADLINE_HM)),
        "--selection-scope",
        "founder_pick_1740_briefing_to_1900_draftbox",
        "--business-window-start",
        "17:40",
        "--business-window-end",
        "19:00",
    ]
    if write:
        command.append("--write")
    lines = run_command(command)
    return latest_path_from_stdout(lines, "__approved-topic.md")


def parse_prefixed_fields(lines: list[str], prefix: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in lines:
        if not line.startswith(prefix) or "=" not in line:
            continue
        key, value = line.split("=", 1)
        parsed[key] = value.strip()
    return parsed


def run_downstream(approved_topic_path: str, write: bool) -> tuple[str, str, dict[str, str]]:
    if not approved_topic_path:
        return "", "", {}
    if not DRAFT_PACK_BUILDER.exists():
        raise SystemExit(f"Draft-pack builder missing: {DRAFT_PACK_BUILDER}")
    draft_command = [
        "python3",
        str(DRAFT_PACK_BUILDER),
        "--approved-topic-path",
        approved_topic_path,
    ]
    if write:
        draft_command.append("--write")
    draft_lines = run_command(draft_command)
    draft_pack_dir = latest_path_from_stdout(draft_lines, "/00_draft-pack-card.md")
    if draft_pack_dir.endswith("/00_draft-pack-card.md"):
        draft_pack_dir = str(Path(draft_pack_dir).parent)
    elif not draft_pack_dir and draft_lines:
        draft_pack_dir = draft_lines[0]
    if not draft_pack_dir:
        return "", "", {}

    if not CONTENT_POLISH_BUILDER.exists():
        raise SystemExit(f"Content-polish builder missing: {CONTENT_POLISH_BUILDER}")
    polish_command = [
        "python3",
        str(CONTENT_POLISH_BUILDER),
        "--draft-pack-dir",
        draft_pack_dir,
        "--status",
        "ready",
    ]
    if write:
        polish_command.append("--write")
    run_command(polish_command)

    request_id = ""
    feishu_doc_meta: dict[str, str] = {}
    if WECHAT_BRIDGE_ENQUEUE.exists():
        bridge_command = [
            "python3",
            str(WECHAT_BRIDGE_ENQUEUE),
            "--draft-pack-dir",
            draft_pack_dir,
        ]
        if write:
            bridge_command.append("--write")
        bridge_lines = run_command(bridge_command)
        for line in bridge_lines:
            if line.startswith("REQUEST_ID="):
                request_id = line.split("=", 1)[1].strip()
                break
        feishu_doc_meta = parse_prefixed_fields(bridge_lines, "FEISHU_DOC_")
        if not request_id:
            request_id = f"wechat_bridge__{Path(draft_pack_dir).name}"
    return draft_pack_dir, request_id, feishu_doc_meta


def main() -> None:
    args = parse_args()
    state = load_state(args.date)
    if clean(state.get("selected_candidate_key"), ""):
        print(f"SELECTION_STATUS=already_selected")
        print(f"SELECTED_CANDIDATE_KEY={state['selected_candidate_key']}")
        print(f"APPROVED_TOPIC_PATH={state.get('approved_topic_path', '')}")
        return

    chosen_card, reason = candidate_from_state(
        state,
        pick_rank=args.pick_rank,
        pick_key=args.pick_candidate_key,
        reply_text=args.reply_text,
        auto_default=args.auto_default_if_overdue,
    )
    state["selected_rank"] = chosen_card["rank"]
    state["selected_candidate_key"] = chosen_card["candidate_key"]
    state["selected_at"] = format_ts(datetime.now(CN_TZ))
    state["selected_reason"] = reason
    state["status"] = "selected_pending_materialization"

    approved_topic_path = materialize_approved_topic(chosen_card, state, args.approved_by, write=args.write)
    state["approved_topic_path"] = approved_topic_path

    draft_pack_dir = ""
    request_id = ""
    feishu_doc_meta: dict[str, str] = {}
    if args.write and not args.skip_downstream and approved_topic_path:
        draft_pack_dir, request_id, feishu_doc_meta = run_downstream(approved_topic_path, write=True)
    if args.write and not draft_pack_dir and approved_topic_path:
        draft_pack_dir = extract_markdown_field(approved_topic_path, "draft_pack_target_dir")
    state["draft_pack_dir"] = draft_pack_dir
    state["bridge_request_id"] = request_id
    state["feishu_doc_status"] = feishu_doc_meta.get("FEISHU_DOC_STATUS", "")
    state["feishu_doc_mode"] = feishu_doc_meta.get("FEISHU_DOC_MODE", "")
    state["feishu_doc_title"] = feishu_doc_meta.get("FEISHU_DOC_TITLE", "")
    state["feishu_doc_token"] = feishu_doc_meta.get("FEISHU_DOC_TOKEN", "")
    state["feishu_doc_url"] = feishu_doc_meta.get("FEISHU_DOC_URL", "")
    state["feishu_doc_source_fingerprint"] = feishu_doc_meta.get("FEISHU_DOC_SOURCE_FINGERPRINT", "")
    if request_id:
        state["status"] = "downstream_started"
    elif draft_pack_dir:
        state["status"] = "selected_pending_downstream_delivery"
    else:
        state["status"] = "selected_only"

    save_path = save_state(args.date, state) if args.write else state_path_for(args.date)
    print(f"STATE_PATH={save_path}")
    print(f"SELECTED_RANK={state['selected_rank']}")
    print(f"SELECTED_CANDIDATE_KEY={state['selected_candidate_key']}")
    print(f"SELECTION_REASON={state['selected_reason']}")
    if approved_topic_path:
        print(f"APPROVED_TOPIC_PATH={approved_topic_path}")
    if draft_pack_dir:
        print(f"DRAFT_PACK_DIR={draft_pack_dir}")
    if request_id:
        print(f"BRIDGE_REQUEST_ID={request_id}")
    if feishu_doc_meta.get("FEISHU_DOC_URL"):
        print(f"FEISHU_DOC_URL={feishu_doc_meta['FEISHU_DOC_URL']}")


if __name__ == "__main__":
    main()
