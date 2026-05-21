#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import ssl
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
QUEUE_ROOT = ROOT / "06_publish_queue"
FIELD_RE_TEMPLATE = r"^(- `{field}`: `)([^`]*)((?:`)\s*)$"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
CN_TZ = ZoneInfo("Asia/Shanghai")
MAC_CREDENTIAL_PATHS = [
    Path.home() / "Library" / "Application Support" / "THCapital" / "wechat-bridge" / "credentials.json",
    Path.home() / ".config" / "THCapital" / "wechat-bridge" / "credentials.json",
]
CARD_FILE_FIELDS = {
    "wechat_path": "wechat.md",
    "xiaohongshu_path": "xiaohongshu.md",
    "zhihu_path": "zhihu.md",
    "x_path": "x.md",
    "bilibili_path": "bilibili.md",
    "toutiao_path": "toutiao.md",
    "baijiahao_path": "baijiahao.md",
    "title_options_path": "title-options.md",
    "summary_options_path": "summary-options.md",
    "opening_hook_options_path": "opening-hook-options.md",
    "cta_mode_path": "cta-mode.md",
    "packaging_bundle_path": "packaging-bundle.md",
    "context_bridge_path": "context-bridge-notes.md",
    "audience_notes_path": "audience-notes.md",
    "render_plan_path": "platform-render-plan.md",
    "citation_block_path": "citation-block.md",
    "visual_notes_path": "visual-notes.md",
    "inline_visual_plan_path": "inline-visual-plan.md",
    "revision_notes_path": "revision-notes.md",
}
try:
    import certifi  # type: ignore

    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except Exception:
    SSL_CONTEXT = ssl.create_default_context()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit a reviewed WeChat draft through freepublish API and backfill publish metadata."
    )
    parser.add_argument("--queue-item", default="", help="Absolute path to the target publish queue item")
    parser.add_argument("--queue-key", default="", help="queue_key to resolve under the queue root")
    parser.add_argument("--queue-root", default=str(QUEUE_ROOT), help="Publish queue root directory")
    parser.add_argument("--appid", default="", help="Optional AppID override")
    parser.add_argument("--secret", default="", help="Optional AppSecret override")
    parser.add_argument("--poll-seconds", type=int, default=5, help="Polling interval for freepublish/get")
    parser.add_argument("--timeout-seconds", type=int, default=180, help="Overall timeout for waiting publish success")
    parser.add_argument("--dry-run", action="store_true", help="Only validate target item and draft media_id")
    parser.add_argument("--write", action="store_true", help="Write queue item and related doc updates")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def now_iso() -> str:
    return now_cn().isoformat()


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def request_json_call(url: str, payload: dict[str, Any] | None = None, method: str = "GET", timeout: int = 20, _retries: int = 3) -> dict[str, Any]:
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(url, data=body, method=method.upper())
    if body is not None:
        request.add_header("Content-Type", "application/json; charset=utf-8")
    last_exc: Exception | None = None
    for attempt in range(_retries):
        try:
            with urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            response_body = exc.read().decode("utf-8", "ignore")
            last_exc = RuntimeError(f"HTTP {exc.code}: {response_body}")
            if exc.code >= 500 and attempt < _retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise last_exc from exc
        except URLError as exc:
            last_exc = RuntimeError(f"Network error: {exc}")
            if attempt < _retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise last_exc from exc
    raise last_exc or RuntimeError("request_json_call failed after retries")


def load_credentials(appid: str, secret: str) -> tuple[str, str] | None:
    if appid.strip() and secret.strip():
        return appid.strip(), secret.strip()
    env_appid = ""
    env_secret = ""
    try:
        import os

        env_appid = clean(os.environ.get("TH_WECHAT_APPID", ""), "")
        env_secret = clean(os.environ.get("TH_WECHAT_APPSECRET", ""), "")
    except Exception:
        env_appid = ""
        env_secret = ""
    if env_appid and env_secret:
        return env_appid, env_secret
    for path in MAC_CREDENTIAL_PATHS:
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        file_appid = clean(str(payload.get("appid", "")), "")
        file_secret = clean(str(payload.get("secret", "")), "")
        if file_appid and file_secret:
            return file_appid, file_secret
    return None


