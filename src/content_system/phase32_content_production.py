"""Phase 32 autonomous topic-to-article production helpers."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown
from content_system.upstream_intelligence_common import compact_text, markdown_table, stable_id


SCHEMA_VERSION = "v1"
WEAK_LANES = {"reddit_llm_discussion", "developer_community", "youtube_signal", "x_signal", "trend_heat_validation", "wechat_metadata", "china_ai_media"}
BANNED_DRAFT_PATTERNS = ("目标价", "target price", "买入评级")
DISCOURAGED_PHRASES = ("未来可期", "值得关注", "打开想象空间", "持续赋能", "深度赋能", "重塑格局")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    return loaded if isinstance(loaded, dict) else {}


def config(repo_root: Path, name: str) -> dict[str, Any]:
    return load_yaml(repo_root / "config" / name)


def ensure_dirs(paths: ProjectPaths) -> None:
    for relative in ("05_briefs", "06_outlines", "07_drafts", "08_final_candidates"):
        (paths.market_content_root / relative).mkdir(parents=True, exist_ok=True)


def write_outputs(payload: dict[str, Any], markdown: str, outputs: dict[str, Path], repo_root: Path) -> dict[str, Path]:
    write_json_and_markdown(payload, markdown, outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return outputs


def summary_markdown(title: str, summary: dict[str, Any], rows: list[dict[str, Any]] | None = None, columns: tuple[str, ...] = ()) -> str:
    body = "\n".join(f"- {key}: `{value}`" for key, value in summary.items())
    table = markdown_table(rows or [], columns) if rows and columns else ""
    return f"# {title}\n\n## Summary\n\n{body}\n\n{table}\n"


def warning_for_missing(inputs: dict[str, Path]) -> list[str]:
    return [f"Missing input: {name} ({path})" for name, path in inputs.items() if not path.exists()]


def legacy_search_roots(paths: ProjectPaths, repo_root: Path) -> list[tuple[str, Path]]:
    return [
        ("current_repo", repo_root / "config"),
        ("current_repo", repo_root / "docs"),
        ("current_repo", repo_root / "src" / "content_system"),
        ("content_library", paths.legacy_content_root / "09_runbooks" / "skills"),
        ("content_library", paths.legacy_content_root / "09_runbooks" / "templates"),
        ("content_library", paths.legacy_content_root / "02_topic_radar" / "deep_articles"),
        ("openclaw", Path.home() / ".openclaw"),
    ]


def infer_asset_type(path: Path) -> str:
    text = path.as_posix().lower()
    if "skill" in text:
        return "skill"
    if "prompt" in text or path.name == "agent_prompts.json":
        return "prompt"
    if "recipe" in text:
        return "recipe"
    if "rubric" in text or "scorecard" in text or "quality" in text:
        return "rubric"
    if "template" in text:
        return "template"
    if "example" in text or "deep_articles" in text:
        return "example"
    if "failure" in text or "redteam" in text:
        return "failure_case"
    if "methodology" in text:
        return "methodology"
    if "agent" in text:
        return "agent_config"
    return "unknown"


def infer_stage(path: Path) -> str:
    text = path.as_posix().lower()
    pairs = (
        ("topic", "topic_selection"),
        ("brief", "brief"),
        ("outline", "outline"),
        ("draft", "draft"),
        ("review", "review"),
        ("redteam", "review"),
        ("rewrite", "rewrite"),
        ("title", "title"),
        ("opening", "opening"),
        ("evidence", "evidence"),
        ("visual", "visual"),
    )
    for marker, stage in pairs:
        if marker in text:
            return stage
    return "unknown"


def infer_agent(path: Path) -> str:
    text = path.as_posix().lower()
    for agent in ("signal-harvester", "market-scout", "knowledge-curator", "topic-planner", "content-analyst", "market-editor", "chief-editor", "critic", "judge", "rewrite"):
        if agent in text:
            return agent
    if "proponent" in text:
        return "proponent"
    if "editor" in text:
        return "market-editor"
    return ""


def migration_value_for(asset_type: str, stage: str, path: Path) -> tuple[str, str, str]:
    text = path.as_posix().lower()
    if "publish" in text and "template" not in text:
        return "NONE", "HIGH", "DO_NOT_MIGRATE"
    if asset_type in {"skill", "methodology", "rubric", "recipe"}:
        return "HIGH", "MEDIUM", "ADAPT"
    if asset_type in {"template", "prompt"} and stage in {"brief", "outline", "draft", "review", "rewrite", "title", "opening"}:
        return "HIGH", "MEDIUM", "ADAPT"
    if asset_type == "example":
        return "MEDIUM", "LOW", "REFERENCE_ONLY"
    if asset_type == "failure_case":
        return "MEDIUM", "LOW", "REFERENCE_ONLY"
    return "LOW", "LOW", "REFERENCE_ONLY"


def file_digest(path: Path) -> str:
    try:
        return hashlib.sha1(path.read_bytes()).hexdigest()[:12]
    except OSError:
        return hashlib.sha1(path.as_posix().encode("utf-8")).hexdigest()[:12]


def audit_legacy_content_assets(paths: ProjectPaths, repo_root: Path, limit: int = 260) -> tuple[dict[str, Any], dict[str, Path]]:
    warnings: list[str] = []
    assets: list[dict[str, Any]] = []
    keywords = re.compile(r"(prompt|skill|recipe|rubric|template|methodolog|review|rewrite|draft|outline|brief|title|opening|editor|judge|critic|quality|redteam)", re.I)
    allowed_suffixes = {".md", ".json", ".yaml", ".yml", ".toml", ".txt", ".py"}
    for source_system, root in legacy_search_roots(paths, repo_root):
        if not root.exists():
            warnings.append(f"Missing search root: {root}")
            continue
        for path in root.rglob("*"):
            if len(assets) >= limit:
                break
            if not path.is_file() or path.suffix.lower() not in allowed_suffixes:
                continue
            rel = repo_relative(path, repo_root)
            if any(part in rel for part in ("__pycache__", "node_modules", ".git", "11_frontstage")):
                continue
            if not keywords.search(path.name) and not keywords.search(rel):
                continue
            asset_type = infer_asset_type(path)
            stage = infer_stage(path)
            value, risk, action = migration_value_for(asset_type, stage, path)
            assets.append(
                {
                    "asset_id": f"legacy_asset_{file_digest(path)}",
                    "asset_name": path.stem[:120],
                    "asset_type": asset_type,
                    "source_path": rel if source_system != "openclaw" else path.as_posix().replace(str(Path.home()), "~"),
                    "source_system": source_system,
                    "related_agent": infer_agent(path),
                    "related_stage": stage,
                    "migration_value": value,
                    "migration_risk": risk,
                    "requires_rewrite": action in {"ADAPT", "MIGRATE"},
                    "legacy_dependency": ["legacy_path_or_schema_review"] if source_system != "current_repo" else [],
                    "summary": compact_text(f"{asset_type} asset for {stage}; migrate only after normalization and safety review.", 180),
                    "recommended_action": action,
                }
            )
        if len(assets) >= limit:
            warnings.append(f"Asset audit capped at {limit} items to avoid copying legacy content wholesale.")
            break
    counts = Counter(item["asset_type"] for item in assets)
    summary = {
        "asset_count": len(assets),
        "high_value": sum(1 for item in assets if item["migration_value"] == "HIGH"),
        "medium_value": sum(1 for item in assets if item["migration_value"] == "MEDIUM"),
        "low_value": sum(1 for item in assets if item["migration_value"] == "LOW"),
        "do_not_migrate": sum(1 for item in assets if item["recommended_action"] == "DO_NOT_MIGRATE"),
        "skills": counts.get("skill", 0),
        "prompts": counts.get("prompt", 0),
        "recipes": counts.get("recipe", 0),
        "rubrics": counts.get("rubric", 0),
        "examples": counts.get("example", 0),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "assets": assets,
        "summary": summary,
        "warnings": warnings,
        "policy": {"read_only_audit": True, "no_prompt_auto_apply": True, "no_legacy_file_mutation": True},
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_legacy_content_asset_audit.json",
        "latest_md": paths.logs_root / "latest_legacy_content_asset_audit.md",
    }
    rows = [{"type": a["asset_type"], "stage": a["related_stage"], "value": a["migration_value"], "action": a["recommended_action"], "name": compact_text(a["asset_name"], 48)} for a in assets[:30]]
    write_outputs(payload, summary_markdown("Legacy Content Asset Audit", summary, rows, ("type", "stage", "value", "action", "name")), outputs, repo_root)
    return payload, outputs


def target_component_for(asset: dict[str, Any]) -> str:
    stage = str(asset.get("related_stage") or "")
    asset_type = str(asset.get("asset_type") or "")
    if stage == "topic_selection":
        return "topic_methodology"
    if stage == "brief":
        return "brief_builder"
    if stage == "outline":
        return "outline_builder"
    if stage in {"draft", "title", "opening"}:
        return "draft_writer"
    if stage == "review" or asset_type == "rubric":
        return "critic_agent"
    if stage == "rewrite":
        return "rewrite_agent"
    if stage == "visual":
        return "visual_plan"
    if asset_type in {"methodology", "recipe"}:
        return "content_recipe"
    return "quality_regression"


def map_legacy_knowhow(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    audit_path = paths.logs_root / "latest_legacy_content_asset_audit.json"
    audit = read_json(audit_path)
    warnings = warning_for_missing({"legacy_content_asset_audit": audit_path})
    mappings: list[dict[str, Any]] = []
    for asset in list_payload(audit, "assets"):
        action = str(asset.get("recommended_action") or "")
        if action == "DO_NOT_MIGRATE":
            mode = "REJECT"
        elif action == "REFERENCE_ONLY":
            mode = "REFERENCE_ONLY"
        elif asset.get("source_system") == "current_repo" and asset.get("asset_type") in {"methodology", "rubric"}:
            mode = "DIRECT"
        else:
            mode = "ADAPT"
        mappings.append(
            {
                "mapping_id": stable_id("knowmap", asset.get("asset_id"), target_component_for(asset)),
                "legacy_asset_id": asset.get("asset_id", ""),
                "target_component": target_component_for(asset),
                "migration_mode": mode,
                "normalized_rule": compact_text(f"Use the audited {asset.get('asset_type')} as a reference for {target_component_for(asset)}; rewrite into Phase32 playbooks before production use.", 240),
                "reason": asset.get("summary", ""),
                "requires_human_review": asset.get("migration_risk") in {"MEDIUM", "HIGH"} or mode != "DIRECT",
                "auto_apply": False,
            }
        )
    summary = {
        "mapping_count": len(mappings),
        "direct": sum(1 for item in mappings if item["migration_mode"] == "DIRECT"),
        "adapt": sum(1 for item in mappings if item["migration_mode"] == "ADAPT"),
        "reference_only": sum(1 for item in mappings if item["migration_mode"] == "REFERENCE_ONLY"),
        "reject": sum(1 for item in mappings if item["migration_mode"] == "REJECT"),
        "auto_apply": 0,
        "requires_human_review": sum(1 for item in mappings if item["requires_human_review"]),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "mappings": mappings,
        "summary": summary,
        "warnings": warnings,
        "policy": {"auto_apply": False, "does_not_modify_methodology": True, "does_not_modify_agent_prompts": True},
    }
    outputs = {
        "latest_json": paths.logs_root / "latest_legacy_knowhow_methodology_mapping.json",
        "latest_md": paths.logs_root / "latest_legacy_knowhow_methodology_mapping.md",
    }
    rows = [{"mode": m["migration_mode"], "target": m["target_component"], "review": m["requires_human_review"]} for m in mappings[:30]]
    write_outputs(payload, summary_markdown("Legacy Know-how Methodology Mapping", summary, rows, ("mode", "target", "review")), outputs, repo_root)
    return payload, outputs


def build_content_playbook_report(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    playbooks = config(repo_root, "content_production_playbooks.yaml")
    topic = config(repo_root, "topic_scoring_playbook.yaml")
    brief = config(repo_root, "brief_generation_playbook.yaml")
    outline = config(repo_root, "outline_generation_playbook.yaml")
    draft = config(repo_root, "draft_generation_playbook.yaml")
    review = config(repo_root, "review_rewrite_playbook.yaml")
    summary = {
        "playbook_count": len(playbooks.get("playbooks", {}) if isinstance(playbooks.get("playbooks"), dict) else {}),
        "topic_dimensions": len(topic.get("dimensions", {}) if isinstance(topic.get("dimensions"), dict) else {}),
        "brief_sections": len(brief.get("required_sections", []) if isinstance(brief.get("required_sections"), list) else []),
        "outline_sections": len(outline.get("required_sections", []) if isinstance(outline.get("required_sections"), list) else []),
        "review_checks": len(review.get("review_checks", []) if isinstance(review.get("review_checks"), list) else []),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "summary": summary,
        "configs": {
            "content_production_playbooks": playbooks,
            "topic_scoring_playbook": topic,
            "brief_generation_playbook": brief,
            "outline_generation_playbook": outline,
            "draft_generation_playbook": draft,
            "review_rewrite_playbook": review,
        },
        "policy": {"configured_only": True, "does_not_overwrite_methodology": True},
    }
    outputs = {"latest_json": paths.logs_root / "latest_content_production_playbooks.json", "latest_md": paths.logs_root / "latest_content_production_playbooks.md"}
    write_outputs(payload, summary_markdown("Content Production Playbooks", summary), outputs, repo_root)
    return payload, outputs


def validate_content_playbooks(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    topic = config(repo_root, "topic_scoring_playbook.yaml")
    brief = config(repo_root, "brief_generation_playbook.yaml")
    outline = config(repo_root, "outline_generation_playbook.yaml")
    draft = config(repo_root, "draft_generation_playbook.yaml")
    review = config(repo_root, "review_rewrite_playbook.yaml")
    checks: list[dict[str, Any]] = []
    dimensions = topic.get("dimensions") if isinstance(topic.get("dimensions"), dict) else {}
    weight_sum = round(sum(safe_float(item.get("weight")) for item in dimensions.values() if isinstance(item, dict)), 4)
    checks.append({"check_id": "topic_dimension_weight_sum", "status": "PASS" if 0.99 <= weight_sum <= 1.01 else "FAIL", "message": f"weight_sum={weight_sum}"})
    checks.append({"check_id": "brief_required_sections", "status": "PASS" if len(brief.get("required_sections", [])) >= 8 else "FAIL", "message": "Brief playbook has required sections."})
    checks.append({"check_id": "outline_has_story_sections", "status": "PASS" if "core_judgment" in outline.get("required_sections", []) else "FAIL", "message": "Outline includes core_judgment."})
    checks.append({"check_id": "draft_do_not_publish", "status": "PASS" if (draft.get("draft_rules") or {}).get("do_not_publish") is True else "FAIL", "message": "Draft playbook forces do_not_publish."})
    checks.append({"check_id": "review_rewrite_sidecar", "status": "PASS" if (review.get("boundaries") or {}).get("rewrite_creates_new_version") is True else "FAIL", "message": "Rewrite creates new versions."})
    fail = sum(1 for item in checks if item["status"] == "FAIL")
    summary = {
        "check_count": len(checks),
        "pass": sum(1 for item in checks if item["status"] == "PASS"),
        "warn": sum(1 for item in checks if item["status"] == "WARN"),
        "fail": fail,
        "blocking_failures": fail,
        "playbook_count": 6,
        "topic_dimensions": len(dimensions),
        "brief_sections": len(brief.get("required_sections", [])),
        "review_checks": len(review.get("review_checks", [])),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "validate_status": "PASS" if fail == 0 else "FAIL", "checks": checks, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_content_production_playbook_validation.json", "latest_md": paths.logs_root / "latest_content_production_playbook_validation.md"}
    write_outputs(payload, summary_markdown("Content Production Playbook Validation", summary, checks, ("check_id", "status", "message")), outputs, repo_root)
    return payload, outputs


def evidence_backfill_by_signal(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "03_topic_candidates" / "latest_openclaw_signal_evidence_backfill.json")
    return {str(item.get("signal_id")): item for item in list_payload(payload, "backfill_items") if item.get("signal_id")}


def confirmation_by_signal(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.logs_root / "latest_weak_signal_confirmation_workflow.json")
    return {str(item.get("signal_id")): item for item in list_payload(payload, "confirmation_items") if item.get("signal_id")}


def collect_topic_inputs(paths: ProjectPaths) -> tuple[list[dict[str, Any]], list[str]]:
    topic_root = paths.market_content_root / "03_topic_candidates"
    inputs = {
        "openclaw_activated_topic_candidates": topic_root / "latest_openclaw_activated_topic_candidates.json",
        "connector_promoted_topic_candidates": topic_root / "latest_connector_promoted_topic_candidates.json",
        "acquisition_to_content_bridge": paths.logs_root / "latest_acquisition_to_content_bridge.json",
        "methodology_topic_scores": topic_root / "latest_methodology_topic_scores.json",
        "connector_evidence_packets": topic_root / "latest_connector_evidence_packets.json",
        "openclaw_signal_evidence_backfill": topic_root / "latest_openclaw_signal_evidence_backfill.json",
    }
    warnings = warning_for_missing(inputs)
    backfills = evidence_backfill_by_signal(paths)
    confirmations = confirmation_by_signal(paths)
    topics: list[dict[str, Any]] = []
    openclaw = read_json(inputs["openclaw_activated_topic_candidates"])
    for item in list_payload(openclaw, "topic_candidates"):
        signal_id = str(item.get("signal_id") or "")
        backfill = backfills.get(signal_id, {})
        confirmation = confirmations.get(signal_id, {})
        topics.append(
            {
                "topic_id": item.get("topic_candidate_id", ""),
                "title": item.get("title", ""),
                "source_origin": "openclaw",
                "lane": item.get("lane", ""),
                "topic_type": item.get("topic_type", "news_explainer"),
                "activation_status": item.get("activation_status", ""),
                "evidence_strength": item.get("evidence_strength", "UNKNOWN"),
                "can_enter_brief_pipeline": bool(item.get("can_enter_brief_pipeline")),
                "can_use_as_hard_evidence": bool(item.get("can_use_as_hard_evidence", False)),
                "evidence_ids": [backfill.get("backfill_id")] if backfill.get("backfill_id") else [],
                "confirmation_status": confirmation.get("confirmation_status", ""),
                "why_now": item.get("why_now", ""),
                "core_angle": item.get("core_angle", ""),
                "missing_evidence": item.get("missing_evidence") if isinstance(item.get("missing_evidence"), list) else [],
                "content_recipe": item.get("topic_type", "news_explainer"),
            }
        )
    connector = read_json(inputs["connector_promoted_topic_candidates"])
    for item in list_payload(connector, "topic_candidates"):
        topics.append(
            {
                "topic_id": item.get("topic_candidate_id", ""),
                "title": item.get("title", ""),
                "source_origin": "connector",
                "lane": ",".join(item.get("domain_tags", []) if isinstance(item.get("domain_tags"), list) else []),
                "topic_type": item.get("topic_type", "news_explainer"),
                "activation_status": item.get("promotion_status", ""),
                "evidence_strength": item.get("evidence_strength", "UNKNOWN"),
                "can_enter_brief_pipeline": item.get("promotion_status") == "PROMOTED",
                "can_use_as_hard_evidence": False,
                "evidence_ids": item.get("evidence_ids") if isinstance(item.get("evidence_ids"), list) else [],
                "confirmation_status": "CONFIRMED_BY_CONNECTOR" if item.get("promotion_status") == "PROMOTED" else "",
                "why_now": item.get("why_now", ""),
                "core_angle": item.get("core_angle", ""),
                "missing_evidence": item.get("missing_evidence") if isinstance(item.get("missing_evidence"), list) else [],
                "content_recipe": item.get("topic_type", "news_explainer"),
            }
        )
    return topics, warnings


def score_strength(value: str, evidence_count: int = 0) -> float:
    base = {"HIGH": 0.92, "MEDIUM": 0.74, "LOW": 0.34, "UNKNOWN": 0.18}.get(str(value or "UNKNOWN"), 0.18)
    return min(1.0, base + (0.06 if evidence_count >= 2 else 0.0))


def score_topic(topic: dict[str, Any], weights: dict[str, Any]) -> dict[str, float]:
    evidence_count = len(topic.get("evidence_ids") or [])
    lane = str(topic.get("lane") or "")
    activation = str(topic.get("activation_status") or "")
    why = str(topic.get("why_now") or topic.get("core_angle") or "")
    scores = {
        "urgency": 0.84 if activation in {"ACTIVATED", "PROMOTED"} else 0.48,
        "reader_value": 0.78 if topic.get("topic_type") in {"startup_tracking", "product_strategy_analysis", "technical_route_analysis", "investment_framework", "builder_insight"} else 0.62,
        "evidence_strength": score_strength(str(topic.get("evidence_strength") or "UNKNOWN"), evidence_count),
        "narrative_potential": 0.76 if len(why) > 30 else 0.48,
        "investment_relevance": 0.80 if any(marker in lane for marker in ("funding", "builder", "official", "infra")) or topic.get("topic_type") in {"startup_tracking", "investment_framework"} else 0.58,
        "differentiation": 0.76 if topic.get("source_origin") == "openclaw" else 0.62,
    }
    configured = weights.get("dimensions") if isinstance(weights.get("dimensions"), dict) else {}
    total = 0.0
    for key, value in scores.items():
        weight = safe_float((configured.get(key) or {}).get("weight")) if isinstance(configured.get(key), dict) else 0.0
        total += value * weight
    scores["total"] = round(total, 4)
    return scores


def score_autonomous_topics(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    topics, warnings = collect_topic_inputs(paths)
    playbook = config(repo_root, "topic_scoring_playbook.yaml")
    thresholds = playbook.get("decision_thresholds") if isinstance(playbook.get("decision_thresholds"), dict) else {}
    scored: list[dict[str, Any]] = []
    for topic in topics:
        scores = score_topic(topic, playbook)
        weak_lane = str(topic.get("lane") or "") in WEAK_LANES
        missing = list(topic.get("missing_evidence") or [])
        if topic.get("can_enter_brief_pipeline") and scores["total"] >= safe_float(thresholds.get("main_candidate") or 0.68) and scores["evidence_strength"] >= 0.7 and not weak_lane:
            decision = "MAIN_CANDIDATE"
        elif topic.get("can_enter_brief_pipeline") and scores["total"] >= safe_float(thresholds.get("backup_candidate") or 0.56):
            decision = "BACKUP_CANDIDATE"
        elif missing or scores["evidence_strength"] < safe_float(thresholds.get("needs_evidence") or 0.42):
            decision = "NEEDS_EVIDENCE"
        elif activation := str(topic.get("activation_status") or ""):
            decision = "WATCH" if activation in {"WATCH", "NEEDS_EVIDENCE"} else "BACKUP_CANDIDATE"
        else:
            decision = "REJECT"
        scored.append(
            {
                "topic_id": topic.get("topic_id", ""),
                "title": topic.get("title", ""),
                "source_origin": topic.get("source_origin", ""),
                "score_total": scores["total"],
                "scores": {key: round(value, 4) for key, value in scores.items() if key != "total"},
                "decision": decision,
                "reason": compact_text(topic.get("core_angle") or topic.get("why_now") or "Scored by configured Phase32 playbook.", 220),
                "missing_evidence": missing,
                "recommended_angle": compact_text(topic.get("core_angle") or "Use this as a confirmed topic, then make evidence limitations explicit.", 220),
                "content_recipe": topic.get("content_recipe") or topic.get("topic_type") or "news_explainer",
                "evidence_ids": topic.get("evidence_ids") or [],
                "lane": topic.get("lane", ""),
                "evidence_strength": topic.get("evidence_strength", "UNKNOWN"),
            }
        )
    scored.sort(key=lambda item: safe_float(item.get("score_total")), reverse=True)
    summary = {
        "topic_count": len(scored),
        "main_candidates": sum(1 for item in scored if item["decision"] == "MAIN_CANDIDATE"),
        "backup_candidates": sum(1 for item in scored if item["decision"] == "BACKUP_CANDIDATE"),
        "needs_evidence": sum(1 for item in scored if item["decision"] == "NEEDS_EVIDENCE"),
        "watch": sum(1 for item in scored if item["decision"] == "WATCH"),
        "reject": sum(1 for item in scored if item["decision"] == "REJECT"),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "topics": scored, "summary": summary, "warnings": warnings, "policy": {"weak_signal_requires_confirmation": True}}
    root = paths.market_content_root / "03_topic_candidates"
    outputs = {"latest_json": root / "latest_autonomous_topic_scores.json", "latest_md": root / "latest_autonomous_topic_scores.md"}
    rows = [{"decision": t["decision"], "score": t["score_total"], "strength": t["evidence_strength"], "title": compact_text(t["title"], 68)} for t in scored[:30]]
    write_outputs(payload, summary_markdown("Autonomous Topic Scores", summary, rows, ("decision", "score", "strength", "title")), outputs, repo_root)
    return payload, outputs


def select_daily_main_topics(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    root = paths.market_content_root / "03_topic_candidates"
    scores_payload = read_json(root / "latest_autonomous_topic_scores.json")
    topics = list_payload(scores_payload, "topics")
    main = next((item for item in topics if item.get("decision") == "MAIN_CANDIDATE"), None)
    backups = [item for item in topics if item.get("decision") == "BACKUP_CANDIDATE"][:3]
    needs = [item for item in topics if item.get("decision") == "NEEDS_EVIDENCE"]
    selected = bool(main)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "SELECTED" if selected else "NO_QUALIFIED_TOPIC",
        "main_topic": {
            "topic_id": main.get("topic_id", "") if main else "",
            "title": main.get("title", "") if main else "",
            "reason": main.get("reason", "") if main else "No topic passed evidence and score thresholds.",
            "recommended_angle": main.get("recommended_angle", "") if main else "",
            "content_recipe": main.get("content_recipe", "") if main else "",
            "evidence_ids": main.get("evidence_ids", []) if main else [],
        },
        "backup_topics": backups,
        "rejected_topics": [item for item in topics if item.get("decision") == "REJECT"],
        "summary": {"selected": selected, "backup_count": len(backups), "needs_evidence_count": len(needs)},
        "policy": {"does_not_force_topic": True, "evidence_weak_topic_not_main": True},
    }
    outputs = {"latest_json": root / "latest_daily_main_topic_selection.json", "latest_md": root / "latest_daily_main_topic_selection.md"}
    rows = [{"role": "main", "title": payload["main_topic"]["title"], "selected": selected}] + [{"role": "backup", "title": b.get("title", ""), "selected": False} for b in backups]
    write_outputs(payload, summary_markdown("Daily Main Topic Selection", payload["summary"], rows, ("role", "selected", "title")), outputs, repo_root)
    return payload, outputs


def evidence_inventory_for(paths: ProjectPaths, evidence_ids: list[Any]) -> list[dict[str, Any]]:
    ids = {str(item) for item in evidence_ids if item}
    inventory: list[dict[str, Any]] = []
    for payload_path, list_name, id_key in (
        (paths.market_content_root / "03_topic_candidates" / "latest_openclaw_signal_evidence_backfill.json", "backfill_items", "backfill_id"),
        (paths.market_content_root / "03_topic_candidates" / "latest_connector_evidence_packets.json", "evidence_packets", "evidence_id"),
    ):
        payload = read_json(payload_path)
        for item in list_payload(payload, list_name):
            if str(item.get(id_key)) in ids:
                inventory.append(
                    {
                        "evidence_id": item.get(id_key, ""),
                        "title": item.get("title", ""),
                        "source_name": item.get("source_name", ""),
                        "url": item.get("url", ""),
                        "evidence_role": item.get("evidence_role") or item.get("source_authority") or "supporting_evidence",
                        "limitations": item.get("limitations") if isinstance(item.get("limitations"), list) else [],
                        "metadata_only": item.get("metadata_only", True),
                        "can_use_as_hard_evidence": item.get("can_use_as_hard_evidence", False),
                    }
                )
    return inventory


def build_autonomous_briefs(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    ensure_dirs(paths)
    selection = read_json(paths.market_content_root / "03_topic_candidates" / "latest_daily_main_topic_selection.json")
    topic = selection.get("main_topic") if isinstance(selection.get("main_topic"), dict) else {}
    briefs: list[dict[str, Any]] = []
    if selection.get("status") == "SELECTED" and topic.get("topic_id"):
        evidence = evidence_inventory_for(paths, topic.get("evidence_ids") if isinstance(topic.get("evidence_ids"), list) else [])
        ready = bool(evidence) and bool(topic.get("reason"))
        briefs.append(
            {
                "brief_id": stable_id("autobrief", topic.get("topic_id"), today_token()),
                "topic_id": topic.get("topic_id", ""),
                "title": topic.get("title", ""),
                "one_sentence_thesis": compact_text(topic.get("recommended_angle") or topic.get("reason"), 220),
                "why_now": compact_text(topic.get("reason"), 240),
                "core_reader_question": f"这件事为什么会改变对 {compact_text(topic.get('title'), 32)} 的判断？",
                "target_reader": "AI/Agent 产业与投资读者",
                "evidence_inventory": evidence,
                "narrative_angle": topic.get("recommended_angle", ""),
                "key_tension": "表面是新信号，真正要判断的是它是否改变产品、开发者或资本配置预期。",
                "counterarguments": ["当前证据仍以 metadata-derived supporting evidence 为主，需要人工复核一手来源。"],
                "writing_risks": ["不要把弱信号写成硬事实。", "不要写成新闻转述。", "不要给出目标价或投资建议。"],
                "recommended_structure": "hook -> core judgment -> evidence chain -> industry implication -> risk -> closing framework",
                "status": "READY_FOR_OUTLINE" if ready else "NEEDS_EVIDENCE",
            }
        )
    summary = {
        "brief_count": len(briefs),
        "ready_for_outline": sum(1 for item in briefs if item["status"] == "READY_FOR_OUTLINE"),
        "needs_evidence": sum(1 for item in briefs if item["status"] == "NEEDS_EVIDENCE"),
        "hold": sum(1 for item in briefs if item["status"] == "HOLD"),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "briefs": briefs, "summary": summary}
    root = paths.market_content_root / "05_briefs"
    outputs = {"latest_json": root / "latest_autonomous_briefs.json", "latest_md": root / "latest_autonomous_briefs.md"}
    write_outputs(payload, summary_markdown("Autonomous Briefs", summary), outputs, repo_root)
    return payload, outputs


def build_autonomous_outlines(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    ensure_dirs(paths)
    briefs_payload = read_json(paths.market_content_root / "05_briefs" / "latest_autonomous_briefs.json")
    outlines: list[dict[str, Any]] = []
    for brief in list_payload(briefs_payload, "briefs"):
        if brief.get("status") != "READY_FOR_OUTLINE":
            outlines.append({"outline_id": stable_id("autooutline", brief.get("brief_id")), "brief_id": brief.get("brief_id", ""), "topic_id": brief.get("topic_id", ""), "title_options": [], "opening_strategy": "", "sections": [], "ending_strategy": "", "status": "NEEDS_BRIEF_REPAIR"})
            continue
        evidence_ids = [item.get("evidence_id") for item in brief.get("evidence_inventory", []) if isinstance(item, dict) and item.get("evidence_id")]
        sections = [
            ("hook", "先抛出为什么今天这条信号不只是新闻。", [brief.get("key_tension", "")], [], brief.get("core_reader_question", ""), ""),
            ("core_judgment", "用一句话明确本文判断。", [brief.get("one_sentence_thesis", "")], evidence_ids[:1], "本文到底判断什么？", ""),
            ("evidence_chain", "把证据链与判断逐项对应。", [f"证据 {eid} 支撑的只是可审计线索，不是全文事实。" for eid in evidence_ids], evidence_ids, "证据能支撑到什么程度？", "metadata-derived evidence 需要人工复核。"),
            ("implication", "解释产业、产品或投资观察含义。", ["看它是否改变开发者、客户预算或资本关注点。"], evidence_ids[:1], "读者读完能做什么判断？", ""),
            ("risk_and_counterargument", "给出反方和可证伪条件。", brief.get("counterarguments", []), [], "什么情况会让本文判断不成立？", ""),
            ("closing_framework", "留下可复述的判断框架。", ["把这类信号放进：变化强度、证据强度、产业影响三格框架。"], [], "读者应该带走什么框架？", ""),
        ]
        outlines.append(
            {
                "outline_id": stable_id("autooutline", brief.get("brief_id"), today_token()),
                "brief_id": brief.get("brief_id", ""),
                "topic_id": brief.get("topic_id", ""),
                "title_options": [f"{brief.get('title')}：真正值得看的不是消息本身", f"为什么现在要重看：{brief.get('title')}", f"从一个信号看 AI/Agent 变化：{brief.get('title')}"],
                "opening_strategy": "question_first_with_judgment",
                "sections": [
                    {"section_id": sid, "heading": heading.replace("_", " ").title(), "purpose": purpose, "key_points": points, "evidence_ids": evs, "reader_question_answered": question, "risk": risk}
                    for sid, purpose, points, evs, question, risk in sections
                    for heading in [sid]
                ],
                "ending_strategy": "用一组三格判断框架收束，不做发布承诺或投资建议。",
                "status": "READY_FOR_DRAFT",
            }
        )
    summary = {"outline_count": len(outlines), "ready_for_draft": sum(1 for item in outlines if item["status"] == "READY_FOR_DRAFT"), "needs_brief_repair": sum(1 for item in outlines if item["status"] == "NEEDS_BRIEF_REPAIR"), "hold": sum(1 for item in outlines if item["status"] == "HOLD")}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "outlines": outlines, "summary": summary}
    root = paths.market_content_root / "06_outlines"
    outputs = {"latest_json": root / "latest_autonomous_outlines.json", "latest_md": root / "latest_autonomous_outlines.md"}
    write_outputs(payload, summary_markdown("Autonomous Outlines", summary), outputs, repo_root)
    return payload, outputs


def brief_index(paths: ProjectPaths) -> dict[str, dict[str, Any]]:
    payload = read_json(paths.market_content_root / "05_briefs" / "latest_autonomous_briefs.json")
    return {str(item.get("brief_id")): item for item in list_payload(payload, "briefs") if item.get("brief_id")}


def compose_article(outline: dict[str, Any], brief: dict[str, Any]) -> str:
    title = (outline.get("title_options") or [brief.get("title") or "自动候选稿"])[0]
    lines = [
        f"# {title}",
        "",
        f"这篇文章先回答一个问题：{brief.get('core_reader_question')}",
        "",
        f"我的初步判断是：{brief.get('one_sentence_thesis')}",
        "",
        "## 为什么现在写",
        brief.get("why_now") or "当前信号进入了可观察窗口，但仍需要人工复核证据边界。",
        "",
    ]
    for section in outline.get("sections", []):
        if not isinstance(section, dict):
            continue
        lines.extend([f"## {section.get('heading')}", section.get("purpose", "")])
        for point in section.get("key_points", [])[:3]:
            lines.append(f"- {point}")
        evs = section.get("evidence_ids") if isinstance(section.get("evidence_ids"), list) else []
        if evs:
            lines.append(f"- 证据线索：{', '.join(str(item) for item in evs)}")
        if section.get("risk"):
            lines.append(f"- 风险边界：{section.get('risk')}")
        lines.append("")
    lines.extend(
        [
            "## 反方与限制",
            "这仍是一份自动生成的候选稿，证据来自 metadata-derived sidecar。进入人工发布前，需要复核来源、时间、链接和上下文。",
            "",
            "## 结尾框架",
            "判断这类 AI/Agent 信号，不要只看热度，而要同时看三件事：变化是否真实、证据是否足够、它是否改变产业链里的行为。",
        ]
    )
    return "\n".join(line for line in lines if line is not None)


def write_autonomous_drafts(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    ensure_dirs(paths)
    outlines_payload = read_json(paths.market_content_root / "06_outlines" / "latest_autonomous_outlines.json")
    briefs = brief_index(paths)
    drafts: list[dict[str, Any]] = []
    for outline in list_payload(outlines_payload, "outlines"):
        brief = briefs.get(str(outline.get("brief_id")), {})
        if outline.get("status") != "READY_FOR_DRAFT":
            status = "NEEDS_OUTLINE_REPAIR"
            article = ""
        else:
            status = "READY_FOR_REVIEW"
            article = compose_article(outline, brief)
        drafts.append(
            {
                "draft_id": stable_id("autodraft", outline.get("outline_id"), today_token()),
                "outline_id": outline.get("outline_id", ""),
                "brief_id": outline.get("brief_id", ""),
                "topic_id": outline.get("topic_id", ""),
                "title": (outline.get("title_options") or [brief.get("title", "")])[0],
                "subtitle": "自动生成候选稿，需人工复核后才可使用",
                "article_markdown": article,
                "evidence_ids": sorted({str(eid) for section in outline.get("sections", []) if isinstance(section, dict) for eid in (section.get("evidence_ids") or []) if eid}),
                "style_flags": [phrase for phrase in DISCOURAGED_PHRASES if phrase in article],
                "known_weaknesses": ["metadata-derived evidence needs human source review", "final publication is blocked until manual review"],
                "status": status,
                "do_not_publish": True,
            }
        )
    summary = {"draft_count": len(drafts), "ready_for_review": sum(1 for item in drafts if item["status"] == "READY_FOR_REVIEW"), "needs_outline_repair": sum(1 for item in drafts if item["status"] == "NEEDS_OUTLINE_REPAIR"), "hold": sum(1 for item in drafts if item["status"] == "HOLD"), "do_not_publish_all_true": all(item.get("do_not_publish") is True for item in drafts)}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "drafts": drafts, "summary": summary}
    root = paths.market_content_root / "07_drafts"
    outputs = {"latest_json": root / "latest_autonomous_drafts.json", "latest_md": root / "latest_autonomous_drafts.md"}
    write_outputs(payload, summary_markdown("Autonomous Drafts", summary), outputs, repo_root)
    return payload, outputs


def run_article_review_pipeline(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    ensure_dirs(paths)
    drafts_payload = read_json(paths.market_content_root / "07_drafts" / "latest_autonomous_drafts.json")
    reviews: list[dict[str, Any]] = []
    rewrites: list[dict[str, Any]] = []
    for draft in list_payload(drafts_payload, "drafts"):
        if draft.get("status") != "READY_FOR_REVIEW":
            decision, quality_score, status = "HOLD", 0.0, "HELD"
        else:
            quality_score = 0.82 if draft.get("evidence_ids") else 0.58
            decision = "REVISE" if draft.get("known_weaknesses") else "ACCEPT"
            status = "REVISED" if decision == "REVISE" else "ACCEPTED"
        rewrite_id = stable_id("autorewrite", draft.get("draft_id"), today_token()) if decision in {"REVISE", "ACCEPT"} else ""
        if rewrite_id:
            rewritten = str(draft.get("article_markdown") or "") + "\n\n> 人工复核提醒：本稿由自动链路生成，证据与表述需要编辑确认后才能进入发布准备。"
            rewrites.append({"rewrite_version_id": rewrite_id, "draft_id": draft.get("draft_id", ""), "title": draft.get("title", ""), "article_markdown": rewritten, "do_not_publish": True, "overwrite_original": False})
        reviews.append(
            {
                "review_id": stable_id("autoreview", draft.get("draft_id"), today_token()),
                "draft_id": draft.get("draft_id", ""),
                "proponent": {"support_level": "MEDIUM" if quality_score >= 0.7 else "LOW", "strongest_points": ["有明确 why now", "保留证据边界"]},
                "critic": {"severity": "MEDIUM", "main_concerns": draft.get("known_weaknesses", []), "must_fix_before_publish": True},
                "judge": {"decision": decision, "reason": "Rule-based Phase32 judge; does not override gates.", "quality_score": quality_score},
                "rewrite": {"generated": bool(rewrite_id), "rewrite_version_id": rewrite_id},
                "status": status,
            }
        )
    summary = {"review_count": len(reviews), "accepted": sum(1 for item in reviews if item["status"] == "ACCEPTED"), "revised": sum(1 for item in reviews if item["status"] == "REVISED"), "held": sum(1 for item in reviews if item["status"] == "HELD"), "rejected": sum(1 for item in reviews if item["status"] == "REJECTED")}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "reviews": reviews, "summary": summary}
    rewrite_payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "versions": rewrites, "summary": {"rewrite_count": len(rewrites), "do_not_publish_all_true": all(item.get("do_not_publish") is True for item in rewrites), "overwrite_original_count": sum(1 for item in rewrites if item.get("overwrite_original"))}}
    root = paths.market_content_root / "07_drafts"
    outputs = {
        "reviews_json": root / "latest_autonomous_article_reviews.json",
        "rewrites_json": root / "latest_autonomous_article_rewrite_versions.json",
        "summary_md": root / "latest_autonomous_article_review_summary.md",
    }
    outputs["reviews_json"].parent.mkdir(parents=True, exist_ok=True)
    outputs["reviews_json"].write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    outputs["rewrites_json"].write_text(json.dumps(rewrite_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    outputs["summary_md"].write_text(summary_markdown("Autonomous Article Review", summary), encoding="utf-8")
    payload["rewrite_summary"] = rewrite_payload["summary"]
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def build_final_candidates(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    ensure_dirs(paths)
    drafts_payload = read_json(paths.market_content_root / "07_drafts" / "latest_autonomous_drafts.json")
    reviews_payload = read_json(paths.market_content_root / "07_drafts" / "latest_autonomous_article_reviews.json")
    rewrites_payload = read_json(paths.market_content_root / "07_drafts" / "latest_autonomous_article_rewrite_versions.json")
    drafts = {str(item.get("draft_id")): item for item in list_payload(drafts_payload, "drafts") if item.get("draft_id")}
    rewrites = {str(item.get("draft_id")): item for item in list_payload(rewrites_payload, "versions") if item.get("draft_id")}
    candidates: list[dict[str, Any]] = []
    for review in list_payload(reviews_payload, "reviews"):
        if review.get("status") not in {"ACCEPTED", "REVISED"}:
            continue
        draft = drafts.get(str(review.get("draft_id")), {})
        rewrite = rewrites.get(str(review.get("draft_id")), {})
        article = rewrite.get("article_markdown") or draft.get("article_markdown") or ""
        candidates.append(
            {
                "candidate_id": stable_id("autofinal", review.get("review_id"), review.get("draft_id")),
                "topic_id": draft.get("topic_id", ""),
                "draft_id": draft.get("draft_id", ""),
                "rewrite_version_id": rewrite.get("rewrite_version_id", ""),
                "title": rewrite.get("title") or draft.get("title", ""),
                "article_markdown": article,
                "quality_summary": f"Judge {review.get('judge', {}).get('decision')} score {review.get('judge', {}).get('quality_score')}",
                "evidence_summary": f"{len(draft.get('evidence_ids') or [])} evidence ids; metadata-derived evidence requires human review.",
                "visual_plan_required": True,
                "manual_review_required": True,
                "do_not_publish": True,
                "status": "READY_FOR_HUMAN_REVIEW" if review.get("status") in {"ACCEPTED", "REVISED"} else "HOLD",
            }
        )
    summary = {"candidate_count": len(candidates), "ready_for_human_review": sum(1 for item in candidates if item["status"] == "READY_FOR_HUMAN_REVIEW"), "needs_revision": sum(1 for item in candidates if item["status"] == "NEEDS_REVISION"), "hold": sum(1 for item in candidates if item["status"] == "HOLD")}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "final_candidates": candidates, "summary": summary}
    root = paths.market_content_root / "08_final_candidates"
    outputs = {"latest_json": root / "latest_autonomous_final_candidates.json", "latest_md": root / "latest_autonomous_final_candidates.md"}
    write_outputs(payload, summary_markdown("Autonomous Final Candidates", summary), outputs, repo_root)
    return payload, outputs


def run_quality_regression(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    final_payload = read_json(paths.market_content_root / "08_final_candidates" / "latest_autonomous_final_candidates.json")
    candidates = list_payload(final_payload, "final_candidates")
    checks: list[dict[str, Any]] = []
    article_text = "\n".join(str(item.get("article_markdown") or "") for item in candidates)
    title_text = "\n".join(str(item.get("title") or "") for item in candidates)
    def add(check_id: str, ok: bool, message: str, warn: bool = False) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if ok else ("WARN" if warn else "FAIL"), "message": message})
    add("has_final_candidate", bool(candidates), "At least one final candidate exists.", warn=True)
    add("has_why_now", "为什么现在" in article_text, "Draft includes why-now section.", warn=True)
    add("has_reader_question", "问题" in article_text[:300], "Opening includes reader question.", warn=True)
    add("has_core_judgment", "初步判断" in article_text or "核心判断" in article_text, "Draft includes core judgment.", warn=True)
    add("has_story_line", article_text.count("## ") >= 5, "Draft has sectioned story line.", warn=True)
    add("has_evidence_chain", "证据线索" in article_text or "evidence" in article_text.lower(), "Draft includes evidence chain.", warn=True)
    add("has_limits", "限制" in article_text or "风险边界" in article_text, "Draft includes limits/counterarguments.", warn=True)
    add("avoid_generic_ai_taste", not any(phrase in article_text for phrase in DISCOURAGED_PHRASES), "Draft avoids discouraged generic phrases.", warn=True)
    add("title_is_specific", bool(title_text.strip()) and len(title_text.strip()) >= 8, "Title is non-empty and specific.", warn=True)
    add("opening_has_pull", bool(article_text.strip()[:180]), "Opening has content.", warn=True)
    add("industry_judgment", "产业" in article_text or "投资" in article_text or "开发者" in article_text, "Draft keeps industry/investment judgment.", warn=True)
    add("no_target_price", not any(pattern in article_text.lower() for pattern in BANNED_DRAFT_PATTERNS), "No target price or rating language.")
    add("no_fake_citations", "据某媒体" not in article_text and "匿名人士" not in article_text, "No fabricated anonymous citation pattern.")
    fail = sum(1 for item in checks if item["status"] == "FAIL")
    warn = sum(1 for item in checks if item["status"] == "WARN")
    summary = {"check_count": len(checks), "pass": sum(1 for item in checks if item["status"] == "PASS"), "warn": warn, "fail": fail, "blocking_failures": fail}
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "regression_status": "PASS" if fail == 0 and warn == 0 else ("ACTIONABLE" if fail == 0 else "FAIL"), "checks": checks, "summary": summary}
    outputs = {"latest_json": paths.logs_root / "latest_legacy_vs_new_quality_regression.json", "latest_md": paths.logs_root / "latest_legacy_vs_new_quality_regression.md"}
    write_outputs(payload, summary_markdown("Legacy vs New Quality Regression", summary, checks, ("check_id", "status", "message")), outputs, repo_root)
    return payload, outputs


def run_topic_to_article_pipeline(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    steps: list[dict[str, Any]] = []
    functions = [
        ("autonomous_topic_score", score_autonomous_topics),
        ("daily_main_topic_selection", select_daily_main_topics),
        ("autonomous_briefs", build_autonomous_briefs),
        ("autonomous_outlines", build_autonomous_outlines),
        ("autonomous_drafts", write_autonomous_drafts),
        ("autonomous_article_review", run_article_review_pipeline),
        ("autonomous_final_candidates", build_final_candidates),
        ("legacy_vs_new_quality_regression", run_quality_regression),
    ]
    status = "SUCCESS"
    for name, func in functions:
        try:
            payload, _ = func(paths, repo_root)
            step_status = payload.get("status") or payload.get("regression_status") or payload.get("validate_status") or "OK"
            steps.append({"step": name, "status": step_status, "summary": payload.get("summary", {})})
        except Exception as exc:  # pragma: no cover - defensive pipeline guard
            status = "ACTIONABLE"
            steps.append({"step": name, "status": "FAILED", "error": str(exc)})
            break
    final_payload = read_json(paths.market_content_root / "08_final_candidates" / "latest_autonomous_final_candidates.json")
    selection = read_json(paths.market_content_root / "03_topic_candidates" / "latest_daily_main_topic_selection.json")
    candidate_count = int((final_payload.get("summary") or {}).get("candidate_count") or 0) if isinstance(final_payload.get("summary"), dict) else 0
    if selection.get("status") == "NO_QUALIFIED_TOPIC":
        status = "SUCCESS_EMPTY"
    elif candidate_count == 0 and status == "SUCCESS":
        status = "ACTIONABLE_EMPTY"
    summary = {
        "step_count": len(steps),
        "steps_ok": sum(1 for item in steps if item.get("status") not in {"FAILED", "FAIL"}),
        "selected_topic": (selection.get("main_topic") or {}).get("title") if isinstance(selection.get("main_topic"), dict) else "",
        "final_candidate_count": candidate_count,
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": today_token(), "status": status, "steps": steps, "summary": summary, "policy": {"do_not_publish": True, "no_wechat_api": True, "no_image_generation": True, "cost_guard_not_bypassed": True}}
    outputs = {"latest_json": paths.logs_root / "latest_autonomous_topic_to_article.json", "latest_md": paths.logs_root / "latest_autonomous_topic_to_article.md"}
    write_outputs(payload, summary_markdown("Autonomous Topic-to-Article Pipeline", summary), outputs, repo_root)
    return payload, outputs

