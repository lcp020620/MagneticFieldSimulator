if (-not (Test-Path "venv")) {
    Write-Host "Generating Virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

$VenvActivate = ".\venv\Scripts\Activate.ps1"

if (Test-Path $VenvActivate) {
    & $VenvActivate
} else {
    Write-Error "Virtual environment activation script not found."
    pause
    exit
}

Write-Host "Installing requirements..." -ForegroundColor Cyan
pip install -r requirements.txt

if (-not $?) {
    Write-Host ""
    Write-Host "[error] There was an issue during library installation." -ForegroundColor Red
    Write-Host "Check your python version or internet connection." -ForegroundColor Yellow
    pause
    exit
}

Write-Host "Starting app.py..." -ForegroundColor Green
python app.py

exit
