"""Persist lightweight workbench feedback preferences."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


def output_paths(paths: ProjectPaths) -> dict[str, Path]:
    root = paths.market_content_root / "09_workbench_actions"
    return {
        "json": root / "workbench_feedback_memory.json",
        "md": root / "workbench_feedback_memory.md",
        "frontstage_md": paths.frontstage_root / "workbench_feedback_memory_board.md",
    }


def preference_from_response(response: dict[str, Any]) -> dict[str, Any]:
    message = str(response.get("user_message") or "")
    intent = str(response.get("intent") or "unknown")
    mapping = {
        "rewrite_angle": ("angle", "prefer_specific_editorial_angle"),
        "strengthen_evidence": ("evidence", "require_stronger_evidence"),
        "rewrite_title": ("title", "stronger_title_hook"),
        "rewrite_opening": ("style", "stronger_opening_hook"),
        "change_topic": ("topic", "prefer_topic_control"),
        "hold": ("risk", "hold_when_uncertain"),
        "approve": ("platform", "approve_ready_candidate_with_human_confirmation"),
    }
    pref_type, summary = mapping.get(intent, ("style", "needs_more_editor_clarification"))
    digest = hashlib.sha1(f"{pref_type}|{summary}".encode("utf-8")).hexdigest()[:10]
    return {
        "preference_id": f"pref_{digest}",
        "preference_type": pref_type,
        "summary": summary,
        "evidence_messages": [message] if message else [],
        "confidence": 0.72 if intent != "ask_clarification" else 0.45,
        "status": "active" if intent != "ask_clarification" else "tentative",
    }


def merge_preference(existing: list[dict[str, Any]], new_pref: dict[str, Any]) -> list[dict[str, Any]]:
    for item in existing:
        if item.get("preference_id") == new_pref.get("preference_id"):
            messages = item.get("evidence_messages") if isinstance(item.get("evidence_messages"), list) else []
            for message in new_pref.get("evidence_messages", []):
                if message and message not in messages:
                    messages.append(message)
            item["evidence_messages"] = messages[-10:]
            item["confidence"] = max(float(item.get("confidence") or 0.0), float(new_pref.get("confidence") or 0.0))
            item["status"] = new_pref.get("status") or item.get("status")
            return existing
    existing.append(new_pref)
    return existing


def update_workbench_feedback_memory(paths: ProjectPaths, repo_root: Path) -> dict[str, Any]:
    outputs = output_paths(paths)
    existing = read_json(outputs["json"])
    response = read_json(paths.market_content_root / "09_workbench_actions" / "latest_chief_editor_response.json")
    pending = read_json(paths.market_content_root / "09_workbench_actions" / "latest_pending_actions.json")
    memory = {
        "schema_version": SCHEMA_VERSION,
        "updated_at": utc_now(),
        "preferences": existing.get("preferences") if isinstance(existing.get("preferences"), list) else [],
        "recent_feedback": existing.get("recent_feedback") if isinstance(existing.get("recent_feedback"), list) else [],
        "rule_suggestion_inputs": existing.get("rule_suggestion_inputs") if isinstance(existing.get("rule_suggestion_inputs"), list) else [],
    }
    if response:
        memory["preferences"] = merge_preference(memory["preferences"], preference_from_response(response))
        memory["recent_feedback"].append(
            {
                "message_id": response.get("message_id"),
                "intent": response.get("intent"),
                "user_message": response.get("user_message"),
                "created_at": response.get("generated_at") or utc_now(),
            }
        )
    for action in list_payload(pending, "actions"):
        memory["rule_suggestion_inputs"].append(
            {
                "source": "workbench_action",
                "action_type": action.get("action_type"),
                "description": action.get("description"),
                "status": action.get("status"),
            }
        )
    memory["recent_feedback"] = memory["recent_feedback"][-50:]
    memory["rule_suggestion_inputs"] = memory["rule_suggestion_inputs"][-100:]
    write_json_and_markdown(memory, render_markdown(memory), outputs)
    memory["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return memory


def render_markdown(memory: dict[str, Any]) -> str:
    prefs = memory.get("preferences") if isinstance(memory.get("preferences"), list) else []
    rows = "\n".join(
        f"| {item.get('preference_type')} | {item.get('summary')} | {item.get('confidence')} | {item.get('status')} |"
        for item in prefs
    ) or "| - | - | - | - |"
    return f"""# Workbench Feedback Memory

## Summary

- Updated at: `{memory.get('updated_at')}`
- Preferences: `{len(prefs)}`
- Recent feedback: `{len(memory.get('recent_feedback') or [])}`
- Rule suggestion inputs: `{len(memory.get('rule_suggestion_inputs') or [])}`

## Preferences

| Type | Summary | Confidence | Status |
|---|---|---:|---|
{rows}
"""
