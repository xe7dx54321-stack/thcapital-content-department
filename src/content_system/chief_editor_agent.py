"""Rule-based Chief Editor Agent for the local workbench."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"
DEFAULT_MESSAGE = "请根据当前稿件生成下一步主编 action plan"


@dataclass(frozen=True)
class ChiefEditorAgentResult:
    run_date: str
    message_id: str
    intent: str
    output_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions"
    return {
        "dated_json": root / f"{run_date}__chief-editor-response.json",
        "dated_md": root / f"{run_date}__chief-editor-response.md",
        "latest_json": root / "latest_chief_editor_response.json",
        "latest_md": root / "latest_chief_editor_response.md",
    }


def message_id(run_date: str, message: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{message}|{utc_now()}".encode("utf-8")).hexdigest()[:12]
    return f"ce_{run_date}_{digest}"


def selected_article(context: dict[str, Any]) -> dict[str, Any]:
    article = context.get("selected_article")
    return article if isinstance(article, dict) else {}


def extract_source_targets(message: str) -> list[str]:
    targets = []
    for name in ("OpenAI", "Anthropic", "Google", "NVIDIA", "Meta", "Microsoft", "Claude", "Gemini"):
        if name.lower() in message.lower():
            targets.append(name)
    if "浏览器" in message or "browser" in message.lower():
        targets.append("AI Agent 浏览器")
    return targets


def detect_intent(message: str) -> str:
    lowered = message.lower()
    if any(token in message for token in ("搁置", "别发", "先不发", "今天别发", "hold")):
        return "hold"
    if any(token in message for token in ("进入发布候选", "这篇可以", "批准", "可以发", "approve")):
        return "approve"
    if any(token in message for token in ("换选题", "选题不好", "别写这个", "换成")) and "视角" not in message:
        return "change_topic"
    if any(token in message for token in ("证据", "补充", "找更多", "一手来源", "最新进展", "更多信息")):
        return "strengthen_evidence"
    if any(token in message for token in ("标题", "题目")):
        return "rewrite_title"
    if any(token in message for token in ("开头", "第一段")):
        return "rewrite_opening"
    if any(token in message for token in ("投资人视角", "产业链视角", "太泛", "角度", "深度分析")):
        return "rewrite_angle"
    if "?" in message or "？" in message:
        return "ask_clarification"
    return "ask_clarification"


def action_for_intent(intent: str, message: str, article: dict[str, Any]) -> list[dict[str, Any]]:
    target = str(article.get("article_id") or article.get("package_id") or "")
    actions: list[dict[str, Any]] = []

    def add(action_type: str, description: str, priority: str = "MEDIUM") -> None:
        actions.append({"action_type": action_type, "description": description, "target": target, "priority": priority, "status": "PENDING"})

    if intent == "change_topic":
        add("topic_replacement_request", f"Replace current topic according to user request: {message}", "HIGH")
    elif intent == "rewrite_angle":
        add("rewrite_instruction", f"Revise article angle according to user request: {message}", "HIGH")
    elif intent == "strengthen_evidence":
        add("evidence_expansion_request", f"Find stronger first-party evidence and update the evidence plan: {message}", "HIGH")
    elif intent == "rewrite_title":
        add("title_rewrite_request", f"Rewrite the title with a stronger but evidence-bounded hook: {message}", "HIGH")
        if "开头" in message or "第一段" in message:
            add("opening_rewrite_request", "Rewrite the opening paragraph with a sharper setup.", "HIGH")
    elif intent == "rewrite_opening":
        add("opening_rewrite_request", f"Rewrite the opening paragraph: {message}", "HIGH")
    elif intent == "approve":
        add("publishing_status_update", "Move this article toward publishing candidate review, pending human confirmation.", "HIGH")
    elif intent == "hold":
        add("publishing_status_update", "Hold this article and remove it from near-term publishing consideration.", "HIGH")
    else:
        add("clarification_request", "Ask the human editor to clarify the desired direction before execution.", "LOW")
    return actions


def agent_to_call(intent: str) -> str:
    return {
        "change_topic": "topic_selector",
        "rewrite_angle": "rewrite_agent",
        "strengthen_evidence": "evidence_expansion",
        "rewrite_title": "rewrite_agent",
        "rewrite_opening": "rewrite_agent",
        "approve": "chief_editor_only",
        "hold": "chief_editor_only",
    }.get(intent, "none")


def human_reply(intent: str, article: dict[str, Any], actions: list[dict[str, Any]]) -> str:
    title = article.get("wechat_title") or article.get("title") or "当前稿件"
    if intent == "approve":
        return f"我理解为：你希望将《{title}》推进到发布候选，但仍保留人工确认。我已生成待确认动作。"
    if intent == "hold":
        return f"我理解为：你希望先搁置《{title}》。我已生成 hold 动作，不会自动改稿或发布。"
    if intent == "ask_clarification":
        return "我需要进一步确认你的编辑目标。已生成一个澄清动作，等待人工补充。"
    return f"我理解为：你希望对《{title}》执行 {intent}。我已拆成 {len(actions)} 个待处理动作，当前只进入 pending queue。"


def run_chief_editor_agent(paths: ProjectPaths, repo_root: Path, message: str | None = None) -> tuple[ChiefEditorAgentResult, dict[str, Any]]:
    context = read_json(paths.logs_root / "latest_workbench_context.json")
    run_date = str(context.get("run_date") or today_token()).replace("-", "")[:8]
    user_message = message or DEFAULT_MESSAGE
    article = selected_article(context)
    intent = detect_intent(user_message)
    actions = action_for_intent(intent, user_message, article)
    msg_id = message_id(run_date, user_message)
    targets = extract_source_targets(user_message)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "message_id": msg_id,
        "user_message": user_message,
        "intent": intent,
        "target_artifact_id": article.get("article_id") or article.get("package_id") or "",
        "user_request_summary": user_message[:240],
        "system_understanding": human_reply(intent, article, actions),
        "required_actions": actions,
        "agent_to_call": agent_to_call(intent),
        "needs_additional_research": intent in {"change_topic", "strengthen_evidence"},
        "source_targets": targets,
        "execution_policy": "PLAN_ONLY",
        "status": "NEEDS_CONFIRMATION" if intent == "ask_clarification" else "READY_TO_EXECUTE",
        "human_readable_reply": human_reply(intent, article, actions),
        "provider_id": "anthropic",
        "model": "claude-sonnet-4.6",
        "mode": "dry_run",
        "fallback_used": False,
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return ChiefEditorAgentResult(run_date, msg_id, intent, repo_relative(outputs["latest_json"], repo_root)), payload


def render_markdown(payload: dict[str, Any]) -> str:
    action_lines = "\n".join(
        f"- `{item.get('action_type')}` [{item.get('priority')}] {item.get('description')}"
        for item in payload.get("required_actions", [])
        if isinstance(item, dict)
    ) or "- None"
    return f"""# Chief Editor Agent Response

## User Message

{payload.get('user_message')}

## Understanding

{payload.get('human_readable_reply')}

## Structured Intent

- Intent: `{payload.get('intent')}`
- Target: `{payload.get('target_artifact_id')}`
- Agent to call: `{payload.get('agent_to_call')}`
- Execution policy: `{payload.get('execution_policy')}`
- Status: `{payload.get('status')}`

## Required Actions

{action_lines}
"""
