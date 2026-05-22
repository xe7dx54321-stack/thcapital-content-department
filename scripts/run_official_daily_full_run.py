#!/usr/bin/env python3
"""Run the official lane daily flow end to end.

P0-016 is an orchestration wrapper. It does not rewrite the official lane
fetcher, add retry/fallback behavior, create a scheduler, or introduce a DB.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402


HARD_STOP_STEPS = {
    "official_lane_health_check",
    "source_runtime_health",
    "daily_source_summary",
}


@dataclass(frozen=True)
class FullRunStep:
    name: str
    command: str
    returncode: int
    status: str
    started_at: str
    finished_at: str
    stdout_tail: str
    stderr_tail: str


@dataclass(frozen=True)
class OfficialDailyFullRun:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    steps: list[FullRunStep]
    outputs: dict[str, str]
    summary: dict[str, Any]
    warnings: list[str]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def tail_text(text: str, max_lines: int = 20) -> str:
    lines = text.strip().splitlines()
    return "\n".join(lines[-max_lines:])


def run_step(name: str, command: list[str]) -> FullRunStep:
    started_at = utc_now()
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    finished_at = utc_now()
    return FullRunStep(
        name=name,
        command=" ".join(command),
        returncode=completed.returncode,
        status="OK" if completed.returncode == 0 else "FAILED",
        started_at=started_at,
        finished_at=finished_at,
        stdout_tail=tail_text(completed.stdout),
        stderr_tail=tail_text(completed.stderr),
    )


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def safe_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default


def nested_get(payload: dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def manifest_metrics(manifest: dict[str, Any]) -> dict[str, Any]:
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        sources = []
    source_count = safe_int(manifest.get("source_count"), len(sources))
    total_items_found = safe_int(
        manifest.get("total_items_found"),
        sum(safe_int(source.get("items_found")) for source in sources if isinstance(source, dict)),
    )
    total_items_written = safe_int(
        manifest.get("total_items_written"),
        sum(safe_int(source.get("items_written")) for source in sources if isinstance(source, dict)),
    )
    return {
        "manifest_status": str(manifest.get("status") or "UNKNOWN"),
        "source_count": source_count,
        "total_items_found": total_items_found,
        "total_items_written": total_items_written,
    }


def collect_outputs() -> dict[str, str]:
    paths = get_project_paths(REPO_ROOT)
    logs_root = paths.logs_root
    return {
        "official_runtime_manifest": str(logs_root / "latest_official_runtime_manifest.json"),
        "source_runtime_health": str(logs_root / "latest_source_runtime_health.json"),
        "daily_source_summary": str(logs_root / "latest_daily_source_run_summary.json"),
        "quality_gate": str(logs_root / "latest_official_lane_quality_gate.json"),
        "official_daily_dashboard": str(logs_root / "latest_official_daily_dashboard.json"),
    }


def build_summary(outputs: dict[str, str]) -> dict[str, Any]:
    manifest = load_json(Path(outputs["official_runtime_manifest"]))
    daily_summary = load_json(Path(outputs["daily_source_summary"]))
    quality_gate = load_json(Path(outputs["quality_gate"]))

    metrics = manifest_metrics(manifest)
    quality_gate_status = (
        quality_gate.get("gate_status")
        or nested_get(quality_gate, "quality_gate", "level")
        or quality_gate.get("level")
        or quality_gate.get("status")
        or "UNKNOWN"
    )
    metrics.update(
        {
            "quality_gate_status": str(quality_gate_status),
            "daily_summary_status": str(daily_summary.get("status") or "UNKNOWN"),
        }
    )
    return metrics


def determine_status(steps: list[FullRunStep], summary: dict[str, Any], warnings: list[str]) -> str:
    failed_steps = [step for step in steps if step.returncode != 0]
    hard_failures = [step for step in failed_steps if step.name in HARD_STOP_STEPS]
    if hard_failures:
        return "FAILED"
    if failed_steps:
        return "DEGRADED"
    if str(summary.get("quality_gate_status", "UNKNOWN")) not in {"GREEN", "OK"}:
        return "DEGRADED"
    if warnings:
        return "DEGRADED"
    return "SUCCESS"


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: OfficialDailyFullRun) -> str:
    step_rows = "\n".join(
        f"| {markdown_escape(step.name)} | {markdown_escape(step.status)} | {step.returncode} |"
        for step in report.steps
    )
    output_lines = "\n".join(f"- `{key}`: `{value}`" for key, value in report.outputs.items())
    warning_lines = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    next_action = (
        "进入人工复核或查看失败步骤 stderr。"
        if report.status == "FAILED"
        else "查看 quality gate 和 dashboard，按 Phase 1 baseline 计划持续观察。"
    )

    return f"""# Official Daily Full Run

## Status

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**

## Steps

