#!/usr/bin/env bash
set -e

echo "===================================================================="
echo "  NexusAI Frontier Research — One-Click macOS/Linux Launcher"
echo "===================================================================="

echo "[1/3] Checking Python Virtual Environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment (venv)..."
    python3 -m venv venv
fi

echo "[2/3] Installing/Verifying Dependencies in Virtual Environment..."
source venv/bin/activate
python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r requirements.txt

echo "[3/3] Starting NexusAI Frontier API Server on http://localhost:8000..."
echo ""
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
