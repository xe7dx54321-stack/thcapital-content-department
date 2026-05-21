#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from market_morning_roundup_utils import sanitize_morning_roundup_markdown

PROJECT_ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
DEFAULT_OUTBOX_DIR = PROJECT_ROOT / "07_wechat_bridge_outbox"
QUEUE_DIR = PROJECT_ROOT / "06_publish_queue"
FEISHU_DOC_DELIVERY_SCRIPT = PROJECT_ROOT / "09_runbooks" / "scripts" / "market_feishu_doc_delivery.py"
TITLE_RE = re.compile(r"^- 标题：(.+?)\s*$")
TOP_HEADING_RE = re.compile(r"^#\s+(.+?)\s*$")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
QUEUE_ID_RE = re.compile(r"^- `queue_id`: `([^`]+)`", re.M)
TIMESTAMP_TOKEN_RE = re.compile(r"(\d{8}_\d{6})")
FIELD_RE_TEMPLATE = r"^(- `{field}`: `)([^`]*)((?:`)\s*)$"
WECHAT_INLINE_ALLOWED_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}
LOW_CONFIDENCE_ASSET_KINDS = {
    "ai-explainer",
    "structured-explainer",
    "generated-explainer",
    "external-safe-image",
    "story-card",
    "slot-story-card",
}
RELIABLE_ASSET_KINDS = {"source-screenshot", "official-asset"}


def now_cn() -> datetime:
    return datetime.now().astimezone()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a WeChat bridge request package for the Windows draft-box bridge.")
    parser.add_argument("--draft-pack-dir", required=True, help="Draft pack directory path")
    parser.add_argument("--outbox-dir", default=str(DEFAULT_OUTBOX_DIR), help="Synced WeChat bridge outbox directory")
    parser.add_argument("--author", default="TH Capital", help="Default article author")
    parser.add_argument("--queue-item-path", default="", help="Optional queue item path override")
    parser.add_argument("--write", action="store_true", help="Write request package to outbox")
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def clean(value: object, fallback: str = "") -> str:
    normalized = re.sub(r"\s+", " ", str(value or "")).strip().strip("`")
    return normalized or fallback


def extract_title(markdown: str, fallback: str) -> str:
    for raw in markdown.splitlines():
        match = TITLE_RE.match(raw.strip())
        if match:
            return match.group(1).strip()
    for raw in markdown.splitlines():
        match = TOP_HEADING_RE.match(raw.strip())
        if match:
            heading = match.group(1).strip()
            heading = heading.replace("微信稿｜", "").replace("微信稿|", "").strip()
            if heading:
                return heading
    return fallback


def extract_digest(markdown: str) -> str:
    lines = [line.strip() for line in markdown.splitlines()]
    in_opening = False
    opening_lines: list[str] = []
    for line in lines:
        if line.startswith("## "):
            heading = line[3:].strip()
            if heading == "开头":
                in_opening = True
                continue
            if in_opening:
                break
        if in_opening and line and not line.startswith("- "):
            opening_lines.append(line)
    if not opening_lines:
        for line in lines:
            if line and not line.startswith("#") and not line.startswith("- "):
                opening_lines.append(line)
            if len(" ".join(opening_lines)) >= 120:
                break
    digest = " ".join(opening_lines).strip()
    return digest[:120]


def load_asset_manifest(pack_dir: Path) -> dict[str, dict]:
    manifest_path = pack_dir / "visual-assets" / "_asset-manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    manifest: dict[str, dict] = {}
    for entry in payload.get("entries") or []:
        raw_path = str((entry or {}).get("path", "")).strip()
        if not raw_path:
            continue
        try:
            relative = Path(raw_path).resolve().relative_to(pack_dir.resolve()).as_posix()
        except Exception:
            continue
        manifest[relative] = entry
    return manifest


def reliable_visual_paths(manifest: dict[str, dict]) -> list[str]:
    return [
        path
        for path, entry in manifest.items()
        if str(entry.get("asset_kind", "")).strip() in RELIABLE_ASSET_KINDS
    ]


def low_confidence_visual_paths(manifest: dict[str, dict]) -> set[str]:
    return {
        path
        for path, entry in manifest.items()
        if str(entry.get("asset_kind", "")).strip() in LOW_CONFIDENCE_ASSET_KINDS
    }


def count_markdown_images(markdown: str) -> int:
    return len(IMAGE_RE.findall(markdown))


