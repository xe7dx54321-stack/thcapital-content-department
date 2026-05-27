#!/usr/bin/env python3
"""Sync the runtime store and write an artifact repository summary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.artifact_repository import repository_summary  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402
from content_system.phase7_report_utils import repo_relative, today_token, utc_now, write_json_and_markdown  # noqa: E402
from content_system.runtime_store import sync_runtime_store  # noqa: E402


def output_paths(run_date: str) -> dict[str, Path]:
    paths = get_project_paths(REPO_ROOT)
    return {
        "dated_json": paths.logs_root / f"{run_date}__artifact-repository-summary.json",
        "dated_md": paths.logs_root / f"{run_date}__artifact-repository-summary.md",
        "latest_json": paths.logs_root / "latest_artifact_repository_summary.json",
        "latest_md": paths.logs_root / "latest_artifact_repository_summary.md",
    }


def render_markdown(payload: dict[str, object]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    recent = summary.get("recent_artifacts") if isinstance(summary.get("recent_artifacts"), list) else []
    agents = summary.get("recent_agent_runs") if isinstance(summary.get("recent_agent_runs"), list) else []
    candidates = summary.get("publishing_candidates") if isinstance(summary.get("publishing_candidates"), list) else []
    artifact_rows = "\n".join(
        f"| {item.get('artifact_type')} | {item.get('title') or item.get('artifact_id')} | {item.get('status')} |"
        for item in recent[:10]
    ) or "| - | - | - |"
    agent_rows = "\n".join(
        f"| {item.get('agent_name')} | {item.get('provider_id')} | {item.get('mode')} | {item.get('status')} |"
        for item in agents[:10]
    ) or "| - | - | - | - |"
    candidate_rows = "\n".join(
        f"| {item.get('publishing_candidate_id')} | {item.get('publish_status')} | {item.get('publish_priority')} |"
        for item in candidates[:10]
    ) or "| - | - | - |"
    return f"""# Artifact Repository Summary

## Summary

- Generated at: `{payload.get('generated_at')}`
- Run date: `{payload.get('run_date')}`
- Status: **{payload.get('status')}**
- Recent artifacts: `{len(recent)}`
- Recent agent runs: `{len(agents)}`
- Publishing candidates: `{len(candidates)}`

## Recent Artifacts

| Type | Title | Status |
|---|---|---|
{artifact_rows}

## Recent Agent Runs

| Agent | Provider | Mode | Status |
|---|---|---|---|
{agent_rows}

## Publishing Candidates

| Candidate | Status | Priority |
|---|---|---|
{candidate_rows}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync artifact repository summary from runtime store.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    sync_report = sync_runtime_store(paths, REPO_ROOT)
    run_date = today_token()
    summary = repository_summary(paths)
    payload = {
        "schema_version": "v1",
        "generated_at": utc_now(),
        "run_date": run_date,
        "status": sync_report.status,
        "sync_summary": sync_report.summary,
        "summary": summary,
    }
    outputs = output_paths(run_date)
    written = write_json_and_markdown(payload, render_markdown(payload), outputs)
    if args.json:
        print(json.dumps({**payload, "outputs": {key: repo_relative(path, REPO_ROOT) for key, path in written.items()}}, ensure_ascii=False, indent=2))
    else:
        print("Artifact Repository Summary")
        print("===========================")
        print(f"status: {payload['status']}")
        print(f"recent_artifacts: {len(summary['recent_artifacts'])}")
        print(f"recent_agent_runs: {len(summary['recent_agent_runs'])}")
        print(f"publishing_candidates: {len(summary['publishing_candidates'])}")
        for key, path in written.items():
            print(f"{key}: {path}")
    return 0 if sync_report.status != "FAILED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
