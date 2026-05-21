param(
    [string]$RootDir = "D:\THCapital\wechat-bridge-outbox"
)

$ErrorActionPreference = "Stop"

$ToolsDir = Join-Path $RootDir "tools"
$RunnerPath = Join-Path $ToolsDir "run_wechat_bridge_consumer_forever.ps1"
$StartupDir = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $StartupDir "THCapital WeChat Bridge Consumer.lnk"

if (-not (Test-Path $RootDir)) {
    throw "RootDir not found: $RootDir"
}

if (-not (Test-Path $RunnerPath)) {
    throw "Runner script not found: $RunnerPath"
}

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$RunnerPath`" -RootDir `"$RootDir`""
$Shortcut.WorkingDirectory = $ToolsDir
$Shortcut.WindowStyle = 7
$Shortcut.Description = "Start TH Capital WeChat bridge consumer watchdog at logon."
$Shortcut.Save()

Write-Host "STARTUP_SHORTCUT_INSTALLED $ShortcutPath"
Write-Host "RUNNER $RunnerPath"
