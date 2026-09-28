# Run this once after cloning: powershell -ExecutionPolicy Bypass -File setup.ps1

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python was not found on PATH." -ForegroundColor Red
    Write-Host "Install it with:  winget install Python.Python.3.11 -e" -ForegroundColor Yellow
    Write-Host "Then open a new terminal and re-run this script." -ForegroundColor Yellow
    exit 1
}

$versionOutput = & python --version 2>&1
if ($versionOutput -match "Python (\d+)\.(\d+)") {
    $major = [int]$Matches[1]
    $minor = [int]$Matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
        Write-Host "Found $versionOutput, but this workshop needs Python 3.10+." -ForegroundColor Red
        Write-Host "Install a newer one with:  winget install Python.Python.3.11 -e" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "Could not parse '$versionOutput' as a Python version. Continuing anyway." -ForegroundColor Yellow
}

Write-Host "Found $versionOutput" -ForegroundColor Green

$claude = Get-Command claude -ErrorAction SilentlyContinue
if (-not $claude) {
    Write-Host "Claude Code CLI was not found on PATH. Make sure it's installed before the workshop." -ForegroundColor Red
    exit 1
}
Write-Host "Found Claude Code CLI: $($claude.Source)" -ForegroundColor Green

Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "pip install failed - see the error above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Setup complete. Run 'claude' from this folder to start the workshop." -ForegroundColor Green