def local_markdown_asset_exists(pack_dir: Path, raw_path: str) -> bool:
    normalized = normalize_markdown_asset_path(raw_path)
    if not normalized or is_remote_path(normalized):
        return True
    candidate = (pack_dir / normalized).resolve()
    try:
        candidate.relative_to(pack_dir.resolve())
    except ValueError:
        return False
    return candidate.exists() and candidate.is_file()


def insert_reliable_visual(markdown: str, reliable_paths: list[str], manifest: dict[str, dict]) -> str:
    if not reliable_paths:
        return markdown
    candidate_path = reliable_paths[0]
    entry = manifest.get(candidate_path, {})
    alt_text = str(entry.get("source_title", "")).strip() or Path(candidate_path).stem.replace("_", " ")
    image_line = f"![{alt_text}]({candidate_path})"
    lines = markdown.rstrip().splitlines()
    for index, raw_line in enumerate(lines):
        if raw_line.strip().startswith("## "):
            updated = lines[:index] + ["", image_line, ""] + lines[index:]
            return "\n".join(updated).rstrip() + "\n"
    return markdown.rstrip() + "\n\n" + image_line + "\n"


def sanitize_markdown_for_bridge(markdown: str, pack_dir: Path) -> str:
    sanitized_base = sanitize_morning_roundup_markdown(markdown)
    manifest = load_asset_manifest(pack_dir)
    low_confidence_paths = low_confidence_visual_paths(manifest)
    kept_lines: list[str] = []
    previous_blank = False
    for raw_line in sanitized_base.splitlines():
        stripped = raw_line.strip()
        match = IMAGE_RE.match(stripped)
        if match:
            image_path = normalize_markdown_asset_path(match.group(1))
            if image_path in low_confidence_paths or not local_markdown_asset_exists(pack_dir, image_path):
                if not previous_blank:
                    kept_lines.append("")
                    previous_blank = True
                continue
        kept_lines.append(raw_line)
        previous_blank = not stripped
    sanitized = "\n".join(kept_lines).rstrip() + "\n"
    if count_markdown_images(sanitized) >= 1:
        return sanitized
    return insert_reliable_visual(sanitized, reliable_visual_paths(manifest), manifest)


def write_temp_text_file(filename: str, content: str) -> tuple[Path, Path]:
    temp_dir = Path(tempfile.mkdtemp(prefix="wechat_bridge_request_"))
    temp_path = temp_dir / filename
    temp_path.write_text(content, encoding="utf-8")
    return temp_path, temp_dir


def find_cover_asset(pack_dir: Path, markdown_text: str = "") -> Path | None:
    visual_dir = pack_dir / "visual-assets"
    if visual_dir.exists():
        for name in ("00__cover.png", "00__cover.jpg", "00__cover.jpeg"):
            candidate = visual_dir / name
            if candidate.exists():
                return candidate
    cover_candidates = []
    if markdown_text:
        for match in IMAGE_RE.finditer(markdown_text):
            raw_path = normalize_markdown_asset_path(match.group(1))
            if not raw_path or is_remote_path(raw_path):
                continue
            candidate = (pack_dir / raw_path).resolve()
            try:
                candidate.relative_to(pack_dir.resolve())
            except ValueError:
                continue
            if candidate.exists() and candidate.is_file():
                cover_candidates.append(candidate)
        if cover_candidates:
            return cover_candidates[0]
    if markdown_text:
        return None
    if not visual_dir.exists():
        return None
    priority: list[Path] = []
    for suffix in ("*.png", "*.jpg", "*.jpeg"):
        priority.extend(sorted(visual_dir.glob(suffix)))
    return priority[0] if priority else None


def find_wechat_queue_item(draft_key: str) -> Path | None:
    pattern = f"*__{draft_key}__wechat__publish-queue-item.md"
    candidates = sorted(QUEUE_DIR.glob(pattern), key=queue_item_sort_key)
    if candidates:
        return candidates[-1]
    archive_candidates = sorted(
        QUEUE_DIR.glob(f"archive/**/*__{draft_key}__wechat__publish-queue-item.md"),
        key=queue_item_sort_key,
    )
    return archive_candidates[-1] if archive_candidates else None


def queue_item_sort_key(path: Path) -> tuple[str, int, str]:
    text = read_text(path)
    queue_id_match = QUEUE_ID_RE.search(text)
    for candidate in ((queue_id_match.group(1) if queue_id_match else ""), path.name):
        match = TIMESTAMP_TOKEN_RE.search(candidate)
        if match:
            return (match.group(1), 1, path.name)
    try:
        return (f"{path.stat().st_mtime_ns:020d}", 0, path.name)
    except FileNotFoundError:
        return ("", 0, path.name)


