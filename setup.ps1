# Run this once after cloning: powershell -ExecutionPolicy Bypass -File setup.ps1
# Assumes Python 3.10+ is already installed and on PATH.

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python was not found on PATH. Install Python 3.10+ before running this script." -ForegroundColor Red
    exit 1
}

Write-Host "Found $(& python --version 2>&1)" -ForegroundColor Green

Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "pip install failed - see the error above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Setup complete. Run 'nxt-llm claude' from this folder to start the workshop." -ForegroundColor Green
