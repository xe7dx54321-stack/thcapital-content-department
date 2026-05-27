"""Daily LLM cost and call-count guard."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, safe_int, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class CostBudgetGuardReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    daily_cost_limit_usd: float
    estimated_cost_today_usd: float
    max_calls_per_day: int
    calls_today: int
    remaining_budget_usd: float
    remaining_calls: int
    recommended_mode: str
    issues: tuple[str, ...]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__cost-budget-guard.json",
        "dated_md": paths.logs_root / f"{run_date}__cost-budget-guard.md",
        "latest_json": paths.logs_root / "latest_cost_budget_guard.json",
        "latest_md": paths.logs_root / "latest_cost_budget_guard.md",
    }


def config_limits(paths: ProjectPaths) -> dict[str, Any]:
    config = read_json(paths.repo_root / "config" / "llm_providers.json")
    limits = config.get("limits") if isinstance(config.get("limits"), dict) else {}
    return limits


def env_float(name: str, fallback: float) -> float:
    value = os.environ.get(name, "").strip()
    return safe_float(value) if value else fallback


def env_int(name: str, fallback: int) -> int:
    value = os.environ.get(name, "").strip()
    return safe_int(value) if value else fallback


def build_cost_budget_guard(paths: ProjectPaths) -> CostBudgetGuardReport:
    run_date = today_token()
    limits = config_limits(paths)
    daily_limit = env_float("THCAP_LLM_DAILY_COST_LIMIT_USD", safe_float(limits.get("daily_cost_limit_usd") or 2.0))
    max_calls = env_int("THCAP_LLM_MAX_CALLS_PER_DAY", safe_int(limits.get("max_calls_per_run") or 20))
    agent_log = read_json(paths.logs_root / "agent_run_log.json")
    records = [
        record
        for record in list_payload(agent_log, "records")
        if str(record.get("run_date") or "").replace("-", "")[:8] == run_date
    ]
    if not records:
        summary = read_json(paths.logs_root / "latest_agent_run_summary.json")
        records = [
            record
            for record in list_payload(summary, "records")
            if str(record.get("run_date") or "").replace("-", "")[:8] == run_date
        ]
    estimated_cost = round(sum(safe_float(record.get("estimated_cost_usd")) for record in records), 6)
    calls_today = len(records)
    remaining_budget = round(max(daily_limit - estimated_cost, 0.0), 6)
    remaining_calls = max(max_calls - calls_today, 0)
    issues: list[str] = []
    if estimated_cost >= daily_limit and daily_limit >= 0:
        issues.append("Daily cost limit reached or exceeded.")
    elif daily_limit > 0 and estimated_cost >= daily_limit * 0.8:
        issues.append("Daily cost is above 80% of the limit.")
    if calls_today >= max_calls:
        issues.append("Daily call limit reached or exceeded.")
    elif max_calls > 0 and calls_today >= int(max_calls * 0.8):
        issues.append("Daily call count is above 80% of the limit.")
    if any("exceeded" in issue or "reached" in issue for issue in issues):
        status = "BLOCK"
    elif issues:
        status = "WARN"
    else:
        status = "ALLOW"
    recommended_mode = "dry_run" if status == "BLOCK" else "live"
    return CostBudgetGuardReport(
        SCHEMA_VERSION,
        utc_now(),
        run_date,
        status,
        daily_limit,
        estimated_cost,
        max_calls,
        calls_today,
        remaining_budget,
        remaining_calls,
        recommended_mode,
        tuple(issues),
    )


def render_markdown(report: CostBudgetGuardReport) -> str:
    issues = "\n".join(f"- {item}" for item in report.issues) if report.issues else "- None"
    return f"""# Cost Budget Guard

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**
- Daily cost limit USD: `{report.daily_cost_limit_usd}`
- Estimated cost today USD: `{report.estimated_cost_today_usd}`
- Max calls per day: `{report.max_calls_per_day}`
- Calls today: `{report.calls_today}`
- Remaining budget USD: `{report.remaining_budget_usd}`
- Remaining calls: `{report.remaining_calls}`
- Recommended mode: `{report.recommended_mode}`

## Issues

{issues}
"""


def write_cost_budget_guard(report: CostBudgetGuardReport, paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    outputs = output_paths(paths, report.run_date)
    payload = asdict(report)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return write_json_and_markdown(payload, render_markdown(report), outputs)


def report_to_dict(report: CostBudgetGuardReport) -> dict[str, Any]:
    return asdict(report)
