#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
QUEUE_ROOT = ROOT / "06_publish_queue"
INTAKE_ROOT = ROOT / "12_public_intake_requests"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
CN_TZ = ZoneInfo("Asia/Shanghai")

TYPE_ROUTE_MAP = {
    "content_request": "market_content_factory",
    "research_request": "vc_research",
    "project_review_request": "vc_project_line",
    "cooperation_request": "market_business_dev",
    "unknown_request": "founder_triage",
}

TYPE_KEYWORDS = {
    "content_request": [
        "写一篇",
        "拆解",
        "聊聊",
        "内容",
        "选题",
        "文章",
        "稿子",
        "话题",
        "怎么看",
    ],
    "research_request": [
        "研究",
        "行业",
        "赛道",
        "梳理",
        "报告",
        "调研",
        "分析一下",
        "分析下",
    ],
    "project_review_request": [
        "项目",
        "bp",
        "商业计划书",
        "融资",
        "投资",
        "尽调",
        "看看这个项目",
        "帮我看看项目",
    ],
    "cooperation_request": [
        "合作",
        "推广",
        "对接",
        "商务",
        "投放",
        "联名",
        "渠道",
        "置换",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record public-facing business requests from wechat comments or messages.")
    parser.add_argument("--source-platform", default="wechat")
    parser.add_argument("--source-channel", default="wechat_comment")
    parser.add_argument("--source-message-id", default="")
    parser.add_argument("--queue-item", default="", help="Absolute publish queue item path")
    parser.add_argument("--queue-key", default="", help="queue_key under publish queue root")
    parser.add_argument("--queue-root", default=str(QUEUE_ROOT))
    parser.add_argument("--intake-root", default=str(INTAKE_ROOT))
    parser.add_argument("--requester-handle", default="")
    parser.add_argument("--submitted-at", default="")
    parser.add_argument("--message-text", default="")
    parser.add_argument("--message-file", default="")
    parser.add_argument(
        "--request-type",
        default="auto",
        choices=[
            "auto",
            "content_request",
            "research_request",
            "project_review_request",
            "cooperation_request",
            "unknown_request",
        ],
    )
    parser.add_argument("--priority-hint", default="normal", choices=["normal", "elevated"])
    parser.add_argument("--manual-tag", action="append", default=[])
    parser.add_argument("--note", action="append", default=[])
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def clean(value: str, fallback: str = "") -> str:
    text = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return text if text else fallback


def slugify(text: str) -> str:
    text = clean(text).lower()
    text = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:48] or "public-intake"


def parse_queue_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if match:
            key, value = match.groups()
            fields[key] = clean(value)
    return fields


def resolve_queue_item_path(queue_root: Path, queue_item: str, queue_key: str) -> Path | None:
    if clean(queue_item):
        path = Path(queue_item).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"queue item not found: {path}")
        return path
    if not clean(queue_key):
        return None
    matches = sorted(queue_root.glob(f"*__{queue_key}__publish-queue-item.md"))
    if not matches:
        raise SystemExit(f"queue_key not found under {queue_root}: {queue_key}")
    if len(matches) > 1:
        raise SystemExit(f"queue_key matched multiple items, please use --queue-item: {queue_key}")
    return matches[0]


def resolve_message_text(args: argparse.Namespace) -> str:
    direct = clean(args.message_text)
    if direct:
        return direct
    message_file = clean(args.message_file)
    if message_file:
        path = Path(message_file).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"message file not found: {path}")
        return clean(path.read_text(encoding="utf-8", errors="ignore"))
    raise SystemExit("provide either --message-text or --message-file")


def classify_request_type(text: str) -> tuple[str, str, list[str], str]:
    lowered = text.lower()
    scores = {key: 0 for key in TYPE_KEYWORDS}
    matched_tags: list[str] = []

    for request_type, keywords in TYPE_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in lowered:
                scores[request_type] += 1
                matched_tags.append(keyword)

    # 项目相关优先级高于泛研究，避免“研究某个项目”被打成行业研究。
    if scores["project_review_request"] > 0:
        scores["project_review_request"] += 1
    if "合作" in text and ("项目" in text or "推广" in text):
        scores["cooperation_request"] += 1

    winner = max(scores, key=scores.get)
    top_score = scores[winner]
    if top_score == 0:
        return "unknown_request", "low", [], "no strong keyword hit; founder should triage manually"

    nonzero_types = [request_type for request_type, score in scores.items() if score > 0]
    ordered_scores = sorted(scores.values(), reverse=True)
    second_score = ordered_scores[1] if len(ordered_scores) > 1 else 0
    confidence = "high" if top_score >= 2 and top_score >= second_score + 1 else "medium"
    if top_score == second_score:
        confidence = "low"
    elif len(nonzero_types) > 1 and top_score < second_score + 2:
        confidence = "medium"

    rationale = (
        f"keyword hits={top_score}; matched_types={','.join(nonzero_types)}; "
        f"nearest route={TYPE_ROUTE_MAP[winner]}"
    )
    return winner, confidence, sorted(set(matched_tags)), rationale


