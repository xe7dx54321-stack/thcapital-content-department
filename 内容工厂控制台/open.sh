#!/bin/bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_FILE="$APP_DIR/runtime/server.json"

if [[ ! -f "$STATE_FILE" ]]; then
  echo "展示台尚未启动，请先执行 ./start.sh"
  exit 1
fi

URL="$(python3 - <<'PY'
import json
from pathlib import Path
path = Path("/Users/apple/Documents/同行资本内容部门/内容工厂控制台/runtime/server.json")
data = json.loads(path.read_text(encoding="utf-8"))
print(data.get("entry_url", ""))
PY
)"

if [[ -z "$URL" ]]; then
  echo "未能读取入口地址。"
  exit 1
fi

open "$URL"
