#!/bin/bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
CONTENT_ROOT="/Users/apple/Documents/同行资本内容部门/内容生产系统"
SERVER_SCRIPT="$CONTENT_ROOT/09_runbooks/scripts/market_ops_console_server.py"
FRONTSTAGE_BUILDER="$CONTENT_ROOT/09_runbooks/scripts/market_frontstage_board_builder.py"
DASHBOARD_BUILDER="$CONTENT_ROOT/09_runbooks/scripts/market_ops_dashboard_builder.py"

HOST="127.0.0.1"
PORT="${CONTENT_FACTORY_DASHBOARD_PORT:-8780}"
DATE_ARG="${1:-$(TZ=Asia/Shanghai date +%F)}"
WINDOW_START="${CONTENT_FACTORY_WINDOW_START:-19:00}"
WINDOW_END="${CONTENT_FACTORY_WINDOW_END:-12:20}"
SCREEN_NAME="th_content_factory_dashboard"
LABEL="com.thcapital.content-factory-dashboard"
DOMAIN="gui/$(id -u)"
PLIST_FILE="$APP_DIR/runtime/$LABEL.plist"
PYTHON_BIN="$(command -v python3)"
LAUNCH_SCRIPT="$APP_DIR/runtime/$LABEL-launch.sh"

PID_FILE="$APP_DIR/runtime/server.pid"
STATE_FILE="$APP_DIR/runtime/server.json"
LOG_FILE="$APP_DIR/logs/server.log"

listening_pid() {
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t 2>/dev/null | head -n 1 || true
}

health_ok() {
  /usr/bin/curl -fsS "http://$HOST:$PORT/health" >/dev/null 2>&1
}

screen_session_exists() {
  /usr/bin/screen -ls 2>/dev/null | grep -q "[[:space:]][0-9][0-9]*\\.${SCREEN_NAME}[[:space:]]"
}

write_state() {
  local pid="$1"
  local started_at
  started_at="$(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S CST')"
  echo "$pid" >"$PID_FILE"
  cat >"$STATE_FILE" <<EOF
{
  "host": "127.0.0.1",
  "port": $PORT,
  "date": "$DATE_ARG",
  "window_start": "$WINDOW_START",
  "window_end": "$WINDOW_END",
  "pid": $pid,
  "screen_session": "$SCREEN_NAME",
  "started_at": "$started_at",
  "base_url": "http://$HOST:$PORT",
  "entry_url": "http://$HOST:$PORT/intake?date=$DATE_ARG"
}
EOF
  echo "http://$HOST:$PORT/intake?date=$DATE_ARG" >"$APP_DIR/runtime/current-url.txt"
}

write_launch_script() {
  cat >"$LAUNCH_SCRIPT" <<EOF
#!/bin/bash
set -euo pipefail
cd "$CONTENT_ROOT"
exec "$PYTHON_BIN" -u "$SERVER_SCRIPT" \
  --host "$HOST" \
  --port "$PORT" \
  --date "$DATE_ARG" \
  --window-start "$WINDOW_START" \
  --window-end "$WINDOW_END" \
  >> "$LOG_FILE" 2>&1
EOF
  chmod +x "$LAUNCH_SCRIPT"
}

cleanup_launchd() {
  launchctl bootout "$DOMAIN" "$PLIST_FILE" >/dev/null 2>&1 || true
  launchctl bootout "$DOMAIN/$LABEL" >/dev/null 2>&1 || true
}

is_running() {
  local pid
  pid="$(listening_pid)"
  if [[ -n "$pid" ]] && health_ok; then
    write_state "$pid"
    return 0
  fi
  rm -f "$PID_FILE"
  return 1
}

if is_running; then
  echo "内容工厂展示台已在运行： http://$HOST:$PORT/intake?date=$DATE_ARG"
  exit 0
fi

echo "刷新内容工厂前台快照..."
python3 "$FRONTSTAGE_BUILDER" --date "$DATE_ARG" --write >/dev/null
python3 "$DASHBOARD_BUILDER" --date "$DATE_ARG" --window-start "$WINDOW_START" --window-end "$WINDOW_END" --write >/dev/null

echo "启动内容工厂展示台..."
cleanup_launchd
/usr/bin/screen -S "$SCREEN_NAME" -X quit >/dev/null 2>&1 || true
EXISTING_PID="$(listening_pid)"
if [[ -n "$EXISTING_PID" ]]; then
  kill "$EXISTING_PID" >/dev/null 2>&1 || true
  sleep 1
fi
: >"$LOG_FILE"
write_launch_script
/usr/bin/screen -dmS "$SCREEN_NAME" "$LAUNCH_SCRIPT"

for _ in {1..30}; do
  if health_ok; then
    break
  fi
  sleep 0.5
done

if health_ok; then
  REAL_PID="$(listening_pid)"
  write_state "${REAL_PID:-0}"
  echo "内容工厂展示台已启动： http://$HOST:$PORT/intake?date=$DATE_ARG"
else
  rm -f "$PID_FILE" "$STATE_FILE"
  echo "展示台启动命令已发出，但健康检查未立即通过。请查看日志： $LOG_FILE"
  exit 1
fi
