#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import market_frontstage_board_builder as board_builder


DEFAULT_STATE_PATH = board_builder.FRONTSTAGE_DIR / "_sync_state" / "market_frontstage_sync_state.json"
DEFAULT_TARGET = f"chat:{board_builder.FRONTSTAGE_GROUP_ID}"
DEFAULT_ACCOUNT = "market"
DEFAULT_SYNC_LOG_SUFFIX = "__market-frontstage-sync-execution.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh frontstage board and sync critical market updates to Feishu group")
    parser.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--write", action="store_true", help="Write refreshed board back to 11_frontstage/")
    parser.add_argument("--close-out", action="store_true", help="Send one end-of-day summary if the day had activity")
    parser.add_argument("--force-send", action="store_true", help="Force a group sync regardless of signature state")
    parser.add_argument("--dry-run", action="store_true", help="Build board and message but skip real delivery")
    parser.add_argument("--state-path", default=str(DEFAULT_STATE_PATH), help="State file path")
    parser.add_argument("--account", default=DEFAULT_ACCOUNT, help="OpenClaw Feishu account id")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="OpenClaw message target")
    parser.add_argument(
        "--routine-issues-only",
        action="store_true",
        help="Only send a compact issue summary; skip delivery when no issue is detected",
    )
    return parser.parse_args()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_state(path: Path, state: dict) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def hash_signature(payload: dict) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def dedupe_preserve_order(values: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


def refresh_board(date_text: str, write: bool) -> tuple[Path, str]:
    board_path = board_builder.FRONTSTAGE_DIR / f"{board_builder.day_token(date_text)}__market-frontstage-board.md"
    content = board_builder.build_board(date_text)
    if write or not board_path.exists() or board_path.read_text(encoding="utf-8") != content:
        ensure_parent(board_path)
        board_path.write_text(content, encoding="utf-8")
    return board_path, content


def build_snapshot(date_text: str, write_board: bool) -> dict:
    board_path, _ = refresh_board(date_text, write_board)
    token = board_builder.day_token(date_text)
    radar_board_path = board_builder.BOARD_DIR / f"{token}__daily-top8-to-top5.md"
    radar_exec_path = board_builder.LOG_DIR / f"{token}__market-topic-radar-execution.md"

    source_packets = board_builder.list_source_packets_in_business_window(date_text)
    asset_chains = board_builder.list_daily_files(board_builder.ASSET_CHAIN_DIR, token, "__asset-chain.md")
    topic_clusters = board_builder.list_daily_files(board_builder.TOPIC_CLUSTER_DIR, token, "__topic-cluster.md")
    approved_topics = board_builder.load_approved_topics(token)
    topic_lookup = {topic.topic_id: topic.topic_key for topic in approved_topics}
    today_topic_ids = {topic.topic_id for topic in approved_topics}
    platform_task_sheet_path = board_builder.BOARD_DIR / f"{token}__platform-task-sheet.md"
    active_task_topic_keys = sorted(board_builder.extract_active_task_sheet_topic_keys(platform_task_sheet_path))
    today_draft_packs, active_draft_packs = board_builder.load_draft_packs(
        date_text,
        today_topic_ids,
        set(active_task_topic_keys),
    )
    queue_items_today = board_builder.load_queue_items(token)
    queue_items_all = board_builder.load_queue_items()
    topic_truths = board_builder.build_topic_truths(approved_topics, queue_items_all, token)
    waiting_publish_items_all = [item for item in queue_items_all if item.status == "waiting_human_publish"]
    dirty_waiting_publish_items = [item for item in waiting_publish_items_all if board_builder.queue_item_is_dirty(item)]
    waiting_publish_items = [item for item in waiting_publish_items_all if not board_builder.queue_item_is_dirty(item)]
    published_items = [item for item in queue_items_today if item.status == "published"]
    review_files = board_builder.list_daily_files(board_builder.REVIEW_DIR, token, "-review.md")
    board_exists = board_builder.top5_board_is_ready(radar_board_path)
    top_titles = board_builder.parse_top_titles(radar_board_path)
    top_decisions, holdout_decisions = board_builder.load_candidate_decisions(radar_board_path)
    radar_exec_fields = board_builder.parse_fields(radar_exec_path)
    supply_status = board_builder.clean(radar_exec_fields.get("supply_status", "n/a"))

    formal_tasks = board_builder.infer_formal_tasks(
        len(source_packets),
        board_exists,
        approved_topics,
        topic_truths,
        active_draft_packs,
        waiting_publish_items,
        topic_lookup,
        active_task_topic_keys,
    )
    current_focus = board_builder.infer_current_focus(
        board_exists,
        top_titles,
        approved_topics,
        topic_truths,
        active_draft_packs,
        waiting_publish_items,
        len(source_packets),
        topic_lookup,
        active_task_topic_keys,
    )
    decision_digest = board_builder.build_decision_digest(top_decisions, holdout_decisions, topic_truths)
    stage_results = board_builder.build_stage_results(
        len(source_packets),
        len(asset_chains),
        len(topic_clusters),
        board_exists,
        radar_board_path,
        top_titles,
        approved_topics,
        topic_truths,
        today_draft_packs,
        waiting_publish_items,
        len(dirty_waiting_publish_items),
        active_task_topic_keys,
    )
    approval_summary = board_builder.build_light_approval_summary(
        board_exists,
        approved_topics,
        topic_truths,
        waiting_publish_items,
        published_items,
        len(review_files),
        len(dirty_waiting_publish_items),
        topic_lookup,
    )
    next_actions = board_builder.build_next_actions(
        board_exists,
        approved_topics,
        topic_truths,
        active_draft_packs,
        waiting_publish_items,
        active_task_topic_keys,
    )
    human_assist = board_builder.build_human_assist(
        waiting_publish_items,
        board_exists,
        approved_topics,
        topic_truths,
        len(dirty_waiting_publish_items),
        supply_status,
        topic_lookup,
    )
    day_mainline_unbacked_count = len(board_builder.day_mainline_unbacked_truths(topic_truths))
    premium_ready_count = len(board_builder.premium_ready_truths(topic_truths))
    blocked_final_gate_count = len(board_builder.blocked_final_gate_truths(topic_truths))
    group_sync_lines = board_builder.build_group_sync_draft(
        formal_tasks,
        current_focus,
        decision_digest,
        stage_results,
        approval_summary,
        next_actions,
        human_assist,
        board_path,
    )

    markers: list[str] = []
    if board_exists:
        markers.append("top5_ready")
    if approved_topics:
        markers.append("approved_topic")
    if day_mainline_unbacked_count > 0:
        markers.append("top5_truth_gap")
    if any(pack.status in {"drafting", "needs_revision", "ready"} for pack in today_draft_packs):
        markers.append("draft_progress")
    if waiting_publish_items:
        markers.append("waiting_human_publish")
    if dirty_waiting_publish_items:
        markers.append("dirty_waiting_publish")
    if blocked_final_gate_count > 0:
        markers.append("final_gate_blocked")
    if published_items and not review_files:
        markers.append("review_pending")
    if supply_status == "insufficient":
        markers.append("supply_insufficient")

    signature_payload = {
        "date": date_text,
        "markers": markers,
        "top_titles": top_titles[:5],
        "decision_digest": decision_digest[:5],
        "approved_topics": [
            {
                "topic_id": topic.topic_id,
                "topic_key": topic.topic_key,
                "status": topic.status,
                "selected_rank": topic.selected_rank,
                "selection_bucket": topic.selection_bucket,
                "approved_angle": topic.approved_angle,
                "lock_truth": board_builder.infer_lock_truth(topic, token),
                "top5_backing_status": board_builder.infer_top5_backing_status(topic, token),
            }
            for topic in approved_topics
        ],
        "draft_packs": [
            {
                "draft_key": pack.draft_key,
                "topic_id": pack.topic_id,
                "status": pack.status,
            }
            for pack in today_draft_packs
            if pack.status in {"drafting", "needs_revision", "ready"}
        ],
        "waiting_publish_items": [
            {
                "queue_id": item.queue_id,
                "topic_id": item.topic_id,
                "platform": item.platform,
                "status": item.status,
            }
            for item in waiting_publish_items
        ],
        "dirty_waiting_publish_count": len(dirty_waiting_publish_items),
        "published_items": [
            {
                "queue_id": item.queue_id,
                "topic_id": item.topic_id,
                "platform": item.platform,
                "status": item.status,
            }
            for item in published_items
        ],
        "day_mainline_unbacked_count": day_mainline_unbacked_count,
        "premium_ready_count": premium_ready_count,
        "blocked_final_gate_count": blocked_final_gate_count,
        "approval_summary": [item for item in approval_summary if item != "当前没有新的拍板 / 发布提醒堆积。"],
        "next_actions": next_actions[:3],
        "human_assist": [item for item in human_assist if item != "暂时无。"],
    }

    has_activity = any(
        [
            source_packets,
            asset_chains,
            topic_clusters,
            board_exists,
            approved_topics,
            today_draft_packs,
            queue_items_all,
            review_files,
        ]
    )

    return {
        "date": date_text,
        "token": token,
        "board_path": board_path,
        "board_exists": board_exists,
        "markers": markers,
        "has_activity": has_activity,
        "message_lines": group_sync_lines,
        "signature_payload": signature_payload,
        "source_packet_count": len(source_packets),
        "approved_topic_count": len(approved_topics),
        "active_draft_pack_count": len(active_draft_packs),
        "today_draft_pack_count": len(today_draft_packs),
        "waiting_publish_count": len(waiting_publish_items),
        "dirty_waiting_publish_count": len(dirty_waiting_publish_items),
        "published_count": len(published_items),
        "day_mainline_unbacked_count": day_mainline_unbacked_count,
        "premium_ready_count": premium_ready_count,
        "blocked_final_gate_count": blocked_final_gate_count,
        "review_count": len(review_files),
        "supply_status": supply_status,
        "waiting_publish_topics": dedupe_preserve_order(
            [
                board_builder.topic_display(item.topic_id, topic_lookup)
                for item in waiting_publish_items
            ]
        ),
        "waiting_publish_topic_count": len(
            {
                board_builder.topic_display(item.topic_id, topic_lookup)
                for item in waiting_publish_items
            }
        ),
    }


def build_message(snapshot: dict, close_out: bool) -> str:
    lines = list(snapshot["message_lines"])
    if close_out and lines:
        lines[0] = "内容工厂晚盘收口。"
    return "\n".join(lines).strip() + "\n"


def build_routine_issue_lines(snapshot: dict, close_out: bool) -> list[str]:
    lines: list[str] = []
    if snapshot["source_packet_count"] == 0:
        lines.append("输入：本业务日没有拿到任何 source packet。")
    if snapshot["supply_status"] == "insufficient":
        lines.append("输入：topic radar 已标记 supply_status=insufficient，说明有效供给不足。")
    if not snapshot["board_exists"] and snapshot["source_packet_count"] > 0:
        lines.append("选题：Top 8 -> Top 5 建议板尚未形成。")
    if snapshot.get("day_mainline_unbacked_count", 0) > 0:
        lines.append(f"锁题：仍有 {snapshot['day_mainline_unbacked_count']} 个 day_mainline approved-topic 缺少 Top5 正式背书。")
    if snapshot["board_exists"] and snapshot["approved_topic_count"] == 0:
        lines.append("选题：建议板已形成，但 approved-topic 仍为 0。")
    if snapshot["approved_topic_count"] > 0 and snapshot["active_draft_pack_count"] == 0 and snapshot["waiting_publish_count"] == 0 and snapshot["published_count"] == 0:
        lines.append("交付：已有 approved-topic，但还没进入 Draft Pack / 发布队列。")
    if snapshot.get("blocked_final_gate_count", 0) > 0:
        lines.append(f"交付：仍有 {snapshot['blocked_final_gate_count']} 个对象被最终 publish-ready 放行门阻断。")
    if snapshot["approved_topic_count"] > 0 and snapshot.get("premium_ready_count", 0) == 0:
        lines.append("交付：今天虽已有 approved-topic，但还没有对象通过最终 publish-ready 放行门。")
    if snapshot["waiting_publish_count"] > 0:
        waiting = "、".join(snapshot["waiting_publish_topics"][:3])
        unique_topics = snapshot.get("waiting_publish_topic_count", 0)
        topic_suffix = f"，涉及 {unique_topics} 个话题" if unique_topics > 0 else ""
        detail_suffix = f"：{waiting}" if waiting else ""
        lines.append(
            f"发布：仍有 {snapshot['waiting_publish_count']} 个发布任务停在 waiting_human_publish{topic_suffix}{detail_suffix}。"
        )
    if snapshot.get("dirty_waiting_publish_count", 0) > 0:
        lines.append(f"队列：仍有 {snapshot['dirty_waiting_publish_count']} 个脏发布对象待清理。")
    if close_out and snapshot["approved_topic_count"] > 0 and snapshot["published_count"] == 0 and snapshot["waiting_publish_count"] == 0:
        lines.append("收口：今天已拍板选题，但截至晚间还没有稿件进入发布完成态。")
    if close_out and snapshot["source_packet_count"] > 0 and snapshot["approved_topic_count"] == 0:
        lines.append("收口：今天 intake 已收盘，但 approved-topic 仍挂 0。")

    deduped: list[str] = []
    seen: set[str] = set()
    for item in lines:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped[:6]


def build_routine_issue_message(snapshot: dict, close_out: bool, issue_lines: list[str]) -> str:
    label = "内容线日常问题汇报（晚间）" if close_out else "内容线日常问题汇报（晨间）"
    lines = [f"【同行资本｜{label}｜{snapshot['date']}】"]
    for item in issue_lines:
        lines.append(f"- {item}")
    return "\n".join(lines).strip() + "\n"


def should_send_key_sync(snapshot: dict, state: dict, force_send: bool) -> tuple[bool, str, str]:
    signature = hash_signature(snapshot["signature_payload"])
    if force_send:
        return True, "force_send", signature
    if not snapshot["markers"]:
        return False, "no_meaningful_event", signature
    if state.get("last_key_signature") == signature:
        return False, "no_new_signature", signature
    return True, ",".join(snapshot["markers"]), signature


def should_send_close_out(snapshot: dict, state: dict, force_send: bool) -> tuple[bool, str, str]:
    signature = hash_signature(snapshot["signature_payload"])
    if force_send:
        return True, "force_send_close_out", signature
    if not snapshot["has_activity"]:
        return False, "no_activity_today", signature
    if state.get("close_out_sent_for") == snapshot["date"]:
        return False, "close_out_already_sent", signature
    return True, "close_out", signature


def send_group_message(account: str, target: str, message: str, dry_run: bool) -> dict:
    command = [
        "openclaw",
        "message",
        "send",
        "--channel",
        "feishu",
        "--account",
        account,
        "--target",
        target,
        "--message",
        message,
        "--json",
    ]
    if dry_run:
        command.append("--dry-run")
    result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False)
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "unknown delivery error").strip())
    raw = (result.stdout or result.stderr or "").strip()
    if not raw:
        return {"ok": True, "raw": ""}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"ok": True, "raw": raw}


