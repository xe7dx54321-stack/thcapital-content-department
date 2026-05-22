#!/usr/bin/env python3
"""Run official lane, validate runtime manifest, and rebuild source runtime health.

P0-011B promotes the P0-010 wrapper route into a safer daily check entrypoint.
It intentionally does not modify ``market_official_update_lane.py``. Instead it:

1. runs ``scripts/run_official_lane_with_manifest.py`` unless ``--skip-run`` is used;
2. validates the latest official runtime manifest with the P0-008 validator;
3. rebuilds source runtime health so P0-011A can consume manifest evidence.

The script only orchestrates existing commands and reports a small summary.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402


@dataclass(frozen=True)
class StepResult:
    name: str
    command: list[str]
    returncode: int
    stdout_tail: str
    stderr_tail: str


@dataclass(frozen=True)
class OfficialLaneHealthCheckResult:
    generated_at: str
    status: str
    manifest_path: str
    source_runtime_health_path: str
    steps: tuple[StepResult, ...]


def tail_text(text: str, max_lines: int = 20) -> str:
    lines = text.strip().splitlines()
    return "\n".join(lines[-max_lines:])


def run_command(name: str, command: list[str]) -> StepResult:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return StepResult(
        name=name,
        command=command,
        returncode=completed.returncode,
        stdout_tail=tail_text(completed.stdout),
        stderr_tail=tail_text(completed.stderr),
    )


def load_manifest_summary(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.exists():
        return {}
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    sources = data.get("sources") or []
    return {
        "run_id": data.get("run_id", ""),
        "status": data.get("status", ""),
        "pipeline_name": data.get("pipeline_name", ""),
        "script_name": data.get("script_name", ""),
        "source_count": len(sources) if isinstance(sources, list) else 0,
        "total_items_found": sum(
            int(item.get("items_found", 0) or 0)
            for item in sources
            if isinstance(item, dict)
        )
        if isinstance(sources, list)
        else 0,
    }


def build_result(steps: list[StepResult]) -> OfficialLaneHealthCheckResult:
    paths = get_project_paths(REPO_ROOT)
    manifest_path = paths.logs_root / "latest_official_runtime_manifest.json"
    source_runtime_health_path = paths.logs_root / "latest_source_runtime_health.json"
    has_failure = any(step.returncode != 0 for step in steps)
    status = "FAILED" if has_failure else "SUCCESS"
    return OfficialLaneHealthCheckResult(
        generated_at=datetime.now(timezone.utc).isoformat(),
        status=status,
        manifest_path=str(manifest_path),
        source_runtime_health_path=str(source_runtime_health_path),
        steps=tuple(steps),
    )


def print_summary(result: OfficialLaneHealthCheckResult) -> None:
    manifest_summary = load_manifest_summary(Path(result.manifest_path))
    print("\nOfficial Lane Health Check")
    print("=" * 36)
    print(f"status: {result.status}")
    print(f"manifest: {result.manifest_path}")
    print(f"source_runtime_health: {result.source_runtime_health_path}")

    if manifest_summary:
        print(f"manifest_status: {manifest_summary.get('status', '')}")
        print(f"source_count: {manifest_summary.get('source_count', 0)}")
        print(f"total_items_found: {manifest_summary.get('total_items_found', 0)}")

    print("\nSteps:")
    for step in result.steps:
        status = "OK" if step.returncode == 0 else "FAIL"
        print(f"- {step.name}: {status} ({step.returncode})")
        if step.returncode != 0 and step.stderr_tail:
            print(f"  stderr: {step.stderr_tail}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-run",
        action="store_true",
        help="Do not run official lane; validate the latest existing official runtime manifest.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON summary instead of text summary.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = get_project_paths(REPO_ROOT)
    manifest_path = paths.logs_root / "latest_official_runtime_manifest.json"

    steps: list[StepResult] = []

    if not args.skip_run:
        steps.append(
            run_command(
                "official_lane_with_manifest",
                [sys.executable, "scripts/run_official_lane_with_manifest.py"],
            )
        )

    steps.append(
        run_command(
            "validate_official_runtime_manifest",
            [sys.executable, "scripts/validate_runtime_manifest.py", str(manifest_path)],
        )
    )
    steps.append(
        run_command(
            "build_source_runtime_health",
            [sys.executable, "scripts/build_source_runtime_health.py"],
        )
    )

    result = build_result(steps)

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print_summary(result)

    return 1 if result.status != "SUCCESS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
