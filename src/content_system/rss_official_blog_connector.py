"""Run lightweight RSS / official blog metadata connectors."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.source_connector_common import count_by_status, fetch_url, item_count_from_rows, parse_feed_items, parse_html_index_items, source_status
from content_system.upstream_intelligence_common import compact_text, markdown_table


KNOWN_URLS = {
    "OpenAI News": ["https://openai.com/news/"],
    "Anthropic News": ["https://www.anthropic.com/news/"],
    "Google DeepMind Blog": ["https://deepmind.google/blog/"],
    "Google AI Blog": ["https://blog.google/technology/ai/"],
    "Meta AI Blog": ["https://ai.meta.com/blog/"],
    "Microsoft AI Blog": ["https://blogs.microsoft.com/ai/"],
    "NVIDIA AI Blog": ["https://developer.nvidia.com/blog/category/generative-ai/", "https://developer.nvidia.com/blog/feed/"],
}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__rss-official-blog-connector-run.json",
        "dated_md": paths.logs_root / f"{run_date}__rss-official-blog-connector-run.md",
        "latest_json": paths.logs_root / "latest_rss_official_blog_connector_run.json",
        "latest_md": paths.logs_root / "latest_rss_official_blog_connector_run.md",
    }


def selected_rss_sources(selection: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in list_payload(selection, "selected_sources")
        if item.get("implementation_status") == "SELECTED" and item.get("connector_type") == "rss_official_blog"
    ]


def candidate_urls(source: dict[str, Any]) -> list[str]:
    urls: list[str] = []
    configured = str(source.get("configured_url") or "")
    if configured:
        urls.append(configured)
    urls.extend(KNOWN_URLS.get(str(source.get("source_name") or ""), []))
    deduped: list[str] = []
    for url in urls:
        if url and url not in deduped:
            deduped.append(url)
    return deduped


def run_source(source: dict[str, Any], fetched_at: str) -> dict[str, Any]:
    source_name = str(source.get("source_name") or "official_blog")
    errors: list[str] = []
    for url in candidate_urls(source):
        try:
            text, content_type = fetch_url(url)
            if "xml" in content_type.lower() or text.lstrip().startswith("<?xml") or "<rss" in text[:500].lower() or "<feed" in text[:500].lower():
                items = parse_feed_items(text, source_name, "rss_official_blog", limit=12)
                fetch_method = "rss"
            else:
                items = parse_html_index_items(text, url, source_name, "rss_official_blog", limit=12)
                fetch_method = "html_index"
            for item in items:
                item["fetched_at"] = fetched_at
            return {
                "source_id": source.get("selection_id", ""),
                "source_name": source_name,
                "status": source_status(len(items)),
                "fetch_method": fetch_method,
                "item_count": len(items),
                "error": "",
                "items": items,
            }
        except Exception as exc:  # noqa: BLE001 - source errors are report data.
            errors.append(f"{url}: {exc}")
            continue
    return {
        "source_id": source.get("selection_id", ""),
        "source_name": source_name,
        "status": "FAILED" if errors else "SKIPPED",
        "fetch_method": "configured_url",
        "item_count": 0,
        "error": compact_text("; ".join(errors), 400),
        "items": [],
    }


def build_rss_official_blog_connector_run(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    fetched_at = utc_now()
    selection = read_json(paths.logs_root / "latest_p0_source_connector_selection.json")
    sources = [run_source(source, fetched_at) for source in selected_rss_sources(selection)]
    summary = {
        "source_count": len(sources),
        "success_sources": count_by_status(sources, "SUCCESS"),
        "failed_sources": count_by_status(sources, "FAILED"),
        "empty_sources": count_by_status(sources, "EMPTY"),
        "item_count": item_count_from_rows(sources),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": fetched_at,
        "run_date": run_date,
        "connector": "rss_official_blog",
        "sources": sources,
        "summary": summary,
        "policy": {
            "metadata_only": True,
            "copyright_safe": True,
            "no_full_text": True,
            "no_login": True,
            "no_api_key": True,
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
            "source": item.get("source_name"),
            "status": item.get("status"),
            "method": item.get("fetch_method"),
            "items": item.get("item_count"),
            "error": compact_text(item.get("error"), 70),
        }
        for item in list_payload(payload, "sources")
    ]
    return f"""# RSS / Official Blog Connector Run

## Summary

- source_count: `{summary.get('source_count', 0)}`
- success_sources: `{summary.get('success_sources', 0)}`
- failed_sources: `{summary.get('failed_sources', 0)}`
- empty_sources: `{summary.get('empty_sources', 0)}`
- item_count: `{summary.get('item_count', 0)}`

## Sources

{markdown_table(rows, ('source', 'status', 'method', 'items', 'error'))}

## Boundary

Metadata only. No full text, no login, no API key, and single-source failures remain local to this report.
"""
