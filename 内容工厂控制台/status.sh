#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENT_FACTORY_CONSOLE_ROOT="${THCAP_CONTENT_CONSOLE_ROOT:-${SCRIPT_DIR}}"
PID_FILE="$CONTENT_FACTORY_CONSOLE_ROOT/runtime/server.pid"
STATE_FILE="$CONTENT_FACTORY_CONSOLE_ROOT/runtime/server.json"
HOST="${CONTENT_FACTORY_DASHBOARD_HOST:-127.0.0.1}"
PORT="${CONTENT_FACTORY_DASHBOARD_PORT:-8780}"
SCREEN_NAME="th_content_factory_dashboard"

listening_pid() {
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t 2>/dev/null | head -n 1 || true
}

health_ok() {
  /usr/bin/curl -fsS "http://$HOST:$PORT/health" >/dev/null 2>&1
}

screen_session_exists() {
  /usr/bin/screen -ls 2>/dev/null | grep -q "[[:space:]][0-9][0-9]*\\.${SCREEN_NAME}[[:space:]]"
}

PID="$(listening_pid)"
if [[ -n "$PID" ]] && health_ok; then
  if [[ -f "$STATE_FILE" ]]; then
    python3 - "$STATE_FILE" "$PID" "$SCREEN_NAME" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
pid = int(sys.argv[2])
screen_name = sys.argv[3]
try:
    data = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    data = {}
data["pid"] = pid
data["screen_session"] = screen_name
path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(data, ensure_ascii=False, indent=2))
PY
  else
    echo "{\"host\":\"$HOST\",\"port\":$PORT,\"pid\":$PID,\"screen_session\":\"$SCREEN_NAME\",\"base_url\":\"http://$HOST:$PORT\"}"
  fi
  echo
  echo "status=running pid=$PID session=$SCREEN_NAME"
  exit 0
fi

if screen_session_exists; then
  echo "status=starting session=$SCREEN_NAME"
  exit 0
fi

if [[ -f "$STATE_FILE" ]]; then
  cat "$STATE_FILE"
  echo
fi

rm -f "$PID_FILE"
echo "status=stopped"
