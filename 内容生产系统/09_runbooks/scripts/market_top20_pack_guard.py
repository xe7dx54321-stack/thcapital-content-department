#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path

from market_business_day import day_token
from market_stage_artifact_status import inspect_artifact


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
SCRIPT_DIR = ROOT / "09_runbooks" / "scripts"
BOOTSTRAP_SCRIPT = SCRIPT_DIR / "market_stage_bootstrap.py"
MANIFEST_SCRIPT = SCRIPT_DIR / "market_daily_source_manifest.py"
BUILDER_SCRIPT = SCRIPT_DIR / "market_top20_pack_builder.py"
LOG_DIR = ROOT / "10_logs"
TOPIC_DIR = ROOT / "03_topic_candidates"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Guarantee that the canonical Top20 pack is materially present for day_mainline.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Logical date in YYYY-MM-DD.")
    parser.add_argument("--write", action="store_true", help="Actually write bootstrap / manifest / builder outputs.")
    return parser.parse_args()


def run_command(command: list[str], write: bool) -> dict[str, object]:
    if not write:
        return {
            "command": command,
            "returncode": 0,
            "stdout": "DRY_RUN",
            "stderr": "",
        }
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": (completed.stdout or "").strip(),
        "stderr": (completed.stderr or "").strip(),
    }


def main() -> int:
    args = parse_args()
    token = day_token(args.date)
    pack_path = TOPIC_DIR / f"{token}__top20-screening-pack.md"
    manifest_path = LOG_DIR / f"{token}__market-source-manifest.md"
    runtime_log_path = LOG_DIR / f"{token}__market-scout-runtime-state.md"

    commands: list[dict[str, object]] = []
    commands.append(
        run_command(
            ["python3", str(BOOTSTRAP_SCRIPT), "--stage", "top20_pack", "--date", args.date, "--write"],
            write=args.write,
        )
    )
    commands.append(
        run_command(
            ["python3", str(MANIFEST_SCRIPT), "--date", args.date, "--write"],
            write=args.write,
        )
    )

    before = inspect_artifact(pack_path, "pack")
    builder_ran = False
    builder_result: dict[str, object] | None = None
    if before["state"] != "final":
        builder_ran = True
        builder_result = run_command(
            [
                "python3",
                str(BUILDER_SCRIPT),
                "--date",
                args.date,
                "--manifest-path",
                str(manifest_path),
                "--output-path",
                str(pack_path),
                "--runtime-log-path",
                str(runtime_log_path),
                "--write",
            ],
            write=args.write,
        )

    after = inspect_artifact(pack_path, "pack")
    payload = {
        "date": args.date,
        "token": token,
        "pack_path": str(pack_path),
        "manifest_path": str(manifest_path),
        "runtime_log_path": str(runtime_log_path),
        "before": before,
        "after": after,
        "builder_ran": builder_ran,
        "commands": commands,
        "builder_result": builder_result,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if after["state"] == "final" else 1


if __name__ == "__main__":
    raise SystemExit(main())
