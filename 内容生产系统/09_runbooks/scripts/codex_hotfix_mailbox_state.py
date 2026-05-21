#!/usr/bin/env python3
"""State helper for the Codex hotfix mailbox."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


HOTFIX_DIR = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统/07_wechat_bridge_outbox/codex_content_hotfix")
REQUEST_PATH = HOTFIX_DIR / "老板给Codex.md"
REPLY_PATH = HOTFIX_DIR / "Codex回复.md"
STATE_PATH = HOTFIX_DIR / "Codex状态.json"
LOG_PATH = HOTFIX_DIR / "处理记录.md"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def read_state(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def request_preview(text: str, limit: int = 120) -> str:
    cleaned = " ".join(line.strip() for line in text.splitlines() if line.strip())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1] + "…"


def now_cst() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S CST")


def build_status() -> dict[str, object]:
    request_text = read_text(REQUEST_PATH)
    reply_text = read_text(REPLY_PATH)
    state = read_state(STATE_PATH)

    normalized_request = request_text.strip()
    request_sha = sha256_text(request_text) if request_text else ""
    reply_sha = sha256_text(reply_text) if reply_text else ""
    last_processed_sha = str(state.get("last_processed_request_sha256", "")).strip()

    return {
        "request_path": str(REQUEST_PATH),
        "reply_path": str(REPLY_PATH),
        "state_path": str(STATE_PATH),
        "log_path": str(LOG_PATH),
        "request_exists": REQUEST_PATH.exists(),
        "reply_exists": REPLY_PATH.exists(),
        "state_exists": STATE_PATH.exists(),
        "request_sha256": request_sha,
        "reply_sha256": reply_sha,
        "request_preview": request_preview(request_text),
        "request_is_empty": normalized_request == "",
        "last_processed_request_sha256": last_processed_sha,
        "last_processed_at": state.get("last_processed_at", ""),
        "last_processed_summary": state.get("last_processed_summary", ""),
        "has_new_request": normalized_request != "" and request_sha != "" and request_sha != last_processed_sha,
    }


def write_state(summary: str) -> dict[str, object]:
    status = build_status()
    request_text = read_text(REQUEST_PATH)
    reply_text = read_text(REPLY_PATH)
    reply_preview = request_preview(reply_text, limit=160)

    payload = {
        "updated_at": now_cst(),
        "request_path": str(REQUEST_PATH),
        "reply_path": str(REPLY_PATH),
        "log_path": str(LOG_PATH),
        "last_processed_at": now_cst(),
        "last_processed_request_sha256": status["request_sha256"],
        "last_processed_request_preview": status["request_preview"],
        "last_processed_summary": summary.strip(),
        "last_reply_sha256": sha256_text(reply_text) if reply_text else "",
        "last_reply_preview": reply_preview,
        "request_is_empty": status["request_is_empty"],
    }
    STATE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    append_log(payload)
    return payload


def append_log(payload: dict[str, object]) -> None:
    if not LOG_PATH.exists():
        LOG_PATH.write_text("# Codex 处理记录\n\n", encoding="utf-8")
    lines = [
        f"## {payload.get('last_processed_at', now_cst())}",
        "",
        f"- request_sha256: `{payload.get('last_processed_request_sha256', '')}`",
        f"- 请求摘要: {payload.get('last_processed_request_preview', '') or 'none'}",
        f"- 处理摘要: {payload.get('last_processed_summary', '') or 'none'}",
        "",
    ]
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage Codex hotfix mailbox state")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="show current mailbox state")
    status_parser.add_argument("--json", action="store_true", help="print JSON only")

    mark_parser = subparsers.add_parser("mark-processed", help="mark current request as processed")
    mark_parser.add_argument("--summary", required=True, help="short processing summary")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "status":
        status = build_status()
        if args.json:
            print(json.dumps(status, ensure_ascii=False, indent=2))
            return
        for key, value in status.items():
            print(f"{key}: {value}")
        return

    if args.command == "mark-processed":
        payload = write_state(args.summary)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
