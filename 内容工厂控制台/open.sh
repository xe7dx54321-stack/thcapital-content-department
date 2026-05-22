#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENT_FACTORY_CONSOLE_ROOT="${THCAP_CONTENT_CONSOLE_ROOT:-${SCRIPT_DIR}}"
STATE_FILE="$CONTENT_FACTORY_CONSOLE_ROOT/runtime/server.json"

if [[ ! -f "$STATE_FILE" ]]; then
  echo "展示台尚未启动，请先执行 ./start.sh"
  exit 1
fi

URL="$(python3 - "$STATE_FILE" <<'PY'
import json
import sys
from pathlib import Path
path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
print(data.get("entry_url", ""))
PY
)"

if [[ -z "$URL" ]]; then
  echo "未能读取入口地址。"
  exit 1
fi

open "$URL"
