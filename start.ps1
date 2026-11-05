Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$PidFile = Join-Path $ProjectRoot ".backend.pid"
$OutputLog = Join-Path $ProjectRoot "backend.out.log"
$ErrorLog = Join-Path $ProjectRoot "backend.err.log"

if (-not (Test-Path $Python)) {
    throw "Virtual environment not found. Run: py -3.12 -m venv .venv; pip install -r requirements.txt"
}

if (Test-Path $PidFile) {
    $ExistingPid = Get-Content $PidFile -Raw
    if ($ExistingPid -match "^\d+$" -and (Get-Process -Id ([int]$ExistingPid) -ErrorAction SilentlyContinue)) {
        Write-Host "Backend is already running with PID $ExistingPid."
        exit 0
    }
    Remove-Item $PidFile -Force
}

$Process = Start-Process `
    -FilePath $Python `
    -ArgumentList @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000") `
    -WorkingDirectory $ProjectRoot `
    -RedirectStandardOutput $OutputLog `
    -RedirectStandardError $ErrorLog `
    -PassThru

$Process.Id | Set-Content $PidFile
Write-Host "Backend started with PID $($Process.Id)."
Write-Host "Health check: http://localhost:8000/health"
Write-Host "Output log: $OutputLog"
Write-Host "Error log: $ErrorLog"