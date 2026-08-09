import os
import logging
from pathlib import Path
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
from backend.config import settings

# REQUIREMENT 13: Verify that the required SQLAlchemy models are imported BEFORE Base.metadata.create_all(...)
from backend.database.models import (
    Base,
    PublishedPost,
    RejectedTopic,
    MemoryNode,
    AgentStatus,
    utcnow,
)

logger = logging.getLogger("nexusai.database")

DATABASE_URL = settings.DATABASE_URL

# Check if SQLite is used
is_sqlite = DATABASE_URL.startswith("sqlite")

engine_kwargs = {}
if is_sqlite:
    # REQUIREMENT 10: Correct SQLite connection arguments
    engine_kwargs["connect_args"] = {"check_same_thread": False}

    # REQUIREMENT 4: Automatically create the database directory before creating the SQLite engine
    # Extract file path from SQLite URL (handles both sqlite:////home/user/... and sqlite:///C:/...)
    url_path = DATABASE_URL.replace("sqlite:///", "")
    if url_path and url_path != ":memory:":
        try:
            db_file_path = Path(url_path).resolve()
            db_dir = db_file_path.parent
            db_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Verified/created SQLite database directory: {db_dir}")
        except Exception as e:
            logger.warning(f"Could not create database directory for {url_path}: {e}")

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    REQUIREMENT 12: Make database initialization idempotent.
    Create all tables and seed the singleton AgentStatus if missing. Auto-migrate missing columns.
    """
    Base.metadata.create_all(bind=engine)
    
    # Idempotent auto-migration check for newly added hackathon columns
    try:
        insp = inspect(engine)
        if "agent_status" in insp.get_table_names():
            cols = [c["name"] for c in insp.get_columns("agent_status")]
            with engine.begin() as conn:
                if "agent_id" not in cols:
                    conn.execute(text("ALTER TABLE agent_status ADD COLUMN agent_id VARCHAR(64) DEFAULT 'agent-nexusai-2026'"))
                if "persona_name" not in cols:
                    conn.execute(text("ALTER TABLE agent_status ADD COLUMN persona_name VARCHAR(64) DEFAULT 'NexusAI'"))
                if "persona_domain" not in cols:
                    conn.execute(text("ALTER TABLE agent_status ADD COLUMN persona_domain VARCHAR(128) DEFAULT 'AI & Technology Research'"))
        
        if "published_posts" in insp.get_table_names():
            cols = [c["name"] for c in insp.get_columns("published_posts")]
            with engine.begin() as conn:
                if "rationale" not in cols:
                    conn.execute(text("ALTER TABLE published_posts ADD COLUMN rationale TEXT DEFAULT ''"))
    except Exception as e:
        # Ignore if DB doesn't support or column already exists
        pass

    db = SessionLocal()
    try:
        status = db.query(AgentStatus).filter(AgentStatus.id == 1).first()
        if not status:
            status = AgentStatus(
                id=1,
                agent_id="agent-nexusai-2026",
                persona_name="NexusAI",
                persona_domain="AI & Technology Research",
                current_phase="IDLE",
                is_initialized=False,
                started_at=utcnow(),
                status_message="System initialized. Ready for autonomous cognitive research loop."
            )
            db.add(status)
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
