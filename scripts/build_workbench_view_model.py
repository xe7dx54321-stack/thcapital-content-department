#!/usr/bin/env python3
"""Build the clean Workbench view model used by the Phase 33B UI."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.workbench_view_model import build_workbench_view_model, write_workbench_view_model  # noqa: E402


def main() -> int:
    paths = get_project_paths(REPO_ROOT)
    view_model = build_workbench_view_model(paths)
    outputs = write_workbench_view_model(view_model, paths, REPO_ROOT)
    overview = view_model.get("today_overview", {})
    quality = view_model.get("quality_check", {})
    replay = view_model.get("replay_dashboard", {}).get("summary", {})
    print("Workbench View Model")
    print("====================")
    print(f"overall_status: {overview.get('overall_status')}")
    print(f"candidate_status: {overview.get('candidate_status')}")
    print(f"quality_status: {overview.get('quality_status')}")
    print(f"main_topic: {overview.get('main_topic')}")
    print(f"quality_blocking_issues: {quality.get('blocking_issue_count')}")
    print(f"replay_selected_days: {replay.get('selected_days')}")
    print(f"latest: {outputs['latest_json']}")
    print(json.dumps({"outputs": {key: str(path) for key, path in outputs.items()}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