class WeChatOfficialClient:
    def __init__(self, appid: str, secret: str):
        self.appid = appid
        self.secret = secret
        self.access_token = ""

    def ensure_access_token(self) -> str:
        if self.access_token:
            return self.access_token
        qs = urlencode({"grant_type": "client_credential", "appid": self.appid, "secret": self.secret})
        payload = request_json_call(f"https://api.weixin.qq.com/cgi-bin/token?{qs}")
        token = clean(str(payload.get("access_token", "")), "")
        if not token:
            raise RuntimeError(f"access_token failed: {payload}")
        self.access_token = token
        return token

    def freepublish_submit(self, media_id: str) -> dict[str, Any]:
        token = self.ensure_access_token()
        return request_json_call(
            f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}",
            payload={"media_id": media_id},
            method="POST",
        )

    def freepublish_get(self, publish_id: str) -> dict[str, Any]:
        token = self.ensure_access_token()
        return request_json_call(
            f"https://api.weixin.qq.com/cgi-bin/freepublish/get?access_token={token}",
            payload={"publish_id": publish_id},
            method="POST",
        )


def update_field(text: str, field: str, value: str) -> str:
    pattern = re.compile(FIELD_RE_TEMPLATE.format(field=re.escape(field)), re.M)
    if pattern.search(text):
        return pattern.sub(lambda match: f"{match.group(1)}{value}{match.group(3)}", text, count=1)
    return text


def refresh_card_paths(text: str, pack_dir: Path) -> str:
    updated = text
    for field_name, filename in CARD_FILE_FIELDS.items():
        candidate = pack_dir / filename
        updated = update_field(updated, field_name, str(candidate) if candidate.exists() else "n/a")
    return updated


def merge_notes(existing: str, extras: dict[str, str]) -> str:
    chunks = [item.strip() for item in existing.split("|") if item.strip() and item.strip() != "n/a"]
    filtered = [chunk for chunk in chunks if not any(chunk.startswith(f"{key}=") for key in extras)]
    for key, value in extras.items():
        filtered.append(f"{key}={value}")
    return " | ".join(filtered) if filtered else "n/a"


def parse_item_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def resolve_queue_item_path(queue_root: Path, queue_item: str, queue_key: str) -> Path:
    if queue_item.strip():
        path = Path(queue_item).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"queue item not found: {path}")
        return path
    if not queue_key.strip():
        raise SystemExit("provide either --queue-item or --queue-key")
    matches = sorted(queue_root.glob(f"*__{queue_key}__publish-queue-item.md"))
    if not matches:
        raise SystemExit(f"queue_key not found under {queue_root}: {queue_key}")
    if len(matches) > 1:
        raise SystemExit(f"queue_key matched multiple items, please use --queue-item: {queue_key}")
    return matches[0]


def extract_note_value(notes: str, key: str) -> str:
    for chunk in notes.split("|"):
        stripped = chunk.strip()
        if stripped.startswith(f"{key}="):
            return clean(stripped.split("=", 1)[1], "")
    return ""


def extract_media_id(fields: dict[str, str]) -> str:
    publish_url = clean(fields.get("publish_url", ""), "")
    if publish_url.startswith("wechat-draft://"):
        return publish_url.split("wechat-draft://", 1)[1].strip()
    notes = clean(fields.get("notes", ""), "")
    return extract_note_value(notes, "wechat_draft_media_id")


def update_approved_topic_status(text: str, queue_status: str) -> str:
    mapping = {
        "published": {
            "status": "published",
            "next_step": "published -> performance_review",
        },
    }
    target = mapping.get(queue_status)
    if not target:
        return text
    updated = update_field(text, "status", target["status"])
    updated = update_field(updated, "next_step", target["next_step"])
    return updated


def update_draft_pack_card(text: str, queue_status: str) -> str:
    mapping = {
        "published": {
            "status": "published",
            "next_step": "published -> performance_review",
            "publish_gate": "completed",
        },
    }
    target = mapping.get(queue_status)
    if not target:
        return text
    updated = update_field(text, "status", target["status"])
    updated = update_field(updated, "next_step", target["next_step"])
    updated = update_field(updated, "publish_gate", target["publish_gate"])
    updated = update_field(updated, "updated_at", format_ts(now_cn()))
    return updated


