#!/usr/bin/env python3
"""Check macOS LaunchAgent installation status."""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path


LABEL = "com.thcapital.content-factory-runtime"
LAUNCH_AGENT = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
SECRET_VALUE_RE = re.compile(r"sk-[A-Za-z0-9_-]{8,}")
SECRET_ENV_RE = re.compile(r"\b(?:MINIMAX|ANTHROPIC|OPENAI|API)_API_KEY\s*=>\s*[^\n]+")


def sanitize(text: str) -> str:
    sanitized = SECRET_ENV_RE.sub("<secret-env> => <redacted>", text or "")
    return SECRET_VALUE_RE.sub("<redacted>", sanitized)


def service_name() -> str:
    return f"gui/{os.getuid()}/{LABEL}"


def main() -> int:
    printed = subprocess.run(["launchctl", "print", service_name()], text=True, capture_output=True, check=False)
    loaded = printed.returncode == 0
    enabled = loaded and "state = running" in printed.stdout.lower() or loaded
    result = {
        "label": LABEL,
        "launch_agent": str(LAUNCH_AGENT),
        "installed": LAUNCH_AGENT.exists(),
        "loaded": loaded,
        "enabled": enabled,
        "user_level": True,
        "service_name": service_name(),
        "stdout_tail": sanitize(printed.stdout)[-2000:],
        "stderr_tail": sanitize(printed.stderr)[-2000:],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["installed"] and result["loaded"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
