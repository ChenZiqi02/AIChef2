@echo off
setlocal
cd /d "%~dp0"

echo [AIChef] Starting One-Click Setup & Run...
echo ==========================================

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

:: 2. Setup/Connect Virtual Environment
if not exist ".venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate

:: 3. Install Python Dependencies
echo [INFO] Checking Python dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] Failed to install some requirements. Attempting to continue...
)

:: 4. Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js v18+.
    pause
    exit /b
)

:: 5. Install Frontend Dependencies (if needed)
if not exist "frontend\node_modules" (
    echo [INFO] Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

echo.
echo [INFO] All systems go! Starting services...
echo.

:: 6. Launch Backend and Frontend in parallel
:: Use 'start' to open new windows or run in background

:: Start Backend
start "AIChef Backend" cmd /k "call .venv\Scripts\activate && python run.py"

:: Start Frontend
cd frontend
start "AIChef Frontend" cmd /k "npm run dev"

echo [INFO] Backend starting on http://localhost:8000
echo [INFO] Frontend starting on http://localhost:5173
echo.
echo Press any key to close this launcher (services will keep running).
pause
