#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

from market_stage_artifact_status import (
    artifact_alias_paths,
    best_artifact_in_family,
    inspect_artifact,
    promote_best_artifact_to_canonical,
    state_satisfies,
)


OPENCLAW_CWD = Path("/Users/apple/.openclaw")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trigger an OpenClaw stage job and poll a canonical artifact until it reaches the requested state.")
    parser.add_argument("--job-id", required=True, help="OpenClaw cron job id.")
    parser.add_argument("--watch-path", required=True, help="Canonical artifact path to watch.")
    parser.add_argument("--kind", required=True, choices=["pack", "redteam", "scorecard", "top5_board", "platform_task_sheet"])
    parser.add_argument("--accept-state", choices=["materialized", "final"], default="final")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--poll-seconds", type=int, default=5)
    parser.add_argument(
        "--require-update",
        action="store_true",
        help="Only succeed when the watched artifact family changes after trigger; by default the runner also accepts already-materialized recovery states.",
    )
    return parser.parse_args()


def run_job(job_id: str) -> dict:
    proc = subprocess.run(
        ["openclaw", "cron", "run", job_id],
        cwd=OPENCLAW_CWD,
        capture_output=True,
        text=True,
    )
    stdout = (proc.stdout or "").strip()
    payload: dict = {
        "returncode": proc.returncode,
        "stdout": stdout,
        "stderr": (proc.stderr or "").strip(),
    }
    if stdout.startswith("{") and stdout.endswith("}"):
        try:
            payload["json"] = json.loads(stdout)
        except json.JSONDecodeError:
            pass
    data = payload.get("json", {})
    if proc.returncode == 0:
        return payload
    if data.get("ok") and data.get("reason") == "already-running":
        return payload
    if data.get("ok") and data.get("enqueued"):
        return payload
    raise RuntimeError(f"openclaw cron run failed: {payload}")


def main() -> int:
    args = parse_args()
    watch_path = Path(args.watch_path).expanduser()
    family_paths = artifact_alias_paths(watch_path)
    previous_mtimes = {
        str(path): path.stat().st_mtime if path.exists() else 0.0
        for path in family_paths
    }
    previous_best = best_artifact_in_family(watch_path, args.kind)
    trigger = run_job(args.job_id)
    started_at = time.time()
    last_result = inspect_artifact(watch_path, args.kind)
    while time.time() - started_at <= args.timeout_seconds:
        promotion = promote_best_artifact_to_canonical(watch_path, args.kind)
        current = best_artifact_in_family(watch_path, args.kind)
        canonical = inspect_artifact(watch_path, args.kind)
        last_result = canonical
        current_path = Path(current["path"])
        current_mtime = current_path.stat().st_mtime if current_path.exists() else 0.0
        previous_mtime = previous_mtimes.get(str(current_path), 0.0)
        is_new_or_updated = current_mtime > previous_mtime or promotion.get("promoted", False)
        if state_satisfies(current["state"], args.accept_state) and (
            is_new_or_updated or (not args.require_update and state_satisfies(previous_best["state"], args.accept_state))
        ):
            print(
                json.dumps(
                    {
                        "job_id": args.job_id,
                        "trigger": trigger,
                        "artifact": current,
                        "canonical_artifact": canonical,
                        "promotion": promotion,
                        "updated": is_new_or_updated,
                        "reused_existing": not is_new_or_updated,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0
        time.sleep(args.poll_seconds)
    print(
        json.dumps(
            {
                "job_id": args.job_id,
                "trigger": trigger,
                "artifact": best_artifact_in_family(watch_path, args.kind),
                "canonical_artifact": inspect_artifact(watch_path, args.kind),
                "updated": False,
                "reused_existing": False,
                "timeout_seconds": args.timeout_seconds,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
