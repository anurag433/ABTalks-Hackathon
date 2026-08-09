import pytest
from backend.agents.editor import editor_agent


def test_editorial_accepts_high_impact_cuda_topic():
    result = editor_agent.evaluate_topic(
        title="FlashAttention-3: Asynchrony and Low-Precision Tensor Core Acceleration",
        summary="A novel attention algorithm on NVIDIA Hopper GPUs achieving 740 TFLOPs/s in FP16/FP8.",
        url="https://arxiv.org/abs/2407.08608",
        source_name="ArXiv Hardware",
        category="CUDA & Hardware",
    )
    assert result["composite_score"] >= 7.0
    assert result["decision"] == "ACCEPT"
    assert result["engineering_impact"] >= 8.0


def test_editorial_rejects_celebrity_ai_drama():
    result = editor_agent.evaluate_topic(
        title="Sam Altman posts enigmatic tweet about secret AGI timeline",
        summary="Social media users speculate after OpenAI CEO posts cryptic message online.",
        url="https://example.com/gossip",
        source_name="AI Gossip",
        category="Celebrity AI Drama",
    )
    assert result["composite_score"] < 7.0
    assert result["decision"] == "REJECT"
    assert "celebrity" in result["reason"].lower() or "clickbait" in result["reason"].lower()


def test_editorial_rejects_duplicate_topic():
    result = editor_agent.evaluate_topic(
        title="FlashAttention-3: Asynchrony and Low-Precision",
        summary="Same attention algorithm already covered in prior research brief.",
        url="https://arxiv.org/abs/2407.08608",
        source_name="ArXiv",
        category="CUDA & Hardware",
        similarity_score=0.92,
        evolution_status="DUPLICATE",
        matched_title="FlashAttention-3: Fast and Accurate Attention",
    )
    assert result["decision"] == "REJECT"
    assert "duplicate" in result["reason"].lower()
