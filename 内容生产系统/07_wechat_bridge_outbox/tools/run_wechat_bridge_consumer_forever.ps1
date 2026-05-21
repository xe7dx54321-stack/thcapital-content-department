param(
    [string]$RootDir = "",
    [int]$RestartDelaySeconds = 5,
    [int]$WatchIntervalSeconds = 20,
    [string]$MutexName = "Local\THCapital-WeChat-Bridge-Consumer"
)

$ErrorActionPreference = "Stop"

if (-not $RootDir) {
    $RootDir = Join-Path $PSScriptRoot ".."
}

$RootDir = (Resolve-Path $RootDir).Path
$ToolsDir = Join-Path $RootDir "tools"
$ConsumerPath = Join-Path $ToolsDir "wechat_bridge_consumer.py"
$LogDir = Join-Path $RootDir "logs"
$LogFile = Join-Path $LogDir "wechat_bridge_consumer.log"

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

function Write-RunnerLog {
    param([string]$Message)
    $timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffK")
    Add-Content -Path $LogFile -Value "[$timestamp] $Message"
}

$createdNew = $false
$mutex = [System.Threading.Mutex]::new($true, $MutexName, [ref]$createdNew)

if (-not $createdNew) {
    Write-RunnerLog "WATCHDOG_ALREADY_RUNNING mutex=$MutexName"
    exit 0
}

try {
    Write-RunnerLog "WATCHDOG_START root=$RootDir consumer=$ConsumerPath"

    while ($true) {
        $launcher = $null
        $arguments = @()
        $sawAlreadyRunning = $false

        $py = Get-Command py -ErrorAction SilentlyContinue
        if ($py) {
            $launcher = $py.Source
            $arguments = @("-3", $ConsumerPath, "--watch", "--interval", "$WatchIntervalSeconds")
        } else {
            $python = Get-Command python -ErrorAction SilentlyContinue
            if (-not $python) {
                throw "Neither 'py' nor 'python' was found on PATH."
            }
            $launcher = $python.Source
            $arguments = @($ConsumerPath, "--watch", "--interval", "$WatchIntervalSeconds")
        }

        Write-RunnerLog "CONSUMER_START launcher=$launcher interval=$WatchIntervalSeconds"

        try {
            & $launcher @arguments 2>&1 | ForEach-Object {
                $line = $_.ToString().TrimEnd()
                if ($line) {
                    Add-Content -Path $LogFile -Value $line
                    if ($line -like "*WATCHER_ALREADY_RUNNING*") {
                        $sawAlreadyRunning = $true
                    }
                }
            }
            $exitCode = if ($LASTEXITCODE -ne $null) { $LASTEXITCODE } else { 0 }
        }
        catch {
            $exitCode = 1
            Write-RunnerLog "CONSUMER_EXCEPTION $($_.Exception.Message)"
        }

        Write-RunnerLog "CONSUMER_EXIT code=$exitCode"
        if ($sawAlreadyRunning -or $exitCode -eq 0) {
            Write-RunnerLog "WATCHDOG_EXIT clean_stop_or_existing_watcher"
            break
        }
        Start-Sleep -Seconds $RestartDelaySeconds
    }
}
finally {
    if ($createdNew) {
        try {
            $mutex.ReleaseMutex() | Out-Null
        }
        catch {
        }
    }
    $mutex.Dispose()
}