| Step | Status | Return Code |
|---|---|---:|
{step_rows}

## Key Metrics

- manifest_status: `{report.summary.get('manifest_status', 'UNKNOWN')}`
- source_count: `{report.summary.get('source_count', 0)}`
- total_items_found: `{report.summary.get('total_items_found', 0)}`
- total_items_written: `{report.summary.get('total_items_written', 0)}`
- daily_summary_status: `{report.summary.get('daily_summary_status', 'UNKNOWN')}`
- quality_gate_status: `{report.summary.get('quality_gate_status', 'UNKNOWN')}`

## Outputs

{output_lines}

## Warnings

{warning_lines}

## Next Action

{next_action}
"""


def write_outputs(report: OfficialDailyFullRun) -> dict[str, str]:
    paths = get_project_paths(REPO_ROOT)
    logs_root = paths.logs_root
    frontstage_root = paths.frontstage_root
    logs_root.mkdir(parents=True, exist_ok=True)
    frontstage_root.mkdir(parents=True, exist_ok=True)

    dated_json = logs_root / f"{report.run_date}__official-daily-full-run.json"
    dated_md = logs_root / f"{report.run_date}__official-daily-full-run.md"
    latest_json = logs_root / "latest_official_daily_full_run.json"
    latest_md = logs_root / "latest_official_daily_full_run.md"
    frontstage_dated = frontstage_root / f"{report.run_date}__official-daily-full-run-board.md"
    frontstage_latest = frontstage_root / "latest_official_daily_full_run_board.md"

    payload = json.dumps(asdict(report), ensure_ascii=False, indent=2)
    markdown = render_markdown(report)

    for path in (dated_json, latest_json):
        path.write_text(payload + "\n", encoding="utf-8")
    for path in (dated_md, latest_md, frontstage_dated, frontstage_latest):
        path.write_text(markdown, encoding="utf-8")

    return {
        "dated_json": str(dated_json),
        "dated_md": str(dated_md),
        "latest_json": str(latest_json),
        "latest_md": str(latest_md),
        "frontstage_dated_md": str(frontstage_dated),
        "frontstage_latest_md": str(frontstage_latest),
    }


def build_report(steps: list[FullRunStep], run_date: str, warnings: list[str]) -> OfficialDailyFullRun:
    outputs = collect_outputs()
    summary = build_summary(outputs)
    status = determine_status(steps, summary, warnings)
    return OfficialDailyFullRun(
        schema_version="v1",
        generated_at=utc_now(),
        run_date=run_date,
        status=status,
        steps=steps,
        outputs=outputs,
        summary=summary,
        warnings=warnings,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the official lane daily flow end to end.")
    parser.add_argument("--json", action="store_true", help="Print JSON full-run summary to stdout.")
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue through hard-stop steps even when an earlier step fails.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_date = today_token()
    warnings: list[str] = []
    steps: list[FullRunStep] = []

    planned_steps = [
        ("official_lane_health_check", [sys.executable, "scripts/run_official_lane_health_check.py"]),
        ("source_runtime_health", [sys.executable, "scripts/build_source_runtime_health.py"]),
        ("daily_source_summary", [sys.executable, "scripts/build_daily_source_run_summary.py"]),
        ("quality_gate", [sys.executable, "scripts/check_official_lane_quality_gate.py"]),
        ("official_daily_dashboard", [sys.executable, "scripts/build_official_daily_dashboard.py"]),
    ]

    for name, command in planned_steps:
        step = run_step(name, command)
        steps.append(step)
        if step.returncode != 0:
            warnings.append(f"{name} exited with return code {step.returncode}.")
            if name in HARD_STOP_STEPS and not args.continue_on_error:
                warnings.append(f"Stopped after {name}; use --continue-on-error to attempt downstream reports.")
                break

    report = build_report(steps, run_date, warnings)
    output_paths = write_outputs(report)

    if args.json:
        print(json.dumps({**asdict(report), "full_run_outputs": output_paths}, ensure_ascii=False, indent=2))
    else:
        print("Official Daily Full Run")
        print("=======================")
        print(f"status: {report.status}")
        print(f"run_date: {report.run_date}")
        print(f"manifest_status: {report.summary.get('manifest_status')}")
        print(f"source_count: {report.summary.get('source_count')}")
        print(f"total_items_found: {report.summary.get('total_items_found')}")
        print(f"quality_gate_status: {report.summary.get('quality_gate_status')}")
        print("\nSteps:")
        for step in report.steps:
            print(f"  {step.name}: {step.status} ({step.returncode})")
        print("\nReports:")
        for key, value in output_paths.items():
            print(f"  {key}: {value}")
        if report.warnings:
            print("\nWarnings:")
            for warning in report.warnings:
                print(f"  - {warning}")

    return 1 if report.status == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
