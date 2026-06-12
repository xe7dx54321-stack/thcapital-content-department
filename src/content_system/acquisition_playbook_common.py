"""Shared helpers for Phase31C acquisition playbooks."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import repo_relative, safe_int, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import markdown_table


SCHEMA_VERSION = "v1"
TIME_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
ALLOWED_FETCH_METHODS = {
    "rss",
    "atom",
    "official_blog_index",
    "public_html_index",
    "public_metadata",
    "github_release",
    "github_trending",
    "huggingface_feed",
    "arxiv_query",
    "newsletter_archive",
    "manual_url",
    "manual_only",
    "disabled",
}
FORBIDDEN_FETCH_METHODS = {"browser_login", "paywall_bypass", "full_text_scrape", "credentialed_fetch"}
WEAK_LANES = {"developer_community", "reddit_llm_discussion", "wechat_metadata", "youtube_signal", "x_signal", "trend_heat_validation", "keyword_discovery"}


def config_path(repo_root: Path, filename: str) -> Path:
    return repo_root / "config" / filename


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    return loaded if isinstance(loaded, dict) else {}


def load_config(repo_root: Path, filename: str) -> dict[str, Any]:
    return load_yaml(config_path(repo_root, filename))


def mapping(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    return value if isinstance(value, dict) else {}


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def unique_list(items: list[Any]) -> list[Any]:
    seen: set[str] = set()
    output = []
    for item in items:
        marker = str(item)
        if marker in seen:
            continue
        seen.add(marker)
        output.append(item)
    return output


def parse_minutes(value: str) -> int:
    if not TIME_RE.match(str(value)):
        raise ValueError(f"invalid HH:MM time: {value}")
    hour, minute = str(value).split(":", 1)
    return int(hour) * 60 + int(minute)


def grouped_slot_key(time_value: str, window_minutes: int) -> str:
    minutes = parse_minutes(time_value)
    group_start = (minutes // max(1, window_minutes)) * max(1, window_minutes)
    return f"{group_start // 60:02d}:{group_start % 60:02d}"


def source_lane_map(source_playbooks: dict[str, Any]) -> dict[str, str]:
    return {source_id: str(source.get("lane") or "") for source_id, source in source_playbooks.items() if isinstance(source, dict)}


def sources_for_lane(source_playbooks: dict[str, Any], lane: str) -> list[tuple[str, dict[str, Any]]]:
    output = []
    for source_id, source in source_playbooks.items():
        if not isinstance(source, dict):
            continue
        secondary = [str(item) for item in list_value(source.get("secondary_lanes"))]
        if source.get("lane") == lane or lane in secondary:
            output.append((str(source_id), source))
    return output


def validation_payload(checks: list[dict[str, Any]], extra: dict[str, Any] | None = None) -> dict[str, Any]:
    pass_count = sum(1 for item in checks if item.get("status") == "PASS")
    warn_count = sum(1 for item in checks if item.get("status") == "WARN")
    fail_count = sum(1 for item in checks if item.get("status") == "FAIL")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "PASS" if fail_count == 0 and warn_count == 0 else ("ACTIONABLE" if fail_count == 0 else "FAIL"),
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "pass": pass_count,
            "warn": warn_count,
            "fail": fail_count,
            "blocking_failures": fail_count,
        },
    }
    if extra:
        payload.update(extra)
    return payload


def check(checks: list[dict[str, Any]], check_id: str, condition: bool, message: str, warn: bool = False) -> None:
    if condition:
        status = "WARN" if warn else "PASS"
    else:
        status = "WARN" if warn else "FAIL"
    checks.append({"check_id": check_id, "status": status, "message": message})


def write_latest_report(paths: ProjectPaths, repo_root: Path, slug: str, payload: dict[str, Any], markdown: str) -> dict[str, Path]:
    outputs = {
        "latest_json": paths.logs_root / f"latest_{slug}.json",
        "latest_md": paths.logs_root / f"latest_{slug}.md",
    }
    write_json_and_markdown(payload, markdown, outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return outputs


def write_dated_and_latest_report(paths: ProjectPaths, repo_root: Path, slug: str, payload: dict[str, Any], markdown: str) -> dict[str, Path]:
    run_date = str(payload.get("run_date") or today_token())
    outputs = {
        "dated_json": paths.logs_root / f"{run_date}__{slug}.json",
        "dated_md": paths.logs_root / f"{run_date}__{slug}.md",
        "latest_json": paths.logs_root / f"latest_{slug.replace('-', '_')}.json",
        "latest_md": paths.logs_root / f"latest_{slug.replace('-', '_')}.md",
    }
    write_json_and_markdown(payload, markdown, outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return outputs


def basic_markdown(title: str, summary: dict[str, Any], rows: list[dict[str, Any]] | None = None, columns: tuple[str, ...] = ()) -> str:
    summary_rows = "\n".join(f"- {key}: `{value}`" for key, value in summary.items())
    table = markdown_table(rows or [], columns) if rows and columns else ""
    return f"""# {title}

