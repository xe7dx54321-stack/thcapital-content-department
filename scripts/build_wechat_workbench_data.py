#!/usr/bin/env python3
"""Build data for the local WeChat workbench."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.wechat_workbench_data import build_wechat_workbench_data, report_to_dict, write_wechat_workbench_data  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build WeChat workbench data.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    report = build_wechat_workbench_data(paths)
    written = write_wechat_workbench_data(report, paths, REPO_ROOT)
    if args.json:
        print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        print("WeChat Workbench Data")
        print("=====================")
        print(f"topics: {report.summary.get('topic_count')}")
        print(f"articles: {report.summary.get('article_count')}")
        print(f"ready_count: {report.summary.get('ready_count')}")
        print(f"selected_article_id: {report.selected_article_id}")
        for key, path in written.items():
            print(f"{key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
