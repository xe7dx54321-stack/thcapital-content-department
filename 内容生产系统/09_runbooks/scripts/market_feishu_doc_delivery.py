#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
LOG_DIR = ROOT / "10_logs"
TITLE_RE = re.compile(r"^- 标题：(.+?)\s*$")
TOP_HEADING_RE = re.compile(r"^#\s+(.+?)\s*$")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
SIDECAR_NAME = "feishu-doc-delivery.json"
DEFAULT_AGENT_ID = "lead"
CN_TZ = ZoneInfo("Asia/Shanghai")
OPENCLAW_MEDIA_ROOT = Path.home() / ".openclaw" / "media" / "feishu-doc-delivery"
FALLBACK_MEDIA_ROOT = Path(tempfile.gettempdir()) / "openclaw-media" / "feishu-doc-delivery"
FALLBACK_OPENCLAW_STATE_ROOT = Path(tempfile.gettempdir()) / "openclaw-state"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or refresh a Feishu cloud doc from a market draft pack markdown file.")
    parser.add_argument("--draft-pack-dir", required=True, help="Draft pack directory path.")
    parser.add_argument("--markdown-path", default="", help="Override markdown path. Defaults to <draft-pack-dir>/wechat.md")
    parser.add_argument("--title", default="", help="Override Feishu doc title.")
    parser.add_argument("--agent-id", default=DEFAULT_AGENT_ID, help="OpenClaw agent id used to call feishu_doc.")
    parser.add_argument("--timeout-seconds", type=int, default=600, help="OpenClaw agent timeout in seconds.")
    parser.add_argument("--write", action="store_true", help="Actually create/update the Feishu cloud doc.")
    return parser.parse_args()


def clean(value: object, fallback: str = "") -> str:
    normalized = re.sub(r"\s+", " ", str(value or "")).strip().strip("`")
    return normalized or fallback


def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def format_ts(dt: datetime) -> str:
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def ensure_writable_media_root() -> Path:
    override = clean(os.environ.get("TH_CAPITAL_OPENCLAW_MEDIA_ROOT") or os.environ.get("OPENCLAW_MEDIA_ROOT"), "")
    candidates = [Path(override).expanduser() if override else None, OPENCLAW_MEDIA_ROOT, FALLBACK_MEDIA_ROOT]
    for candidate in candidates:
        if candidate is None:
            continue
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".write_probe"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
            return candidate
        except OSError:
            continue
    raise RuntimeError("No writable media root available for Feishu doc staging.")


def prepare_openclaw_env(agent_id: str) -> dict[str, str]:
    env = os.environ.copy()
    state_root = Path(env.get("OPENCLAW_STATE_DIR") or FALLBACK_OPENCLAW_STATE_ROOT).expanduser()
    env["OPENCLAW_STATE_DIR"] = str(state_root)
    target_agent_dir = state_root / "agents" / agent_id / "agent"
    target_agent_dir.mkdir(parents=True, exist_ok=True)
    source_agent_dir = Path.home() / ".openclaw" / "agents" / agent_id / "agent"
    for filename in ("auth-profiles.json",):
        source_path = source_agent_dir / filename
        target_path = target_agent_dir / filename
        if source_path.exists() and not target_path.exists():
            shutil.copy2(source_path, target_path)
    return env


def extract_title(markdown: str, fallback: str) -> str:
    for raw in markdown.splitlines():
        match = TITLE_RE.match(raw.strip())
        if match:
            return clean(match.group(1), fallback)
    for raw in markdown.splitlines():
        match = TOP_HEADING_RE.match(raw.strip())
        if match:
            heading = clean(match.group(1), fallback)
            heading = heading.replace("微信稿｜", "").replace("微信稿|", "").strip()
            return heading or fallback
    return fallback


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize_markdown_asset_path(raw: str) -> str:
    cleaned = raw.strip().strip("<>").strip().split(maxsplit=1)[0]
    return cleaned.replace("\\", "/")


def is_remote_path(raw: str) -> bool:
    lowered = raw.strip().lower()
    return lowered.startswith(("http://", "https://", "data:", "file://"))


def resolve_markdown_path(pack_dir: Path, override: str) -> Path:
    if clean(override):
        return Path(override).expanduser().resolve()
    return (pack_dir / "wechat.md").resolve()


