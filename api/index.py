# Vercel Serverless Function Entrypoint
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app

# Vercel expects the FastAPI application object to be exported as 'app'
__all__ = ["app"]
