@echo off
setlocal
set SCRIPT_DIR=%~dp0

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -3 "%SCRIPT_DIR%wechat_bridge_consumer.py" --watch --interval 20
  goto :eof
)

python "%SCRIPT_DIR%wechat_bridge_consumer.py" --watch --interval 20
