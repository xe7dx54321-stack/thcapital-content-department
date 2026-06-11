#!/usr/bin/env python3
"""Check macOS LaunchAgent installation status."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


LABEL = "com.thcapital.content-factory-runtime"
LAUNCH_AGENT = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"


def main() -> int:
    completed = subprocess.run(["launchctl", "list"], text=True, capture_output=True, check=False)
    loaded = LABEL in completed.stdout
    result = {
        "label": LABEL,
        "launch_agent": str(LAUNCH_AGENT),
        "installed": LAUNCH_AGENT.exists(),
        "loaded": loaded,
        "user_level": True,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
