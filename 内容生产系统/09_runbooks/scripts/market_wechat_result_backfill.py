#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import ssl
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
QUEUE_ROOT = ROOT / "06_publish_queue"
REVIEW_ROOT = ROOT / "07_performance_reviews"
FRONTSTAGE_DIR = ROOT / "11_frontstage"
METRICS_ROOT = REVIEW_ROOT / "_wechat_metrics"
MANUAL_FEEDBACK_ROOT = REVIEW_ROOT / "_manual_feedback"
OUTBOX_DIR = ROOT / "07_wechat_bridge_outbox"

FIELD_RE_TEMPLATE = r"^(- `{field}`: `)([^`]*)((?:`)\s*)$"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
CN_TZ = ZoneInfo("Asia/Shanghai")
WINDOW_HOURS = {"24h": 24, "72h": 72}
REVIEW_STATUS_ORDER = {"scheduled": 0, "collecting": 1, "ready": 2, "closed": 3}
ACTIVE_TRACK_STATUSES = {"queued", "waiting_human_publish", "published"}
FOLLOWER_CONTEXT_DAYS = 3
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


@dataclass
class QueueItem:
    path: Path
    queue_id: str
    queue_key: str
    topic_id: str
    approved_topic_path: str
    platform: str
    content_path: str
    publish_owner: str
    planned_publish_at: str
    actual_publish_at: str
    publish_url: str
    manual_gate: str
    human_action_required: str
    frontstage_summary: str
    status: str
    notes: str
    title: str


@dataclass
class PublishedArticle:
    article_id: str
    title: str
    url: str
    update_time: int
    publish_id: str
    idx: int

    @property
    def update_dt(self) -> datetime | None:
        if self.update_time <= 0:
            return None
        return datetime.fromtimestamp(self.update_time, CN_TZ)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill WeChat publish URLs and post-publish metrics.")
    parser.add_argument("--queue-root", default=str(QUEUE_ROOT), help="Publish queue root directory")
    parser.add_argument("--review-root", default=str(REVIEW_ROOT), help="Performance review root directory")
    parser.add_argument("--frontstage-dir", default=str(FRONTSTAGE_DIR), help="Frontstage output directory")
    parser.add_argument("--platform", default="wechat", help="Target platform, default wechat")
    parser.add_argument("--recent-days", type=int, default=14, help="Only inspect queue items updated in recent N days")
    parser.add_argument("--page-size", type=int, default=20, help="Published article page size")
    parser.add_argument("--max-pages", type=int, default=5, help="Maximum freepublish pages to inspect")
    parser.add_argument("--appid", default="", help="Optional AppID override")
    parser.add_argument("--secret", default="", help="Optional AppSecret override")
    parser.add_argument("--write", action="store_true", help="Write queue/review/frontstage changes")
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


def parse_cst(raw: str) -> datetime | None:
    raw = clean(raw, "")
    if not raw or raw == "n/a":
        return None
    for fmt in (
        "%Y-%m-%d %H:%M:%S CST",
        "%Y-%m-%d %H:%M CST",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return None


def parse_iso_dt(raw: str) -> datetime | None:
    raw = clean(raw, "")
    if not raw or raw == "n/a":
        return None
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=CN_TZ)
    return dt.astimezone(CN_TZ)


def normalize_title(value: str) -> str:
    return re.sub(r"[^\w]+", "", value or "").lower()


def is_draft_publish_url(value: str) -> bool:
    return clean(value, "").startswith("wechat-draft://")


def classify_official_api_error(raw: str) -> tuple[str, str]:
    message = clean(raw, "n/a")
    ip_match = re.search(r"invalid ip ([^ ,]+)", message)
    if "40164" in message and "not in whitelist" in message:
        blocked_ip = ip_match.group(1) if ip_match else "unknown"
        return "blocked_by_whitelist", f"公众号官方 API 被白名单拦截，当前出口 IP={blocked_ip}"
    return "official_api_error", message


