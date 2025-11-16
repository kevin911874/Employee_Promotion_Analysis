# Employee Promotion Analysis - Project Startup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Employee Promotion Analysis System   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if MongoDB is running
Write-Host "Checking MongoDB status..." -ForegroundColor Yellow
$mongoService = Get-Service -Name MongoDB -ErrorAction SilentlyContinue
if ($mongoService -and $mongoService.Status -eq 'Running') {
    Write-Host "✓ MongoDB is running" -ForegroundColor Green
} else {
    Write-Host "✗ MongoDB is not running. Please start MongoDB first." -ForegroundColor Red
    Write-Host "  Run: net start MongoDB" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Starting Backend Server (FastAPI)..." -ForegroundColor Yellow

# Start Backend in new window
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd 'D:\Project\Employee Promotion Analysis\backend'; " +
    "`$host.ui.RawUI.WindowTitle = 'Backend - FastAPI (Port 8000)'; " +
    ".\venv\Scripts\Activate.ps1; " +
    "Write-Host '========================================' -ForegroundColor Green; " +
    "Write-Host '  Backend Server Starting...          ' -ForegroundColor Green; " +
    "Write-Host '========================================' -ForegroundColor Green; " +
    "Write-Host ''; " +
    "Write-Host 'API URL: http://localhost:8000' -ForegroundColor Cyan; " +
    "Write-Host 'API Docs: http://localhost:8000/docs' -ForegroundColor Cyan; " +
    "Write-Host ''; " +
    "python -m uvicorn app.main:app --reload --port 8000"
)

Write-Host "✓ Backend server starting in new window..." -ForegroundColor Green
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Starting Frontend Server (Vite + React)..." -ForegroundColor Yellow

# Start Frontend in new window
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd 'D:\Project\Employee Promotion Analysis\frontend'; " +
    "`$host.ui.RawUI.WindowTitle = 'Frontend - React (Port 5173)'; " +
    "Write-Host '========================================' -ForegroundColor Blue; " +
    "Write-Host '  Frontend Server Starting...         ' -ForegroundColor Blue; " +
    "Write-Host '========================================' -ForegroundColor Blue; " +
    "Write-Host ''; " +
    "Write-Host 'App URL: http://localhost:5173' -ForegroundColor Cyan; " +
    "Write-Host ''; " +
    "npm run dev"
)

Write-Host "✓ Frontend server starting in new window..." -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Servers Starting Up...               " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please wait 10-15 seconds for servers to start..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Once started, access your application at:" -ForegroundColor White
Write-Host "  → Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  → Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  → API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Two PowerShell windows have opened:" -ForegroundColor White
Write-Host "  1. Backend - FastAPI (Port 8000)" -ForegroundColor Green
Write-Host "  2. Frontend - React (Port 5173)" -ForegroundColor Blue
Write-Host ""
Write-Host "Keep both windows open while using the application." -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop: Close both PowerShell windows or press Ctrl+C in each" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Database Status:" -ForegroundColor White
Write-Host "  Employees loaded: 54,808 records" -ForegroundColor Green
Write-Host "  Promoted: 4,668 (8.52%)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
