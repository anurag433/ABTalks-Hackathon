from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.memory.embedder import embedder
from backend.memory.search import MemoryEngine


class VectorStoreService:
    def __init__(self, db: Session):
        self.db = db
        self.engine = MemoryEngine(db)

    def store_post_memory(
        self, post_id: str, title: str, summary: str
    ) -> Dict[str, Any]:
        from backend.database.repository import ResearchRepository
        repo = ResearchRepository(self.db)
        combined = f"{title}. {summary}"
        vec = embedder.embed_text(combined)
        node = repo.add_memory_node(post_id, title, summary, vec)
        return node.to_dict()

    def query_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        return self.engine.search_similar_topics(query, top_k=top_k)

    def check_duplicate(
        self, title: str, summary: str, similarity_threshold: float = 0.85
    ):
        return self.engine.check_duplicate_and_evolution(title, summary, similarity_threshold)

    def get_graph(self, max_nodes: int = 30) -> Dict[str, Any]:
        return self.engine.get_knowledge_graph(max_nodes=max_nodes)