def request_json_call(url: str, payload: dict[str, Any] | None = None, method: str = "GET", timeout: int = 20) -> dict[str, Any]:
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(url, data=body, method=method.upper())
    if body is not None:
        request.add_header("Content-Type", "application/json; charset=utf-8")
    try:
        with urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        response_body = exc.read().decode("utf-8", "ignore")
        raise RuntimeError(f"HTTP {exc.code}: {response_body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


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

    def freepublish_batchget(self, offset: int, count: int, no_content: int = 0) -> dict[str, Any]:
        token = self.ensure_access_token()
        return request_json_call(
            f"https://api.weixin.qq.com/cgi-bin/freepublish/batchget?access_token={token}",
            payload={"offset": offset, "count": count, "no_content": no_content},
            method="POST",
        )

    def article_total_detail(self, publish_date: str) -> dict[str, Any]:
        token = self.ensure_access_token()
        return request_json_call(
            f"https://api.weixin.qq.com/datacube/getarticletotaldetail?access_token={token}",
            payload={"begin_date": publish_date, "end_date": publish_date},
            method="POST",
        )

    def user_summary(self, begin_date: str, end_date: str) -> dict[str, Any]:
        token = self.ensure_access_token()
        return request_json_call(
            f"https://api.weixin.qq.com/datacube/getusersummary?access_token={token}",
            payload={"begin_date": begin_date, "end_date": end_date},
            method="POST",
        )

    def user_cumulate(self, begin_date: str, end_date: str) -> dict[str, Any]:
        token = self.ensure_access_token()
        return request_json_call(
            f"https://api.weixin.qq.com/datacube/getusercumulate?access_token={token}",
            payload={"begin_date": begin_date, "end_date": end_date},
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


def note_value(notes: str, key: str) -> str:
    for chunk in (notes or "").split("|"):
        stripped = chunk.strip()
        if stripped.startswith(f"{key}="):
            return clean(stripped.split("=", 1)[1], "")
    return ""


def manual_feedback_state_path(review_root: Path, item: QueueItem) -> Path:
    return review_root / "_manual_feedback" / f"{item.queue_key}.json"


def load_manual_feedback(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def has_founder_publish_confirmation(item: QueueItem) -> bool:
    return note_value(item.notes, "human_publish_confirmed_by_founder").lower() == "yes"


def bridge_metric_state_path(outbox_dir: Path, item: QueueItem) -> Path:
    request_id = f"wechat_bridge__{queue_topic_key(item)}"
    return outbox_dir / "requests" / request_id / "official_metrics.json"


def bridge_publish_confirmation_path(outbox_dir: Path, item: QueueItem) -> Path:
    request_id = f"wechat_bridge__{queue_topic_key(item)}"
    return outbox_dir / "requests" / request_id / "publish_confirmation.json"


def load_bridge_metric_state(outbox_dir: Path, item: QueueItem) -> dict[str, Any]:
    path = bridge_metric_state_path(outbox_dir, item)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def sync_bridge_publish_confirmation(outbox_dir: Path, item: QueueItem, write: bool) -> str:
    path = bridge_publish_confirmation_path(outbox_dir, item)
    publish_dt, publish_time_source = resolve_publish_dt(item)
    final_publish_url = clean(item.publish_url, "n/a")
    if is_draft_publish_url(final_publish_url):
        final_publish_url = "n/a"
    if item.status != "published" or publish_dt is None:
        if write and path.exists():
            path.unlink()
            return "removed"
        return "noop"
    payload = {
        "status": "published",
        "queue_key": item.queue_key,
        "queue_id": item.queue_id,
        "topic_id": item.topic_id,
        "confirmed_by": note_value(item.notes, "human_publish_confirmed_by") or item.publish_owner,
        "confirmed_at": note_value(item.notes, "human_publish_confirmed_recorded_at") or now_iso(),
        "published_at": format_ts(publish_dt),
        "published_at_iso": publish_dt.isoformat(),
        "publish_url": final_publish_url,
        "publish_time_source": publish_time_source,
        "source": "market_wechat_result_backfill",
    }
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    changed = True
    if path.exists():
        changed = path.read_text(encoding="utf-8") != serialized
    if write and changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(serialized, encoding="utf-8")
        return "written"
    return "unchanged" if not changed else "pending"


def resolve_publish_dt(item: QueueItem) -> tuple[datetime | None, str]:
    actual_dt = parse_cst(item.actual_publish_at)
    if actual_dt:
        return actual_dt, "actual_publish_at"
    publish_update_dt = parse_iso_dt(note_value(item.notes, "wechat_publish_update_time"))
    if publish_update_dt:
        return publish_update_dt, "wechat_publish_update_time"
    confirmed_dt = parse_iso_dt(note_value(item.notes, "human_publish_confirmed_recorded_at"))
    if confirmed_dt:
        return confirmed_dt, "human_publish_confirmed_recorded_at"
    planned_dt = parse_cst(item.planned_publish_at)
    if has_founder_publish_confirmation(item) and planned_dt:
        return planned_dt, "planned_publish_at"
    return planned_dt if item.status == "published" else None, "planned_publish_at_pending" if planned_dt else "missing"


def parse_item_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def extract_markdown_title(path: Path) -> str:
    if not path.exists():
        return path.stem
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith("# "):
            return clean(raw_line[2:].strip(), path.stem)
    return path.stem


def load_queue_items(queue_root: Path, platform: str, recent_days: int) -> list[QueueItem]:
    cutoff = now_cn() - timedelta(days=max(1, recent_days))
    items: list[QueueItem] = []
    for path in sorted(queue_root.glob("*__publish-queue-item.md")):
        if datetime.fromtimestamp(path.stat().st_mtime, CN_TZ) < cutoff:
            continue
        fields = parse_item_fields(path)
        if clean(fields.get("platform", "")) != platform:
            continue
        if clean(fields.get("status", "")) not in ACTIVE_TRACK_STATUSES:
            continue
        content_path = Path(clean(fields.get("content_path", "n/a")))
        items.append(
            QueueItem(
                path=path,
                queue_id=clean(fields.get("queue_id", path.stem)),
                queue_key=clean(fields.get("queue_key", path.stem)),
                topic_id=clean(fields.get("topic_id", "n/a")),
                approved_topic_path=clean(fields.get("approved_topic_path", "n/a")),
                platform=clean(fields.get("platform", "n/a")),
                content_path=str(content_path),
                publish_owner=clean(fields.get("publish_owner", "n/a")),
                planned_publish_at=clean(fields.get("planned_publish_at", "n/a")),
                actual_publish_at=clean(fields.get("actual_publish_at", "n/a")),
                publish_url=clean(fields.get("publish_url", "n/a")),
                manual_gate=clean(fields.get("manual_gate", "n/a")),
                human_action_required=clean(fields.get("human_action_required", "n/a")),
                frontstage_summary=clean(fields.get("frontstage_summary", "n/a")),
                status=clean(fields.get("status", "n/a")),
                notes=clean(fields.get("notes", "n/a")),
                title=extract_markdown_title(content_path),
            )
        )
    return items


def rebuild_queue_board(queue_root: Path) -> Path:
    rows: list[dict[str, str]] = []
    for path in sorted(queue_root.glob("*__publish-queue-item.md")):
        rows.append(parse_item_fields(path))
    status_counts: dict[str, int] = {}
    for row in rows:
        status = row.get("status", "n/a")
        status_counts[status] = status_counts.get(status, 0) + 1
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
        "",
        "## Queue Table",
        "",
        "| queue_id | topic_key | platform | status | manual_gate | publish_owner | planned_publish_at | actual_publish_at | publish_url |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        queue_key = row.get("queue_key", "n/a")
        topic_key = queue_key.rsplit("__", 1)[0] if "__" in queue_key else row.get("topic_id", "n/a")
        lines.append(
            f"| `{row.get('queue_id', 'n/a')}` | `{topic_key}` | `{row.get('platform', 'n/a')}` | `{row.get('status', 'n/a')}` | `{row.get('manual_gate', 'n/a')}` | `{row.get('publish_owner', 'n/a')}` | `{row.get('planned_publish_at', 'n/a')}` | `{row.get('actual_publish_at', 'n/a')}` | `{row.get('publish_url', 'n/a')}` |"
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


def update_approved_topic_status(path_text: str, queue_status: str) -> str:
    mapping = {
        "published": {
            "status": "published",
            "next_step": "published -> performance_review",
        },
        "waiting_human_publish": {
            "status": "waiting_human_publish",
            "next_step": "waiting_human_publish -> human publish / publish_url backfill",
        },
    }
    target = mapping.get(queue_status)
    if not target:
        return path_text
    updated = update_field(path_text, "status", target["status"])
    updated = update_field(updated, "next_step", target["next_step"])
    return updated


def update_draft_pack_card(text: str, queue_status: str) -> str:
    mapping = {
        "published": {
            "status": "published",
            "next_step": "published -> performance_review",
            "publish_gate": "completed",
        },
        "waiting_human_publish": {
            "status": "waiting_human_publish",
            "next_step": "waiting_human_publish -> human publish",
            "publish_gate": "allowed",
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


def sync_status_to_related_docs(item: QueueItem, queue_status: str, write: bool) -> None:
    if item.approved_topic_path != "n/a":
        approved_path = Path(item.approved_topic_path)
        if approved_path.exists():
            updated = update_approved_topic_status(approved_path.read_text(encoding="utf-8"), queue_status)
            if write:
                approved_path.write_text(updated, encoding="utf-8")
    pack_dir = Path(item.content_path).parent
    card_path = pack_dir / "00_draft-pack-card.md"
    if card_path.exists():
        refreshed = refresh_card_paths(card_path.read_text(encoding="utf-8"), pack_dir)
        updated = update_draft_pack_card(refreshed, queue_status)
        if write:
            card_path.write_text(updated, encoding="utf-8")


def fetch_recent_published(client: WeChatOfficialClient, page_size: int, max_pages: int) -> list[PublishedArticle]:
    results: list[PublishedArticle] = []
    offset = 0
    for _ in range(max(1, max_pages)):
        payload = client.freepublish_batchget(offset=offset, count=page_size, no_content=0)
        raw_items = payload.get("item") or []
        total_count = int(payload.get("total_count") or 0)
        if not raw_items:
            break
        for raw_item in raw_items:
            article_id = clean(str(raw_item.get("article_id", "")), "")
            publish_id = clean(str(raw_item.get("publish_id", article_id)), article_id or "n/a")
            update_time = int(raw_item.get("update_time") or 0)
            news_items = ((raw_item.get("content") or {}).get("news_item") or [])
            for idx, news_item in enumerate(news_items, start=1):
                results.append(
                    PublishedArticle(
                        article_id=article_id,
                        title=clean(str(news_item.get("title", "")), ""),
                        url=clean(str(news_item.get("url", "")), ""),
                        update_time=update_time,
                        publish_id=publish_id,
                        idx=idx,
                    )
                )
        offset += len(raw_items)
        if total_count and offset >= total_count:
            break
    results.sort(key=lambda item: item.update_time, reverse=True)
    return results


def match_published_article(item: QueueItem, published_articles: list[PublishedArticle]) -> PublishedArticle | None:
    if item.status == "published" and item.publish_url not in {"n/a", ""}:
        exact = [article for article in published_articles if article.url and article.url == item.publish_url]
        if exact:
            return exact[0]
    normalized_title = normalize_title(item.title)
    if not normalized_title:
        return None
    candidates = [article for article in published_articles if normalize_title(article.title) == normalized_title]
    if not candidates:
        return None
    planned_dt = parse_cst(item.planned_publish_at)
    if planned_dt:
        candidates.sort(
            key=lambda article: (
                0 if article.update_dt and article.update_dt >= planned_dt - timedelta(days=2) else 1,
                abs((article.update_dt or planned_dt) - planned_dt),
            )
        )
        return candidates[0]
    return candidates[0]


def write_queue_item_publish_backfill(item: QueueItem, article: PublishedArticle, write: bool) -> bool:
    original = item.path.read_text(encoding="utf-8")
    updated = original
    actual_publish_at = item.actual_publish_at
    if actual_publish_at == "n/a" and article.update_dt:
        actual_publish_at = format_ts(article.update_dt)
    notes_value = merge_notes(
        item.notes,
        {
            "wechat_publish_sync_source": "freepublish_batchget",
            "wechat_publish_sync_at": now_iso(),
            "wechat_article_id": clean(article.article_id, "n/a"),
            "wechat_publish_update_time": article.update_dt.isoformat() if article.update_dt else "n/a",
            "wechat_publish_title": clean(article.title, "n/a"),
        },
    )
    updated = update_field(updated, "status", "published")
    updated = update_field(updated, "manual_gate", "human_publish_completed")
    updated = update_field(updated, "actual_publish_at", actual_publish_at)
    updated = update_field(updated, "publish_url", clean(article.url, "n/a"))
    updated = update_field(updated, "human_action_required", "wechat 已发，下一步自动回填平台数据并进入 24h / 72h review")
    updated = update_field(updated, "frontstage_summary", "wechat 已发布，结果回流与复盘链路已启动。")
    updated = update_field(updated, "notes", notes_value)
    changed = updated != original
    if write and changed:
        item.path.write_text(updated, encoding="utf-8")
    return changed


def is_official_metrics_ready(publish_dt: datetime, now_dt: datetime) -> tuple[bool, datetime]:
    ready_at = datetime.combine(publish_dt.date() + timedelta(days=1), time(hour=8, minute=0), tzinfo=CN_TZ)
    return now_dt >= ready_at, ready_at


def review_token_from_item(item: QueueItem) -> str:
    publish_dt, _ = resolve_publish_dt(item)
    target_dt = publish_dt or now_cn()
    return target_dt.strftime("%Y%m%d")


def queue_topic_key(item: QueueItem) -> str:
    return item.queue_key.rsplit("__", 1)[0] if "__" in item.queue_key else item.queue_key


def metric_state_path(metrics_root: Path, item: QueueItem) -> Path:
    return metrics_root / f"{item.queue_key}.json"


def load_metric_state(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def latest_scene_breakdown(detail: dict[str, Any]) -> str:
    scene_rows = detail.get("read_user_source") or []
    parts: list[str] = []
    for row in scene_rows[:6]:
        scene = clean(str(row.get("scene_desc", "")), "")
        count = clean(str(row.get("user_count", "")), "")
        if scene and count:
            parts.append(f"{scene}={count}")
    return " | ".join(parts) if parts else "n/a"


def latest_jump_breakdown(detail: dict[str, Any]) -> str:
    rows = detail.get("read_jump_position") or []
    parts: list[str] = []
    for row in rows:
        position = clean(str(row.get("position", "")), "")
        rate = clean(str(row.get("rate", "")), "")
        if position and rate:
            parts.append(f"{position}={rate}")
    return " | ".join(parts) if parts else "n/a"


def build_metric_state(
    client: WeChatOfficialClient | None,
    item: QueueItem,
    published_article: PublishedArticle | None,
    manual_feedback: dict[str, Any],
) -> dict[str, Any]:
    now_dt = now_cn()
    title = item.title
    publish_dt, publish_time_source = resolve_publish_dt(item)
    final_publish_url = clean(item.publish_url, "n/a")
    if is_draft_publish_url(final_publish_url):
        final_publish_url = "n/a"
    base: dict[str, Any] = {
        "queue_id": item.queue_id,
        "queue_key": item.queue_key,
        "topic_id": item.topic_id,
        "title": title,
        "platform": item.platform,
        "publish_owner": item.publish_owner,
        "publish_url": final_publish_url,
        "article_id": "n/a",
        "published_at": format_ts(publish_dt) if publish_dt else item.actual_publish_at,
        "publish_time_source": publish_time_source,
        "captured_at": now_iso(),
        "metric_source": "wechat datacube/getarticletotaldetail",
        "status": "pending",
        "message": "n/a",
        "is_delay": "n/a",
        "publish_date": "n/a",
        "official_ready_at": "n/a",
        "latest_stat_date": "n/a",
        "latest": {},
        "detail_list": [],
        "read_source_breakdown": "n/a",
        "jump_breakdown": "n/a",
        "follower_context": {},
        "follower_summary": "n/a",
        "manual_feedback_present": "yes" if manual_feedback else "no",
    }
    if published_article:
        base["article_id"] = clean(published_article.article_id, "n/a")
        if base["publish_url"] == "n/a":
            base["publish_url"] = clean(published_article.url, "n/a")
        if base["published_at"] == "n/a" and published_article.update_dt:
            base["published_at"] = format_ts(published_article.update_dt)
            publish_dt = published_article.update_dt
            base["publish_time_source"] = "freepublish_batchget"
    if item.status != "published":
        base["status"] = "waiting_publish"
        base["message"] = "queue item is not in published state yet"
        return base
    if not publish_dt:
        base["status"] = "published_time_pending"
        base["message"] = "published confirmed but actual publish timestamp is still missing; run market_human_publish_record.py or wait for founder-confirmed inference"
        return base
    ready, ready_at = is_official_metrics_ready(publish_dt, now_dt)
    base["publish_date"] = publish_dt.date().isoformat()
    base["official_ready_at"] = ready_at.isoformat()
    if not ready:
        base["status"] = "waiting_t_plus_one"
        base["message"] = "official WeChat metrics are T+1 and available after next-day 08:00 CST"
        base["follower_context"] = build_follower_context(client=client, publish_dt=publish_dt, now_dt=now_dt)
        base["follower_summary"] = format_follower_summary(base["follower_context"])
        return base
    if (now_dt.date() - publish_dt.date()).days > 30:
        base["status"] = "expired"
        base["message"] = "official detail API only keeps first 30 days after publish"
        return base
    if client is None:
        base["status"] = "credentials_missing"
        base["message"] = "missing local WeChat credentials on this Mac"
        return base
    try:
        payload = client.article_total_detail(publish_dt.date().isoformat())
    except Exception as exc:
        status, message = classify_official_api_error(str(exc))
        base["status"] = status
        base["message"] = message
        return base
    base["is_delay"] = str(payload.get("is_delay", "n/a")).lower()
    article_rows = payload.get("list") or []
    target_url = clean(str(base["publish_url"]), "")
    target_title = normalize_title(title)
    matched_row = None
    for row in article_rows:
        row_url = clean(str(row.get("content_url", "")), "")
        row_title = clean(str(row.get("title", "")), "")
        if target_url and row_url and row_url == target_url:
            matched_row = row
            break
        if target_title and normalize_title(row_title) == target_title:
            matched_row = row
            break
    if matched_row is None:
        base["status"] = "article_not_found"
        base["message"] = f"published article not found in official datacube list for {publish_dt.date().isoformat()}"
        base["follower_context"] = build_follower_context(client=client, publish_dt=publish_dt, now_dt=now_dt)
        base["follower_summary"] = format_follower_summary(base["follower_context"])
        return base
    detail_list = matched_row.get("detail_list") or []
    latest_detail = detail_list[-1] if detail_list else {}
    base["status"] = "ready"
    base["message"] = "ok"
    base["publish_url"] = clean(str(matched_row.get("content_url", "")), base["publish_url"])
    base["latest_stat_date"] = clean(str(latest_detail.get("stat_date", "")), "n/a")
    base["detail_list"] = detail_list
    base["latest"] = latest_detail
    base["read_source_breakdown"] = latest_scene_breakdown(latest_detail)
    base["jump_breakdown"] = latest_jump_breakdown(latest_detail)
    base["follower_context"] = build_follower_context(client=client, publish_dt=publish_dt, now_dt=now_dt)
    base["follower_summary"] = format_follower_summary(base["follower_context"])
    return base


def build_follower_context(
    client: WeChatOfficialClient | None,
    publish_dt: datetime | None,
    now_dt: datetime,
) -> dict[str, Any]:
    if client is None:
        return {"status": "credentials_missing", "message": "missing local WeChat credentials on this Mac"}
    if publish_dt is None:
        return {"status": "publish_time_missing", "message": "publish timestamp missing"}
    end_day = min(now_dt.date() - timedelta(days=1), publish_dt.date() + timedelta(days=FOLLOWER_CONTEXT_DAYS))
    if end_day < publish_dt.date():
        return {"status": "waiting_t_plus_one", "message": "followers summary is also T+1"}
    begin_text = publish_dt.date().isoformat()
    end_text = end_day.isoformat()
    try:
        summary_payload = client.user_summary(begin_text, end_text)
        cumulate_payload = client.user_cumulate(begin_text, end_text)
    except Exception as exc:
        status, message = classify_official_api_error(str(exc))
        return {"status": status, "message": message}
    summary_rows = summary_payload.get("list") or []
    daily: dict[str, dict[str, int]] = {}
    for row in summary_rows:
        ref_date = clean(str(row.get("ref_date", "")), "")
        if not ref_date:
            continue
        bucket = daily.setdefault(ref_date, {"new_user": 0, "cancel_user": 0, "net_user": 0})
        bucket["new_user"] += int(row.get("new_user") or 0)
        bucket["cancel_user"] += int(row.get("cancel_user") or 0)
    for ref_date, bucket in daily.items():
        bucket["net_user"] = bucket["new_user"] - bucket["cancel_user"]
    cumulate_rows = {
        clean(str(row.get("ref_date", "")), ""): int(row.get("cumulate_user") or 0)
        for row in (cumulate_payload.get("list") or [])
        if clean(str(row.get("ref_date", "")), "")
    }
    ordered_dates = sorted(daily.keys())
    rows: list[dict[str, Any]] = []
    net_total = 0
    for ref_date in ordered_dates:
        bucket = daily[ref_date]
        net_total += bucket["net_user"]
        rows.append(
            {
                "ref_date": ref_date,
                "new_user": bucket["new_user"],
                "cancel_user": bucket["cancel_user"],
                "net_user": bucket["net_user"],
                "cumulate_user": cumulate_rows.get(ref_date, "n/a"),
            }
        )
    return {
        "status": "ready" if rows else "empty",
        "message": "ok" if rows else "no follower summary rows yet",
        "begin_date": begin_text,
        "end_date": end_text,
        "rows": rows,
        "net_total": net_total,
    }


def format_follower_summary(context: dict[str, Any]) -> str:
    if clean(str(context.get("status", "n/a")), "n/a") != "ready":
        return clean(str(context.get("message", "n/a")), "n/a")
    parts: list[str] = []
    for row in (context.get("rows") or [])[: FOLLOWER_CONTEXT_DAYS + 1]:
        ref_date = clean(str(row.get("ref_date", "")), "n/a")
        net_user = clean(str(row.get("net_user", "n/a")), "n/a")
        cumulate_user = clean(str(row.get("cumulate_user", "n/a")), "n/a")
        parts.append(f"{ref_date}: net={net_user}, cumulate={cumulate_user}")
    total = clean(str(context.get("net_total", "n/a")), "n/a")
    return " | ".join(parts + [f"window_net_total={total}"])


def metric_status_priority(status: str) -> int:
    priorities = {
        "ready": 7,
        "waiting_t_plus_one": 6,
        "article_not_found": 5,
        "expired": 4,
        "published_time_pending": 3,
        "blocked_by_whitelist": 2,
        "official_api_error": 2,
        "credentials_missing": 1,
        "ready_empty": 1,
        "waiting_publish": 0,
    }
    return priorities.get(clean(status, "n/a"), 0)


def merge_bridge_metric_state(local_state: dict[str, Any], bridge_state: dict[str, Any], queue_status: str) -> dict[str, Any]:
    if not bridge_state:
        return local_state
    if clean(queue_status, "n/a") != "published":
        bridge_status = clean(str(bridge_state.get("status", "n/a")), "n/a")
        if bridge_status != "waiting_publish":
            return local_state
    if metric_status_priority(clean(str(bridge_state.get("status", "n/a")), "n/a")) < metric_status_priority(
        clean(str(local_state.get("status", "n/a")), "n/a")
    ):
        return local_state
    merged = dict(local_state)
    for key, value in bridge_state.items():
        if key in {"published_at", "publish_time_source"} and clean(str(local_state.get(key, "n/a")), "n/a") != "n/a":
            continue
        if value in (None, "", [], {}):
            continue
        merged[key] = value
    merged["metric_source"] = clean(
        f"{clean(str(local_state.get('metric_source', 'n/a')), 'n/a')} + {clean(str(bridge_state.get('metric_source', 'n/a')), 'n/a')}"
    )
    return merged


def review_status_for_window(
    existing_status: str,
    metric_state: dict[str, Any],
    publish_dt: datetime | None,
    window: str,
    queue_status: str,
) -> str:
    if existing_status == "closed":
        return "closed"
    if queue_status != "published" or publish_dt is None:
        return "scheduled"
    if publish_dt is None:
        computed = "scheduled"
    else:
        age_hours = max(0.0, (now_cn() - publish_dt).total_seconds() / 3600)
        due = age_hours >= WINDOW_HOURS[window]
        if not due:
            computed = "scheduled"
        elif metric_state.get("status") == "ready":
            computed = "ready"
        else:
            computed = "collecting"
    if REVIEW_STATUS_ORDER.get(existing_status, -1) > REVIEW_STATUS_ORDER.get(computed, -1):
        return existing_status
    return computed


def review_file_path(review_root: Path, item: QueueItem, window: str) -> Path:
    return review_root / f"{review_token_from_item(item)}__{queue_topic_key(item)}__{window}-review.md"


def parse_review_fields(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return parse_item_fields(path)


def format_metrics_line(metric_state: dict[str, Any]) -> str:
    if metric_state.get("status") != "ready":
        return clean(metric_state.get("message", "n/a"))
    latest = metric_state.get("latest") or {}
    fields = [
        ("read_user", latest.get("read_user")),
        ("share_user", latest.get("share_user")),
        ("zaikan_user", latest.get("zaikan_user")),
        ("like_user", latest.get("like_user")),
        ("comment_count", latest.get("comment_count")),
        ("collection_user", latest.get("collection_user")),
        ("read_finish_rate", latest.get("read_finish_rate")),
        ("read_avg_activetime_min", latest.get("read_avg_activetime")),
        ("read_subscribe_user", latest.get("read_subscribe_user")),
        ("read_delivery_rate", latest.get("read_delivery_rate")),
        ("praise_money_fen", latest.get("praise_money")),
    ]
    parts = [f"{key}={clean(str(value), 'n/a')}" for key, value in fields]
    return " | ".join(parts)


def format_manual_feedback_line(manual_feedback: dict[str, Any]) -> str:
    if not manual_feedback:
        return "n/a"
    fields = [
        ("private_messages", manual_feedback.get("private_message_count", "0")),
        ("project_leads", manual_feedback.get("project_lead_count", "0")),
        ("business_leads", manual_feedback.get("business_lead_count", "0")),
        ("founder_summary", manual_feedback.get("founder_summary", "n/a")),
    ]
    return " | ".join(f"{key}={clean(str(value), 'n/a')}" for key, value in fields)


def review_text(
    item: QueueItem,
    window: str,
    metric_state: dict[str, Any],
    manual_feedback: dict[str, Any],
    existing: dict[str, str],
) -> str:
    review_path = review_file_path(REVIEW_ROOT, item, window)
    publish_dt, _ = resolve_publish_dt(item)
    computed_status = review_status_for_window(
        clean(existing.get("status", "scheduled")),
        metric_state,
        publish_dt,
        window,
        item.status,
    )
    review_id = clean(
        existing.get(
            "review_id",
            f"review__{review_token_from_item(item)}__{queue_topic_key(item)}__{window}",
        )
    )
    topic_key = queue_topic_key(item)
    note_defaults = {
        "adoption_result": "n/a",
        "title_learnings": "n/a",
        "platform_fit_learnings": "n/a",
        "source_learnings": "n/a",
        "topic_selection_learnings": "n/a",
        "distribution_learnings": "n/a",
        "next_actions": "n/a",
        "workflow_gap": "n/a",
        "skill_update_hint": "n/a",
        "ops_owner_next_action": "n/a",
        "topic_planner_feedback": "n/a",
        "content_writer_feedback": "n/a",
        "publish_ops_feedback": "n/a",
        "content_analyst_feedback": "n/a",
    }
    for key, default in list(note_defaults.items()):
        note_defaults[key] = clean(existing.get(key, default), default)
    if note_defaults["adoption_result"] == "n/a" and manual_feedback:
        note_defaults["adoption_result"] = clean(manual_feedback.get("founder_summary", "n/a"), "n/a")
    if note_defaults["title_learnings"] == "n/a" and manual_feedback:
        note_defaults["title_learnings"] = clean(manual_feedback.get("title_feedback", "n/a"), "n/a")
    if note_defaults["platform_fit_learnings"] == "n/a" and manual_feedback:
        note_defaults["platform_fit_learnings"] = clean(manual_feedback.get("packaging_feedback", "n/a"), "n/a")
    if note_defaults["next_actions"] == "n/a" and manual_feedback:
        note_defaults["next_actions"] = clean(manual_feedback.get("next_topic_hint", "n/a"), "n/a")
    metrics_gap = "n/a"
    if metric_state.get("status") == "waiting_t_plus_one":
        metrics_gap = "wechat official metrics are T+1 only; 24h review can start after next-day 08:00 CST"
    elif metric_state.get("status") != "ready":
        metrics_gap = clean(metric_state.get("message", "n/a"))
    lines = [
        "# Performance Review",
        "",
        f"- `review_id`: `{review_id}`",
        f"- `review_key`: `{topic_key}__{window}`",
        f"- `topic_id`: `{item.topic_id}`",
        f"- `queue_ids`: `{item.queue_id}`",
        f"- `review_window`: `{window}`",
        f"- `status`: `{computed_status}`",
        "",
        "## Publish Evidence",
        "",
        f"- `platform`: `{item.platform}`",
        f"- `title`: `{item.title}`",
        f"- `publish_owner`: `{item.publish_owner}`",
        f"- `published_at`: `{clean(str(metric_state.get('published_at', item.actual_publish_at)), 'n/a')}`",
        f"- `publish_url`: `{clean(str(metric_state.get('publish_url', item.publish_url)), 'n/a')}`",
        f"- `article_id`: `{clean(str(metric_state.get('article_id', 'n/a')), 'n/a')}`",
        f"- `publish_time_source`: `{clean(str(metric_state.get('publish_time_source', 'n/a')), 'n/a')}`",
        "",
        "## Metrics Snapshot",
        "",
        f"- `captured_at`: `{clean(str(metric_state.get('captured_at', 'n/a')), 'n/a')}`",
        f"- `metric_source`: `{clean(str(metric_state.get('metric_source', 'n/a')), 'n/a')}`",
        f"- `metric_status`: `{clean(str(metric_state.get('status', 'n/a')), 'n/a')}`",
        f"- `official_ready_at`: `{clean(str(metric_state.get('official_ready_at', 'n/a')), 'n/a')}`",
        f"- `latest_stat_date`: `{clean(str(metric_state.get('latest_stat_date', 'n/a')), 'n/a')}`",
        f"- `is_delay`: `{clean(str(metric_state.get('is_delay', 'n/a')), 'n/a')}`",
        "",
        "## Platform Metrics",
        "",
        f"- `wechat`: `{format_metrics_line(metric_state)}`",
        "",
        "## Read Source",
        "",
        f"- `wechat`: `{clean(str(metric_state.get('read_source_breakdown', 'n/a')), 'n/a')}`",
        "",
        "## Read Completion",
        "",
        f"- `wechat_jump_breakdown`: `{clean(str(metric_state.get('jump_breakdown', 'n/a')), 'n/a')}`",
        "",
        "## Account Growth Context",
        "",
        f"- `wechat_followers`: `{clean(str(metric_state.get('follower_summary', 'n/a')), 'n/a')}`",
        "",
        "## Current Gaps",
        "",
        f"- `metrics_backfill_gap`: `{metrics_gap}`",
        "- `distribution_context_gap`: `n/a`",
        f"- `comment_or_feedback_gap`: `{'manual feedback captured' if manual_feedback else 'manual feedback pending'}`",
        "",
        "## Frontstage Brief",
        "",
        f"- `wechat`: {item.frontstage_summary}",
        f"- `tracker_path`: `{review_path}`",
        "",
        "## Manual Feedback / Leads",
        "",
        f"- `manual_feedback`: `{format_manual_feedback_line(manual_feedback)}`",
        f"- `notable_comments`: `{clean(' || '.join(manual_feedback.get('notable_comments', [])), 'n/a') if manual_feedback else 'n/a'}`",
        f"- `manual_tags`: `{clean(' | '.join(manual_feedback.get('manual_tags', [])), 'n/a') if manual_feedback else 'n/a'}`",
        "",
        "## Learnings",
        "",
        f"- `adoption_result`: `{note_defaults['adoption_result']}`",
        f"- `title_learnings`: `{note_defaults['title_learnings']}`",
        f"- `platform_fit_learnings`: `{note_defaults['platform_fit_learnings']}`",
        f"- `source_learnings`: `{note_defaults['source_learnings']}`",
        f"- `topic_selection_learnings`: `{note_defaults['topic_selection_learnings']}`",
        f"- `distribution_learnings`: `{note_defaults['distribution_learnings']}`",
        f"- `next_actions`: `{note_defaults['next_actions']}`",
        "",
        "## Workflow Feedback",
        "",
        f"- `workflow_gap`: `{note_defaults['workflow_gap']}`",
        f"- `skill_update_hint`: `{note_defaults['skill_update_hint']}`",
        f"- `ops_owner_next_action`: `{note_defaults['ops_owner_next_action']}`",
        f"- `topic_planner_feedback`: `{note_defaults['topic_planner_feedback']}`",
        f"- `content_writer_feedback`: `{note_defaults['content_writer_feedback']}`",
        f"- `publish_ops_feedback`: `{note_defaults['publish_ops_feedback']}`",
        f"- `content_analyst_feedback`: `{note_defaults['content_analyst_feedback']}`",
    ]
    return "\n".join(lines).rstrip() + "\n"


def upsert_reviews(
    review_root: Path,
    item: QueueItem,
    metric_state: dict[str, Any],
    manual_feedback: dict[str, Any],
    write: bool,
) -> list[Path]:
    written: list[Path] = []
    for window in WINDOW_HOURS:
        path = review_file_path(review_root, item, window)
        existing_fields = parse_review_fields(path)
        content = review_text(item, window, metric_state, manual_feedback, existing_fields)
        if write:
            review_root.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def write_metric_backfill(item: QueueItem, metric_state: dict[str, Any], write: bool) -> bool:
    original = item.path.read_text(encoding="utf-8")
    updated = original
    publish_dt, publish_time_source = resolve_publish_dt(item)
    final_publish_url = clean(str(metric_state.get("publish_url", "n/a")), "n/a")
    if item.actual_publish_at == "n/a" and publish_dt is not None:
        updated = update_field(updated, "actual_publish_at", format_ts(publish_dt))
        updated = update_field(updated, "human_action_required", "人工发布已确认，下一步等待微信官方 T+1 数据与人工补充线索反馈")
        updated = update_field(updated, "frontstage_summary", "稿件已确认发布，系统等待微信官方结果回流。")
    if final_publish_url != "n/a" and not is_draft_publish_url(final_publish_url):
        updated = update_field(updated, "publish_url", final_publish_url)
        updated = update_field(updated, "human_action_required", "公众号已发布，系统将自动追踪 24h / 72h 结果并等待人工补充线索反馈")
        updated = update_field(updated, "frontstage_summary", "公众号已发布，官方结果回流与人工反馈链路已启动。")
    notes_value = merge_notes(
        item.notes,
        {
            "wechat_metrics_backfill_at": now_iso(),
            "wechat_metrics_status": clean(str(metric_state.get("status", "n/a")), "n/a"),
            "wechat_publish_time_inferred_from": publish_time_source if publish_dt is not None else "n/a",
            "human_publish_url_backfill": "done" if final_publish_url != "n/a" else note_value(item.notes, "human_publish_url_backfill") or "required",
        },
    )
    updated = update_field(updated, "notes", notes_value)
    changed = updated != original
    if write and changed:
        item.path.write_text(updated, encoding="utf-8")
    return changed


def build_board_item(
    item: QueueItem,
    metric_state: dict[str, Any],
    manual_feedback: dict[str, Any],
    review_statuses: dict[str, str],
    official_api_state: dict[str, Any],
) -> dict[str, Any]:
    publish_dt, _ = resolve_publish_dt(item)
    latest = metric_state.get("latest") or {}
    next_actions: list[str] = []
    draft_media_id = note_value(item.notes, "wechat_draft_media_id")
    if item.status != "published":
        next_actions.append("等老板发布后自动回填永久链接。")
    elif metric_state.get("status") == "publish_backfill_pending":
        if official_api_state.get("status") == "blocked_by_whitelist":
            next_actions.append(f"{clean(str(official_api_state.get('message', 'n/a')), 'n/a')}；永久链接与发布时间暂时无法自动回填。")
        elif official_api_state.get("status") == "ready_empty":
            if item.manual_gate == "human_publish_completed" and draft_media_id:
                next_actions.append("这条稿件大概率走的是“草稿箱人工发送”链路，freepublish 列表未必可见；后续建议改用 freepublish/submit 正式发布。")
            else:
                next_actions.append("公众号官方 API 已连通，但最近已发布列表返回 0 条；需要核对人工发布记录是否进入 freepublish 列表。")
        else:
            next_actions.append(clean(str(metric_state.get("message", "n/a")), "等待自动回流。"))
    elif metric_state.get("status") == "waiting_t_plus_one":
        ready_at = clean(str(metric_state.get("official_ready_at", "n/a")), "n/a")
        next_actions.append(f"等 `{ready_at}` 后自动拉取微信官方数据。")
    elif metric_state.get("status") == "credentials_missing":
        next_actions.append("先在这台 Mac 配置本地公众号凭据，开启自动结果回流。")
    elif metric_state.get("status") in {"blocked_by_whitelist", "official_api_error"}:
        next_actions.append(clean(str(metric_state.get("message", "n/a")), "公众号官方 API 暂不可用。"))
    elif metric_state.get("status") != "ready":
        next_actions.append(clean(str(metric_state.get("message", "n/a")), "等待自动回流。"))
    else:
        pending_windows = [window for window, status in review_statuses.items() if status != "closed"]
        if pending_windows:
            next_actions.append(
                f"content-analyst 先补 `{pending_windows[0]}` 复盘，再把学习反馈给 topic-planner / content-writer / publish-ops。"
            )
        else:
            next_actions.append("当前 review 已闭环，等待下一条真实表现样本。")
        if not manual_feedback:
            next_actions.append("补一条人工质化反馈：有没有私聊、项目线索、代表性留言，以及这篇最大的成败点。")
    age_hours = round(max(0.0, (now_cn() - publish_dt).total_seconds() / 3600), 1) if publish_dt else "n/a"
    return {
        "queue_id": item.queue_id,
        "queue_key": item.queue_key,
        "topic_key": queue_topic_key(item),
        "title": item.title,
        "status": item.status,
        "publish_owner": item.publish_owner,
        "planned_publish_at": item.planned_publish_at,
        "actual_publish_at": clean(str(metric_state.get("published_at", item.actual_publish_at)), "n/a"),
        "publish_url": item.publish_url,
        "publish_age_hours": age_hours,
        "metric_status": clean(str(metric_state.get("status", "n/a")), "n/a"),
        "latest_stat_date": clean(str(metric_state.get("latest_stat_date", "n/a")), "n/a"),
        "read_user": clean(str(latest.get("read_user", "n/a")), "n/a"),
        "share_user": clean(str(latest.get("share_user", "n/a")), "n/a"),
        "zaikan_user": clean(str(latest.get("zaikan_user", "n/a")), "n/a"),
        "like_user": clean(str(latest.get("like_user", "n/a")), "n/a"),
        "comment_count": clean(str(latest.get("comment_count", "n/a")), "n/a"),
        "collection_user": clean(str(latest.get("collection_user", "n/a")), "n/a"),
        "read_finish_rate": clean(str(latest.get("read_finish_rate", "n/a")), "n/a"),
        "read_avg_activetime": clean(str(latest.get("read_avg_activetime", "n/a")), "n/a"),
        "read_subscribe_user": clean(str(latest.get("read_subscribe_user", "n/a")), "n/a"),
        "follower_summary": clean(str(metric_state.get("follower_summary", "n/a")), "n/a"),
        "manual_feedback": format_manual_feedback_line(manual_feedback),
        "review_statuses": review_statuses,
        "next_actions": next_actions,
        "metric_message": clean(str(metric_state.get("message", "n/a")), "n/a"),
    }


def build_performance_board(
    frontstage_dir: Path,
    items: list[dict[str, Any]],
    official_api_state: dict[str, Any],
    write: bool,
) -> tuple[Path, Path]:
    token = now_cn().strftime("%Y%m%d")
    md_path = frontstage_dir / f"{token}__market-performance-board.md"
    json_path = frontstage_dir / f"{token}__market-performance-board.snapshot.json"
    published_count = sum(1 for item in items if item["status"] == "published")
    metrics_ready_count = sum(1 for item in items if item["metric_status"] == "ready")
    waiting_count = sum(1 for item in items if item["status"] != "published")
    lines = [
        "# Market Performance Board",
        "",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `total_items`: `{len(items)}`",
        f"- `published_items`: `{published_count}`",
        f"- `waiting_publish_items`: `{waiting_count}`",
        f"- `metrics_ready_items`: `{metrics_ready_count}`",
        f"- `wechat_local_credentials`: `{'ready' if official_api_state.get('credentials_available') else 'missing'}`",
        f"- `wechat_official_api_status`: `{clean(str(official_api_state.get('status', 'n/a')), 'n/a')}`",
        f"- `wechat_official_api_note`: `{clean(str(official_api_state.get('message', 'n/a')), 'n/a')}`",
        "",
        "## Tracker Table",
        "",
        "| queue_key | title | status | published_at | metric_status | latest_stat_date | read | share | zaikan | like | comment | collect | finish_rate | avg_read_min | followers | manual_feedback | 24h | 72h |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        review_statuses = item["review_statuses"]
        lines.append(
            f"| `{item['queue_key']}` | {item['title']} | `{item['status']}` | `{item['actual_publish_at']}` | `{item['metric_status']}` | `{item['latest_stat_date']}` | `{item['read_user']}` | `{item['share_user']}` | `{item['zaikan_user']}` | `{item['like_user']}` | `{item['comment_count']}` | `{item['collection_user']}` | `{item['read_finish_rate']}` | `{item['read_avg_activetime']}` | `{item['follower_summary']}` | `{item['manual_feedback']}` | `{review_statuses.get('24h', 'n/a')}` | `{review_statuses.get('72h', 'n/a')}` |"
        )
    lines.extend(["", "## Action Queue", ""])
    if official_api_state.get("status") == "credentials_missing":
        lines.append("- `system`｜这台 Mac 还没有配置本地公众号凭据，永久链接与官方数据自动回流暂时不能真正触发。")
    elif official_api_state.get("status") == "blocked_by_whitelist":
        lines.append(f"- `system`｜{clean(str(official_api_state.get('message', 'n/a')), 'n/a')}；先把当前出口 IP 加到公众号 API 白名单，再自动回填永久链接与官方数据。")
    elif official_api_state.get("status") == "ready_empty":
        lines.append("- `system`｜公众号官方 API 已连通，但 `freepublish/batchget` 最近返回 0 条已发布文章；如果业务走的是“草稿箱人工发送”，这类记录本来就可能不在这条接口里，建议改成 `freepublish/submit` 正式发布。")
    elif official_api_state.get("status") == "official_api_error":
        lines.append(f"- `system`｜公众号官方 API 调用报错：{clean(str(official_api_state.get('message', 'n/a')), 'n/a')}")
    for item in items:
        for action in item["next_actions"]:
            lines.append(f"- `{item['queue_key']}`｜{action}")
    snapshot = {
        "generated_at": now_iso(),
        "total_items": len(items),
        "published_items": published_count,
        "waiting_publish_items": waiting_count,
        "metrics_ready_items": metrics_ready_count,
        "wechat_local_credentials": "ready" if official_api_state.get("credentials_available") else "missing",
        "wechat_official_api": official_api_state,
        "items": items,
    }
    if write:
        frontstage_dir.mkdir(parents=True, exist_ok=True)
        md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md_path, json_path


def main() -> None:
    args = parse_args()
    queue_root = Path(args.queue_root).expanduser().resolve()
    review_root = Path(args.review_root).expanduser().resolve()
    frontstage_dir = Path(args.frontstage_dir).expanduser().resolve()
    outbox_dir = OUTBOX_DIR.expanduser().resolve()
    metrics_root = review_root / "_wechat_metrics"
    metrics_root.mkdir(parents=True, exist_ok=True)
    MANUAL_FEEDBACK_ROOT.mkdir(parents=True, exist_ok=True)

    items = load_queue_items(queue_root=queue_root, platform=args.platform, recent_days=args.recent_days)
    credentials = load_credentials(args.appid, args.secret)
    client = WeChatOfficialClient(*credentials) if credentials else None
    official_api_state: dict[str, Any] = {
        "credentials_available": bool(credentials),
        "status": "credentials_missing" if not credentials else "unknown",
        "message": "missing local WeChat credentials on this Mac" if not credentials else "n/a",
        "published_fetch_count": 0,
        "checked_at": now_iso(),
    }
    if credentials:
        print("CREDENTIALS_READY local WeChat credentials loaded")
    else:
        print("CREDENTIALS_MISSING local WeChat credentials missing on this Mac; publish URL / metrics auto-backfill is pending")

    published_articles: list[PublishedArticle] = []
    if client is not None:
        try:
            published_articles = fetch_recent_published(client, page_size=max(1, args.page_size), max_pages=max(1, args.max_pages))
            official_api_state["published_fetch_count"] = len(published_articles)
            if published_articles:
                official_api_state["status"] = "ready"
                official_api_state["message"] = f"freepublish reachable; fetched {len(published_articles)} published article(s)"
            else:
                official_api_state["status"] = "ready_empty"
                official_api_state["message"] = "freepublish reachable, but returned 0 published article(s)"
            print(f"PUBLISHED_FETCHED count={len(published_articles)}")
        except Exception as exc:
            status, message = classify_official_api_error(str(exc))
            official_api_state["status"] = status
            official_api_state["message"] = message
            print(f"PUBLISHED_FETCH_FAILED {message}")
            published_articles = []

    queue_changed = False
    for item in items:
        matched = match_published_article(item, published_articles)
        if matched is None:
            continue
        if write_queue_item_publish_backfill(item, matched, write=args.write):
            queue_changed = True
            sync_status_to_related_docs(item, "published", write=args.write)
            print(f"QUEUE_PUBLISHED {item.queue_key} -> {matched.url or 'url-pending'}")

    if args.write:
        board_path = rebuild_queue_board(queue_root)
        print(f"QUEUE_BOARD_REBUILT {board_path}")
        if queue_changed:
            items = load_queue_items(queue_root=queue_root, platform=args.platform, recent_days=args.recent_days)

    board_items: list[dict[str, Any]] = []
    for item in items:
        confirmation_sync = sync_bridge_publish_confirmation(outbox_dir, item, write=args.write)
        if confirmation_sync == "written":
            print(f"BRIDGE_PUBLISH_CONFIRMATION {item.queue_key} synced")
        elif confirmation_sync == "removed":
            print(f"BRIDGE_PUBLISH_CONFIRMATION {item.queue_key} cleared")
        matched = match_published_article(item, published_articles)
        manual_feedback = load_manual_feedback(manual_feedback_state_path(review_root, item))
        metric_state = build_metric_state(client=client, item=item, published_article=matched, manual_feedback=manual_feedback)
        metric_state = merge_bridge_metric_state(metric_state, load_bridge_metric_state(outbox_dir, item), item.status)
        metric_path = metric_state_path(metrics_root, item)
        if args.write:
            metric_path.write_text(json.dumps(metric_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if write_metric_backfill(item, metric_state, write=args.write):
            queue_changed = True
            sync_status_to_related_docs(item, "published", write=args.write)
        review_paths = upsert_reviews(
            review_root=review_root,
            item=item,
            metric_state=metric_state,
            manual_feedback=manual_feedback,
            write=args.write,
        )
        review_statuses: dict[str, str] = {}
        for review_path in review_paths:
            fields = parse_review_fields(review_path) if review_path.exists() else {}
            review_statuses[review_path.stem.split("__")[-1].replace("-review", "")] = clean(fields.get("status", "scheduled"))
        board_items.append(
            build_board_item(
                item=item,
                metric_state=metric_state,
                manual_feedback=manual_feedback,
                review_statuses=review_statuses,
                official_api_state=official_api_state,
            )
        )
        print(f"TRACKED {item.queue_key} metric_status={metric_state.get('status', 'n/a')}")

    if args.write and queue_changed:
        board_path = rebuild_queue_board(queue_root)
        print(f"QUEUE_BOARD_REBUILT_POST_METRICS {board_path}")

    md_path, json_path = build_performance_board(
        frontstage_dir=frontstage_dir,
        items=board_items,
        official_api_state=official_api_state,
        write=args.write,
    )
    print(f"PERFORMANCE_BOARD {md_path}")
    print(f"PERFORMANCE_SNAPSHOT {json_path}")


if __name__ == "__main__":
    main()
