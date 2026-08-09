import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database.session import init_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    init_db()


def test_health_check():
    response = client.get("/api/agent/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "NexusAI" in data["service"]


def test_hackathon_init_endpoint():
    """REQUIRED HACKATHON ENDPOINT 1: POST /api/agent/init"""
    payload = {
        "persona": {
            "name": "Ada",
            "domain": "AI Security"
        }
    }
    response = client.post("/api/agent/init", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "agentId" in data
    assert "ai-security" in data["agentId"].lower() or "agent" in data["agentId"].lower()
    assert data["status"] == "success"


def test_hackathon_feed_endpoint():
    """REQUIRED HACKATHON ENDPOINT 2: GET /api/agent/feed?agentId=..."""
    response = client.get("/api/agent/feed?agentId=agent-ai-security-01")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    posts = data["posts"]
    assert isinstance(posts, list)
    assert len(posts) > 0

    first_post = posts[0]
    # Mandatory Hackathon evaluation fields check
    assert "id" in first_post
    assert "createdAt" in first_post
    assert first_post["createdAt"].endswith("Z")
    assert "text" in first_post
    assert len(first_post["text"]) > 20
    assert "rationale" in first_post
    assert "Why Selected:" in first_post["rationale"] or "Why" in first_post["rationale"]
    assert "sources" in first_post
    assert isinstance(first_post["sources"], list)
    for src in first_post["sources"]:
        assert isinstance(src, str)
        assert src.startswith("http")


def test_get_rejected_topics():
    response = client.get("/api/agent/rejected")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "rejected_topics" in data
    for item in data["rejected_topics"]:
        assert item["editorial_score"] < 7.0
        assert len(item["rejection_reason"]) > 5


def test_get_semantic_memory():
    response = client.get("/api/agent/memory")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "timeline" in data
    assert "knowledge_graph" in data
    graph = data["knowledge_graph"]
    assert "nodes" in graph
    assert "edges" in graph
