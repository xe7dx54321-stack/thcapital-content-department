"""Run selected OpenClaw metadata-only source connectors."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


SOURCE_URLS = {
    "trend__reddit_localllama_daily": "https://www.reddit.com/r/LocalLLaMA/",
    "trend__reddit_claude_daily": "https://www.reddit.com/r/ClaudeAI/",
    "trend__reddit_chatgpt_daily": "https://www.reddit.com/r/ChatGPT/",
    "trend__yc_launches_ai": "https://www.ycombinator.com/launches",
    "web__techcrunch_ai": "https://techcrunch.com/category/artificial-intelligence/",
    "web__finsmes_ai_gnews": "https://www.finsmes.com/?s=AI",
    "trend__trend_hunt_ai_agents": "https://www.producthunt.com/topics/artificial-intelligence",
    "web__deeplearning_ai_batch": "https://www.deeplearning.ai/the-batch/",
    "web__latent_space": "https://www.latent.space/",
    "web__interconnects": "https://www.interconnects.ai/",
    "web__simon_willison": "https://simonwillison.net/",
    "web__understanding_ai": "https://www.understandingai.org/",
    "web__infoq_ai_ml": "https://www.infoq.com/ai-ml-data-eng/",
    "wechat__36kr": "https://36kr.com/",
    "wechat__geekpark": "https://www.geekpark.net/",
    "youtube__openai": "https://www.youtube.com/@OpenAI",
    "youtube__ycombinator": "https://www.youtube.com/@ycombinator",
    "youtube__googledeepmind": "https://www.youtube.com/@googledeepmind",
}


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__openclaw-metadata-connector-run.json",
        "dated_md": paths.logs_root / f"{run_date}__openclaw-metadata-connector-run.md",
        "latest_json": paths.logs_root / "latest_openclaw_metadata_connector_run.json",
        "latest_md": paths.logs_root / "latest_openclaw_metadata_connector_run.md",
    }


def is_weak(connector_type: str, role: str) -> bool:
    return connector_type in {"reddit_metadata", "youtube_metadata", "x_metadata", "trend_heat_metadata", "wechat_metadata"} or role in {
        "weak_signal",
        "heat_validation",
        "manual_only",
    }


def source_url(candidate: dict[str, Any]) -> str:
    source_id = str(candidate.get("source_id") or "")
    if source_id in SOURCE_URLS:
        return SOURCE_URLS[source_id]
    if source_id.startswith("candidate:"):
        return ""
    return ""


def status_for_group(connector_type: str, candidates: list[dict[str, Any]]) -> str:
    if not candidates:
        return "EMPTY"
    if connector_type in {"x_metadata"}:
        return "SKIPPED"
    if all(str(item.get("evidence_role")) == "manual_only" for item in candidates):
        return "MANUAL_ONLY"
    if connector_type == "wechat_metadata":
        return "MANUAL_ONLY"
    return "SUCCESS"


def item_from_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    connector_type = str(candidate.get("connector_type") or "manual_backfill")
    role = str(candidate.get("evidence_role") or "manual_only")
    weak = is_weak(connector_type, role)
    url = source_url(candidate)
    source_name = str(candidate.get("source_name") or candidate.get("source_id") or "")
    title = f"OpenClaw source metadata: {source_name}"
    return {
        "item_id": stable_id("ocitem", candidate.get("source_id"), connector_type),
        "source_id": candidate.get("source_id", ""),
        "source_name": source_name,
        "title": title,
        "url": url,
        "published_at": "",
        "fetched_at": utc_now(),
        "summary": compact_text(
            f"Metadata-only migrated OpenClaw source for lane {candidate.get('lane')}. Evidence role: {role}.",
            260,
        ),
        "lane": candidate.get("lane", ""),
        "evidence_role": role if role in {"supporting_evidence", "weak_signal", "heat_validation", "manual_only"} else "manual_only",
        "metadata_only": True,
        "copyright_safe": True,
        "weak_signal": weak,
        "do_not_use_as_hard_evidence": True,
    }


def build_connector(connector_type: str, candidates: list[dict[str, Any]]) -> dict[str, Any]:
    status = status_for_group(connector_type, candidates)
    if status == "SKIPPED":
        items: list[dict[str, Any]] = []
        error = "Skipped because this connector commonly requires login/API or account-state access."
    else:
        items = [item_from_candidate(candidate) for candidate in candidates]
        error = ""
    return {
        "connector_type": connector_type,
        "lane": candidates[0].get("lane", "") if candidates else "",
        "status": status,
        "source_count": len(candidates),
        "item_count": len(items),
        "error": error,
        "items": items,
    }


def run_openclaw_metadata_connectors(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    plan_path = paths.logs_root / "latest_openclaw_migration_plan.json"
    inventory_path = paths.logs_root / "latest_openclaw_source_inventory.json"
    plan = read_json(plan_path)
    inventory = read_json(inventory_path)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in list_payload(plan, "migration_candidates"):
        if not candidate.get("safe_to_implement_now"):
            continue
        grouped[str(candidate.get("connector_type") or "manual_backfill")].append(candidate)
    connectors = [build_connector(connector_type, items) for connector_type, items in sorted(grouped.items())]
    summary = {
        "connector_count": len(connectors),
        "success_connectors": sum(1 for item in connectors if item.get("status") == "SUCCESS"),
        "failed_connectors": sum(1 for item in connectors if item.get("status") == "FAILED"),
        "manual_only_connectors": sum(1 for item in connectors if item.get("status") == "MANUAL_ONLY"),
        "item_count": sum(int(item.get("item_count") or 0) for item in connectors),
        "weak_signal_items": sum(1 for connector in connectors for item in connector.get("items", []) if isinstance(item, dict) and item.get("weak_signal")),
    }
    warnings = []
    if not plan_path.exists():
        warnings.append(f"Missing input: {plan_path}")
    if not inventory_path.exists():
        warnings.append(f"Missing input: {inventory_path}")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "connectors": connectors,
        "summary": summary,
        "context": {
            "inventory_source_count": len(list_payload(inventory, "sources")),
            "migration_candidate_count": len(list_payload(plan, "migration_candidates")),
        },
        "warnings": warnings,
        "policy": {
            "metadata_only": True,
            "copyright_safe": True,
            "no_full_text": True,
            "no_api_key": True,
            "no_login_or_paywall_bypass": True,
            "no_openclaw_gateway": True,
            "no_openclaw_cron_migration": True,
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
            "sources": item.get("source_count"),
            "items": item.get("item_count"),
            "lane": item.get("lane"),
        }
        for item in list_payload(payload, "connectors")
    ]
    return f"""# OpenClaw Metadata Connector Run

## Summary

- connector_count: `{summary.get('connector_count', 0)}`
- success_connectors: `{summary.get('success_connectors', 0)}`
- failed_connectors: `{summary.get('failed_connectors', 0)}`
- manual_only_connectors: `{summary.get('manual_only_connectors', 0)}`
- item_count: `{summary.get('item_count', 0)}`
- weak_signal_items: `{summary.get('weak_signal_items', 0)}`

## Connectors

{markdown_table(rows, ('connector', 'status', 'sources', 'items', 'lane'))}

## Boundary

This connector run emits metadata-only sidecar items. It does not fetch full text, start OpenClaw gateway, migrate cron jobs, use API keys, or bypass login/paywalls.
"""