def is_remote_path(raw: str) -> bool:
    lowered = raw.strip().lower()
    return lowered.startswith(("http://", "https://", "data:", "file://"))


def normalize_markdown_asset_path(raw: str) -> str:
    cleaned = raw.strip().strip("<>").strip().split(maxsplit=1)[0]
    return cleaned.replace("\\", "/")


def update_field(text: str, field: str, value: str) -> str:
    pattern = re.compile(FIELD_RE_TEMPLATE.format(field=re.escape(field)), re.M)
    if pattern.search(text):
        return pattern.sub(lambda match: f"{match.group(1)}{value}{match.group(3)}", text, count=1)
    return text


def extract_field(text: str, field: str) -> str:
    match = re.search(FIELD_RE_TEMPLATE.format(field=re.escape(field)), text, re.M)
    if not match:
        return "n/a"
    return match.group(2).strip() or "n/a"


def merge_notes(existing: str, extras: dict[str, str]) -> str:
    chunks = [item.strip() for item in existing.split("|") if item.strip() and item.strip() != "n/a"]
    filtered = [chunk for chunk in chunks if not any(chunk.startswith(f"{key}=") for key in extras)]
    for key, value in extras.items():
        filtered.append(f"{key}={value}")
    return " | ".join(filtered) if filtered else "n/a"


def append_summary(existing: str, extra: str) -> str:
    base = existing.strip() if existing and existing != "n/a" else ""
    if not base:
        return extra
    if extra in base:
        return base
    suffix = "" if base.endswith(("。", "！", "？")) else "。"
    return f"{base}{suffix}{extra}"


def delivery_lane_from_pack_card(pack_dir: Path) -> str:
    card_path = pack_dir / "00_draft-pack-card.md"
    if not card_path.exists():
        return "n/a"
    for raw_line in card_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^- `delivery_lane`: ?`?(.*?)`?$", raw_line.strip())
        if match:
            return match.group(1).strip().strip("`") or "n/a"
    return "n/a"


def delivery_lane_for_request(pack_dir: Path, queue_item_path: Path | None) -> str:
    if queue_item_path and queue_item_path.exists():
        text = queue_item_path.read_text(encoding="utf-8")
        lane = extract_field(text, "delivery_lane")
        if lane != "n/a":
            return lane
    return delivery_lane_from_pack_card(pack_dir)


