#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_content_hygiene_guard import inspect_content_hygiene
from market_content_pack_truth import ContentPackVerdict, latest_content_pack_verdict


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
DRAFT_PACK_ROOT = ROOT / "05_draft_packs"
QUEUE_DIR = ROOT / "06_publish_queue"
LOG_DIR = ROOT / "10_logs"
QUEUE_BUILDER_SCRIPT = ROOT / "09_runbooks" / "scripts" / "market_publish_queue_builder.py"
CN_TZ = ZoneInfo("Asia/Shanghai")
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
ACTIVE_QUEUE_STATUSES = {"queued", "waiting_human_publish", "published"}
ELIGIBLE_PACK_STATUSES = {"draft_ready", "ready", "needs_revision", "queued", "waiting_human_publish"}
PLATFORM_ORDER = ["wechat", "xiaohongshu", "zhihu", "x", "bilibili", "toutiao", "baijiahao"]
CONTINUITY_MODE_RANK = {
    "same_day_premium": 4,
    "same_day_fallback_publish_safe": 3,
    "backlog_continuity": 2,
    "backlog_fallback_publish_safe": 1,
}
PLATFORM_FILE_MAP = {
    "wechat": "wechat.md",
    "xiaohongshu": "xiaohongshu.md",
    "zhihu": "zhihu.md",
    "x": "x.md",
    "bilibili": "bilibili.md",
    "toutiao": "toutiao.md",
    "baijiahao": "baijiahao.md",
}
HARD_DISABLE_DAY_MAINLINE_BACKLOG = True


@dataclass(frozen=True)
class PublishCandidate:
    topic_key: str
    approved_topic_path: str
    approved_topic_day: str
    draft_pack_dir: str
    current_status: str
    requested_platforms: list[str]
    available_platforms: list[str]
    eligible_platforms: list[str]
    blocked_platforms: list[str]
    latest_verdict_score: str
    latest_verdict_day: str
    latest_verdict_path: str
    continuity_mode: str
    publish_safety_tier: str
    priority_score: int
    why_now: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select publish continuity candidates for same-day premium pass or recent approved backlog.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--lookback-days", type=int, default=7, help="How many recent days of passed backlog to consider.")
    parser.add_argument("--limit", type=int, default=3, help="Maximum number of topic candidates to output.")
    parser.add_argument("--preferred-platform", default="wechat", help="Prefer this platform when enqueueing eligible candidates.")
    parser.add_argument("--required-platform", default="", help="When set, only keep candidates that can publish to this platform.")
    parser.add_argument("--allow-backlog", action="store_true", help="Allow historical approved topics into continuity selection.")
    parser.add_argument("--min-fallback-score", type=float, default=7.0, help="Minimum overall score required for fallback publish-safe partial release.")
    parser.add_argument("--enqueue", action="store_true", help="Enqueue eligible candidates into publish queue after selection.")
    parser.add_argument("--enqueue-limit", type=int, default=6, help="Maximum number of platform queue items to enqueue in one run.")
    parser.add_argument("--publish-owner", default="老板", help="Publish owner used when enqueueing queue items.")
    parser.add_argument("--planned-publish-at", default="", help="Optional planned publish time when enqueueing.")
    parser.add_argument("--write", action="store_true", help="Write queue snapshot into 10_logs.")
    return parser.parse_args()


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def day_token(date_text: str) -> str:
    return date.fromisoformat(date_text).strftime("%Y%m%d")


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


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


def split_platforms(raw: str) -> list[str]:
    if not raw or raw == "n/a":
        return []
    return [clean(item, "") for item in raw.split(",") if clean(item, "")]


def resolve_doc_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    return ROOT / raw_path


def parse_cst(raw: str) -> datetime | None:
    value = clean(raw, "")
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S CST", "%Y-%m-%d %H:%M CST", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return None


def approved_topic_day(raw_path: str) -> str:
    resolved = clean(raw_path, "")
    if not resolved or resolved == "n/a":
        return "n/a"
    name = Path(resolved).name
    match = re.match(r"^(?P<token>\d{8})(?:_\d{6})?__", name)
    if not match:
        return "n/a"
    token = match.group("token")
    return f"{token[:4]}-{token[4:6]}-{token[6:8]}"


def verdict_day(verdict: ContentPackVerdict) -> str:
    parsed = parse_cst(verdict.generated_at)
    if parsed:
        return parsed.date().isoformat()
    token_match = re.match(r"^(\d{8})__", verdict.path.name)
    if token_match:
        token = token_match.group(1)
        return f"{token[:4]}-{token[4:6]}-{token[6:8]}"
    return date.fromtimestamp(verdict.path.stat().st_mtime).isoformat()


