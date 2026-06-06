"""Run lightweight GitHub / HuggingFace / arXiv metadata connectors."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.source_connector_common import fetch_url, parse_feed_items, parse_html_index_items
from content_system.upstream_intelligence_common import compact_text, markdown_table


GITHUB_URLS = {
    "LangChain Releases": "https://github.com/langchain-ai/langchain/releases.atom",
    "LlamaIndex Releases": "https://github.com/run-llama/llama_index/releases.atom",
    "AutoGen Releases": "https://github.com/microsoft/autogen/releases.atom",
    "CrewAI Releases": "https://github.com/crewAIInc/crewAI/releases.atom",
    "GitHub Trending AI / Agent": "https://github.com/trending/python?since=daily",
}

HUGGINGFACE_URLS = {
    "Hugging Face Blog": "https://huggingface.co/blog/feed.xml",
    "Hugging Face Papers": "https://huggingface.co/papers.rss",
}

ARXIV_URLS = {
    "arXiv AI / LLM / Agent queries": "https://export.arxiv.org/api/query?search_query=all:%28LLM%20OR%20agent%20OR%20AI%20infrastructure%29&sortBy=submittedDate&sortOrder=descending&max_results=20",
}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__lightweight-research-connector-run.json",
        "dated_md": paths.logs_root / f"{run_date}__lightweight-research-connector-run.md",
        "latest_json": paths.logs_root / "latest_lightweight_research_connector_run.json",
        "latest_md": paths.logs_root / "latest_lightweight_research_connector_run.md",
    }


def selected_sources(selection: dict[str, Any], connector_type: str) -> list[dict[str, Any]]:
    return [
        item
        for item in list_payload(selection, "selected_sources")
        if item.get("implementation_status") == "SELECTED" and item.get("connector_type") == connector_type
    ]


def run_one(connector_type: str, query_or_source: str, url: str, fetched_at: str) -> dict[str, Any]:
    try:
        text, content_type = fetch_url(url)
        source_type = "github" if connector_type == "github" else connector_type
        if connector_type == "github" and "trending" in url:
            items = parse_html_index_items(text, url, query_or_source, "github", limit=15)
        elif "xml" in content_type.lower() or text.lstrip().startswith("<?xml") or "<feed" in text[:500].lower() or "<rss" in text[:500].lower():
            items = parse_feed_items(text, query_or_source, source_type, limit=15)
        else:
            items = parse_html_index_items(text, url, query_or_source, source_type, limit=15)
        for item in items:
            item["fetched_at"] = fetched_at
        status = "SUCCESS" if items else "EMPTY"
        return {
            "connector_type": connector_type,
            "status": status,
            "query_or_source": query_or_source,
            "item_count": len(items),
            "error": "",
            "items": items,
        }
    except Exception as exc:  # noqa: BLE001 - connector errors are report data.
        return {
            "connector_type": connector_type,
            "status": "FAILED",
            "query_or_source": query_or_source,
            "item_count": 0,
            "error": compact_text(str(exc), 300),
            "items": [],
        }


def build_lightweight_research_connector_run(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    fetched_at = utc_now()
    selection = read_json(paths.logs_root / "latest_p0_source_connector_selection.json")
    backfill = read_json(paths.logs_root / "latest_fallback_backfill_queue.json")
    connectors: list[dict[str, Any]] = []
    for source in selected_sources(selection, "github_repo"):
        name = str(source.get("source_name") or "")
        url = GITHUB_URLS.get(name)
        if url:
            connectors.append(run_one("github", name, url, fetched_at))
    for source in selected_sources(selection, "huggingface_feed"):
        name = str(source.get("source_name") or "")
        url = HUGGINGFACE_URLS.get(name)
        if url:
            connectors.append(run_one("huggingface", name, url, fetched_at))
    for source in selected_sources(selection, "arxiv_keyword"):
        name = str(source.get("source_name") or "arXiv AI / Agent query")
        url = ARXIV_URLS.get(name) or source.get("configured_url") or ARXIV_URLS["arXiv AI / LLM / Agent queries"]
        connectors.append(run_one("arxiv", name, str(url), fetched_at))
    if not connectors:
        for task in list_payload(backfill, "backfill_tasks")[:3]:
            connectors.append(
                {
                    "connector_type": "arxiv",
                    "status": "SKIPPED",
                    "query_or_source": task.get("suggested_query", ""),
                    "item_count": 0,
                    "error": "No selected research connector; fallback task left for manual review.",
                    "items": [],
                }
            )
    summary = {
        "connector_count": len(connectors),
        "success_connectors": sum(1 for item in connectors if item.get("status") == "SUCCESS"),
        "failed_connectors": sum(1 for item in connectors if item.get("status") == "FAILED"),
        "item_count": sum(int(item.get("item_count") or 0) for item in connectors),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": fetched_at,
        "run_date": run_date,
        "connectors": connectors,
        "summary": summary,
        "policy": {
            "metadata_only": True,
            "copyright_safe": True,
            "no_full_text": True,
            "no_pdf_download": True,
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
            "connector": item.get("connector_type"),
            "status": item.get("status"),
            "source": compact_text(item.get("query_or_source"), 45),
            "items": item.get("item_count"),
            "error": compact_text(item.get("error"), 70),
        }
        for item in list_payload(payload, "connectors")
    ]
    return f"""# Lightweight Research Connector Run

## Summary

- connector_count: `{summary.get('connector_count', 0)}`
- success_connectors: `{summary.get('success_connectors', 0)}`
- failed_connectors: `{summary.get('failed_connectors', 0)}`
- item_count: `{summary.get('item_count', 0)}`

## Connectors

{markdown_table(rows, ('connector', 'status', 'source', 'items', 'error'))}

## Boundary

No GitHub token, no API key, no PDF download, no full text capture.
"""