def local_image_entries(markdown: str, pack_dir: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    pack_root = pack_dir.resolve()
    for match in IMAGE_RE.finditer(markdown):
        raw_path = normalize_markdown_asset_path(match.group(1))
        if not raw_path or is_remote_path(raw_path):
            continue
        raw_candidate = Path(raw_path).expanduser()
        candidate = raw_candidate if raw_candidate.is_absolute() else (pack_dir / raw_candidate)
        resolved = candidate.resolve()
        if not resolved.exists() or not resolved.is_file():
            if raw_path not in seen:
                entries.append({"raw_path": raw_path, "status": "missing"})
                seen.add(raw_path)
            continue
        relative_path = ""
        try:
            relative_path = resolved.relative_to(pack_root).as_posix()
        except ValueError:
            relative_path = ""
        key = relative_path or str(resolved)
        if key in seen:
            continue
        entries.append(
            {
                "raw_path": raw_path,
                "resolved_path": str(resolved),
                "relative_path": relative_path,
                "status": "ready",
            }
        )
        seen.add(key)
    return entries


def stage_local_image_for_feishu(pack_dir: Path, resolved: Path, relative_path: str, source_fingerprint: str) -> Path:
    # Stage images into an OpenClaw-approved media root so feishu_doc upload_image
    # can access them reliably during agent execution.
    fingerprint_token = clean(source_fingerprint, "")[:16] or "no_fingerprint"
    target_root = ensure_writable_media_root() / pack_dir.name / fingerprint_token
    relative_target = Path(relative_path) if relative_path else Path(resolved.name)
    target_path = (target_root / relative_target).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(resolved, target_path)
    return target_path


def stage_markdown_for_feishu(markdown: str, pack_dir: Path, source_fingerprint: str) -> tuple[Path, list[dict[str, str]]]:
    staged_entries: list[dict[str, str]] = []
    pack_root = pack_dir.resolve()
    media_root = ensure_writable_media_root()

    def replace_image(match: re.Match[str]) -> str:
        raw_path = normalize_markdown_asset_path(match.group(1))
        if not raw_path or is_remote_path(raw_path):
            return match.group(0)
        raw_candidate = Path(raw_path).expanduser()
        candidate = raw_candidate if raw_candidate.is_absolute() else (pack_dir / raw_candidate)
        resolved = candidate.resolve()
        if not resolved.exists() or not resolved.is_file():
            return match.group(0)
        relative_path = ""
        try:
            relative_path = resolved.relative_to(pack_root).as_posix()
        except ValueError:
            relative_path = ""
        staged = stage_local_image_for_feishu(pack_dir, resolved, relative_path, source_fingerprint)
        staged_entries.append(
            {
                "raw_path": raw_path,
                "resolved_path": str(resolved),
                "staged_path": str(staged),
                "relative_path": relative_path,
                "status": "staged",
            }
        )
        return match.group(0).replace(match.group(1), staged.as_posix(), 1)

    staged_markdown = IMAGE_RE.sub(replace_image, markdown)
    fingerprint_token = clean(source_fingerprint, "")[:16] or "no_fingerprint"
    staged_markdown_path = media_root / pack_dir.name / fingerprint_token / f"{pack_dir.name}__feishu.md"
    staged_markdown_path.parent.mkdir(parents=True, exist_ok=True)
    staged_markdown_path.write_text(staged_markdown, encoding="utf-8")
    return staged_markdown_path, staged_entries


def compute_source_fingerprint(markdown: str, pack_dir: Path) -> tuple[str, list[dict[str, str]]]:
    entries = local_image_entries(markdown, pack_dir)
    digest = hashlib.sha256()
    digest.update(markdown.encode("utf-8"))
    for entry in sorted(entries, key=lambda item: item.get("raw_path", "")):
        digest.update(entry.get("raw_path", "").encode("utf-8"))
        digest.update(entry.get("status", "").encode("utf-8"))
        resolved_path = entry.get("resolved_path", "")
        if not resolved_path:
            continue
        file_path = Path(resolved_path)
        digest.update(file_path.name.encode("utf-8"))
        digest.update(hashlib.sha256(file_path.read_bytes()).digest())
    return digest.hexdigest(), entries
def build_agent_prompt(markdown_path: Path, title: str, existing_doc_token: str) -> str:
    markdown_json = json.dumps(str(markdown_path))
    title_json = json.dumps(title)
    if existing_doc_token:
        doc_token_json = json.dumps(existing_doc_token)
        return (
            f"Read the markdown file at {markdown_json} exactly.\n"
            "Do not summarize, translate, or rewrite anything.\n"
            f'Use the `feishu_doc` tool with action `write` to overwrite document token {doc_token_json} '
            "with the exact markdown content from that file.\n"
            "After the tool call succeeds, reply with ONLY one compact JSON object and no extra text:\n"
            f'{{"mode":"update","document_id":{doc_token_json},"url":"https://feishu.cn/docx/{existing_doc_token}","title":{title_json},"blocks_added":<int>,"images_processed":<int>}}'
        )
    return (
        f"Read the markdown file at {markdown_json} exactly.\n"
        "Do not summarize, translate, or rewrite anything.\n"
        f'First use the `feishu_doc` tool with action `create`, title {title_json}, and `grant_to_requester=false`.\n'
        "Then use the `feishu_doc` tool with action `write` to overwrite that new document with the exact markdown content from the file.\n"
        "After both tool calls succeed, reply with ONLY one compact JSON object and no extra text:\n"
        f'{{"mode":"create","document_id":"<doc_token>","url":"https://feishu.cn/docx/<doc_token>","title":{title_json},"blocks_added":<int>,"images_processed":<int>}}'
    )


def run_openclaw_agent(agent_id: str, prompt: str, timeout_seconds: int) -> dict:
    command = [
        "openclaw",
        "agent",
        "--local",
        "--agent",
        agent_id,
        "--message",
        prompt,
        "--thinking",
        "low",
        "--timeout",
        str(timeout_seconds),
        "--json",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False, env=prepare_openclaw_env(agent_id))
    if completed.returncode != 0:
        detail = clean(completed.stderr or completed.stdout, "openclaw agent failed")
        raise RuntimeError(detail)
    raw = clean(completed.stdout, "")
    if not raw:
        raise RuntimeError("openclaw agent returned empty stdout")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"openclaw agent returned non-json output: {raw[:400]}") from exc


