"""End-to-end daily pipeline graph for autonomous orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import PipelineStep, python_command, repo_relative, run_step, today_token, utc_now, write_json_and_markdown


def pipeline_nodes() -> list[dict[str, Any]]:
    return [
        {"node_id": "runtime_preflight", "type": "required", "command": python_command("scripts/validate_runtime_config.py"), "depends_on": []},
        {"node_id": "network_readiness", "type": "degradable", "command": python_command("scripts/check_runtime_network_readiness.py"), "depends_on": ["runtime_preflight"]},
        {"node_id": "morning_acquisition", "type": "degradable", "command": python_command("scripts/run_phase29_daily_migration_pipeline.py"), "depends_on": ["network_readiness"]},
        {"node_id": "hot_material_refresh", "type": "degradable", "command": python_command("scripts/build_daily_hot_material_pool.py"), "depends_on": ["morning_acquisition"]},
        {"node_id": "evidence_enrichment", "type": "degradable", "command": python_command("scripts/run_phase30_daily_activation_pipeline.py"), "depends_on": ["hot_material_refresh"]},
        {"node_id": "topic_activation", "type": "required", "command": python_command("scripts/activate_openclaw_migrated_topics.py"), "depends_on": ["evidence_enrichment"]},
        {"node_id": "methodology_topic_score", "type": "required", "command": python_command("scripts/score_topics_with_methodology.py"), "depends_on": ["topic_activation"]},
        {"node_id": "topic_selection", "type": "required", "command": python_command("scripts/build_high_value_candidate_pool.py"), "depends_on": ["methodology_topic_score"]},
        {"node_id": "brief_generation", "type": "required", "command": python_command("scripts/build_methodology_briefs.py"), "depends_on": ["topic_selection"]},
        {"node_id": "outline_generation", "type": "required", "command": python_command("scripts/build_methodology_outlines.py"), "depends_on": ["brief_generation"]},
        {"node_id": "draft_generation", "type": "required", "command": python_command("scripts/build_methodology_drafts.py"), "depends_on": ["outline_generation"]},
        {"node_id": "agent_review", "type": "required", "command": python_command("scripts/run_phase3_daily_pipeline.py"), "depends_on": ["draft_generation"]},
        {"node_id": "article_quality_review", "type": "required", "command": python_command("scripts/review_content_quality.py"), "depends_on": ["agent_review"]},
        {"node_id": "visual_plan", "type": "optional", "command": python_command("scripts/build_visual_plans.py"), "depends_on": ["article_quality_review"]},
        {"node_id": "final_candidate", "type": "required", "command": python_command("scripts/build_final_article_candidates.py"), "depends_on": ["article_quality_review"]},
        {"node_id": "workbench_build", "type": "required", "command": python_command("scripts/build_wechat_workbench_frontend.py"), "depends_on": ["final_candidate"]},
        {"node_id": "daily_closeout", "type": "required", "command": python_command("scripts/run_stable_daily_ops.py"), "depends_on": ["workbench_build"]},
    ]


def build_daily_pipeline_graph_payload() -> dict[str, Any]:
    nodes = pipeline_nodes()
    return {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "nodes": nodes,
        "summary": {
            "node_count": len(nodes),
            "required": sum(1 for node in nodes if node["type"] == "required"),
            "optional": sum(1 for node in nodes if node["type"] == "optional"),
            "degradable": sum(1 for node in nodes if node["type"] == "degradable"),
            "manual_gate": sum(1 for node in nodes if node["type"] == "manual_gate"),
        },
        "boundaries": {
            "no_auto_publish": True,
            "no_wechat_api": True,
            "no_image_generation": True,
        },
    }


def build_daily_pipeline_graph(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    payload = build_daily_pipeline_graph_payload()
    outputs = {
        "latest_json": paths.logs_root / "latest_daily_pipeline_graph.json",
        "latest_md": paths.logs_root / "latest_daily_pipeline_graph.md",
    }
    write_json_and_markdown(payload, render_graph_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def run_daily_end_to_end(paths: ProjectPaths, repo_root: Path, execute: bool = False) -> tuple[dict[str, Any], dict[str, Path]]:
    graph = build_daily_pipeline_graph_payload()
    steps: list[PipelineStep] = []
    safe_execute_nodes = {"runtime_preflight", "network_readiness", "workbench_build", "daily_closeout"}
    for node in graph["nodes"]:
        should_execute = execute and node["node_id"] in safe_execute_nodes
        steps.append(run_step(str(node["node_id"]), list(node["command"]), repo_root, dry_run=not should_execute))
    failed_required = [step for step, node in zip(steps, graph["nodes"]) if step.returncode != 0 and node["type"] == "required"]
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": today_token(),
        "status": "SUCCESS" if not failed_required else "ACTIONABLE",
        "execution_mode": "execute_safe_nodes" if execute else "dry_run",
        "graph_summary": graph["summary"],
        "steps": [step.__dict__ for step in steps],
        "summary": {
            "step_count": len(steps),
            "ok": sum(1 for step in steps if step.returncode == 0),
            "warn": sum(1 for step in steps if step.status == "SKIPPED_DRY_RUN"),
            "failed": sum(1 for step in steps if step.returncode != 0),
        },
    }
    outputs = {
        "dated_json": paths.logs_root / f"{payload['run_date']}__daily-end-to-end-run.json",
        "dated_md": paths.logs_root / f"{payload['run_date']}__daily-end-to-end-run.md",
        "latest_json": paths.logs_root / "latest_daily_end_to_end_run.json",
        "latest_md": paths.logs_root / "latest_daily_end_to_end_run.md",
    }
    write_json_and_markdown(payload, render_run_markdown(payload), outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_graph_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(f"- `{node.get('node_id')}` {node.get('type')} depends_on={node.get('depends_on')}" for node in payload.get("nodes", []))
    return f"""# Daily Pipeline Graph

{rows}
"""


def render_run_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Daily End-to-End Run

- status: `{payload.get('status')}`
- execution_mode: `{payload.get('execution_mode')}`
- step_count: `{summary.get('step_count', 0)}`
- ok: `{summary.get('ok', 0)}`
- warn: `{summary.get('warn', 0)}`
- failed: `{summary.get('failed', 0)}`
"""
