"""Build human final publish checklists for final article candidates."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class FinalPublishChecklistResult:
    run_date: str
    checklist_count: int
    ready: int
    needs_attention: int
    blocked: int
    output_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "07_publishing"
    return {
        "dated_json": root / f"{run_date}__final-publish-checklist.json",
        "dated_md": root / f"{run_date}__final-publish-checklist.md",
        "latest_json": root / "latest_final_publish_checklist.json",
        "latest_md": root / "latest_final_publish_checklist.md",
    }


def checklist_id(run_date: str, candidate_id: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{candidate_id}".encode("utf-8")).hexdigest()[:12]
    return f"chk_{run_date}_{digest}"


def check(check_id: str, label: str, status: str, note: str = "") -> dict[str, str]:
    return {"check_id": check_id, "label": label, "status": status, "note": note}


def first_paragraph(body: str) -> str:
    for raw in body.splitlines():
        text = raw.strip()
        if text and not text.startswith("#") and not text.startswith("- "):
            return text
    return ""


def build_checks(candidate: dict[str, Any], source_health: dict[str, Any]) -> list[dict[str, str]]:
    title = str(candidate.get("wechat_title") or candidate.get("title") or "")
    body = str(candidate.get("wechat_body_markdown") or candidate.get("body_markdown") or "")
    opening = first_paragraph(body)
    has_evidence = bool(re.search(r"证据|来源|https?://|`web__", body, re.I))
    has_first_party = bool(re.search(r"官方|openai|anthropic|google|nvidia|source|web__", body, re.I))
    has_overclaim = bool(re.search(r"必然|一定|保证|颠覆一切|唯一答案", body))
    has_risk_note = bool(re.search(r"风险|人工确认|发布前|核验", body))
    readable_length = len(body) >= 500 and len(body) <= 6000
    checks = [
        check("title_check", "标题是否明确、有吸引力且不标题党", "PASS" if 10 <= len(title) <= 80 else "WARN", "标题为空或过长需要人工调整。" if not (10 <= len(title) <= 80) else ""),
        check("opening_check", "开头是否能抓住读者", "PASS" if len(opening) >= 30 else "WARN", "开头偏短，需要人工确认。" if len(opening) < 30 else ""),
        check("logic_check", "正文是否逻辑顺畅", "PASS" if body.count("## ") >= 2 else "WARN", "小标题或结构偏弱。" if body.count("## ") < 2 else ""),
        check("evidence_check", "证据是否足够", "PASS" if has_evidence else "FAIL", "" if has_evidence else "正文没有清楚证据或来源说明。"),
        check("first_party_source_check", "是否有一手来源或清楚来源说明", "PASS" if has_first_party else "WARN", "" if has_first_party else "一手来源信号不明显。"),
        check("fact_risk_check", "是否有明显事实风险", "WARN" if source_health.get("status") == "FAILED" else "PASS", "source runtime health 需要人工复核。" if source_health.get("status") == "FAILED" else ""),
        check("overclaim_check", "是否有过度承诺或夸张表达", "WARN" if has_overclaim else "PASS", "存在可能过度承诺表达。" if has_overclaim else ""),
        check("risk_note_check", "是否有风险提示", "PASS" if has_risk_note else "WARN", "" if has_risk_note else "建议补充发布前风险提示。"),
        check("wechat_readability_check", "是否适合公众号阅读", "PASS" if readable_length else "WARN", "" if readable_length else "篇幅可能过短或过长。"),
        check("manual_copy_check", "是否需要人工复制到公众号后台", "PASS", "本系统不接公众号 API，必须人工复制。"),
        check("no_auto_publish_check", "是否确认不自动发布", "PASS", "would_publish=false；最终发布必须人工确认。"),
    ]
    return checks


def item_status(checks: list[dict[str, str]]) -> str:
    if any(item.get("status") == "FAIL" for item in checks):
        return "BLOCKED"
    if any(item.get("status") == "WARN" for item in checks):
        return "NEEDS_ATTENTION"
    return "READY"


def manual_steps() -> list[str]:
    return [
        "打开 latest_wechat_workbench.html。",
        "阅读 final candidate。",
        "检查 checklist。",
        "人工复制标题。",
        "人工复制正文。",
        "人工进入公众号后台。",
        "人工粘贴、排版、预览。",
        "人工最终决定是否发布。",
    ]


def build_final_publish_checklist(paths: ProjectPaths, repo_root: Path) -> tuple[FinalPublishChecklistResult, dict[str, Any]]:
    candidates_payload = read_json(paths.market_content_root / "07_publishing" / "latest_final_article_candidates.json")
    source_health = read_json(paths.logs_root / "latest_source_runtime_health.json")
    run_date = str(candidates_payload.get("run_date") or today_token()).replace("-", "")[:8]
    items: list[dict[str, Any]] = []
    for candidate in list_payload(candidates_payload, "candidates"):
        checks = build_checks(candidate, source_health)
        items.append(
            {
                "checklist_id": checklist_id(run_date, str(candidate.get("final_candidate_id") or "")),
                "final_candidate_id": candidate.get("final_candidate_id") or "",
                "version_id": candidate.get("version_id") or "",
                "title": candidate.get("wechat_title") or candidate.get("title") or "",
                "status": item_status(checks),
                "checks": checks,
                "manual_steps": manual_steps(),
                "copy_to_wechat_steps": manual_steps()[3:],
                "final_human_confirmation_required": True,
                "would_publish": False,
            }
        )
    summary = {
        "checklist_count": len(items),
        "ready": sum(1 for item in items if item.get("status") == "READY"),
        "needs_attention": sum(1 for item in items if item.get("status") == "NEEDS_ATTENTION"),
        "blocked": sum(1 for item in items if item.get("status") == "BLOCKED"),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "items": items, "summary": summary}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        FinalPublishChecklistResult(run_date, summary["checklist_count"], summary["ready"], summary["needs_attention"], summary["blocked"], repo_relative(outputs["latest_json"], repo_root)),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('checklist_id')}` | `{item.get('final_candidate_id')}` | `{item.get('status')}` | `{item.get('would_publish')}` | {item.get('title') or ''} |"
        for item in list_payload(payload, "items")
    ) or "| - | - | SUCCESS_EMPTY | false | No final candidates |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Final Publish Checklist

## Summary

- Run date: `{payload.get('run_date')}`
- Checklists: `{summary.get('checklist_count', 0)}`
- Ready: `{summary.get('ready', 0)}`
- Needs attention: `{summary.get('needs_attention', 0)}`
- Blocked: `{summary.get('blocked', 0)}`
- Policy: no API call, no draft-box write, no auto-publish.

| Checklist | Final Candidate | Status | Would Publish | Title |
|---|---|---|---|---|
{rows}
"""
