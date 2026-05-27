#!/usr/bin/env python3
"""Serve the static WeChat workbench on localhost."""

from __future__ import annotations

import argparse
import functools
import http.server
import socketserver
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve WeChat workbench static files.")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    paths = get_project_paths(REPO_ROOT)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(paths.frontstage_root))
    with socketserver.TCPServer(("127.0.0.1", args.port), handler) as httpd:
        print(f"Serving WeChat workbench at http://127.0.0.1:{args.port}/latest_wechat_workbench.html")
        httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
