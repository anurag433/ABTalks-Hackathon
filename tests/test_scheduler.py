import pytest
from backend.schedulers.autonomous_loop import autonomous_scheduler
from backend.database.session import SessionLocal
from backend.database.repository import ResearchRepository


def test_autonomous_sweep_execution():
    """Verifies that an autonomous sweep collects, evaluates, and publishes without human prompts."""
    stats = autonomous_scheduler.run_sweep_sync()
    assert "discovered" in stats
    assert "accepted" in stats
    assert "rejected" in stats
    assert "published" in stats
    assert stats["errors"] == 0

    db = SessionLocal()
    try:
        repo = ResearchRepository(db)
        status = repo.get_agent_status()
        assert status["total_discovered"] >= stats["discovered"]
        assert status["current_phase"] == "IDLE"
    finally:
        db.close()
