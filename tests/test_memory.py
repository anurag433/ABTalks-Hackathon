import pytest
from backend.memory.embedder import embedder
from backend.memory.search import cosine_similarity
from backend.database.session import SessionLocal
from backend.memory.vector_store import VectorStoreService


def test_local_semantic_embedding_properties():
    text1 = "Transformer self-attention architecture with CUDA kernel optimization."
    text2 = "CUDA kernel optimizations for Transformer attention mechanisms."
    text3 = "Sam Altman posts enigmatic tweet about secret AGI timeline."

    vec1 = embedder.embed_text(text1)
    vec2 = embedder.embed_text(text2)
    vec3 = embedder.embed_text(text3)

    assert len(vec1) == 1536
    assert len(vec2) == 1536

    sim_1_2 = cosine_similarity(vec1, vec2)
    sim_1_3 = cosine_similarity(vec1, vec3)

    # Semantically similar tech texts must have much higher cosine similarity than unrelated gossip
    assert sim_1_2 > sim_1_3
    assert sim_1_2 > 0.50


def test_vector_store_duplicate_check():
    db = SessionLocal()
    try:
        vs = VectorStoreService(db)
        is_dup, matched, sim_score, evo_status, related = vs.check_duplicate(
            title="Unrelated Topic Completely Novel",
            summary="This summary shares no semantic overlap with existing CUDA or Robotics papers.",
        )
        assert is_dup is False
        assert evo_status in ["NOVEL", "EVOLVING"]
    finally:
        db.close()