def write_sync_log(
    snapshot: dict,
    mode: str,
    reason: str,
    signature: str,
    account: str,
    target: str,
    message: str,
    delivery_result: dict,
    dry_run: bool,
) -> Path:
    stamp = board_builder.now_cn().strftime("%Y%m%d_%H%M%S")
    log_path = board_builder.LOG_DIR / f"{stamp}{DEFAULT_SYNC_LOG_SUFFIX}"
    ensure_parent(log_path)
    lines = [
        "# Market Frontstage Sync Execution",
        "",
        f"- `date`: `{snapshot['date']}`",
        f"- `generated_at`: `{board_builder.format_ts(board_builder.now_cn())}`",
        f"- `mode`: `{mode}`",
        f"- `reason`: `{reason}`",
        f"- `signature`: `{signature}`",
        f"- `dry_run`: `{'true' if dry_run else 'false'}`",
        f"- `account`: `{account}`",
        f"- `target`: `{target}`",
        f"- `board_path`: `{snapshot['board_path']}`",
        "",
        "## Message",
        "",
        "```text",
        message.rstrip(),
        "```",
        "",
        "## Delivery Result",
        "",
        "```json",
        json.dumps(delivery_result, ensure_ascii=False, indent=2),
        "```",
    ]
    log_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return log_path