def queue_status_by_platform(topic_key: str) -> dict[str, str]:
    latest_by_platform: dict[str, tuple[datetime, str]] = {}
    for path in sorted(QUEUE_DIR.glob(f"*__{topic_key}__*__publish-queue-item.md")):
        fields = parse_fields(path)
        platform = clean(fields.get("platform", ""), "")
        status = clean(fields.get("status", "n/a"))
        if not platform:
            continue
        ts = datetime.fromtimestamp(path.stat().st_mtime, tz=CN_TZ)
        previous = latest_by_platform.get(platform)
        if previous is None or ts >= previous[0]:
            latest_by_platform[platform] = (ts, status)
    return {platform: status for platform, (_ts, status) in latest_by_platform.items()}


def available_platforms_for(pack_card: Path, fields: dict[str, str]) -> list[str]:
    available: list[str] = []
    pack_dir = pack_card.parent
    for platform in PLATFORM_ORDER:
        raw_path = clean(fields.get(f"{platform}_path", "n/a"))
        if raw_path != "n/a":
            content_path = resolve_doc_path(raw_path)
        else:
            content_path = pack_dir / PLATFORM_FILE_MAP[platform]
        if content_path.exists():
            available.append(platform)
    return available


def content_path_for(pack_card: Path, fields: dict[str, str], platform: str) -> Path:
    raw_path = clean(fields.get(f"{platform}_path", "n/a"))
    if raw_path != "n/a":
        return resolve_doc_path(raw_path)
    return pack_card.parent / PLATFORM_FILE_MAP[platform]


def candidate_for(
    pack_card: Path,
    requested_date: str,
    lookback_days: int,
    preferred_platform: str,
    required_platform: str,
    allow_backlog: bool,
    min_fallback_score: float,
) -> PublishCandidate | None:
    fields = parse_fields(pack_card)
    topic_key = clean(fields.get("draft_key", pack_card.parent.name))
    current_status = clean(fields.get("status", "n/a"))
    delivery_lane = clean(fields.get("delivery_lane", "day_mainline"))
    if current_status not in ELIGIBLE_PACK_STATUSES:
        return None
    if delivery_lane != "day_mainline":
        return None

    verdict = latest_content_pack_verdict(topic_key)
    if verdict is None:
        return None

    safety_tier = "premium_publish_ready" if verdict.allows_publish_queue else "fallback_publish_safe"
    partial_publish_safe = (
        not verdict.allows_publish_queue
        and bool(verdict.publish_ready_platforms)
        and verdict.score_value is not None
        and verdict.score_value >= min_fallback_score
    )
    if not verdict.allows_publish_queue and not partial_publish_safe:
        return None

    origin_day = approved_topic_day(fields.get("approved_topic_path", ""))
    same_day_origin = origin_day == requested_date
    effective_allow_backlog = False if HARD_DISABLE_DAY_MAINLINE_BACKLOG else allow_backlog
    if not same_day_origin and not effective_allow_backlog:
        return None

    verdict_day_text = verdict_day(verdict)
    try:
        age_days = (date.fromisoformat(requested_date) - date.fromisoformat(origin_day if origin_day != "n/a" else verdict_day_text)).days
    except ValueError:
        age_days = lookback_days + 1
    if age_days < 0 or age_days > lookback_days:
        return None

    requested_platforms = split_platforms(fields.get("requested_platforms", ""))
    available_platforms = available_platforms_for(pack_card, fields)
    queue_statuses = queue_status_by_platform(topic_key)
    eligible_platforms: list[str] = []
    blocked_platforms: list[str] = []
    for platform in available_platforms:
        queue_status = queue_statuses.get(platform, "")
        if queue_status in ACTIVE_QUEUE_STATUSES:
            blocked_platforms.append(f"{platform}:{queue_status}")
            continue
        content_path = content_path_for(pack_card, fields, platform)
        hygiene = inspect_content_hygiene(pack_card.parent, platform, content_path=content_path)
        if hygiene.blocking_issues:
            blocked_platforms.append(f"{platform}:content_hygiene={','.join(hygiene.blocking_issues)}")
            continue
        if verdict.allows_publish_queue_for(platform):
            eligible_platforms.append(platform)
        else:
            blocked_platforms.append(f"{platform}:gate_blocked")

    required_platform_normalized = clean(required_platform, "").lower()
    if required_platform_normalized:
        if required_platform_normalized not in eligible_platforms:
            return None
        eligible_platforms = [required_platform_normalized]

    if not eligible_platforms:
        return None

    if same_day_origin and verdict.allows_publish_queue:
        continuity_mode = "same_day_premium"
    elif same_day_origin:
        continuity_mode = "same_day_fallback_publish_safe"
    elif not HARD_DISABLE_DAY_MAINLINE_BACKLOG and verdict.allows_publish_queue:
        continuity_mode = "backlog_continuity"
    elif not HARD_DISABLE_DAY_MAINLINE_BACKLOG:
        continuity_mode = "backlog_fallback_publish_safe"
    else:
        return None
    priority_score = {
        "same_day_premium": 240,
        "same_day_fallback_publish_safe": 225,
        "backlog_continuity": 150,
        "backlog_fallback_publish_safe": 135,
    }[continuity_mode]
    if verdict.score_value is not None:
        priority_score += int(verdict.score_value * 10)
    priority_score += max(0, lookback_days - max(age_days, 0)) * 6
    priority_score += len(eligible_platforms) * 8
    if preferred_platform in eligible_platforms:
        priority_score += 18
    if current_status == "ready":
        priority_score += 20
    elif current_status == "draft_ready":
        priority_score += 10
    elif current_status == "needs_revision":
        priority_score += 6

    why_parts = [
        f"latest_verdict={verdict.normalized_status}(score={verdict.score_text or 'n/a'})",
        f"mode={continuity_mode}",
        f"publish_safety_tier={safety_tier}",
        f"eligible_platforms={','.join(eligible_platforms)}",
    ]
    if blocked_platforms:
        why_parts.append(f"blocked_platforms={','.join(blocked_platforms)}")
    if not same_day_origin:
        why_parts.append(f"fallback_from={origin_day if origin_day != 'n/a' else verdict_day_text}")

    return PublishCandidate(
        topic_key=topic_key,
        approved_topic_path=clean(fields.get("approved_topic_path", "n/a")),
        approved_topic_day=origin_day,
        draft_pack_dir=str(pack_card.parent),
        current_status=current_status,
        requested_platforms=requested_platforms,
        available_platforms=available_platforms,
        eligible_platforms=eligible_platforms,
        blocked_platforms=blocked_platforms,
        latest_verdict_score=verdict.score_text or "n/a",
        latest_verdict_day=verdict_day_text,
        latest_verdict_path=str(verdict.path),
        continuity_mode=continuity_mode,
        publish_safety_tier=safety_tier,
        priority_score=priority_score,
        why_now="; ".join(why_parts),
    )


