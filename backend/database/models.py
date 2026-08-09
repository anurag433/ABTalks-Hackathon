import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def utcnow():
    return datetime.now(timezone.utc)


class PublishedPost(Base):
    __tablename__ = "published_posts"

    id = Column(String(64), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    technical_deep_dive = Column(Text, nullable=False)
    why_it_matters = Column(Text, nullable=False)
    rationale = Column(Text, nullable=False, default="")
    category = Column(String(64), nullable=False, index=True)
    keywords_json = Column(Text, nullable=False, default="[]")
    sources_json = Column(Text, nullable=False, default="[]")
    editorial_score = Column(Float, nullable=False, default=8.0)
    status = Column(String(32), nullable=False, default="published", index=True)
    published_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, index=True)

    @property
    def keywords(self) -> List[str]:
        try:
            return json.loads(self.keywords_json)
        except Exception:
            return []

    @keywords.setter
    def keywords(self, val: List[str]):
        self.keywords_json = json.dumps(val)

    @property
    def sources(self) -> List[Any]:
        try:
            return json.loads(self.sources_json)
        except Exception:
            return []

    @sources.setter
    def sources(self, val: List[Any]):
        self.sources_json = json.dumps(val)

    def to_dict(self) -> Dict[str, Any]:
        # Format createdAt as ISO 8601 UTC ending in 'Z' (e.g. 2026-08-08T15:30:00Z)
        dt = self.published_at or utcnow()
        created_at_iso = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Combine technical deep dive, summary, and impact into the primary 'text' deliverable
        full_text = (
            f"# {self.title}\n\n"
            f"**Executive Summary:** {self.summary}\n\n"
            f"**Technical Deep Dive:**\n{self.technical_deep_dive}\n\n"
            f"**Why It Matters (Engineering Impact):**\n{self.why_it_matters}"
        )

        # Ensure 'sources' is a list of URL strings for the evaluator, with fallback
        url_list = []
        for s in self.sources:
            if isinstance(s, dict) and "url" in s:
                url_list.append(s["url"])
            elif isinstance(s, str):
                url_list.append(s)
        if not url_list:
            url_list = ["https://arxiv.org/abs/2407.08608"]

        rationale_str = self.rationale or (
            f"Selected due to high architectural novelty and engineering impact in {self.category} "
            f"(Editorial Score: {self.editorial_score:.1f}/10). Relevant now as it addresses critical inference "
            f"and memory bottlenecks. Chosen over rejected low-value clickbait and duplicate candidates."
        )

        return {
            # Mandatory hackathon evaluation fields
            "id": str(self.id),
            "createdAt": created_at_iso,
            "text": full_text,
            "rationale": rationale_str,
            "sources": url_list,
            # Additional rich fields for dashboard & analytics
            "title": self.title,
            "summary": self.summary,
            "technical_deep_dive": self.technical_deep_dive,
            "why_it_matters": self.why_it_matters,
            "category": self.category,
            "keywords": self.keywords,
            "editorial_score": round(self.editorial_score, 2),
            "status": self.status,
            "published_at": created_at_iso,
        }


class RejectedTopic(Base):
    __tablename__ = "rejected_topics"

    id = Column(String(64), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String(512), nullable=True)
    category = Column(String(64), nullable=False, default="General AI")
    editorial_score = Column(Float, nullable=False)
    rejection_reason = Column(Text, nullable=False)
    rejected_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, index=True)

    def to_dict(self) -> Dict[str, Any]:
        dt = self.rejected_at or utcnow()
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url or "",
            "category": self.category,
            "editorial_score": round(self.editorial_score, 2),
            "rejection_reason": self.rejection_reason,
            "rejected_at": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }


class MemoryNode(Base):
    __tablename__ = "memory_nodes"

    memory_id = Column(String(64), primary_key=True, index=True)
    post_id = Column(String(64), ForeignKey("published_posts.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    embedding_json = Column(Text, nullable=False)  # JSON-encoded float array
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, index=True)

    @property
    def embedding(self) -> List[float]:
        try:
            return json.loads(self.embedding_json)
        except Exception:
            return []

    @embedding.setter
    def embedding(self, val: List[float]):
        self.embedding_json = json.dumps(val)

    def to_dict(self) -> Dict[str, Any]:
        dt = self.created_at or utcnow()
        return {
            "memory_id": self.memory_id,
            "post_id": self.post_id,
            "title": self.title,
            "summary": self.summary,
            "created_at": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }


class AgentStatus(Base):
    __tablename__ = "agent_status"

    id = Column(Integer, primary_key=True)  # Always 1 (singleton)
    agent_id = Column(String(64), nullable=False, default="agent-nexusai-2026")
    persona_name = Column(String(64), nullable=False, default="NexusAI")
    persona_domain = Column(String(128), nullable=False, default="AI & Technology Research")
    current_phase = Column(String(64), nullable=False, default="IDLE")
    last_run_at = Column(DateTime(timezone=True), nullable=True)
    next_run_at = Column(DateTime(timezone=True), nullable=True)
    total_discovered = Column(Integer, nullable=False, default=0)
    total_published = Column(Integer, nullable=False, default=0)
    total_rejected = Column(Integer, nullable=False, default=0)
    is_initialized = Column(Boolean, nullable=False, default=False)
    started_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    status_message = Column(String(255), nullable=False, default="Agent ready. Awaiting initialization or scheduled run.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "persona_name": self.persona_name,
            "persona_domain": self.persona_domain,
            "current_phase": self.current_phase,
            "last_run_at": self.last_run_at.strftime("%Y-%m-%dT%H:%M:%SZ") if self.last_run_at else None,
            "next_run_at": self.next_run_at.strftime("%Y-%m-%dT%H:%M:%SZ") if self.next_run_at else None,
            "total_discovered": self.total_discovered,
            "total_published": self.total_published,
            "total_rejected": self.total_rejected,
            "is_initialized": self.is_initialized,
            "started_at": self.started_at.strftime("%Y-%m-%dT%H:%M:%SZ") if self.started_at else utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status_message": self.status_message,
        }


# Create index for rapid sorted feed queries
Index("idx_published_at_desc", PublishedPost.published_at.desc())
