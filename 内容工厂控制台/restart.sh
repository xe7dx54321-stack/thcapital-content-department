#!/bin/bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
"$APP_DIR/stop.sh" || true
"$APP_DIR/start.sh" "${1:-}"