## Summary

{summary_rows}

{table}
"""


def count_by(items: list[dict[str, Any]], key: str) -> Counter[str]:
    return Counter(str(item.get(key) or "") for item in items)


def collect_config_summary(repo_root: Path) -> dict[str, Any]:
    lanes = mapping(load_config(repo_root, "acquisition_lanes.yaml"), "lanes")
    cadence = mapping(load_config(repo_root, "acquisition_cadence.yaml"), "lanes")
    sources = mapping(load_config(repo_root, "acquisition_source_playbooks.yaml"), "sources")
    queries = mapping(load_config(repo_root, "acquisition_query_strategies.yaml"), "strategies")
    fallbacks = mapping(load_config(repo_root, "acquisition_fallback_strategies.yaml"), "strategies")
    routes = mapping(load_config(repo_root, "acquisition_downstream_routing.yaml"), "routes")
    return {
        "lanes": lanes,
        "cadence": cadence,
        "sources": sources,
        "queries": queries,
        "fallbacks": fallbacks,
        "routes": routes,
    }


def expected_runtime_slots_for_today(cadence: dict[str, Any]) -> list[dict[str, Any]]:
    today = datetime.now().strftime("%Y-%m-%d")
    slots = []
    for lane, item in cadence.items():
        if not isinstance(item, dict):
            continue
        for time_value in list_value(item.get("schedules")):
            slots.append(
                {
                    "lane": lane,
                    "business_date": today,
                    "time": str(time_value),
                    "catchup_policy": item.get("catchup_policy", "latest_only"),
                    "network_requirement": item.get("network_requirement", "mixed"),
                }
            )
    return sorted(slots, key=lambda item: (item["time"], item["lane"]))


def source_fetch_key(source_id: str, source: dict[str, Any], group_key: str) -> str:
    return f"{source.get('fetch_method')}::{source.get('url') or source_id}::{group_key}"


def grouped_runtime_runs(cadence: dict[str, Any], sources: dict[str, Any], window_minutes: int = 20) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    lane_runs = expected_runtime_slots_for_today(cadence)
    groups: dict[str, dict[str, Any]] = defaultdict(lambda: {"lanes": set(), "source_keys": set(), "connector_runs": []})
    for run in lane_runs:
        group_key = grouped_slot_key(run["time"], window_minutes)
        group = groups[group_key]
        group["lanes"].add(run["lane"])
        for source_id, source in sources_for_lane(sources, str(run["lane"])):
            fetch_key = source_fetch_key(source_id, source, group_key)
            if fetch_key not in group["source_keys"]:
                group["source_keys"].add(fetch_key)
                group["connector_runs"].append(
                    {
                        "source_id": source_id,
                        "lane": run["lane"],
                        "fetch_method": source.get("fetch_method"),
                        "group_key": group_key,
                    }
                )
    grouped = [
        {
            "group_key": key,
            "lanes": sorted(value["lanes"]),
            "connector_runs": value["connector_runs"],
            "connector_run_count": len(value["connector_runs"]),
        }
        for key, value in sorted(groups.items())
    ]
    return lane_runs, grouped


def safe_ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def safe_positive_int(value: Any, default: int = 0) -> int:
    parsed = safe_int(value)
    return parsed if parsed > 0 else default
