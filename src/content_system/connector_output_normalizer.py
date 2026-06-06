"""Normalize connector outputs into a shared upstream item contract."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, detect_event_type, detect_lane, markdown_table, stable_id


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__normalized-upstream-items.json",
        "dated_md": paths.logs_root / f"{run_date}__normalized-upstream-items.md",
        "latest_json": paths.logs_root / "latest_normalized_upstream_items.json",
        "latest_md": paths.logs_root / "latest_normalized_upstream_items.md",
    }


def normalize_text(value: Any) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", str(value or "").lower())


def dedupe_key(title: str, url: str) -> str:
    if url:
        return url.split("#", 1)[0].rstrip("/")
    return normalize_text(title)


def upstream_item(raw: dict[str, Any], source_type: str) -> dict[str, Any] | None:
    title = compact_text(raw.get("title"), 220)
    url = str(raw.get("url") or "").strip()
    if not title or not url:
        return None
    source_name = str(raw.get("source_name") or raw.get("source") or source_type)
    lane_id = detect_lane(title, source_name)
    tags = raw.get("tags") if isinstance(raw.get("tags"), list) else []
    event_type = detect_event_type(title)
    return {
        "upstream_item_id": stable_id("upitem", source_type, title, url),
        "title": title,
        "url": url,
        "source_name": source_name,
        "source_type": source_type,
        "lane_id": lane_id,
        "event_type": event_type,
        "domain_tags": [lane_id, event_type, *[str(tag) for tag in tags[:4]]],
        "published_at": raw.get("published_at", ""),
        "fetched_at": raw.get("fetched_at", ""),
        "summary": compact_text(raw.get("summary") or raw.get("notes") or "", 280),
        "dedupe_key": dedupe_key(title, url),
        "metadata_only": bool(raw.get("metadata_only", True)),
        "copyright_safe": bool(raw.get("copyright_safe", True)),
        "candidate_for_hot_material_pool": bool(raw.get("metadata_only", True)) and bool(raw.get("copyright_safe", True)),
    }


def collect_items(rss: dict[str, Any], research: dict[str, Any], manual: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for source in list_payload(rss, "sources"):
        for item in list_payload(source, "items"):
            normalized = upstream_item({**item, "source_name": source.get("source_name") or item.get("source_name")}, "rss_official_blog")
            if normalized:
                items.append(normalized)
    for connector in list_payload(research, "connectors"):
        connector_type = str(connector.get("connector_type") or "github")
        for item in list_payload(connector, "items"):
            normalized = upstream_item({**item, "source_name": connector.get("query_or_source") or item.get("source_name")}, connector_type)
            if normalized:
                items.append(normalized)
    for item in list_payload(manual, "manual_items"):
        if item.get("status") != "READY_FOR_REVIEW":
            continue
        normalized = upstream_item(item, "manual_url")
        if normalized:
            items.append(normalized)
    return items


def build_normalized_upstream_items(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    rss = read_json(paths.logs_root / "latest_rss_official_blog_connector_run.json")
    research = read_json(paths.logs_root / "latest_lightweight_research_connector_run.json")
    manual = read_json(paths.logs_root / "latest_manual_url_backfill_ingestion.json")
    raw_items = collect_items(rss, research, manual)
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    deduped = 0
    for item in raw_items:
        key = str(item.get("dedupe_key") or item.get("upstream_item_id"))
        if key in seen:
            deduped += 1
            continue
        seen.add(key)
        items.append(item)
    summary = {
        "item_count": len(items),
        "deduped_count": deduped,
        "candidate_for_hot_material_pool": sum(1 for item in items if item.get("candidate_for_hot_material_pool")),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "items": items,
        "summary": summary,
        "policy": {
            "metadata_only": True,
            "copyright_safe": True,
            "no_full_text": True,
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
            "source_type": item.get("source_type"),
            "lane": item.get("lane_id"),
            "candidate": item.get("candidate_for_hot_material_pool"),
            "title": compact_text(item.get("title"), 80),
        }
        for item in list_payload(payload, "items")[:40]
    ]
    return f"""# Normalized Upstream Items

## Summary

- item_count: `{summary.get('item_count', 0)}`
- deduped_count: `{summary.get('deduped_count', 0)}`
- candidate_for_hot_material_pool: `{summary.get('candidate_for_hot_material_pool', 0)}`

## Items

{markdown_table(rows, ('source_type', 'lane', 'candidate', 'title'))}

## Boundary

Normalized items are metadata-only and copyright-safe. No full text is retained.
"""
