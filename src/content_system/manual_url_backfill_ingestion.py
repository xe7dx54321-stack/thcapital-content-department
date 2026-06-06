"""Ingest manual URL backfill metadata without fetching page bodies."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


URL_RE = re.compile(r"https?://[^\s)>\]]+")


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__manual-url-backfill-ingestion.json",
        "dated_md": paths.logs_root / f"{run_date}__manual-url-backfill-ingestion.md",
        "latest_json": paths.logs_root / "latest_manual_url_backfill_ingestion.json",
        "latest_md": paths.logs_root / "latest_manual_url_backfill_ingestion.md",
    }


def item_from_backfill(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "manual_item_id": stable_id("manualurl", "fallback", task.get("task_id")),
        "source": "fallback_backfill_queue",
        "title": compact_text(task.get("suggested_query") or task.get("reason") or task.get("lane_id"), 180),
        "url": "",
        "lane_id": task.get("lane_id", ""),
        "priority": task.get("priority", "MEDIUM"),
        "status": "NEEDS_FETCH",
        "notes": compact_text(task.get("reason"), 240),
        "do_not_auto_fetch": True,
    }


def items_from_url_queue(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    items: list[dict[str, Any]] = []
    for line in text.splitlines():
        urls = URL_RE.findall(line)
        for url in urls:
            title = compact_text(URL_RE.sub("", line).strip(" -|[]()#\t") or url, 180)
            items.append(
                {
                    "manual_item_id": stable_id("manualurl", "queue", url),
                    "source": "url_capture_queue",
                    "title": title,
                    "url": url.rstrip(".,;"),
                    "lane_id": "manual_url_backfill",
                    "priority": "MEDIUM",
                    "status": "READY_FOR_REVIEW",
                    "notes": "Read from local URL capture queue; not fetched automatically.",
                    "do_not_auto_fetch": True,
                }
            )
    return items


def build_manual_url_backfill_ingestion(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    backfill = read_json(paths.logs_root / "latest_fallback_backfill_queue.json")
    url_queue = repo_root / "内容素材库" / "URL抓取" / "url_capture_queue.md"
    raw_items = [item_from_backfill(task) for task in list_payload(backfill, "backfill_tasks")]
    raw_items.extend(items_from_url_queue(url_queue))
    seen_urls: set[str] = set()
    items: list[dict[str, Any]] = []
    for item in raw_items:
        url = str(item.get("url") or "")
        if url and url in seen_urls:
            item = {**item, "status": "DUPLICATE"}
        elif url:
            seen_urls.add(url)
        elif item.get("source") == "url_capture_queue":
            item = {**item, "status": "INVALID"}
        items.append(item)
    summary = {
        "manual_item_count": len(items),
        "ready_for_review": sum(1 for item in items if item.get("status") == "READY_FOR_REVIEW"),
        "needs_fetch": sum(1 for item in items if item.get("status") == "NEEDS_FETCH"),
        "invalid": sum(1 for item in items if item.get("status") == "INVALID"),
        "duplicate": sum(1 for item in items if item.get("status") == "DUPLICATE"),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "manual_items": items,
        "summary": summary,
        "inputs": {
            "url_capture_queue": str(url_queue),
            "url_capture_queue_exists": url_queue.exists(),
        },
        "policy": {
            "do_not_auto_fetch": True,
            "read_only_local_queue": True,
            "no_source_file_mutation": True,
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = [
        {
            "source": item.get("source"),
            "status": item.get("status"),
            "priority": item.get("priority"),
            "title": compact_text(item.get("title"), 80),
        }
        for item in list_payload(payload, "manual_items")[:30]
    ]
    return f"""# Manual URL Backfill Ingestion

## Summary

- manual_item_count: `{summary.get('manual_item_count', 0)}`
- ready_for_review: `{summary.get('ready_for_review', 0)}`
- needs_fetch: `{summary.get('needs_fetch', 0)}`
- invalid: `{summary.get('invalid', 0)}`
- duplicate: `{summary.get('duplicate', 0)}`

## Manual Items

{markdown_table(rows, ('source', 'status', 'priority', 'title'))}

## Boundary

The local URL capture queue is read-only. Manual URLs are not fetched automatically and are not committed.
"""
