@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "POWERSHELL_RUNNER=%SCRIPT_DIR%run_wechat_bridge_consumer_forever.ps1"
set "ROOT_DIR=%SCRIPT_DIR%.."

if not exist "%POWERSHELL_RUNNER%" (
  echo Runner script not found: %POWERSHELL_RUNNER%
  exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%POWERSHELL_RUNNER%" -RootDir "%ROOT_DIR%"
exit /b %ERRORLEVEL%
