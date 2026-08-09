import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.database.models import PublishedPost, RejectedTopic, MemoryNode, AgentStatus, utcnow


class ResearchRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_agent_status(self) -> Dict[str, Any]:
        status = self.db.query(AgentStatus).filter(AgentStatus.id == 1).first()
        if not status:
            status = AgentStatus(id=1, current_phase="IDLE", is_initialized=False, started_at=utcnow())
            self.db.add(status)
            self.db.commit()
            self.db.refresh(status)
        return status.to_dict()

    def update_agent_status(
        self,
        phase: Optional[str] = None,
        status_message: Optional[str] = None,
        incr_discovered: int = 0,
        incr_published: int = 0,
        incr_rejected: int = 0,
        set_initialized: Optional[bool] = None,
        set_last_run: Optional[bool] = None,
        set_next_run: Optional[Any] = None,
        persona_name: Optional[str] = None,
        persona_domain: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        status = self.db.query(AgentStatus).filter(AgentStatus.id == 1).first()
        if not status:
            status = AgentStatus(id=1)
            self.db.add(status)

        if phase is not None:
            status.current_phase = phase
        if status_message is not None:
            status.status_message = status_message
        if incr_discovered > 0:
            status.total_discovered += incr_discovered
        if incr_published > 0:
            status.total_published += incr_published
        if incr_rejected > 0:
            status.total_rejected += incr_rejected
        if set_initialized is not None:
            status.is_initialized = set_initialized
        if set_last_run:
            status.last_run_at = utcnow()
        if set_next_run is not None:
            status.next_run_at = set_next_run
        if persona_name:
            status.persona_name = persona_name
        if persona_domain:
            status.persona_domain = persona_domain
        if agent_id:
            status.agent_id = agent_id

        self.db.commit()
        self.db.refresh(status)
        return status.to_dict()

    def create_published_post(
        self,
        title: str,
        summary: str,
        technical_deep_dive: str,
        why_it_matters: str,
        category: str,
        keywords: List[str],
        sources: List[Any],
        editorial_score: float,
        status: str = "published",
        post_id: Optional[str] = None,
        rationale: str = "",
    ) -> PublishedPost:
        p_id = post_id or str(uuid.uuid4())
        post = PublishedPost(
            id=p_id,
            title=title,
            summary=summary,
            technical_deep_dive=technical_deep_dive,
            why_it_matters=why_it_matters,
            rationale=rationale,
            category=category,
            editorial_score=editorial_score,
            status=status,
            published_at=utcnow(),
        )
        post.keywords = keywords
        post.sources = sources
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_feed_posts(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Returns newest posts first with UTC timestamps."""
        posts = (
            self.db.query(PublishedPost)
            .order_by(desc(PublishedPost.published_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [p.to_dict() for p in posts]

    def get_post_by_id(self, post_id: str) -> Optional[Dict[str, Any]]:
        p = self.db.query(PublishedPost).filter(PublishedPost.id == post_id).first()
        return p.to_dict() if p else None

    def create_rejected_topic(
        self,
        title: str,
        url: str,
        category: str,
        editorial_score: float,
        rejection_reason: str,
    ) -> RejectedTopic:
        r_id = str(uuid.uuid4())
        rejected = RejectedTopic(
            id=r_id,
            title=title,
            url=url,
            category=category,
            editorial_score=editorial_score,
            rejection_reason=rejection_reason,
            rejected_at=utcnow(),
        )
        self.db.add(rejected)
        self.db.commit()
        self.db.refresh(rejected)
        return rejected

    def get_rejected_topics(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        items = (
            self.db.query(RejectedTopic)
            .order_by(desc(RejectedTopic.rejected_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [i.to_dict() for i in items]

    def add_memory_node(
        self, post_id: str, title: str, summary: str, embedding: List[float]
    ) -> MemoryNode:
        m_id = str(uuid.uuid4())
        node = MemoryNode(
            memory_id=m_id,
            post_id=post_id,
            title=title,
            summary=summary,
            created_at=utcnow(),
        )
        node.embedding = embedding
        self.db.add(node)
        self.db.commit()
        self.db.refresh(node)
        return node

    def get_all_memory_nodes(self) -> List[MemoryNode]:
        return self.db.query(MemoryNode).order_by(desc(MemoryNode.created_at)).all()

    def get_memory_timeline(self, limit: int = 30) -> List[Dict[str, Any]]:
        nodes = (
            self.db.query(MemoryNode)
            .order_by(desc(MemoryNode.created_at))
            .limit(limit)
            .all()
        )
        return [n.to_dict() for n in nodes]
