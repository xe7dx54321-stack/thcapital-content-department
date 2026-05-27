#!/usr/bin/env python3
"""Build the local WeChat workbench HTML."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.wechat_workbench_frontend import build_wechat_workbench_frontend  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build WeChat workbench HTML.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = build_wechat_workbench_frontend(get_project_paths(REPO_ROOT), REPO_ROOT)
    payload = asdict(result)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("WeChat Workbench")
        print("================")
        print(f"selected_article_id: {result.selected_article_id}")
        print(f"html: {result.html_path}")
        print(f"latest: {result.latest_html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
