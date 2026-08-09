@echo off
echo ====================================================================
echo   NexusAI Frontier Research — One-Click Windows Launcher
echo ====================================================================

echo [1/3] Checking Python Virtual Environment...
if not exist venv (
    echo Creating virtual environment (venv)...
    python -m venv venv
)

echo [2/3] Installing/Verifying Dependencies in Virtual Environment...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt

echo [3/3] Starting NexusAI Frontier API Server on http://localhost:8000...
echo.
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
pause
