#!/usr/bin/env python3
"""Serve the local WeChat workbench UI and safe API endpoints."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.workbench_ui_server import DEFAULT_PORT, HOST, make_server  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the local Workbench operator console.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    server = make_server(get_project_paths(REPO_ROOT), REPO_ROOT, args.port)
    print(f"Serving workbench UI at http://{HOST}:{args.port}")
    print("Policy: local only, no publish, no WeChat API, no credentials.")
    print("Runtime control stays local and must respect idempotency, cost, and safety gates.")
    print("Default view: 今日总览 / 今日稿件 / 质量检查 / 历史回放 / 系统运维.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping workbench UI server.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
