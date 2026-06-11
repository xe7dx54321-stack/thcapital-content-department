#!/usr/bin/env python3
"""Uninstall the macOS LaunchAgent for autonomous runtime."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


LABEL = "com.thcapital.content-factory-runtime"
LAUNCH_AGENT = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"


def main() -> int:
    parser = argparse.ArgumentParser(description="Uninstall Content Factory Runtime LaunchAgent.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(f"would_unload: {LAUNCH_AGENT}")
        print("removed: false")
        return 0
    subprocess.run(["launchctl", "unload", str(LAUNCH_AGENT)], check=False)
    if LAUNCH_AGENT.exists():
        LAUNCH_AGENT.unlink()
    print(f"removed: {not LAUNCH_AGENT.exists()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
