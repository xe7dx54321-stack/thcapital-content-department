param(
    [string]$TaskName = "THCapital-WeChat-Bridge-Consumer"
)

$ErrorActionPreference = "Stop"
$StartupDir = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $StartupDir "THCapital WeChat Bridge Consumer.lnk"

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "TASK_REMOVED $TaskName"
} else {
    Write-Host "TASK_NOT_FOUND $TaskName"
}

if (Test-Path $ShortcutPath) {
    Remove-Item $ShortcutPath -Force
    Write-Host "STARTUP_SHORTCUT_REMOVED $ShortcutPath"
} else {
    Write-Host "STARTUP_SHORTCUT_NOT_FOUND $ShortcutPath"
}
