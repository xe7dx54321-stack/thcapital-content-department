"""Clean operator-facing view model for the Workbench UI.

The legacy Workbench data payload intentionally keeps rich engineering panels.
This module distills that payload into five user-facing areas:

- today_overview
- today_article
- quality_check
- replay_dashboard
- system_ops
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_int, today_token, utc_now


SCHEMA_VERSION = "v1"


SOURCE_METADATA_PATTERNS = (
    "openclaw source metadata:",
    "source metadata:",
    "finsmes ai gnews",
    "techcrunch ai feed item",
    "reddit metadata",
    "hacker news item",
)


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.frontstage_root / f"{run_date}__workbench-view-model.json",
        "latest_json": paths.frontstage_root / "latest_workbench_view_model.json",
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any, fallback: str = "") -> str:
    text = str(value or "").strip()
    return text or fallback


def _first(items: Any) -> dict[str, Any]:
    rows = _list(items)
    return rows[0] if rows and isinstance(rows[0], dict) else {}


def looks_like_source_metadata(value: Any) -> bool:
    text = _text(value).lower()
    if not text:
        return False
    if any(pattern in text for pattern in SOURCE_METADATA_PATTERNS):
        return True
    return bool(re.search(r"\b(feed item|metadata item|source item)\b", text))


def clean_display_text(value: Any) -> str:
    text = _text(value)
    if not text:
        return ""
    text = re.sub(r"OpenClaw source metadata:\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"source metadata:\s*", "", text, flags=re.IGNORECASE)
    text = text.replace("OpenClaw source metadata", "信源 metadata")
    text = text.replace("OpenClaw", "迁移信源")
    return text.strip()


def _status_zh(value: str) -> str:
    mapping = {
        "READY_TO_REVIEW": "可审阅",
        "NO_CANDIDATE": "未产出",
        "NEEDS_ATTENTION": "需要处理",
        "SYSTEM_ISSUE": "系统异常",
        "NORMAL": "正常",
        "WARNING": "有警告",
        "ERROR": "异常",
        "READY": "已生成",
        "MISSING": "未生成",
        "NEEDS_REVISION": "需要修订",
        "HOLD": "暂缓",
        "PASS": "通过",
        "ACTIONABLE": "有问题",
        "FAIL": "失败",
        "UNKNOWN": "未检查",
    }
    return mapping.get(value, value or "未知")


def _panel(data: dict[str, Any], key: str) -> dict[str, Any]:
    return _dict(data.get(key))


def _selected_auto_content(data: dict[str, Any]) -> dict[str, Any]:
    panel = _panel(data, "autonomous_content_production_panel")
    final = _dict(panel.get("selected_final_candidate"))
    review = _dict(panel.get("selected_review"))
    draft = _dict(panel.get("selected_draft"))
    brief = _dict(panel.get("selected_brief"))
    topic = _dict(panel.get("selected_topic"))
    regression = {
        "status": panel.get("quality_regression_status", "UNKNOWN"),
        "summary": _dict(panel.get("quality_regression_summary")),
        "checks": _list(panel.get("quality_checks")),
    }
    if final:
        return {"source": "autonomous", "final": final, "review": review, "draft": draft, "brief": brief, "topic": topic, "regression": regression}

    final_review = _panel(data, "final_review")
    legacy_final = _dict(final_review.get("selected_candidate"))
    selected_article_id = str(data.get("selected_article_id") or "")
    articles = _list(data.get("articles"))
    article = next((item for item in articles if isinstance(item, dict) and item.get("article_id") == selected_article_id), _first(articles))
    return {
        "source": "legacy",
        "final": legacy_final,
        "review": {},
        "draft": article,
        "brief": {},
        "topic": {"title": article.get("title") or article.get("wechat_title") or ""},
        "regression": {"status": "UNKNOWN", "summary": {}, "checks": []},
    }


def _runtime_system_status(runtime: dict[str, Any], acceptance: dict[str, Any]) -> str:
    gate_status = str(acceptance.get("gate_status") or "")
    blocking = safe_int((_dict(acceptance.get("summary"))).get("blocking_failures"))
    runtime_status = str(runtime.get("runtime_status") or "UNKNOWN")
    heartbeat_age = safe_int(runtime.get("heartbeat_age_seconds"))
    launch_ok = bool(runtime.get("launchagent_installed")) and bool(runtime.get("launchagent_loaded"))
    if blocking > 0 or gate_status == "BLOCKED" or runtime_status in {"FAILED", "ERROR"}:
        return "ERROR"
    if not launch_ok or heartbeat_age > 7200 or runtime_status not in {"IDLE", "RUNNING", "STOPPING"}:
        return "WARNING"
    return "NORMAL"


def _candidate_status(final: dict[str, Any]) -> str:
    if not final:
        return "MISSING"
    status = str(final.get("status") or "")
    if status in {"READY_FOR_HUMAN_REVIEW", "READY_FOR_FINAL_REVIEW", "READY"}:
        return "READY"
    if status in {"NEEDS_REVISION", "REVISED"}:
        return "NEEDS_REVISION"
    if status in {"HOLD", "HELD"}:
        return "HOLD"
    return "READY"


def _quality_status(selected: dict[str, Any]) -> str:
    regression = _dict(selected.get("regression"))
    status = str(regression.get("status") or "UNKNOWN")
    if status in {"PASS", "ACTIONABLE", "FAIL"}:
        return status
    review = _dict(selected.get("review"))
    judge = _dict(review.get("judge"))
    if judge.get("decision") in {"ACCEPT", "REVISE"}:
        return "ACTIONABLE" if judge.get("decision") == "REVISE" else "PASS"
    return "UNKNOWN"


def _overall_status(system_status: str, candidate_status: str, quality_status: str) -> str:
    if system_status == "ERROR":
        return "SYSTEM_ISSUE"
    if candidate_status == "MISSING":
        return "NO_CANDIDATE"
    if candidate_status in {"NEEDS_REVISION", "HOLD"} or quality_status in {"ACTIONABLE", "FAIL"} or system_status == "WARNING":
        return "NEEDS_ATTENTION"
    return "READY_TO_REVIEW"


def _agent_review_summary(review: dict[str, Any]) -> dict[str, Any]:
    critic = _dict(review.get("critic"))
    judge = _dict(review.get("judge"))
    proponent = _dict(review.get("proponent"))
    rewrite = _dict(review.get("rewrite"))
    concerns = [str(item) for item in _list(critic.get("main_concerns"))[:3]]
    strengths = [str(item) for item in _list(proponent.get("strongest_points"))[:3]]
    return {
        "decision": judge.get("decision") or review.get("status") or "UNKNOWN",
        "quality_score": judge.get("quality_score", ""),
        "core_issue": concerns[0] if concerns else "暂无阻断问题。",
        "recommendation": "补充一手来源，并收紧标题与结尾判断。" if concerns else "进入人工精修。",
        "strengths": strengths,
        "concerns": concerns,
        "rewrite_generated": bool(rewrite.get("generated")),
        "rewrite_version_id": rewrite.get("rewrite_version_id") or "",
        "details": {
            "proponent": proponent,
            "critic": critic,
            "judge": judge,
            "rewrite": rewrite,
        },
    }


def _quality_checklist(checks: list[Any]) -> list[dict[str, Any]]:
    label_map = {
        "has_final_candidate": "是否有最终候选稿",
        "has_why_now": "why now 是否清楚",
        "has_reader_question": "核心读者问题是否清楚",
        "has_core_judgment": "是否有观点",
        "has_story_line": "故事线是否清晰",
        "has_evidence_chain": "证据是否足够",
        "has_limits": "是否有反方 / 限制",
        "avoid_generic_ai_taste": "是否有 AI 味",
        "title_is_specific": "标题是否像公众号标题",
        "opening_has_pull": "开头是否有抓力",
        "industry_judgment": "是否保留产业判断",
        "no_target_price": "是否出现 target price",
        "no_fake_citations": "是否有伪造引用风险",
    }
    rows: list[dict[str, Any]] = []
    for item in checks:
        if not isinstance(item, dict):
            continue
        check_id = str(item.get("check_id") or "")
        status = str(item.get("status") or "UNKNOWN")
        rows.append(
            {
                "check_id": check_id,
                "label": label_map.get(check_id, check_id or "质量检查"),
                "status": status,
                "status_zh": _status_zh(status),
                "reason": item.get("message") or "",
            }
        )
    return rows


def _evidence_summary(brief: dict[str, Any], final: dict[str, Any]) -> dict[str, Any]:
    evidence = [item for item in _list(brief.get("evidence_inventory")) if isinstance(item, dict)]
    weak = [item for item in evidence if item.get("can_use_as_hard_evidence") is False or item.get("evidence_role") == "weak_signal"]
    primary = [item for item in evidence if item.get("evidence_role") == "hard_evidence"]
    secondary = [item for item in evidence if item.get("evidence_role") in {"supporting_evidence", "heat_validation"}]
    needs_confirmation = [
        clean_display_text(item.get("title") or item.get("source_name") or item.get("evidence_id"))
        for item in evidence
        if item.get("can_use_as_hard_evidence") is False or item.get("metadata_only")
    ]
    if not evidence:
        ids = _list(final.get("evidence_ids"))
        return {
            "core_evidence_count": len(ids),
            "primary_source_count": 0,
            "secondary_source_count": len(ids),
            "weak_signal_count": 0,
            "needs_human_confirmation": [],
            "note": "只找到 evidence id，未找到详细 evidence inventory。",
        }
    return {
        "core_evidence_count": len(evidence),
        "primary_source_count": len(primary),
        "secondary_source_count": len(secondary),
        "weak_signal_count": len(weak),
        "needs_human_confirmation": needs_confirmation[:6],
        "note": "弱信号和 metadata-only 证据不会作为硬证据。",
    }


def _human_review_items(quality_status: str, source_metadata_warning: bool, evidence_summary: dict[str, Any]) -> list[str]:
    rows = [
        "这个标题是否足够具体，像一篇公众号文章而不是 source 名称？",
        "开头是否值得继续读，是否在前两段说明了 why now？",
        "关键证据是否真实可靠，是否有一手来源可以补充？",
        "有没有明显 AI 味、空泛判断或硬凑结构？",
        "是否值得人工改后进入发布准备？",
    ]
    if source_metadata_warning:
        rows.insert(0, "当前标题疑似 source metadata 污染，请先重写标题和选题表达。")
    if safe_int(evidence_summary.get("weak_signal_count")):
        rows.append("弱信号只可作为线索，发布前必须人工确认。")
    if quality_status == "FAIL":
        rows.append("质量回归失败，先不要进入人工发布准备。")
    return rows


def build_workbench_view_model_from_data(data: dict[str, Any], acceptance_gate: dict[str, Any] | None = None) -> dict[str, Any]:
    selected = _selected_auto_content(data)
    final = _dict(selected.get("final"))
    review = _dict(selected.get("review"))
    brief = _dict(selected.get("brief"))
    topic = _dict(selected.get("topic"))
    runtime = _panel(data, "runtime_control_center_panel")
    replay = _panel(data, "replay_trial_panel")
    acquisition = _panel(data, "acquisition_playbook_panel")
    openclaw = _panel(data, "openclaw_migration_panel")
    activation = _panel(data, "openclaw_activation_panel")

    acceptance = acceptance_gate if isinstance(acceptance_gate, dict) else {}

    raw_title = final.get("title") or topic.get("title") or ""
    display_title = clean_display_text(raw_title) or "暂无候选稿"
    display_topic = clean_display_text(topic.get("title") or raw_title)
    source_metadata_warning = looks_like_source_metadata(raw_title) or looks_like_source_metadata(topic.get("title"))
    system_status = _runtime_system_status(runtime, acceptance)
    candidate_status = _candidate_status(final)
    quality_status = _quality_status(selected)
    overall_status = _overall_status(system_status, candidate_status, quality_status)
    agent_summary = _agent_review_summary(review)
    evidence = _evidence_summary(brief, final)

    alerts: list[dict[str, str]] = []
    if source_metadata_warning:
        alerts.append({"level": "warning", "message": "当前主选题/标题疑似 source metadata 污染，需要先做标题归一化。"})
    diagnosis_summary = _dict(replay.get("diagnosis_summary"))
    if float(diagnosis_summary.get("duplicate_topic_ratio") or 0) >= 0.5:
        alerts.append({"level": "warning", "message": "7 天回放显示重复选题风险偏高，请观察是否需要加 source diversity penalty。"})
    if safe_int(evidence.get("weak_signal_count")) or evidence.get("needs_human_confirmation"):
        alerts.append({"level": "info", "message": "存在需要人工确认的 metadata / weak signal 证据。"})
    if system_status == "WARNING":
        alerts.append({"level": "warning", "message": "Runtime 或 Go-Live Gate 有非阻断 warning，请在系统运维查看。"})
    if not alerts:
        alerts.append({"level": "ok", "message": "暂无阻断问题。"})
    alerts = alerts[:3]

    why_raw = clean_display_text(brief.get("one_sentence_thesis") or brief.get("narrative_angle") or final.get("quality_summary") or "候选稿已进入人工审阅队列。")
    if "Use migrated" in why_raw or "funding_startup" in why_raw:
        why_raw = "这是一个迁移信源带来的融资/创业公司线索，真正值得看的是它能否被一手来源确认，并改变我们对产业节奏的判断。"
    article_markdown = clean_display_text(final.get("article_markdown") or selected.get("draft", {}).get("article_markdown") or "")
    today_overview = {
        "overall_status": overall_status,
        "overall_status_zh": _status_zh(overall_status),
        "system_status": system_status,
        "system_status_zh": _status_zh(system_status),
        "candidate_status": candidate_status,
        "candidate_status_zh": _status_zh(candidate_status),
        "quality_status": quality_status,
        "quality_status_zh": _status_zh(quality_status),
        "next_scheduled_run": runtime.get("next_scheduled_run") or "",
        "main_topic": display_topic,
        "recommended_title": display_title,
        "one_sentence_judgement": "这是一篇值得人工审阅的候选稿。" if candidate_status == "READY" else "今天还没有可审阅的最终候选稿。",
        "why_worth_reading": why_raw,
        "main_risk": "标题疑似 source metadata，需要人工重写。" if source_metadata_warning else (agent_summary.get("core_issue") or "暂无主要风险。"),
        "recommended_action": "打开“今日稿件”审阅正文。" if candidate_status == "READY" else "先运行或等待自动内容生产链路。",
        "alerts": alerts,
    }

    today_article = {
        "title": display_title,
        "subtitle": clean_display_text(final.get("subtitle") or ""),
        "topic": display_topic,
        "generated_at": final.get("generated_at") or data.get("generated_at") or "",
        "status": final.get("status") or candidate_status,
        "status_zh": _status_zh(candidate_status),
        "quality_rating": quality_status,
        "article_markdown": article_markdown,
        "agent_review_summary": agent_summary,
        "actions": [
            {"action_id": "copy_body", "label": "复制正文", "kind": "copy"},
            {"action_id": "copy_title", "label": "复制标题", "kind": "copy"},
            {"action_id": "mark_worth_editing", "label": "标记为值得人工修改", "kind": "placeholder"},
            {"action_id": "mark_abandoned", "label": "标记为放弃", "kind": "placeholder"},
            {"action_id": "request_title_rewrite", "label": "请求重写标题", "kind": "placeholder"},
            {"action_id": "request_angle_change", "label": "请求换角度", "kind": "placeholder"},
        ],
        "source_metadata_warning": source_metadata_warning,
    }

    regression = _dict(selected.get("regression"))
    regression_summary = _dict(regression.get("summary"))
    checklist = _quality_checklist(_list(regression.get("checks")))
    quality_check = {
        "rating": quality_status,
        "rating_zh": _status_zh(quality_status),
        "can_review": candidate_status == "READY" and quality_status in {"PASS", "ACTIONABLE"},
        "blocking_issue_count": safe_int(regression_summary.get("blocking_failures")),
        "warning_count": safe_int(regression_summary.get("warn")),
        "checklist": checklist,
        "evidence_summary": evidence,
        "human_review_checklist": _human_review_items(quality_status, source_metadata_warning, evidence),
    }

    replay_dashboard = {
        "summary": {
            "replay_ready_days": safe_int((_dict(replay.get("availability_summary"))).get("replay_ready_days")),
            "selected_days": safe_int((_dict(replay.get("topic_selection_summary"))).get("selected_days")),
            "final_candidate_count": safe_int((_dict(replay.get("article_review_summary"))).get("final_candidate_count")),
            "pass_days": safe_int((_dict(replay.get("quality_summary"))).get("pass_days")),
            "duplicate_topic_ratio": diagnosis_summary.get("duplicate_topic_ratio", 0),
            "proposal_count": safe_int((_dict(replay.get("calibration_summary"))).get("proposal_count")),
        },
        "days": _list(replay.get("day_cards")),
        "calibration_proposals": [
            {
                **item,
                "auto_apply": False,
                "requires_human_approval": True,
            }
            for item in _list(replay.get("proposals"))
            if isinstance(item, dict)
        ],
        "policy": {
            "replay_is_not_production": True,
            "calibration_auto_apply": False,
        },
    }

    system_ops = {
        "runtime": {
            "status": runtime.get("runtime_status") or "UNKNOWN",
            "pid": runtime.get("runtime_pid"),
            "runtime_instance_id": runtime.get("runtime_instance_id") or "",
            "last_heartbeat": runtime.get("last_heartbeat") or "",
            "heartbeat_age_seconds": runtime.get("heartbeat_age_seconds") or "",
            "current_job": runtime.get("current_job_id") or "",
            "next_scheduled_run": runtime.get("next_scheduled_run") or "",
            "go_live_gate": acceptance.get("gate_status") or "UNKNOWN",
            "blocking_failures": safe_int((_dict(acceptance.get("summary"))).get("blocking_failures")),
        },
        "launchagent": {
            "installed": bool(runtime.get("launchagent_installed")),
            "loaded": bool(runtime.get("launchagent_loaded")),
            "enabled": bool(runtime.get("launchagent_enabled")),
            "plist_path": runtime.get("launchagent_plist_path") or "",
        },
        "jobs": {
            "ledger": _dict(runtime.get("ledger_summary")),
            "retry": _dict(runtime.get("retry_summary")),
            "missed_run": _dict(runtime.get("missed_run_summary")),
            "catchup_plan": _list(runtime.get("catchup_plan"))[:8],
        },
        "acquisition": {
            "network": _dict(runtime.get("network_readiness")),
            "runtime_plan": _dict(acquisition.get("runtime_plan_summary")),
            "next_lanes": _list(acquisition.get("lane_cards"))[:8],
        },
        "openclaw": {
            "conflict_count": safe_int((_dict(openclaw.get("coexistence_summary"))).get("conflict_count")),
            "manual_review_count": safe_int((_dict(openclaw.get("coexistence_summary"))).get("manual_review")),
            "safe_to_disable": safe_int((_dict(openclaw.get("coexistence_summary"))).get("safe_to_disable")),
            "phase29_status": openclaw.get("phase29_status") or "UNKNOWN",
            "phase30_status": activation.get("phase30_status") or "UNKNOWN",
            "gateway_unmodified": True,
            "cron_unmodified": True,
        },
        "debug_actions": [
            {"action_id": "refresh_status", "label": "刷新系统状态", "endpoint": "/api/workbench-data", "dangerous": False},
            {"action_id": "pause_runtime", "label": "暂停 Runtime", "endpoint": "/api/runtime/pause", "dangerous": True},
            {"action_id": "resume_runtime", "label": "恢复 Runtime", "endpoint": "/api/runtime/resume", "dangerous": True},
            {"action_id": "run_daily_content", "label": "手动补跑今日内容生产", "endpoint": "/api/runtime/run-daily", "dangerous": True},
            {"action_id": "run_go_live_acceptance", "label": "运行 Go-Live Acceptance", "endpoint": "/api/runtime/run-validation", "dangerous": True},
        ],
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": data.get("run_date") or today_token(),
        "today_overview": today_overview,
        "today_article": today_article,
        "quality_check": quality_check,
        "replay_dashboard": replay_dashboard,
        "system_ops": system_ops,
    }


def build_workbench_view_model(paths: ProjectPaths, data: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = data if isinstance(data, dict) else read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    if not isinstance(payload, dict):
        payload = {}
    acceptance = read_json(paths.logs_root / "latest_runtime_go_live_acceptance_gate.json")
    return build_workbench_view_model_from_data(payload, acceptance)


def write_workbench_view_model(view_model: dict[str, Any], paths: ProjectPaths, repo_root: Path) -> dict[str, Path]:
    run_date = str(view_model.get("run_date") or today_token()).replace("-", "")[:8]
    outputs = output_paths(paths, run_date)
    payload = {**view_model, "outputs": {key: repo_relative(path, repo_root) for key, path in outputs.items()}}
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return outputs
