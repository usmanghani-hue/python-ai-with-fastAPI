Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PidFile = Join-Path $ProjectRoot ".backend.pid"

if (-not (Test-Path $PidFile)) {
    Write-Host "No managed backend process found."
    exit 0
}

$BackendPid = Get-Content $PidFile -Raw
if ($BackendPid -match "^\d+$" -and (Get-Process -Id ([int]$BackendPid) -ErrorAction SilentlyContinue)) {
    taskkill.exe /PID ([int]$BackendPid) /T /F | Out-Null
    Write-Host "Backend stopped."
} else {
    Write-Host "Backend process was already stopped."
}

Remove-Item $PidFile -Force