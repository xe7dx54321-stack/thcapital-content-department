#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
CN_TZ = ZoneInfo("Asia/Shanghai")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
PLACEHOLDER_SUBSTRINGS = ("[待补", "待补", "占位图", "占位符", "lorem ipsum")
PLACEHOLDER_REGEX_RULES = (
    ("todo_marker", re.compile(r"(?im)^\s*(?:[-*]\s*)?(?:TODO|TBD)\s*(?::|：|-|$)")),
    ("todo_bracket", re.compile(r"(?im)\[(?:TODO|TBD)\]")),
    ("na_literal", re.compile(r"(?i)(?<![A-Za-z0-9_])n/a(?![A-Za-z0-9_])")),
)
INTERNAL_SCAFFOLD_PATTERNS = {
    "confirmed_vs_unverified_heading": ("当前能确认的事实", "仍需验证"),
    "confirmed_and_unverified_labels": ("已确认：", "仍需验证"),
    "writer_speed_disclaimer": ("本文撰写时距离事件发生不足 24 小时",),
    "verification_status_heading": ("Verification Status",),
    "pending_questions_heading": ("待确认问题清单",),
}
WECHAT_DRAFT_SCAFFOLD_HARD = ("## 推荐包装", "## 标题候选", "## 品牌签名")
WECHAT_DRAFT_SCAFFOLD_SOFT = ("## 开头", "## 关注我们", "## 轻 CTA")


@dataclass(frozen=True)
class ContentHygieneResult:
    platform: str
    content_path: Path
    blocking_issues: tuple[str, ...]
    warning_issues: tuple[str, ...]
    image_count: int
    placeholder_hits: tuple[str, ...]
    internal_scaffolding_hits: tuple[str, ...]
    draft_scaffold_hits: tuple[str, ...]

    @property
    def passes(self) -> bool:
        return not self.blocking_issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect final-publish hygiene for TH Capital content drafts.")
    parser.add_argument("--draft-pack-dir", required=True, help="Draft pack directory path")
    parser.add_argument("--platform", required=True, help="Platform label, e.g. wechat / zhihu / xiaohongshu")
    parser.add_argument("--content-path", default="", help="Override markdown path")
    parser.add_argument("--write", action="store_true", help="Write a hygiene report into the draft pack")
    return parser.parse_args()


def clean(value: str, fallback: str = "") -> str:
    value = re.sub(r"\s+", " ", value or "").strip().strip("`")
    return value if value else fallback


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def top_heading_present(text: str) -> bool:
    for raw_line in text.splitlines():
        if raw_line.strip().startswith("# "):
            return True
    return False


def check_placeholders(text: str) -> list[str]:
    lowered = text.lower()
    hits: list[str] = []
    seen: set[str] = set()
    for token in PLACEHOLDER_SUBSTRINGS:
        if token.lower() in lowered and token not in seen:
            hits.append(token)
            seen.add(token)
    for label, pattern in PLACEHOLDER_REGEX_RULES:
        if pattern.search(text) and label not in seen:
            hits.append(label)
            seen.add(label)
    return hits


def internal_scaffolding_hits(text: str) -> list[str]:
    normalized = clean(text, "").replace("**", "")
    hits: list[str] = []
    for label, needles in INTERNAL_SCAFFOLD_PATTERNS.items():
        if all(needle in normalized for needle in needles):
            hits.append(label)
    return hits


def wechat_draft_scaffold_hits(text: str) -> list[str]:
    hits: list[str] = []
    for heading in WECHAT_DRAFT_SCAFFOLD_HARD:
        if heading in text:
            hits.append(heading.replace("## ", ""))
    soft_hits = [heading.replace("## ", "") for heading in WECHAT_DRAFT_SCAFFOLD_SOFT if heading in text]
    if hits:
        hits.extend(item for item in soft_hits if item not in hits)
    elif len(soft_hits) >= 2:
        hits.extend(soft_hits)
    return hits


def count_markdown_images(markdown: str) -> int:
    return len(IMAGE_RE.findall(markdown))


def default_content_path(pack_dir: Path, platform: str) -> Path:
    return pack_dir / f"{platform}.md"