def build_normalized_brief(request_type: str, text: str) -> str:
    prefix = {
        "content_request": "内容需求",
        "research_request": "研究需求",
        "project_review_request": "项目评估需求",
        "cooperation_request": "合作/推广需求",
        "unknown_request": "待创始人分诊需求",
    }[request_type]
    return compact(f"{prefix}：{text}", 96)


def compact(text: str, limit: int = 96) -> str:
    cleaned = clean(text)
    return cleaned if len(cleaned) <= limit else cleaned[: limit - 1] + "…"


def render_markdown(payload: dict[str, str], original_message: str, notes: list[str]) -> str:
    lines = [
        "# market public intake request",
        "",
        f"- `request_id`: `{payload['request_id']}`",
        f"- `created_at`: `{payload['created_at']}`",
        f"- `source_platform`: `{payload['source_platform']}`",
        f"- `source_channel`: `{payload['source_channel']}`",
        f"- `source_message_id`: `{payload['source_message_id'] or 'n/a'}`",
        f"- `source_article_queue_key`: `{payload['source_article_queue_key'] or 'n/a'}`",
        f"- `source_article_title`: `{payload['source_article_title'] or 'n/a'}`",
        f"- `requester_handle`: `{payload['requester_handle'] or 'anonymous'}`",
        f"- `submitted_at`: `{payload['submitted_at']}`",
        f"- `normalized_request_type`: `{payload['normalized_request_type']}`",
        f"- `routed_department`: `{payload['routed_department']}`",
        f"- `classification_confidence`: `{payload['classification_confidence']}`",
        f"- `status`: `{payload['status']}`",
        f"- `followup_mode`: `{payload['followup_mode']}`",
        f"- `priority_hint`: `{payload['priority_hint']}`",
        f"- `tags`: `{payload['tags'] or 'n/a'}`",
        f"- `normalized_brief`: `{payload['normalized_brief']}`",
        f"- `routing_rationale`: `{payload['routing_rationale']}`",
        f"- `next_action`: `{payload['next_action']}`",
        "",
        "## Original Message",
        "",
        original_message,
        "",
        "## Notes",
        "",
    ]
    if notes:
        for note in notes:
            lines.append(f"- {note}")
    else:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    queue_root = Path(args.queue_root).expanduser().resolve()
    intake_root = Path(args.intake_root).expanduser().resolve()
    queue_item_path = resolve_queue_item_path(queue_root, args.queue_item, args.queue_key)
    queue_fields = parse_queue_fields(queue_item_path) if queue_item_path else {}
    message_text = resolve_message_text(args)

    if args.request_type == "auto":
        request_type, confidence, auto_tags, rationale = classify_request_type(message_text)
    else:
        request_type = args.request_type
        confidence = "medium"
        auto_tags = []
        rationale = "manually assigned by operator"

    routed_department = TYPE_ROUTE_MAP[request_type]
    created_at = now_cn()
    submitted_at = clean(args.submitted_at) or created_at.isoformat()
    request_id = f"{created_at.strftime('%Y%m%d_%H%M%S')}__{slugify(message_text)}"
    article_queue_key = clean(queue_fields.get("queue_key", ""))
    article_title = clean(queue_fields.get("title", ""))

    tags = sorted(set([*auto_tags, *(clean(tag) for tag in args.manual_tag if clean(tag))]))
    notes = [clean(note) for note in args.note if clean(note)]
    next_action = {
        "market_content_factory": "进入内容选题或留言反哺池，等待内容岗消化",
        "vc_research": "进入 VC 研究分诊，判断是否形成行业/赛道研究输入",
        "vc_project_line": "进入项目评估分诊，判断是否值得形成项目研究对象",
        "market_business_dev": "进入合作/推广分诊，等待人工商务判断",
        "founder_triage": "先人工看一眼，避免错分流",
    }[routed_department]

    payload = {
        "request_id": request_id,
        "created_at": created_at.isoformat(),
        "source_platform": clean(args.source_platform, "wechat"),
        "source_channel": clean(args.source_channel, "wechat_comment"),
        "source_message_id": clean(args.source_message_id),
        "source_article_queue_key": article_queue_key,
        "source_article_title": article_title,
        "requester_handle": clean(args.requester_handle),
        "submitted_at": submitted_at,
        "normalized_request_type": request_type,
        "routed_department": routed_department,
        "classification_confidence": confidence,
        "status": "pending_triage",
        "followup_mode": "manual_first_phase",
        "priority_hint": clean(args.priority_hint, "normal"),
        "tags": "; ".join(tags),
        "normalized_brief": build_normalized_brief(request_type, message_text),
        "routing_rationale": rationale,
        "next_action": next_action,
    }
    output_path = intake_root / f"{request_id}__public-intake-request.md"
    rendered = render_markdown(payload, message_text, notes)

    if args.write:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    print(output_path)
    if not args.write:
        print(rendered)


if __name__ == "__main__":
    main()
