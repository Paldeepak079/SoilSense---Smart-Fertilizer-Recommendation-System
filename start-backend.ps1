# Quick Start Script for Backend
# Run this from the SoilSense directory

Write-Host "=== SoilSense Backend Setup ===" -ForegroundColor Green

# Check Python version
Write-Host "`nChecking Python version..." -ForegroundColor Yellow
python --version

# Navigate to backend
cd backend

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate venv
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "`nCreating .env file from template..." -ForegroundColor Yellow
    Copy-Item ..\.env.example .env
    Write-Host "IMPORTANT: Edit backend/.env and set your DATABASE_URL!" -ForegroundColor Red
}

# Train ML model if not exists
if (-not (Test-Path "ml/nutrient_model.pkl")) {
    Write-Host "`nTraining ML model (this will take ~2 minutes)..." -ForegroundColor Yellow
    python -m ml.train_model
}

Write-Host "`n=== Starting Backend Server on port 8080 ===" -ForegroundColor Green
Write-Host "API Docs will be at: http://localhost:8080/docs" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8080
