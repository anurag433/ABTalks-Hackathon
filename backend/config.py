import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Robust absolute project root directory using pathlib.Path (works on Windows, Linux, Docker, macOS)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# On Vercel Serverless, only /tmp is writable. Otherwise use data/ folder inside project root.
if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    DEFAULT_DB_FILE = Path("/tmp") / "nexusai_frontier.db"
else:
    DEFAULT_DB_DIR = PROJECT_ROOT / "data"
    DEFAULT_DB_FILE = DEFAULT_DB_DIR / "nexusai_frontier.db"

# Format valid SQLAlchemy SQLite URL (works across Windows C:/..., macOS, Linux, Vercel, and Docker)
DEFAULT_SQLITE_URL = f"sqlite:///{DEFAULT_DB_FILE.resolve().as_posix()}"


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "NexusAI Frontier Research"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = "production"
    
    # API & Key Configurations
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY", "")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY", "")
    
    # Database Settings (Environment-driven: SQLite for local preview/fallback, PostgreSQL + pgvector for production)
    DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
    USE_EMBEDDED_MODE: bool = True
    
    # Scheduler Settings
    SCHEDULE_INTERVAL_MINUTES: int = int(os.getenv("SCHEDULE_INTERVAL_MINUTES", "15"))
    EVALUATION_DEMO_MODE: bool = True  # Allows rapid 60s sweeps or manual API triggers
    
    # Editorial Thresholds
    EDITORIAL_SCORE_THRESHOLD: float = 7.0
    DUPLICATE_SIMILARITY_THRESHOLD: float = 0.85
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