def inspect_content_hygiene(pack_dir: Path, platform: str, content_path: Path | None = None) -> ContentHygieneResult:
    platform_clean = clean(platform, "").lower()
    resolved_path = content_path or default_content_path(pack_dir, platform_clean)
    text = read_text(resolved_path)
    blocking: list[str] = []
    warnings: list[str] = []

    if not resolved_path.exists():
        blocking.append("missing_content_file")
        return ContentHygieneResult(
            platform=platform_clean,
            content_path=resolved_path,
            blocking_issues=tuple(blocking),
            warning_issues=tuple(warnings),
            image_count=0,
            placeholder_hits=tuple(),
            internal_scaffolding_hits=tuple(),
            draft_scaffold_hits=tuple(),
        )

    placeholders = check_placeholders(text)
    scaffolds = internal_scaffolding_hits(text)
    image_count = count_markdown_images(text)
    draft_hits: list[str] = []

    if not top_heading_present(text):
        blocking.append("missing_top_heading")
    if placeholders:
        blocking.append("placeholder_tokens_present")
    if scaffolds:
        blocking.append("internal_scaffolding_present")

    if platform_clean == "wechat":
        draft_hits = wechat_draft_scaffold_hits(text)
        if draft_hits:
            blocking.append("wechat_draft_scaffold_present")
        # Check if inline-visual-plan explicitly allows no images (morning_flash policy)
        inline_plan_path = pack_dir / "inline-visual-plan.md"
        no_images_policy = False
        if inline_plan_path.exists():
            plan_text = read_text(inline_plan_path)
            if "no-inline-images-required" in plan_text or "正文图：非必需" in plan_text:
                no_images_policy = True
        if image_count < 1 and not no_images_policy:
            blocking.append("wechat_missing_inline_images")
        handoff_path = pack_dir / "wechat-html-handoff.md"
        if not handoff_path.exists():
            blocking.append("wechat_handoff_missing")
        if not inline_plan_path.exists():
            warnings.append("inline_visual_plan_missing")

    return ContentHygieneResult(
        platform=platform_clean,
        content_path=resolved_path,
        blocking_issues=tuple(blocking),
        warning_issues=tuple(warnings),
        image_count=image_count,
        placeholder_hits=tuple(placeholders),
        internal_scaffolding_hits=tuple(scaffolds),
        draft_scaffold_hits=tuple(draft_hits),
    )


def render_report(result: ContentHygieneResult, pack_dir: Path) -> str:
    return "\n".join(
        [
            "# Content Hygiene Guard",
            "",
            f"- `generated_at`: `{format_ts(now_cn())}`",
            f"- `draft_pack_dir`: `{pack_dir}`",
            f"- `platform`: `{result.platform}`",
            f"- `content_path`: `{result.content_path}`",
            f"- `passes`: `{'yes' if result.passes else 'no'}`",
            f"- `blocking_issues`: `{', '.join(result.blocking_issues) if result.blocking_issues else 'none'}`",
            f"- `warning_issues`: `{', '.join(result.warning_issues) if result.warning_issues else 'none'}`",
            f"- `image_count`: `{result.image_count}`",
            f"- `placeholder_hits`: `{', '.join(result.placeholder_hits) if result.placeholder_hits else 'none'}`",
            f"- `internal_scaffolding_hits`: `{', '.join(result.internal_scaffolding_hits) if result.internal_scaffolding_hits else 'none'}`",
            f"- `draft_scaffold_hits`: `{', '.join(result.draft_scaffold_hits) if result.draft_scaffold_hits else 'none'}`",
            "",
        ]
    )


def main() -> None:
    args = parse_args()
    pack_dir = Path(args.draft_pack_dir).expanduser().resolve()
    content_path = Path(args.content_path).expanduser().resolve() if clean(args.content_path, "") else None
    result = inspect_content_hygiene(pack_dir, args.platform, content_path=content_path)
    report = render_report(result, pack_dir)
    if args.write:
        report_path = pack_dir / f"content-hygiene__{clean(args.platform, 'platform').lower()}.md"
        report_path.write_text(report, encoding="utf-8")
        print(report_path)
    print(report)


if __name__ == "__main__":
    main()