def parse_prefixed_fields(lines: list[str], prefix: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in lines:
        if not line.startswith(prefix) or "=" not in line:
            continue
        key, value = line.split("=", 1)
        parsed[key] = value.strip()
    return parsed


def annotate_queue_item_feishu_doc(queue_item_path: Path, meta: dict[str, str]) -> None:
    if not queue_item_path.exists():
        return
    original = queue_item_path.read_text(encoding="utf-8")
    updated = original
    notes = extract_field(updated, "notes")
    extras = {
        "feishu_doc_status": clean(meta.get("FEISHU_DOC_STATUS", ""), "unknown"),
        "feishu_doc_token": clean(meta.get("FEISHU_DOC_TOKEN", ""), "n/a"),
        "feishu_doc_url": clean(meta.get("FEISHU_DOC_URL", ""), "n/a"),
        "feishu_doc_source_fingerprint": clean(meta.get("FEISHU_DOC_SOURCE_FINGERPRINT", ""), "n/a"),
        "feishu_doc_synced_at": now_cn().isoformat(),
    }
    mode = clean(meta.get("FEISHU_DOC_MODE", ""), "")
    if mode:
        extras["feishu_doc_mode"] = mode
    error_text = clean(meta.get("FEISHU_DOC_ERROR", ""), "")
    if error_text:
        extras["feishu_doc_error"] = error_text[:240]
    updated = update_field(updated, "notes", merge_notes(notes, extras))
    if clean(meta.get("FEISHU_DOC_STATUS", ""), "") == "success":
        current_summary = extract_field(updated, "frontstage_summary")
        updated = update_field(updated, "frontstage_summary", append_summary(current_summary, "飞书云文档已同步，可作为手动发布兜底。"))
    if updated != original:
        queue_item_path.write_text(updated, encoding="utf-8")


def maybe_create_feishu_doc(pack_dir: Path, queue_item_path: Path | None, write: bool) -> dict[str, str]:
    if not write:
        return {}
    if delivery_lane_for_request(pack_dir, queue_item_path) not in {"day_mainline", "morning_flash"}:
        return {}
    if not FEISHU_DOC_DELIVERY_SCRIPT.exists():
        meta = {
            "FEISHU_DOC_STATUS": "blocked",
            "FEISHU_DOC_MODE": "blocked",
            "FEISHU_DOC_ERROR": f"missing_script:{FEISHU_DOC_DELIVERY_SCRIPT}",
        }
        if queue_item_path:
            annotate_queue_item_feishu_doc(queue_item_path, meta)
        return meta
    command = [
        "python3",
        str(FEISHU_DOC_DELIVERY_SCRIPT),
        "--draft-pack-dir",
        str(pack_dir),
        "--write",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    for line in lines:
        print(line)
    meta = parse_prefixed_fields(lines, "FEISHU_DOC_")
    if completed.returncode != 0:
        error_text = clean(completed.stderr or completed.stdout, "feishu_doc_delivery_failed")
        meta.setdefault("FEISHU_DOC_STATUS", "blocked")
        meta.setdefault("FEISHU_DOC_MODE", "blocked")
        meta["FEISHU_DOC_ERROR"] = error_text[:240]
        print(f"FEISHU_DOC_ERROR={meta['FEISHU_DOC_ERROR']}")
    if queue_item_path:
        annotate_queue_item_feishu_doc(queue_item_path, meta)
    return meta


def prepare_inline_image_asset(markdown_path: str, source_path: Path) -> tuple[str, Path, Path | None]:
    suffix = source_path.suffix.lower()
    if suffix in WECHAT_INLINE_ALLOWED_SUFFIXES:
        return markdown_path, source_path, None
    if shutil.which("sips"):
        tmp_dir = Path(tempfile.mkdtemp(prefix="wechat_bridge_inline_"))
        converted_name = f"{Path(markdown_path).stem}__wechat.png"
        converted_path = tmp_dir / converted_name
        try:
            subprocess.run(
                ["sips", "-s", "format", "png", str(source_path), "--out", str(converted_path)],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            stderr = (exc.stderr or exc.stdout or "").strip()
            raise SystemExit(f"Unsupported inline image could not be converted for WeChat: {source_path} :: {stderr}") from exc
        request_path = str((Path(markdown_path).parent / converted_name).as_posix())
        return request_path, converted_path, tmp_dir
    raise SystemExit(
        f"WeChat inline image format not supported: {source_path}. "
        "Please convert it to png/jpg/jpeg/gif/bmp before enqueueing."
    )


def collect_inline_image_files(markdown: str, pack_dir: Path) -> tuple[dict[str, Path], list[Path]]:
    collected: dict[str, Path] = {}
    temp_dirs: list[Path] = []
    for match in IMAGE_RE.finditer(markdown):
        raw_path = normalize_markdown_asset_path(match.group(1))
        if not raw_path or is_remote_path(raw_path):
            continue
        source_path = (pack_dir / raw_path).resolve()
        try:
            source_path.relative_to(pack_dir.resolve())
        except ValueError:
            continue
        if source_path.exists() and source_path.is_file():
            request_path, prepared_path, temp_dir = prepare_inline_image_asset(raw_path, source_path)
            collected[request_path] = prepared_path
            if temp_dir is not None:
                temp_dirs.append(temp_dir)
    return collected, temp_dirs


def build_request_payload(pack_dir: Path, queue_item_override: str, author: str) -> tuple[dict, dict[str, Path], list[Path]]:
    draft_key = pack_dir.name
    wechat_md = pack_dir / "wechat.md"
    if not wechat_md.exists():
        raise SystemExit(f"Missing wechat draft: {wechat_md}")
    handoff = pack_dir / "wechat-html-handoff.md"
    markdown_text = read_text(wechat_md)
    sanitized_markdown = sanitize_markdown_for_bridge(markdown_text, pack_dir)
    temp_dirs: list[Path] = []
    prepared_wechat_md = wechat_md
    if sanitized_markdown != markdown_text:
        prepared_wechat_md, markdown_temp_dir = write_temp_text_file("wechat.md", sanitized_markdown)
        temp_dirs.append(markdown_temp_dir)
    title = extract_title(markdown_text, draft_key.replace("-", " "))
    digest = extract_digest(sanitized_markdown)
    cover_asset = find_cover_asset(pack_dir, sanitized_markdown)
    inline_image_files, inline_temp_dirs = collect_inline_image_files(sanitized_markdown, pack_dir)
    temp_dirs.extend(inline_temp_dirs)
    queue_item_path = Path(queue_item_override).expanduser() if queue_item_override else find_wechat_queue_item(draft_key)
    request_id = f"wechat_bridge__{draft_key}"
    payload = {
        "request_id": request_id,
        "status": "pending",
        "created_at": now_cn().isoformat(),
        "draft_key": draft_key,
        "article": {
            "title": title,
            "author": author,
            "digest": digest,
        },
        "paths": {
            "source_pack_dir": str(pack_dir),
            "queue_item_path": str(queue_item_path) if queue_item_path else "n/a",
            "source_wechat_markdown": str(wechat_md),
            "source_handoff": str(handoff) if handoff.exists() else "n/a",
            "source_cover_asset": str(cover_asset) if cover_asset else "n/a",
        },
        "files": {
            "wechat_markdown": "wechat.md",
            "handoff": "wechat-html-handoff.md" if handoff.exists() else "n/a",
            "cover_image": f"cover{cover_asset.suffix.lower()}" if cover_asset else "n/a",
            "result": "result.json",
        },
        "inline_images": [
            {
                "markdown_path": markdown_path,
                "request_path": markdown_path,
            }
            for markdown_path in sorted(inline_image_files)
        ],
    }
    source_files = {"wechat.md": prepared_wechat_md}
    if handoff.exists():
        source_files["wechat-html-handoff.md"] = handoff
    if cover_asset:
        source_files[f"cover{cover_asset.suffix.lower()}"] = cover_asset
    for request_path, source_path in inline_image_files.items():
        source_files[request_path] = source_path
    return payload, source_files, temp_dirs


def ensure_outbox(outbox_dir: Path) -> None:
    (outbox_dir / "requests").mkdir(parents=True, exist_ok=True)
    (outbox_dir / "tools").mkdir(parents=True, exist_ok=True)


def write_request(outbox_dir: Path, payload: dict, source_files: dict[str, Path]) -> Path:
    request_dir = outbox_dir / "requests" / payload["request_id"]
    if request_dir.exists():
        shutil.rmtree(request_dir)
    request_dir.mkdir(parents=True, exist_ok=True)
    for target_name, source_path in source_files.items():
        (request_dir / target_name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, request_dir / target_name)
    (request_dir / "request.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return request_dir


def main() -> None:
    args = parse_args()
    pack_dir = Path(args.draft_pack_dir).expanduser().resolve()
    outbox_dir = Path(args.outbox_dir).expanduser().resolve()
    payload, source_files, temp_dirs = build_request_payload(pack_dir, args.queue_item_path, args.author)
    queue_item_path_text = clean(((payload.get("paths") or {}).get("queue_item_path") or ""), "")
    queue_item_path = Path(queue_item_path_text).expanduser() if queue_item_path_text and queue_item_path_text != "n/a" else None
    try:
        feishu_doc_meta: dict[str, str] = {}
        if args.write:
            feishu_doc_meta = maybe_create_feishu_doc(pack_dir, queue_item_path, write=True)
        if feishu_doc_meta:
            payload.setdefault("delivery_artifacts", {})
            payload["delivery_artifacts"]["feishu_doc"] = {
                "status": clean(feishu_doc_meta.get("FEISHU_DOC_STATUS"), "unknown"),
                "mode": clean(feishu_doc_meta.get("FEISHU_DOC_MODE"), "n/a"),
                "title": clean(feishu_doc_meta.get("FEISHU_DOC_TITLE"), "n/a"),
                "document_id": clean(feishu_doc_meta.get("FEISHU_DOC_TOKEN"), "n/a"),
                "url": clean(feishu_doc_meta.get("FEISHU_DOC_URL"), "n/a"),
                "source_fingerprint": clean(feishu_doc_meta.get("FEISHU_DOC_SOURCE_FINGERPRINT"), "n/a"),
            }
        print(json.dumps({"request": payload, "files": {k: str(v) for k, v in source_files.items()}}, ensure_ascii=False, indent=2))
        print(f"REQUEST_ID={payload['request_id']}")
        if not args.write:
            return
        ensure_outbox(outbox_dir)
        request_dir = write_request(outbox_dir, payload, source_files)
        print(f"REQUEST_WRITTEN {request_dir}")
    finally:
        for temp_dir in temp_dirs:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