def render_queue(
    requested_date: str,
    lookback_days: int,
    limit: int,
    allow_backlog: bool,
    items: list[PublishCandidate],
) -> str:
    mode = "none"
    if items:
        mode = items[0].continuity_mode
    backlog_used = any(item.continuity_mode.startswith("backlog_") for item in items)
    lines = [
        "# Publish Continuity Queue",
        "",
        f"- `date`: `{requested_date}`",
        f"- `generated_at`: `{format_ts(now_cn())}`",
        f"- `lookback_days`: `{lookback_days}`",
        f"- `limit`: `{limit}`",
        f"- `allow_backlog`: `{'yes' if allow_backlog else 'no'}`",
        f"- `backlog_used`: `{'yes' if backlog_used else 'no'}`",
        f"- `mode`: `{mode}`",
        f"- `candidate_count`: `{len(items)}`",
        "",
        "## Targets",
        "",
    ]
    if not items:
        lines.append("- `none`")
        return "\n".join(lines).rstrip() + "\n"

    for idx, item in enumerate(items, start=1):
        lines.extend(
            [
                f"### {idx}. `{item.topic_key}`",
                f"- `approved_topic_path`: `{item.approved_topic_path}`",
                f"- `approved_topic_day`: `{item.approved_topic_day}`",
                f"- `draft_pack_dir`: `{item.draft_pack_dir}`",
                f"- `current_status`: `{item.current_status}`",
                f"- `continuity_mode`: `{item.continuity_mode}`",
                f"- `publish_safety_tier`: `{item.publish_safety_tier}`",
                f"- `requested_platforms`: `{', '.join(item.requested_platforms) if item.requested_platforms else 'n/a'}`",
                f"- `available_platforms`: `{', '.join(item.available_platforms) if item.available_platforms else 'none'}`",
                f"- `eligible_platforms`: `{', '.join(item.eligible_platforms) if item.eligible_platforms else 'none'}`",
                f"- `blocked_platforms`: `{', '.join(item.blocked_platforms) if item.blocked_platforms else 'none'}`",
                f"- `latest_verdict_score`: `{item.latest_verdict_score}`",
                f"- `latest_verdict_day`: `{item.latest_verdict_day}`",
                f"- `latest_verdict_path`: `{item.latest_verdict_path}`",
                f"- `priority_score`: `{item.priority_score}`",
                f"- `why_now`: `{item.why_now}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def enqueue_order(platforms: list[str], preferred_platform: str) -> list[str]:
    preferred = preferred_platform.strip().lower()
    return sorted(
        platforms,
        key=lambda platform: (
            0 if platform == preferred else 1,
            PLATFORM_ORDER.index(platform) if platform in PLATFORM_ORDER else len(PLATFORM_ORDER),
        ),
    )


def run_queue_builder(
    candidate: PublishCandidate,
    platform: str,
    publish_owner: str,
    planned_publish_at: str,
    write: bool,
) -> list[str]:
    if not QUEUE_BUILDER_SCRIPT.exists():
        raise SystemExit(f"Publish queue builder missing: {QUEUE_BUILDER_SCRIPT}")
    command = [
        "python3",
        str(QUEUE_BUILDER_SCRIPT),
        "--draft-pack-dir",
        candidate.draft_pack_dir,
        "--status",
        "waiting_human_publish",
        "--platform",
        platform,
        "--publish-owner",
        publish_owner,
        "--publish-safety-tier",
        candidate.publish_safety_tier,
        "--notes",
        (
            f"queue_origin=publish_continuity_queue|continuity_mode={candidate.continuity_mode}|"
            f"publish_safety_tier={candidate.publish_safety_tier}|verdict_score={candidate.latest_verdict_score}|"
            f"verdict_path={candidate.latest_verdict_path}"
        ),
    ]
    if planned_publish_at.strip():
        command.extend(["--planned-publish-at", planned_publish_at.strip()])
    if write:
        command.append("--write")
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    for line in lines:
        print(line)
    return lines


def main() -> None:
    args = parse_args()
    effective_allow_backlog = False if HARD_DISABLE_DAY_MAINLINE_BACKLOG else args.allow_backlog
    candidates = [
        item
        for pack_card in sorted(DRAFT_PACK_ROOT.glob("*/00_draft-pack-card.md"))
        if (
            item := candidate_for(
                pack_card,
                args.date,
                args.lookback_days,
                args.preferred_platform,
                args.required_platform,
                effective_allow_backlog,
                args.min_fallback_score,
            )
        ) is not None
    ]
    candidates.sort(
        key=lambda item: (
            CONTINUITY_MODE_RANK.get(item.continuity_mode, 0),
            item.priority_score,
            item.latest_verdict_day,
            item.topic_key,
        ),
        reverse=True,
    )
    selected = candidates[: max(args.limit, 0)]
    rendered = render_queue(args.date, args.lookback_days, args.limit, effective_allow_backlog, selected)
    print(rendered)
    if args.write:
        path = LOG_DIR / f"{day_token(args.date)}__publish-continuity-queue.md"
        path.write_text(rendered, encoding="utf-8")
        print(f"QUEUE_PATH={path}")
    if args.enqueue:
        planned_publish_at = args.planned_publish_at.strip() or f"{args.date} 17:30:00 CST"
        enqueued = 0
        enqueue_failures: list[str] = []
        for candidate in selected:
            for platform in enqueue_order(candidate.eligible_platforms, args.preferred_platform):
                if enqueued >= max(args.enqueue_limit, 0):
                    break
                try:
                    run_queue_builder(
                        candidate=candidate,
                        platform=platform,
                        publish_owner=args.publish_owner,
                        planned_publish_at=planned_publish_at,
                        write=args.write,
                    )
                    enqueued += 1
                except subprocess.CalledProcessError as exc:
                    stderr = (exc.stderr or "").strip().replace("\n", " | ")
                    enqueue_failures.append(f"{candidate.topic_key}:{platform}:{stderr or exc}")
            if enqueued >= max(args.enqueue_limit, 0):
                break
        print(f"ENQUEUED_ITEMS={enqueued}")
        if enqueue_failures:
            print(f"ENQUEUE_FAILURES={len(enqueue_failures)}")
            for item in enqueue_failures:
                print(f"ENQUEUE_FAILURE {item}")


if __name__ == "__main__":
    main()
