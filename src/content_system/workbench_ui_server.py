"""Local-only WeChat workbench UI server v2."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from content_system.chief_editor_agent import run_chief_editor_agent
from content_system.final_review_actions import record_final_review_action
from content_system.manual_publish_session import update_manual_publish_session
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json
from content_system.post_publish_metrics import record_post_publish_metrics
from content_system.version_acceptance import update_version_review
from content_system.workbench_action_approval import update_action_approval
from content_system.workbench_action_router import route_workbench_actions


HOST = "127.0.0.1"
DEFAULT_PORT = 8767


def optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def optional_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


class WorkbenchUIServerHandler(BaseHTTPRequestHandler):
    paths: ProjectPaths
    repo_root: Path

    def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, text: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = text.encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "text/html; charset=utf-8")
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

    def _publishing_json(self, filename: str) -> dict[str, Any]:
        return read_json(self.paths.market_content_root / "07_publishing" / filename)

    def _versions_json(self, filename: str) -> dict[str, Any]:
        return read_json(self.paths.market_content_root / "09_workbench_actions" / "versions" / filename)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            html_path = self.paths.frontstage_root / "latest_wechat_workbench.html"
            if html_path.exists():
                self._send_html(html_path.read_text(encoding="utf-8"))
            else:
                self._send_html("<h1>Workbench not built</h1><p>Run make wechat-workbench.</p>", HTTPStatus.NOT_FOUND)
            return
        if parsed.path == "/health":
            self._send_json({"status": "OK", "host": HOST, "policy": "local_only_no_publish_no_credentials"})
            return
        api_map = {
            "/api/workbench-data": self.paths.frontstage_root / "latest_wechat_workbench_data.json",
            "/api/final-candidates": self.paths.market_content_root / "07_publishing" / "latest_final_article_candidates.json",
            "/api/final-checklist": self.paths.market_content_root / "07_publishing" / "latest_final_publish_checklist.json",
            "/api/version-review": self.paths.market_content_root / "09_workbench_actions" / "versions" / "latest_version_review_decisions.json",
            "/api/pending-actions": self.paths.market_content_root / "09_workbench_actions" / "latest_pending_actions.json",
            "/api/manual-publish-sessions": self.paths.market_content_root / "07_publishing" / "latest_manual_publish_sessions.json",
            "/api/post-publish-metrics": self.paths.market_content_root / "07_publishing" / "latest_post_publish_metrics.json",
            "/api/performance-memory": self.paths.market_content_root / "07_publishing" / "content_performance_memory.json",
            "/api/performance-feedback": self.paths.logs_root / "latest_performance_learning_feedback.json",
        }
        if parsed.path in api_map:
            self._send_json(read_json(api_map[parsed.path]))
            return
        self._send_json({"error": "not_found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        body = self._read_body()
        try:
            if parsed.path == "/api/chief-editor":
                message = str(body.get("message") or "")
                result, response = run_chief_editor_agent(self.paths, self.repo_root, message)
                router_result, pending = route_workbench_actions(self.paths, self.repo_root)
                self._send_json({"status": "OK", "message_id": result.message_id, "chief_editor": response, "pending_actions": pending, "action_count": router_result.action_count})
                return
            if parsed.path in {"/api/actions/approve", "/api/actions/reject", "/api/actions/defer"}:
                status = {"/api/actions/approve": "APPROVED", "/api/actions/reject": "REJECTED", "/api/actions/defer": "DEFERRED"}[parsed.path]
                result, payload, changed = update_action_approval(self.paths, self.repo_root, str(body.get("action_id") or ""), status, str(body.get("note") or ""))
                self._send_json({"status": "OK" if changed else "NOT_FOUND", "result": result.__dict__, "payload": payload})
                return
            if parsed.path in {"/api/versions/accept", "/api/versions/reject", "/api/versions/revise-more"}:
                decision = {"/api/versions/accept": "ACCEPT", "/api/versions/reject": "REJECT", "/api/versions/revise-more": "REVISE_MORE"}[parsed.path]
                result, payload, changed = update_version_review(self.paths, self.repo_root, str(body.get("version_id") or ""), decision, body.get("score"), str(body.get("note") or ""))
                self._send_json({"status": "OK" if changed else "NOT_FOUND", "result": result.__dict__, "payload": payload})
                return
            if parsed.path in {"/api/final-review/mark-ready", "/api/final-review/mark-needs-edit", "/api/final-review/mark-hold"}:
                action = {"/api/final-review/mark-ready": "MARK_READY", "/api/final-review/mark-needs-edit": "MARK_NEEDS_EDIT", "/api/final-review/mark-hold": "MARK_HOLD"}[parsed.path]
                result, payload, changed = record_final_review_action(self.paths, self.repo_root, str(body.get("final_candidate_id") or ""), action, str(body.get("note") or ""))
                self._send_json({"status": "OK" if changed else "NOT_CHANGED", "result": result.__dict__, "payload": payload})
                return
            if parsed.path == "/api/publish-session/create":
                result, payload, changed = update_manual_publish_session(
                    self.paths,
                    self.repo_root,
                    str(body.get("final_candidate_id") or ""),
                    "",
                    "",
                    "",
                    str(body.get("note") or ""),
                    str(body.get("planned_publish_at") or ""),
                )
                self._send_json({"status": "OK" if changed else "NOT_CHANGED", "result": result.__dict__, "payload": payload})
                return
            if parsed.path == "/api/publish-session/mark-published":
                result, payload, changed = update_manual_publish_session(
                    self.paths,
                    self.repo_root,
                    "",
                    str(body.get("publish_session_id") or ""),
                    "MANUALLY_PUBLISHED",
                    str(body.get("url") or ""),
                    str(body.get("note") or ""),
                )
                self._send_json({"status": "OK" if changed else "NOT_FOUND", "result": result.__dict__, "payload": payload})
                return
            if parsed.path == "/api/performance-metrics/save":
                result, payload, changed = record_post_publish_metrics(
                    self.paths,
                    self.repo_root,
                    str(body.get("publish_session_id") or ""),
                    optional_int(body.get("views")),
                    optional_int(body.get("likes")),
                    optional_int(body.get("wows")),
                    optional_int(body.get("shares")),
                    optional_int(body.get("saves")),
                    optional_int(body.get("comments")),
                    optional_int(body.get("new_followers")),
                    str(body.get("note") or ""),
                    str(body.get("metric_time") or ""),
                    optional_float(body.get("hours_after_publish")),
                )
                self._send_json({"status": "OK" if changed else "NOT_CHANGED", "result": result.__dict__, "payload": payload})
                return
        except Exception as exc:  # noqa: BLE001
            self._send_json({"status": "FAILED", "error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        self._send_json({"error": "not_found"}, HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        print(f"{HOST} - {format % args}")


def make_server(paths: ProjectPaths, repo_root: Path, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    class BoundHandler(WorkbenchUIServerHandler):
        pass

    BoundHandler.paths = paths
    BoundHandler.repo_root = repo_root
    return ThreadingHTTPServer((HOST, port), BoundHandler)
