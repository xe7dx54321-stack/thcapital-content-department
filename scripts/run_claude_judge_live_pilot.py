#!/usr/bin/env python3
"""Run the Claude live pilot readiness check for llm_judge_agent."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.live_pilot_report import run_pilot  # noqa: E402
from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Claude live pilot for llm_judge_agent.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    parser.add_argument("--dry-run-check", action="store_true", help="Only print readiness checks; do not attempt live.")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    return run_pilot(
        repo_root=REPO_ROOT,
        title="Claude Judge Live Pilot",
        slug="claude-judge-live-pilot",
        agent_name="llm_judge_agent",
        provider_id="anthropic",
        provider_label="Anthropic Claude",
        api_key_env="ANTHROPIC_API_KEY",
        adapter_type="anthropic_messages",
        runner_script="scripts/run_llm_judge_gate.py",
        artifact_path=paths.market_content_root / "06_review_queue" / "latest_llm_judge_gate.json",
        list_key="decisions",
        dry_run_check=args.dry_run_check,
        as_json=args.json,
    )


if __name__ == "__main__":
    raise SystemExit(main())
