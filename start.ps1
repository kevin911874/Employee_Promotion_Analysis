Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Employee Promotion Analysis - Starting" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check MongoDB
Write-Host "Checking MongoDB..." -ForegroundColor Yellow
$mongo = Get-Service MongoDB -ErrorAction SilentlyContinue
if ($mongo -and $mongo.Status -eq 'Running') {
    Write-Host "[OK] MongoDB is running" -ForegroundColor Green
} else {
    Write-Host "[ERROR] MongoDB not running" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'D:\Project\Employee Promotion Analysis\backend'; .\venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload --port 8000"

Start-Sleep -Seconds 2

Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'D:\Project\Employee Promotion Analysis\frontend'; npm run dev"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Servers are starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Wait 10-15 seconds then open your browser" -ForegroundColor Yellow
Write-Host ""
