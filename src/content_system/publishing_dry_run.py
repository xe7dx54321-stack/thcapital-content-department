"""Publishing platform dry-run validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class PublishingDryRunReport:
    schema_version: str
    generated_at: str
    run_date: str
    status: str
    items: tuple[dict[str, Any], ...]
    summary: dict[str, int]
    warnings: tuple[str, ...]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    publishing_root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": publishing_root / f"{run_date}__publishing-dry-run.json",
        "dated_md": publishing_root / f"{run_date}__publishing-dry-run.md",
        "latest_json": publishing_root / "latest_publishing_dry_run.json",
        "latest_md": publishing_root / "latest_publishing_dry_run.md",
    }


def by_package(packages: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item.get("package_id")): item for item in packages if item.get("package_id")}


def has_risk_disclaimer(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in ("risk", "requires human", "人工", "风险", "核验"))


def validate_wechat(candidate: dict[str, Any], package: dict[str, Any]) -> tuple[str, list[str], list[str]]:
    issues: list[str] = []
    warnings: list[str] = []
    wechat = package.get("wechat") if isinstance(package.get("wechat"), dict) else {}
    body = str(wechat.get("body_markdown") or "")
    if not wechat.get("title"):
        issues.append("Wechat title is missing.")
    if not body:
        issues.append("Wechat body_markdown is missing.")
    elif len(body) < 200:
        warnings.append("Wechat body is short for a public account draft.")
    if not candidate.get("source_ids"):
        issues.append("source_ids are missing.")
    if not candidate.get("evidence_ids"):
        issues.append("evidence_ids are missing.")
    if not has_risk_disclaimer(body):
        issues.append("Risk disclaimer is missing from Wechat body.")
    if not candidate.get("human_confirmation_required"):
        issues.append("Human confirmation is not required on candidate.")
    status = "READY" if not issues else "NOT_READY"
    if str(candidate.get("publish_status")) == "HOLD":
        status = "HOLD"
    return status, issues, warnings


def validate_xiaohongshu(candidate: dict[str, Any], package: dict[str, Any]) -> tuple[str, list[str], list[str]]:
    issues: list[str] = []
    warnings: list[str] = []
    xhs = package.get("xiaohongshu") if isinstance(package.get("xiaohongshu"), dict) else {}
    body = str(xhs.get("body_markdown") or "")
    tags = xhs.get("tags") if isinstance(xhs.get("tags"), list) else []
    image_brief = xhs.get("image_brief") if isinstance(xhs.get("image_brief"), list) else []
    if not xhs.get("title"):
        issues.append("Xiaohongshu title is missing.")
    if not body:
        issues.append("Xiaohongshu body_markdown is missing.")
    elif len(body) > 2000:
        warnings.append("Xiaohongshu body is long and may need trimming.")
    if not tags:
        issues.append("Xiaohongshu tags are missing.")
    if not image_brief:
        warnings.append("Xiaohongshu image_brief is missing.")
    if not candidate.get("human_confirmation_required"):
        issues.append("Human confirmation is not required on candidate.")
    status = "READY" if not issues else "NOT_READY"
    if str(candidate.get("publish_status")) == "HOLD":
        status = "HOLD"
    return status, issues, warnings


def build_publishing_dry_run_report(paths: ProjectPaths) -> PublishingDryRunReport:
    publishing_root = paths.market_content_root / "07_publishing"
    draft_root = paths.market_content_root / "05_draft_packs"
    candidates_payload = read_json(publishing_root / "latest_publishing_candidate_queue.json")
    packages_payload = read_json(draft_root / "latest_platform_packages.json")
    candidates = list_payload(candidates_payload, "candidates")
    packages = by_package(list_payload(packages_payload, "packages"))
    run_date = str(candidates_payload.get("run_date") or packages_payload.get("run_date") or today_token()).replace("-", "")[:8]
    warnings: list[str] = []
    if not candidates:
        warnings.append("No publishing candidates found.")
    items: list[dict[str, Any]] = []
    for candidate in candidates:
        package = packages.get(str(candidate.get("package_id"))) or {}
        if not package:
            warnings.append(f"Missing platform package for {candidate.get('publishing_candidate_id')}.")
        for platform in candidate.get("platforms") or ["wechat", "xiaohongshu"]:
            if platform == "wechat":
                dry_status, issues, item_warnings = validate_wechat(candidate, package)
            elif platform == "xiaohongshu":
                dry_status, issues, item_warnings = validate_xiaohongshu(candidate, package)
            else:
                dry_status, issues, item_warnings = "NOT_READY", [f"Unsupported platform: {platform}"], []
            items.append(
                {
                    "publishing_candidate_id": candidate.get("publishing_candidate_id", ""),
                    "package_id": candidate.get("package_id", ""),
                    "platform": platform,
                    "dry_run_status": dry_status,
                    "issues": issues,
                    "warnings": item_warnings,
                    "would_publish": False,
                    "human_confirmation_required": True,
                }
            )
    summary = {
        "ready_count": sum(1 for item in items if item["dry_run_status"] == "READY"),
        "not_ready_count": sum(1 for item in items if item["dry_run_status"] == "NOT_READY"),
        "hold_count": sum(1 for item in items if item["dry_run_status"] == "HOLD"),
    }
    status = "SUCCESS" if items and summary["not_ready_count"] == 0 and summary["hold_count"] == 0 else "DEGRADED" if items else "DEGRADED"
    return PublishingDryRunReport(SCHEMA_VERSION, utc_now(), run_date, status, tuple(items), summary, tuple(warnings))


def render_markdown(report: PublishingDryRunReport) -> str:
    rows = "\n".join(
        f"| {item.get('publishing_candidate_id')} | {item.get('platform')} | {item.get('dry_run_status')} | {len(item.get('issues') or [])} | false |"
        for item in report.items
    ) or "| - | - | - | 0 | false |"
    warnings = "\n".join(f"- {item}" for item in report.warnings) if report.warnings else "- None"
    details = "\n".join(
        f"### {item.get('publishing_candidate_id')} / {item.get('platform')}\n\n"
        f"- Status: `{item.get('dry_run_status')}`\n"
        f"- Issues: {', '.join(item.get('issues') or []) or 'None'}\n"
        f"- Warnings: {', '.join(item.get('warnings') or []) or 'None'}\n"
        f"- Would publish: `false`\n"
        for item in report.items
    ) or "No candidates."
    return f"""# Publishing API Dry-run

## Summary

- Generated at: `{report.generated_at}`
- Run date: `{report.run_date}`
- Status: **{report.status}**
- Ready: `{report.summary.get('ready_count')}`
- Not ready: `{report.summary.get('not_ready_count')}`
- Hold: `{report.summary.get('hold_count')}`
- Hard rule: `would_publish` is always `false`

## Items

| Candidate | Platform | Dry-run Status | Issues | Would Publish |
|---|---|---|---:|---|
{rows}

## Details

{details}

## Warnings

{warnings}
"""


def write_publishing_dry_run_report(report: PublishingDryRunReport, paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    outputs = output_paths(paths, report.run_date)
    payload = asdict(report)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return write_json_and_markdown(payload, render_markdown(report), outputs)


def report_to_dict(report: PublishingDryRunReport) -> dict[str, Any]:
    return asdict(report)
