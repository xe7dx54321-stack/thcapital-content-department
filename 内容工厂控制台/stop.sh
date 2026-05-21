#!/bin/bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$APP_DIR/runtime/server.pid"
STATE_FILE="$APP_DIR/runtime/server.json"
PORT="${CONTENT_FACTORY_DASHBOARD_PORT:-8780}"
SCREEN_NAME="th_content_factory_dashboard"
LABEL="com.thcapital.content-factory-dashboard"
DOMAIN="gui/$(id -u)"
PLIST_FILE="$APP_DIR/runtime/$LABEL.plist"

listening_pid() {
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t 2>/dev/null | head -n 1 || true
}

launchctl bootout "$DOMAIN" "$PLIST_FILE" >/dev/null 2>&1 || true
launchctl bootout "$DOMAIN/$LABEL" >/dev/null 2>&1 || true
/usr/bin/screen -S "$SCREEN_NAME" -X quit >/dev/null 2>&1 || true
sleep 1

PID="$(cat "$PID_FILE" 2>/dev/null || true)"
if [[ -z "$PID" ]]; then
  PID="$(listening_pid)"
fi

if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
  kill "$PID" 2>/dev/null || true
  sleep 1
  if kill -0 "$PID" 2>/dev/null; then
    kill -9 "$PID" 2>/dev/null || true
  fi
  echo "内容工厂展示台已停止。"
else
  ALT_PID="$(listening_pid)"
  if [[ -n "$ALT_PID" ]] && kill -0 "$ALT_PID" 2>/dev/null; then
    kill "$ALT_PID" 2>/dev/null || true
    sleep 1
    if kill -0 "$ALT_PID" 2>/dev/null; then
      kill -9 "$ALT_PID" 2>/dev/null || true
    fi
    echo "内容工厂展示台已停止。"
  else
    echo "未发现运行中的内容工厂展示台。"
  fi
fi

rm -f "$PID_FILE"
rm -f "$STATE_FILE"
