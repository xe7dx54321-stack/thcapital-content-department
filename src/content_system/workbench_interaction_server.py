"""Local-only HTTP server for workbench interactions."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from content_system.chief_editor_agent import run_chief_editor_agent
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json
from content_system.runtime_control import run_named, runtime_status, set_pause
from content_system.workbench_action_approval import update_action_approval
from content_system.workbench_action_router import route_workbench_actions


HOST = "127.0.0.1"
DEFAULT_PORT = 8766


class WorkbenchInteractionHandler(BaseHTTPRequestHandler):
    paths: ProjectPaths
    repo_root: Path

    def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else ""
        if not raw:
            return {}
        try:
            payload = json.loads(raw)
            return payload if isinstance(payload, dict) else {}
        except json.JSONDecodeError:
            return {key: values[-1] for key, values in parse_qs(raw).items()}

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json({"status": "OK", "host": HOST, "policy": "local_only_no_publish"})
            return
        if parsed.path == "/actions":
            root = self.paths.market_content_root / "09_workbench_actions"
            self._send_json(
                {
                    "pending": read_json(root / "latest_pending_actions.json"),
                    "approved": read_json(root / "latest_approved_actions.json"),
                }
            )
            return
        if parsed.path == "/runtime/status":
            self._send_json(runtime_status(self.paths))
            return
        self._send_json({"error": "not_found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        body = self._read_body()
        try:
            if parsed.path == "/chief-editor":
                message = str(body.get("message") or "")
                result, response = run_chief_editor_agent(self.paths, self.repo_root, message)
                router_result, pending = route_workbench_actions(self.paths, self.repo_root)
                self._send_json({"status": "OK", "chief_editor": response, "pending_actions": pending, "message_id": result.message_id, "action_count": router_result.action_count})
                return
            action_id = str(body.get("action_id") or "")
            note = str(body.get("note") or "")
            if parsed.path.startswith("/actions/"):
                parts = [part for part in parsed.path.split("/") if part]
                if len(parts) == 3:
                    action_id = parts[1]
                    parsed_action = parts[2]
                    if parsed_action in {"approve", "reject", "defer"}:
                        status = {"approve": "APPROVED", "reject": "REJECTED", "defer": "DEFERRED"}[parsed_action]
                        result, payload, changed = update_action_approval(self.paths, self.repo_root, action_id, status, note)
                        self._send_json({"status": "OK" if changed else "NOT_FOUND", "result": result.__dict__, "approval": payload})
                        return
            mapping = {"/approve-action": "APPROVED", "/reject-action": "REJECTED", "/defer-action": "DEFERRED"}
            if parsed.path in mapping:
                result, payload, changed = update_action_approval(self.paths, self.repo_root, action_id, mapping[parsed.path], note)
                self._send_json({"status": "OK" if changed else "NOT_FOUND", "result": result.__dict__, "approval": payload})
                return
            runtime_mapping = {
                "/runtime/pause": lambda: set_pause(self.paths, True),
                "/runtime/resume": lambda: set_pause(self.paths, False),
                "/runtime/run-daily": lambda: run_named(self.repo_root, "daily-end-to-end"),
                "/runtime/run-validation": lambda: run_named(self.repo_root, "safe-validation"),
                "/runtime/retry-failed": lambda: run_named(self.repo_root, "retry-summary"),
            }
            if parsed.path in runtime_mapping:
                self._send_json({"status": "OK", "runtime": runtime_mapping[parsed.path]()})
                return
        except Exception as exc:  # noqa: BLE001
            self._send_json({"status": "FAILED", "error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        self._send_json({"error": "not_found"}, HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        print(f"127.0.0.1 - {format % args}")


def make_server(paths: ProjectPaths, repo_root: Path, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    class BoundHandler(WorkbenchInteractionHandler):
        pass

    BoundHandler.paths = paths
    BoundHandler.repo_root = repo_root
    return ThreadingHTTPServer((HOST, port), BoundHandler)