def sync_status_to_related_docs(fields: dict[str, str], write: bool) -> None:
    approved_topic_path = Path(clean(fields.get("approved_topic_path", "n/a")))
    if approved_topic_path.exists():
        updated = update_approved_topic_status(approved_topic_path.read_text(encoding="utf-8"), "published")
        if write:
            approved_topic_path.write_text(updated, encoding="utf-8")
    content_path = Path(clean(fields.get("content_path", "n/a")))
    card_path = content_path.parent / "00_draft-pack-card.md"
    if card_path.exists():
        refreshed = refresh_card_paths(card_path.read_text(encoding="utf-8"), content_path.parent)
        updated = update_draft_pack_card(refreshed, "published")
        if write:
            card_path.write_text(updated, encoding="utf-8")


def rebuild_queue_board(queue_root: Path) -> Path:
    rows = [parse_item_fields(path) for path in sorted(queue_root.glob("*__publish-queue-item.md"))]
    status_counts: dict[str, int] = {}
    lane_counts: dict[str, int] = {}
    for row in rows:
        status = row.get("status", "n/a")
        status_counts[status] = status_counts.get(status, 0) + 1
        lane = row.get("delivery_lane", "n/a")
        lane_counts[lane] = lane_counts.get(lane, 0) + 1
    lines = [
        "# Publish Queue Board",
        "",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `total_items`: `{len(rows)}`",
        f"- `queued_items`: `{status_counts.get('queued', 0)}`",
        f"- `waiting_human_publish_items`: `{status_counts.get('waiting_human_publish', 0)}`",
        f"- `published_items`: `{status_counts.get('published', 0)}`",
        f"- `deferred_items`: `{status_counts.get('deferred', 0)}`",
        f"- `cancelled_items`: `{status_counts.get('cancelled', 0)}`",
        f"- `morning_flash_items`: `{lane_counts.get('morning_flash', 0)}`",
        f"- `day_mainline_items`: `{lane_counts.get('day_mainline', 0)}`",
        "",
        "## Queue Table",
        "",
        "| queue_id | topic_key | lane | publish_mode | platform | status | manual_gate | publish_owner | planned_publish_at | actual_publish_at | publish_url |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        queue_key = row.get("queue_key", "n/a")
        topic_key = queue_key.rsplit("__", 1)[0] if "__" in queue_key else row.get("topic_id", "n/a")
        lines.append(
            f"| `{row.get('queue_id', 'n/a')}` | `{topic_key}` | `{row.get('delivery_lane', 'n/a')}` | `{row.get('publish_mode', 'n/a')}` | `{row.get('platform', 'n/a')}` | `{row.get('status', 'n/a')}` | `{row.get('manual_gate', 'n/a')}` | `{row.get('publish_owner', 'n/a')}` | `{row.get('planned_publish_at', 'n/a')}` | `{row.get('actual_publish_at', 'n/a')}` | `{row.get('publish_url', 'n/a')}` |"
        )
    lines.extend(["", "## Human Action Queue", ""])
    action_rows = [row for row in rows if row.get("status") in {"queued", "waiting_human_publish", "deferred"}]
    if action_rows:
        for row in action_rows:
            lines.append(
                f"- `{row.get('queue_key', 'n/a')}`｜{row.get('human_action_required', 'n/a')}｜前台摘要：{row.get('frontstage_summary', 'n/a')}"
            )
    else:
        lines.append("- `none`")
    lines.extend(["", "## Published / Review Follow-up", ""])
    published_rows = [row for row in rows if row.get("status") == "published"]
    if published_rows:
        for row in published_rows:
            lines.append(
                f"- `{row.get('queue_key', 'n/a')}`｜URL：`{row.get('publish_url', 'n/a')}`｜下一步：{row.get('human_action_required', 'n/a')}"
            )
    else:
        lines.append("- `none`")
    board_path = queue_root / f"{now_cn().strftime('%Y%m%d')}__publish-queue-board.md"
    board_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return board_path


def publish_status_label(publish_status: int) -> str:
    mapping = {
        0: "success",
        1: "publishing",
        2: "original_failed",
        3: "general_failed",
        4: "platform_rejected",
        5: "deleted_after_success",
        6: "blocked_after_success",
    }
    return mapping.get(publish_status, f"unknown_{publish_status}")


def first_article_url(payload: dict[str, Any]) -> str:
    article_detail = payload.get("article_detail") or {}
    items = article_detail.get("item") or []
    for item in items:
        url = clean(str(item.get("article_url", "")), "")
        if url:
            return url
    return ""


def submit_and_wait(client: WeChatOfficialClient, media_id: str, poll_seconds: int, timeout_seconds: int) -> tuple[dict[str, Any], str, str]:
    submit_payload = client.freepublish_submit(media_id)
    publish_id = clean(str(submit_payload.get("publish_id", "")), "")
    msg_data_id = clean(str(submit_payload.get("msg_data_id", "")), "")
    if not publish_id:
        raise RuntimeError(f"freepublish_submit failed: {submit_payload}")
    started_at = time.time()
    last_payload = submit_payload
    while True:
        current = client.freepublish_get(publish_id)
        last_payload = current
        publish_status = int(current.get("publish_status") or -1)
        if publish_status != 1:
            return current, publish_id, msg_data_id
        if time.time() - started_at >= timeout_seconds:
            raise RuntimeError(f"publish still running after {timeout_seconds}s: {current}")
        time.sleep(max(1, poll_seconds))


def main() -> None:
    args = parse_args()
    queue_root = Path(args.queue_root).expanduser().resolve()
    queue_item_path = resolve_queue_item_path(queue_root, args.queue_item, args.queue_key)
    fields = parse_item_fields(queue_item_path)
    if clean(fields.get("platform", "")) != "wechat":
        raise SystemExit(f"queue item is not wechat: {queue_item_path}")
    media_id = extract_media_id(fields)
    if not media_id:
        raise SystemExit(f"missing wechat draft media_id in queue item: {queue_item_path}")
    credentials = load_credentials(args.appid, args.secret)
    if credentials is None:
        raise SystemExit("missing local WeChat credentials on this Mac")
    if args.dry_run:
        print(f"DRY_RUN queue_item={queue_item_path}")
        print(f"DRY_RUN queue_key={fields.get('queue_key', 'n/a')}")
        print(f"DRY_RUN media_id={media_id}")
        print("DRY_RUN credentials=ready")
        return

    client = WeChatOfficialClient(*credentials)
    success_observed_at = now_cn()
    payload, publish_id, msg_data_id = submit_and_wait(
        client=client,
        media_id=media_id,
        poll_seconds=max(1, args.poll_seconds),
        timeout_seconds=max(10, args.timeout_seconds),
    )
    publish_status = int(payload.get("publish_status") or -1)
    status_label = publish_status_label(publish_status)
    article_id = clean(str(payload.get("article_id", "")), "")
    article_url = first_article_url(payload)
    if publish_status != 0 or not article_url:
        raise SystemExit(
            f"publish not successful: publish_status={publish_status} ({status_label}), article_id={article_id or 'n/a'}, payload={payload}"
        )

    original = queue_item_path.read_text(encoding="utf-8")
    updated = original
    notes_value = merge_notes(
        clean(fields.get("notes", "n/a")),
        {
            "wechat_publish_route": "freepublish_submit",
            "wechat_publish_submit_at": now_iso(),
            "wechat_publish_id": publish_id,
            "wechat_publish_msg_data_id": msg_data_id or "n/a",
            "wechat_publish_status": status_label,
            "wechat_publish_success_observed_at": success_observed_at.isoformat(),
            "wechat_article_id": article_id or "n/a",
            "wechat_publish_url_source": "freepublish_get",
        },
    )
    updated = update_field(updated, "status", "published")
    updated = update_field(updated, "manual_gate", "api_publish_completed")
    updated = update_field(updated, "actual_publish_at", format_ts(success_observed_at))
    updated = update_field(updated, "publish_url", article_url)
    updated = update_field(updated, "human_action_required", "wechat 已通过 freepublish API 成功发布，下一步自动进入 24h / 72h review")
    updated = update_field(updated, "frontstage_summary", "wechat 已通过 API 发布，结果回流与复盘链路已启动。")
    updated = update_field(updated, "notes", notes_value)
    changed = updated != original
    if args.write and changed:
        queue_item_path.write_text(updated, encoding="utf-8")
        sync_status_to_related_docs(parse_item_fields(queue_item_path), write=True)
        board_path = rebuild_queue_board(queue_root)
        print(f"QUEUE_UPDATED {queue_item_path}")
        print(f"QUEUE_BOARD_REBUILT {board_path}")
    print(f"PUBLISH_SUCCESS queue_key={fields.get('queue_key', 'n/a')} publish_id={publish_id} article_id={article_id or 'n/a'}")
    print(f"PUBLISH_URL {article_url}")


if __name__ == "__main__":
    main()
