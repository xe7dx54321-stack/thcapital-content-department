"""Execute approved rewrite actions into new article versions."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
REWRITE_ACTION_TYPES = {"rewrite_instruction", "rewrite_angle", "title_rewrite_request", "opening_rewrite_request"}


@dataclass(frozen=True)
class RewriteActionExecutorResult:
    run_date: str
    status: str
    version_count: int
    output_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions" / "versions"
    return {
        "dated_json": root / f"{run_date}__rewrite-versions.json",
        "dated_md": root / f"{run_date}__rewrite-versions.md",
        "latest_json": root / "latest_rewrite_versions.json",
        "latest_md": root / "latest_rewrite_versions.md",
    }


def approved_rewrite_actions(paths: ProjectPaths) -> list[dict[str, Any]]:
    payload = read_json(paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json")
    return [
        action
        for action in list_payload(payload, "actions")
        if action.get("approval_status") == "APPROVED" and action.get("action_type") in REWRITE_ACTION_TYPES
    ]


def article_by_id(data: dict[str, Any], article_id: str) -> dict[str, Any]:
    articles = list_payload(data, "articles")
    for article in articles:
        if article.get("article_id") == article_id or article.get("package_id") == article_id or article.get("draft_id") == article_id:
            return article
    selected_id = str(data.get("selected_article_id") or "")
    for article in articles:
        if article.get("article_id") == selected_id:
            return article
    return articles[0] if articles else {}


def version_id(run_date: str, action: dict[str, Any], body: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{action.get('action_id')}|{body}".encode("utf-8")).hexdigest()[:12]
    return f"ver_{run_date}_{digest}"


def first_heading_and_body(body: str) -> tuple[str, str]:
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0][2:].strip(), "\n".join(lines[1:]).lstrip()
    return "", body


def insert_after_title(body: str, insertion: str) -> str:
    title, rest = first_heading_and_body(body)
    if title:
        return f"# {title}\n\n{insertion.strip()}\n\n{rest.strip()}\n"
    return f"{insertion.strip()}\n\n{body.strip()}\n"


def title_options(base_title: str, description: str) -> list[str]:
    clean = base_title.strip() or "当前选题"
    options = [
        f"{clean}：真正值得关注的变化是什么",
        f"为什么现在要重新看 {clean}",
        f"{clean} 背后的机会、风险与下一步",
    ]
    if "投资人" in description:
        options.insert(0, f"投资人视角：{clean} 的机会与风险")
    return options[:5]


def rewrite_body(action: dict[str, Any], article: dict[str, Any]) -> dict[str, Any]:
    action_type = str(action.get("action_type") or "")
    description = str(action.get("description") or "")
    current_title = str(article.get("wechat_title") or article.get("title") or "未命名文章")
    body = str(article.get("wechat_body_markdown") or "")
    issues: list[str] = []
    options = title_options(current_title, description)
    new_title = current_title
    new_opening = ""
    changed_sections: list[str] = []

    if action_type == "title_rewrite_request":
        new_title = options[0]
        new_body = body
        changed_sections.append("title")
    elif action_type == "opening_rewrite_request":
        new_opening = f"这件事不只是一个产品或公司动态，更像是 AI Agent 进入真实工作流的一次信号。{description}"
        new_body = insert_after_title(body, f"## 开头重写\n\n{new_opening}")
        changed_sections.append("opening")
    else:
        if "投资人" in description:
            new_title = f"投资人视角：{current_title}"
            angle_section = (
                "## 主编修订方向\n\n"
                "从投资人视角看，这篇稿件需要把事实动态进一步翻译为产业变量："
                "谁的能力边界在扩大，哪类工作流会先被重构，哪些公司或团队可能因此获得新入口。\n\n"
                f"本次修订依据：{description}"
            )
            changed_sections.extend(["angle", "logic"])
        else:
            angle_section = f"## 主编修订方向\n\n本版本根据人工批准的工作台 action 进行规则型改写：{description}"
            changed_sections.append("body")
        new_opening = angle_section
        new_body = insert_after_title(body, angle_section)

    if new_body.strip() == body.strip() and new_title == current_title:
        issues.append("Rule-based rewrite did not materially change the body.")
    return {
        "new_title": new_title,
        "title_options": options,
        "new_opening": new_opening,
        "new_body_markdown": new_body,
        "changed_sections": changed_sections,
        "issues": issues,
    }


def execute_rewrite_actions(paths: ProjectPaths, repo_root: Path) -> tuple[RewriteActionExecutorResult, dict[str, Any]]:
    data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    approved_payload = read_json(paths.market_content_root / "09_workbench_actions" / "latest_approved_actions.json")
    run_date = str(data.get("run_date") or approved_payload.get("run_date") or today_token()).replace("-", "")[:8]
    versions: list[dict[str, Any]] = []
    for action in approved_rewrite_actions(paths):
        article = article_by_id(data, str(action.get("target_artifact_id") or ""))
        if not article:
            versions.append(
                {
                    "version_id": version_id(run_date, action, "missing_article"),
                    "source_action_id": action.get("action_id"),
                    "source_article_id": action.get("target_artifact_id") or "",
                    "version_type": "rewrite",
                    "change_summary": "Failed to locate source article.",
                    "new_title": "",
                    "new_opening": "",
                    "new_body_markdown": "",
                    "changed_sections": [],
                    "generation_mode": "rule_based",
                    "do_not_overwrite_original": True,
                    "status": "FAILED",
                    "issues": ["source_article_not_found"],
                }
            )
            continue
        rewrite = rewrite_body(action, article)
        body = str(rewrite.get("new_body_markdown") or "")
        versions.append(
            {
                "version_id": version_id(run_date, action, body),
                "source_action_id": action.get("action_id"),
                "source_article_id": article.get("article_id") or "",
                "version_type": "rewrite",
                "change_summary": action.get("description") or "",
                "new_title": rewrite.get("new_title") or "",
                "title_options": rewrite.get("title_options") or [],
                "new_opening": rewrite.get("new_opening") or "",
                "new_body_markdown": body,
                "changed_sections": rewrite.get("changed_sections") or [],
                "generation_mode": "rule_based",
                "do_not_overwrite_original": True,
                "status": "GENERATED" if not rewrite.get("issues") else "FAILED",
                "issues": rewrite.get("issues") or [],
            }
        )
    status = "SUCCESS" if versions else "SUCCESS_EMPTY"
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "status": status, "versions": versions}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return RewriteActionExecutorResult(run_date, status, len(versions), repo_relative(outputs["latest_json"], repo_root)), payload


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('version_id')}` | `{item.get('source_action_id')}` | `{item.get('status')}` | {item.get('change_summary')} |"
        for item in list_payload(payload, "versions")
    ) or "| - | - | SUCCESS_EMPTY | No approved rewrite actions |"
    return f"""# Rewrite Versions

## Summary

- Run date: `{payload.get('run_date')}`
- Status: `{payload.get('status')}`
- Versions: `{len(list_payload(payload, 'versions'))}`
- Policy: `do_not_overwrite_original=true`

| Version | Source Action | Status | Change Summary |
|---|---|---|---|
{rows}
"""