def extract_agent_text(payload: dict) -> str:
    result = payload.get("result") or {}
    for item in result.get("payloads") or []:
        text = clean((item or {}).get("text"), "")
        if text:
            return text
    raise RuntimeError("openclaw agent result missing text payload")


def parse_compact_json(text: str) -> dict:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, re.S)
        if not match:
            raise RuntimeError(f"agent reply is not valid JSON: {text[:400]}")
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"agent reply JSON could not be parsed: {text[:400]}") from exc


def write_log(path: Path, payload: dict[str, object]) -> None:
    lines = [
        "# Market Feishu Doc Delivery",
        "",
        f"- `timestamp`: `{payload.get('timestamp', '')}`",
        f"- `status`: `{payload.get('status', '')}`",
        f"- `draft_pack_dir`: `{payload.get('draft_pack_dir', '')}`",
        f"- `markdown_path`: `{payload.get('markdown_path', '')}`",
        f"- `title`: `{payload.get('title', '')}`",
        f"- `agent_id`: `{payload.get('agent_id', '')}`",
        f"- `sidecar_path`: `{payload.get('sidecar_path', '')}`",
        f"- `source_fingerprint`: `{payload.get('source_fingerprint', '')}`",
    ]
    if payload.get("document_id"):
        lines.append(f"- `document_id`: `{payload.get('document_id')}`")
    if payload.get("url"):
        lines.append(f"- `url`: `{payload.get('url')}`")
    if payload.get("mode"):
        lines.append(f"- `mode`: `{payload.get('mode')}`")
    if payload.get("images_processed") is not None:
        lines.append(f"- `images_processed`: `{payload.get('images_processed')}`")
    if payload.get("blocks_added") is not None:
        lines.append(f"- `blocks_added`: `{payload.get('blocks_added')}`")
    if payload.get("error"):
        lines.append(f"- `error`: `{payload.get('error')}`")
    if payload.get("local_images"):
        lines.extend(
            [
                "",
                "## Local Images",
                "",
                "```json",
                json.dumps(payload["local_images"], ensure_ascii=False, indent=2),
                "```",
            ]
        )
    if payload.get("agent_payload") is not None:
        lines.extend(
            [
                "",
                "## Agent Payload",
                "",
                "```json",
                json.dumps(payload["agent_payload"], ensure_ascii=False, indent=2),
                "```",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def print_result(payload: dict) -> None:
    print(f"FEISHU_DOC_STATUS={clean(payload.get('status'), 'unknown')}")
    print(f"FEISHU_DOC_MODE={clean(payload.get('mode'), 'n/a')}")
    print(f"FEISHU_DOC_REUSED={'yes' if payload.get('reused') else 'no'}")
    print(f"FEISHU_DOC_TITLE={clean(payload.get('title'), 'n/a')}")
    print(f"FEISHU_DOC_TOKEN={clean(payload.get('document_id'), 'n/a')}")
    print(f"FEISHU_DOC_URL={clean(payload.get('url'), 'n/a')}")
    print(f"FEISHU_DOC_SIDECAR={clean(payload.get('sidecar_path'), 'n/a')}")
    print(f"FEISHU_DOC_SOURCE_FINGERPRINT={clean(payload.get('source_fingerprint'), 'n/a')}")
    print(f"FEISHU_DOC_IMAGES_PROCESSED={clean(payload.get('images_processed', 0), '0')}")
    print(f"FEISHU_DOC_BLOCKS_ADDED={clean(payload.get('blocks_added', 0), '0')}")


def main() -> None:
    args = parse_args()
    pack_dir = Path(args.draft_pack_dir).expanduser().resolve()
    markdown_path = resolve_markdown_path(pack_dir, args.markdown_path)
    if not pack_dir.exists():
        raise SystemExit(f"Draft pack directory missing: {pack_dir}")
    if not markdown_path.exists():
        raise SystemExit(f"Markdown source missing: {markdown_path}")

    raw_markdown = read_text(markdown_path)
    if not raw_markdown.strip():
        raise SystemExit(f"Markdown source is empty: {markdown_path}")

    draft_key = pack_dir.name
    title = clean(args.title, extract_title(raw_markdown, draft_key.replace("-", " ")))
    source_fingerprint, image_entries = compute_source_fingerprint(raw_markdown, pack_dir)
    sidecar_path = pack_dir / SIDECAR_NAME
    existing = load_json(sidecar_path)
    existing_doc_token = clean(existing.get("document_id"), "")
    existing_url = clean(existing.get("url"), "")
    existing_title = clean(existing.get("title"), "")
    title_changed = bool(existing_doc_token and existing_title and existing_title != title)

    base_payload: dict[str, object] = {
        "timestamp": format_ts(now_cn()),
        "draft_pack_dir": str(pack_dir),
        "markdown_path": str(markdown_path),
        "title": title,
        "agent_id": args.agent_id,
        "sidecar_path": str(sidecar_path),
        "source_fingerprint": source_fingerprint,
        "local_images": image_entries,
    }

    if not args.write:
        preview = {
            **base_payload,
            "status": "preview",
            "mode": "preview",
            "document_id": existing_doc_token or "n/a",
            "url": existing_url or "n/a",
            "reused": bool(existing_doc_token and existing.get("source_fingerprint") == source_fingerprint and not title_changed),
            "title_changed": title_changed,
            "images_processed": existing.get("images_processed", 0),
            "blocks_added": existing.get("blocks_added", 0),
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return

    timestamp_token = now_cn().strftime("%Y%m%d_%H%M%S")
    if existing_doc_token and existing_url and clean(existing.get("source_fingerprint"), "") == source_fingerprint and not title_changed:
        result_payload = {
            **base_payload,
            "status": "success",
            "mode": clean(existing.get("mode"), "reuse"),
            "document_id": existing_doc_token,
            "url": existing_url,
            "reused": True,
            "images_processed": existing.get("images_processed", 0),
            "blocks_added": existing.get("blocks_added", 0),
            "synced_at": format_ts(now_cn()),
        }
        save_json(sidecar_path, result_payload)
        log_path = LOG_DIR / f"{timestamp_token}__{draft_key}__feishu-doc-delivery.md"
        write_log(log_path, result_payload)
        print_result(result_payload)
        return

    try:
        staged_markdown_path, staged_entries = stage_markdown_for_feishu(raw_markdown, pack_dir, source_fingerprint)
        prompt = build_agent_prompt(staged_markdown_path, title, "" if title_changed else existing_doc_token)
        agent_payload = run_openclaw_agent(args.agent_id, prompt, args.timeout_seconds)
        agent_text = extract_agent_text(agent_payload)
        compact = parse_compact_json(agent_text)
        document_id = clean(compact.get("document_id"), existing_doc_token if not title_changed else "")
        if not document_id:
            raise RuntimeError(f"feishu doc delivery returned no document_id: {agent_text}")
        url = clean(compact.get("url"), f"https://feishu.cn/docx/{document_id}")
        mode = clean(compact.get("mode"), "update" if existing_doc_token and not title_changed else "create")
        result_payload = {
            **base_payload,
            "status": "success",
            "mode": mode,
            "document_id": document_id,
            "url": url,
            "reused": False,
            "title_changed": title_changed,
            "superseded_document_id": existing_doc_token if title_changed else "",
            "markdown_path": str(staged_markdown_path),
            "local_images": staged_entries or image_entries,
            "images_processed": max(int(compact.get("images_processed", 0) or 0), len(staged_entries)),
            "blocks_added": int(compact.get("blocks_added", 0) or 0),
            "synced_at": format_ts(now_cn()),
            "agent_payload": agent_payload,
        }
        save_json(sidecar_path, result_payload)
        log_path = LOG_DIR / f"{timestamp_token}__{draft_key}__feishu-doc-delivery.md"
        write_log(log_path, result_payload)
        print_result(result_payload)
    except Exception as exc:  # noqa: BLE001
        blocked_payload = {
            **base_payload,
            "status": "blocked",
            "mode": "blocked",
            "document_id": existing_doc_token,
            "url": existing_url,
            "error": str(exc),
        }
        save_json(sidecar_path, blocked_payload)
        blocked_log = LOG_DIR / f"{timestamp_token}__{draft_key}__feishu-doc-delivery-blocked.md"
        write_log(blocked_log, blocked_payload)
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
