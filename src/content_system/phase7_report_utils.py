"""Small shared helpers for Phase 7 reports."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PipelineStep:
    name: str
    command: str
    returncode: int
    status: str
    started_at: str
    finished_at: str
    stdout_tail: str
    stderr_tail: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def list_payload(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    raw = payload.get(key)
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def tail_text(text: str, repo_root: Path, max_lines: int = 20) -> str:
    sanitized = text.replace(str(repo_root), "<repo_root>")
    lines = sanitized.strip().splitlines()
    return "\n".join(lines[-max_lines:])


def run_step(name: str, command: list[str], repo_root: Path, dry_run: bool = False) -> PipelineStep:
    started_at = utc_now()
    if dry_run:
        finished_at = utc_now()
        return PipelineStep(name, " ".join(command), 0, "SKIPPED_DRY_RUN", started_at, finished_at, "", "")
    completed = subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
    finished_at = utc_now()
    return PipelineStep(
        name=name,
        command=" ".join(command),
        returncode=completed.returncode,
        status="OK" if completed.returncode == 0 else "FAILED",
        started_at=started_at,
        finished_at=finished_at,
        stdout_tail=tail_text(completed.stdout, repo_root),
        stderr_tail=tail_text(completed.stderr, repo_root),
    )


def python_command(script: str, *args: str) -> list[str]:
    return [sys.executable, script, *args]


def write_json_and_markdown(payload: dict[str, Any], markdown: str, outputs: dict[str, Path]) -> dict[str, Path]:
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    for key, path in outputs.items():
        if key.endswith("_json") or path.suffix == ".json":
            path.write_text(text + "\n", encoding="utf-8")
        elif key.endswith("_md") or path.suffix == ".md":
            path.write_text(markdown, encoding="utf-8")
    return outputs
