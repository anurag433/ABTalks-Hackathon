import pytest
from backend.prompts import (
    NEXUSAI_SYSTEM_PERSONA,
    EDITORIAL_EVALUATION_PROMPT,
    WRITER_SYNTHESIS_PROMPT,
    FACT_CHECKER_PROMPT,
    TOPIC_RANKING_PROMPT,
)


def test_persona_principles():
    assert "NEVER use marketing hype" in NEXUSAI_SYSTEM_PERSONA
    assert "Senior engineering persona" in NEXUSAI_SYSTEM_PERSONA or "senior engineering persona" in NEXUSAI_SYSTEM_PERSONA.lower()
    assert "NEVER publish celebrity AI drama" in NEXUSAI_SYSTEM_PERSONA


def test_prompt_formatting():
    formatted_editor = EDITORIAL_EVALUATION_PROMPT.format(
        title="Test Title",
        source_name="ArXiv",
        url="https://arxiv.org",
        summary="Test Summary",
        category="CUDA",
        similarity_score=0.1,
        evolution_status="NOVEL",
        matched_title="None",
    )
    assert "Test Title" in formatted_editor
    assert "novelty_score" in formatted_editor
    assert "composite_score < 7.0" in formatted_editor
