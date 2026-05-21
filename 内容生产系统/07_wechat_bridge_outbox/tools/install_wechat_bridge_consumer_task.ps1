param(
    [string]$RootDir = "D:\THCapital\wechat-bridge-outbox",
    [string]$TaskName = "THCapital-WeChat-Bridge-Consumer",
    [switch]$RunNow
)

$ErrorActionPreference = "Stop"

$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$ToolsDir = Join-Path $RootDir "tools"
$RunnerPath = Join-Path $ToolsDir "run_wechat_bridge_consumer_forever.ps1"
$StartupInstaller = Join-Path $ToolsDir "install_wechat_bridge_consumer_startup.ps1"
$LogDir = Join-Path $RootDir "logs"

if (-not (Test-Path $RootDir)) {
    throw "RootDir not found: $RootDir"
}

if (-not (Test-Path $RunnerPath)) {
    throw "Runner script not found: $RunnerPath"
}

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$RunnerPath`" -RootDir `"$RootDir`"" `
    -WorkingDirectory $ToolsDir
$ElevatedTriggers = @(
    (New-ScheduledTaskTrigger -AtLogOn -User $CurrentUser),
    (New-ScheduledTaskTrigger -AtStartup)
)
$FallbackTriggers = @(
    (New-ScheduledTaskTrigger -AtLogOn -User $CurrentUser)
)
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Days 3650)

$InstalledMode = $null
$StartupShortcutInstalled = $false

try {
    $Principal = New-ScheduledTaskPrincipal -UserId $CurrentUser -LogonType Interactive -RunLevel Highest
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $ElevatedTriggers `
        -Settings $Settings `
        -Principal $Principal `
        -Description "Keep TH Capital WeChat bridge consumer running and auto-restart it after login/startup." `
        -Force | Out-Null
    $InstalledMode = "elevated_login_plus_startup"
}
catch {
    Write-Warning "Elevated/startup registration failed, falling back to per-user logon task. $($_.Exception.Message)"
    $Principal = New-ScheduledTaskPrincipal -UserId $CurrentUser -LogonType Interactive -RunLevel Limited
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $FallbackTriggers `
        -Settings $Settings `
        -Principal $Principal `
        -Description "Keep TH Capital WeChat bridge consumer running after user logon." `
        -Force | Out-Null
    $InstalledMode = "user_logon_only"
    if (Test-Path $StartupInstaller) {
        try {
            & $StartupInstaller -RootDir $RootDir | Out-Null
            $StartupShortcutInstalled = $true
            $InstalledMode = "user_logon_only + startup_shortcut"
        }
        catch {
            Write-Warning "Startup shortcut fallback failed: $($_.Exception.Message)"
        }
    }
}

if ($RunNow) {
    Start-ScheduledTask -TaskName $TaskName
}

Write-Host "TASK_INSTALLED $TaskName"
Write-Host "USER $CurrentUser"
Write-Host "RUNNER $RunnerPath"
Write-Host "LOG $LogDir\wechat_bridge_consumer.log"
Write-Host "MODE $InstalledMode"
Write-Host "STARTUP_SHORTCUT $StartupShortcutInstalled"
Write-Host "TIP Use Task Scheduler -> Task Scheduler Library to inspect the task."
