#!/bin/bash
set -euo pipefail
cd "/Users/apple/Documents/同行资本内容部门/内容生产系统"
exec "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3" -u "/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_ops_console_server.py"   --host "127.0.0.1"   --port "8780"   --date "2026-03-28"   --window-start "19:00"   --window-end "12:20"   >> "/Users/apple/Documents/同行资本内容部门/内容工厂控制台/logs/server.log" 2>&1