def main() -> None:
    args = parse_args()
    state_path = Path(args.state_path)
    state = load_state(state_path)
    snapshot = build_snapshot(args.date, write_board=args.write)
    issue_lines: list[str] = []

    if args.close_out:
        mode = "close_out"
    else:
        mode = "key_sync"

    if args.routine_issues_only:
        issue_lines = build_routine_issue_lines(snapshot, close_out=args.close_out)
        signature = hash_signature({"date": snapshot["date"], "mode": mode, "issues": issue_lines})
        state_key = "last_routine_close_out_signature" if args.close_out else "last_routine_key_signature"
        if args.force_send:
            should_send, reason = True, "force_send"
        elif not issue_lines:
            should_send, reason = False, "no_issues"
        elif state.get(state_key) == signature:
            should_send, reason = False, "no_new_issue_signature"
        else:
            should_send, reason = True, "routine_issues"
    elif args.close_out:
        should_send, reason, signature = should_send_close_out(snapshot, state, args.force_send)
    else:
        should_send, reason, signature = should_send_key_sync(snapshot, state, args.force_send)

    state["last_refresh_at"] = board_builder.format_ts(board_builder.now_cn())
    state["last_board_path"] = str(snapshot["board_path"])
    state["last_board_date"] = snapshot["date"]

    if not should_send:
        save_state(state_path, state)
        print(f"BOARD_PATH={snapshot['board_path']}")
        print("SYNC_STATUS=skipped")
        print(f"SYNC_REASON={reason}")
        print(f"SIGNATURE={signature}")
        return

    if args.routine_issues_only:
        message = build_routine_issue_message(snapshot, close_out=args.close_out, issue_lines=issue_lines)
    else:
        message = build_message(snapshot, close_out=args.close_out)
    delivery_result = send_group_message(args.account, args.target, message, dry_run=args.dry_run)
    log_path = write_sync_log(
        snapshot=snapshot,
        mode=mode,
        reason=reason,
        signature=signature,
        account=args.account,
        target=args.target,
        message=message,
        delivery_result=delivery_result,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        state["last_dry_run_at"] = board_builder.format_ts(board_builder.now_cn())
        state["last_dry_run_log_path"] = str(log_path)
        state["last_dry_run_reason"] = reason
    else:
        if args.routine_issues_only:
            if args.close_out:
                state["last_routine_close_out_signature"] = signature
                state["last_routine_close_out_reason"] = reason
                state["last_routine_close_out_sent_at"] = board_builder.format_ts(board_builder.now_cn())
            else:
                state["last_routine_key_signature"] = signature
                state["last_routine_key_reason"] = reason
                state["last_routine_key_sent_at"] = board_builder.format_ts(board_builder.now_cn())
        else:
            state["last_key_signature"] = signature
            state["last_key_reason"] = reason
            state["last_key_sent_at"] = board_builder.format_ts(board_builder.now_cn())
        state["last_sync_log_path"] = str(log_path)
        if args.close_out:
            state["close_out_sent_for"] = snapshot["date"]
    save_state(state_path, state)

    print(f"BOARD_PATH={snapshot['board_path']}")
    print(f"SYNC_STATUS={'dry_run_sent' if args.dry_run else 'sent'}")
    print(f"SYNC_REASON={reason}")
    print(f"SIGNATURE={signature}")
    print(f"SYNC_LOG={log_path}")


if __name__ == "__main__":
    main()
