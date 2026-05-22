#!/usr/bin/env python3
"""Official lane daily quality gate.

P0-014 is intentionally report-only by default:
- It reads the latest daily source run summary and official runtime manifest.
- It evaluates a few lightweight thresholds.
- It writes JSON/Markdown/frontstage reports.
- It exits 0 unless --fail-on-red is explicitly passed.

This is not a retry system, scheduler, database, or fetcher rewrite.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT_CANDIDATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT_CANDIDATE / "src"))

from content_system.paths import get_project_paths  # noqa: E402


@dataclass(frozen=True)
class GateRuleResult:
    rule_id: str
    status: str
    severity: str
    message: str
    observed: Any
    threshold: Any


@dataclass(frozen=True)
class GateReport:
    schema_version: str
    generated_at: str
    run_date: str
    gate_status: str
    summary_path: str
    manifest_path: str
    rules: list[GateRuleResult]
    metrics: dict[str, Any]
    outputs: dict[str, str]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def extract_status_distribution(summary: dict[str, Any]) -> dict[str, int]:
    raw = summary.get("status_distribution")
    if isinstance(raw, dict):
        return {str(k): safe_int(v) for k, v in raw.items()}

    # Some report variants may nest health data.
    health = summary.get("source_runtime_health")
    if isinstance(health, dict):
        nested = health.get("status_distribution")
        if isinstance(nested, dict):
            return {str(k): safe_int(v) for k, v in nested.items()}

    return {}


def extract_metrics(summary: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    manifest_sources = manifest.get("sources")
    if not isinstance(manifest_sources, list):
        manifest_sources = []

    status_distribution = extract_status_distribution(summary)
    manifest_status = str(manifest.get("status") or summary.get("status") or "UNKNOWN")

    metrics = {
        "summary_status": str(summary.get("status") or "UNKNOWN"),
        "manifest_status": manifest_status,
        "source_count": safe_int(summary.get("source_count"), len(manifest_sources)),
        "total_items_found": safe_int(summary.get("total_items_found"), safe_int(manifest.get("items_found"))),
        "total_items_written": safe_int(summary.get("total_items_written"), safe_int(manifest.get("items_written"))),
        "enabled_sources": safe_int(summary.get("enabled_sources")),
        "observed_sources": safe_int(summary.get("observed_sources")),
        "missing_expected": safe_int(summary.get("missing_expected")),
        "error_hint_sources": safe_int(summary.get("error_hint_sources")),
        "status_distribution": status_distribution,
    }

    if not metrics["total_items_written"]:
        source_written = 0
        for source in manifest_sources:
            if isinstance(source, dict):
                source_written += safe_int(source.get("items_written"))
        metrics["total_items_written"] = source_written

    return metrics


def evaluate_gate(
    metrics: dict[str, Any],
    *,
    min_sources: int,
    min_items: int,
    max_missing_expected: int,
    max_error_hint_sources: int,
) -> list[GateRuleResult]:
    rules: list[GateRuleResult] = []

    def add(rule_id: str, ok: bool, severity: str, message: str, observed: Any, threshold: Any) -> None:
        rules.append(
            GateRuleResult(
                rule_id=rule_id,
                status="PASS" if ok else "FAIL",
                severity=severity,
                message=message,
                observed=observed,
                threshold=threshold,
            )
        )

    manifest_status = str(metrics.get("manifest_status", "UNKNOWN"))
    add(
        "official_manifest_success",
        manifest_status == "SUCCESS",
        "ERROR",
        "Official runtime manifest should report SUCCESS.",
        manifest_status,
        "SUCCESS",
    )

    source_count = safe_int(metrics.get("source_count"))
    add(
        "minimum_source_count",
        source_count >= min_sources,
        "ERROR",
        "Official lane should observe enough sources.",
        source_count,
        f">= {min_sources}",
    )

    total_items_found = safe_int(metrics.get("total_items_found"))
    add(
        "minimum_items_found",
        total_items_found >= min_items,
        "ERROR",
        "Official lane should find enough items for a healthy daily run.",
        total_items_found,
        f">= {min_items}",
    )

    missing_expected = safe_int(metrics.get("missing_expected"))
    add(
        "missing_expected_limit",
        missing_expected <= max_missing_expected,
        "WARN",
        "Missing expected sources should stay within the report-only warning threshold.",
        missing_expected,
        f"<= {max_missing_expected}",
    )

    error_hint_sources = safe_int(metrics.get("error_hint_sources"))
    add(
        "error_hint_limit",
        error_hint_sources <= max_error_hint_sources,
        "WARN",
        "Sources with error hints should stay within the report-only warning threshold.",
        error_hint_sources,
        f"<= {max_error_hint_sources}",
    )

    return rules


def gate_status(rules: list[GateRuleResult]) -> str:
    failed_errors = [rule for rule in rules if rule.status == "FAIL" and rule.severity == "ERROR"]
    failed_warns = [rule for rule in rules if rule.status == "FAIL" and rule.severity == "WARN"]
    if failed_errors:
        return "RED"
    if failed_warns:
        return "YELLOW"
    return "GREEN"


def markdown_table_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def render_markdown(report: GateReport) -> str:
    lines = [
        "# Official Lane Quality Gate",
        "",
        f"- Generated at: `{report.generated_at}`",
        f"- Run date: `{report.run_date}`",
        f"- Gate status: **{report.gate_status}**",
        f"- Summary: `{report.summary_path}`",
        f"- Manifest: `{report.manifest_path}`",
        "",
        "## Metrics",
        "",
    ]

    for key, value in report.metrics.items():
        if isinstance(value, dict):
            rendered = ", ".join(f"{k}={v}" for k, v in sorted(value.items()))
        else:
            rendered = str(value)
        lines.append(f"- `{key}`: {rendered}")

    lines.extend(
        [
            "",
            "## Rules",
            "",
            "| Rule | Status | Severity | Observed | Threshold | Message |",
            "|---|---|---|---|---|---|",
        ]
    )

    for rule in report.rules:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_table_escape(rule.rule_id),
                    markdown_table_escape(rule.status),
                    markdown_table_escape(rule.severity),
                    markdown_table_escape(rule.observed),
                    markdown_table_escape(rule.threshold),
                    markdown_table_escape(rule.message),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This gate is report-only by default.",
            "- It does not retry failed sources, rewrite fetchers, or block the pipeline unless `--fail-on-red` is passed.",
            "- Thresholds are intentionally lightweight and should be tuned after several real daily runs.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(report: GateReport, logs_root: Path, frontstage_root: Path) -> None:
    logs_root.mkdir(parents=True, exist_ok=True)
    frontstage_root.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(
        {
            "schema_version": report.schema_version,
            "generated_at": report.generated_at,
            "run_date": report.run_date,
            "gate_status": report.gate_status,
            "summary_path": report.summary_path,
            "manifest_path": report.manifest_path,
            "rules": [asdict(rule) for rule in report.rules],
            "metrics": report.metrics,
            "outputs": report.outputs,
        },
        ensure_ascii=False,
        indent=2,
    )
    md_text = render_markdown(report)

    for key in ("dated_json", "latest_json"):
        Path(report.outputs[key]).write_text(json_text, encoding="utf-8")
    for key in ("dated_md", "latest_md", "frontstage_dated_md", "frontstage_latest_md"):
        Path(report.outputs[key]).write_text(md_text, encoding="utf-8")


def build_quality_gate(
    *,
    summary_path: Path,
    manifest_path: Path,
    run_date: str,
    min_sources: int,
    min_items: int,
    max_missing_expected: int,
    max_error_hint_sources: int,
) -> GateReport:
    paths = get_project_paths(REPO_ROOT_CANDIDATE)
    summary = load_json(summary_path)
    manifest = load_json(manifest_path)
    metrics = extract_metrics(summary, manifest)

    rules = evaluate_gate(
        metrics,
        min_sources=min_sources,
        min_items=min_items,
        max_missing_expected=max_missing_expected,
        max_error_hint_sources=max_error_hint_sources,
    )
    status = gate_status(rules)
    generated_at = datetime.now(timezone.utc).isoformat()

    logs_root = paths.logs_root
    frontstage_root = paths.frontstage_root
    outputs = {
        "dated_json": str(logs_root / f"{run_date}__official-lane-quality-gate.json"),
        "dated_md": str(logs_root / f"{run_date}__official-lane-quality-gate.md"),
        "latest_json": str(logs_root / "latest_official_lane_quality_gate.json"),
        "latest_md": str(logs_root / "latest_official_lane_quality_gate.md"),
        "frontstage_dated_md": str(frontstage_root / f"{run_date}__official-lane-quality-gate-board.md"),
        "frontstage_latest_md": str(frontstage_root / "latest_official_lane_quality_gate_board.md"),
    }

    return GateReport(
        schema_version="v1",
        generated_at=generated_at,
        run_date=run_date,
        gate_status=status,
        summary_path=str(summary_path),
        manifest_path=str(manifest_path),
        rules=rules,
        metrics=metrics,
        outputs=outputs,
    )


def default_run_date() -> str:
    return datetime.now().strftime("%Y%m%d")


def parse_args() -> argparse.Namespace:
    paths = get_project_paths(REPO_ROOT_CANDIDATE)
    run_date = default_run_date()
    return argparse.ArgumentParser(description="Build official lane daily quality gate reports.").parse_args()


def build_parser() -> argparse.ArgumentParser:
    paths = get_project_paths(REPO_ROOT_CANDIDATE)
    run_date = default_run_date()
    parser = argparse.ArgumentParser(description="Build official lane daily quality gate reports.")
    parser.add_argument("--run-date", default=run_date, help="Run date in YYYYMMDD format. Defaults to today.")
    parser.add_argument(
        "--summary",
        type=Path,
        default=paths.logs_root / "latest_daily_source_run_summary.json",
        help="Daily source run summary JSON path.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=paths.logs_root / "latest_official_runtime_manifest.json",
        help="Official runtime manifest JSON path.",
    )
    parser.add_argument("--min-sources", type=int, default=5)
    parser.add_argument("--min-items", type=int, default=10)
    parser.add_argument("--max-missing-expected", type=int, default=12)
    parser.add_argument("--max-error-hint-sources", type=int, default=2)
    parser.add_argument("--fail-on-red", action="store_true", help="Return exit code 1 if gate status is RED.")
    parser.add_argument("--json", action="store_true", help="Print compact JSON summary.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    paths = get_project_paths(REPO_ROOT_CANDIDATE)

    report = build_quality_gate(
        summary_path=args.summary,
        manifest_path=args.manifest,
        run_date=args.run_date,
        min_sources=args.min_sources,
        min_items=args.min_items,
        max_missing_expected=args.max_missing_expected,
        max_error_hint_sources=args.max_error_hint_sources,
    )
    write_report(report, paths.logs_root, paths.frontstage_root)

    if args.json:
        print(
            json.dumps(
                {
                    "gate_status": report.gate_status,
                    "run_date": report.run_date,
                    "metrics": report.metrics,
                    "outputs": report.outputs,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print("Official Lane Quality Gate")
        print("==========================")
        print(f"gate_status: {report.gate_status}")
        print(f"run_date: {report.run_date}")
        print(f"manifest_status: {report.metrics.get('manifest_status')}")
        print(f"source_count: {report.metrics.get('source_count')}")
        print(f"total_items_found: {report.metrics.get('total_items_found')}")
        print(f"missing_expected: {report.metrics.get('missing_expected')}")
        print(f"error_hint_sources: {report.metrics.get('error_hint_sources')}")
        print("")
        print("Reports:")
        for key, value in report.outputs.items():
            print(f"  {key}: {value}")

    if args.fail_on_red and report.gate_status == "RED":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
