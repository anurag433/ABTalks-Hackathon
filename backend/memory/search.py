import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from backend.database.models import MemoryNode, PublishedPost
from backend.memory.embedder import embedder


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    arr1 = np.array(v1, dtype=np.float32)
    arr2 = np.array(v2, dtype=np.float32)
    n1 = np.linalg.norm(arr1)
    n2 = np.linalg.norm(arr2)
    if n1 == 0 or n2 == 0:
        return 0.0
    return float(np.dot(arr1, arr2) / (n1 * n2))


class MemoryEngine:
    def __init__(self, db: Session):
        self.db = db

    def search_similar_topics(
        self, query_text: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        query_vec = embedder.embed_text(query_text)
        nodes = self.db.query(MemoryNode).all()
        if not nodes:
            return []

        scored = []
        for n in nodes:
            sim = cosine_similarity(query_vec, n.embedding)
            scored.append((sim, n))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for sim, n in scored[:top_k]:
            results.append({
                "memory_id": n.memory_id,
                "post_id": n.post_id,
                "title": n.title,
                "summary": n.summary,
                "similarity_score": round(sim, 4),
                "created_at": n.created_at.isoformat() if n.created_at else None,
            })
        return results

    def check_duplicate_and_evolution(
        self, title: str, summary: str, similarity_threshold: float = 0.85
    ) -> Tuple[bool, Optional[Dict[str, Any]], float, str, List[Dict[str, Any]]]:
        """
        Returns:
            (is_duplicate, matched_post_dict, max_similarity, evolution_status, related_posts_list)
        evolution_status:
            - 'DUPLICATE': Duplicate of an already published topic
            - 'EVOLVING': Related to an earlier publication (new update / development)
            - 'NOVEL': Entirely new topic
        """
        combined_text = f"{title}. {summary}"
        matches = self.search_similar_topics(combined_text, top_k=5)
        if not matches:
            return False, None, 0.0, "NOVEL", []

        top_match = matches[0]
        max_sim = top_match["similarity_score"]

        # Retrieve the actual published post for the top match
        matched_post = None
        if top_match["post_id"]:
            p = (
                self.db.query(PublishedPost)
                .filter(PublishedPost.id == top_match["post_id"])
                .first()
            )
            if p:
                matched_post = p.to_dict()

        related_posts = matches

        # Check for title similarity or high semantic overlap
        title_words = set(title.lower().split())
        match_title_words = set(top_match["title"].lower().split()) if top_match else set()
        overlap = len(title_words.intersection(match_title_words)) / max(1, len(title_words))

        if max_sim >= similarity_threshold or (max_sim >= 0.75 and overlap >= 0.70):
            # Check if it's an evolving story (e.g. 'v2', 'release', 'update', 'benchmark')
            evolution_keywords = {"v2", "v3", "2.0", "3.0", "update", "benchmark", "results", "follow-up"}
            title_lower = title.lower()
            if any(kw in title_lower for kw in evolution_keywords):
                return False, matched_post, max_sim, "EVOLVING", related_posts
            return True, matched_post, max_sim, "DUPLICATE", related_posts

        if max_sim >= 0.60:
            return False, matched_post, max_sim, "EVOLVING", related_posts

        return False, None, max_sim, "NOVEL", related_posts

    def get_knowledge_graph(self, max_nodes: int = 30) -> Dict[str, Any]:
        """
        Constructs a Knowledge Graph of memory nodes and semantic edges for WOW UI/UX visualization.
        """
        nodes = self.db.query(MemoryNode).order_by(MemoryNode.created_at.desc()).limit(max_nodes).all()
        graph_nodes = []
        graph_edges = []

        for idx, n in enumerate(nodes):
            post = self.db.query(PublishedPost).filter(PublishedPost.id == n.post_id).first()
            category = post.category if post else "AI Research"
            graph_nodes.append({
                "id": n.memory_id,
                "label": n.title[:45] + ("..." if len(n.title) > 45 else ""),
                "full_title": n.title,
                "category": category,
                "created_at": n.created_at.isoformat() if n.created_at else None,
                "post_id": n.post_id,
            })

        # Compute semantic edges between nodes with similarity > 0.55
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                sim = cosine_similarity(nodes[i].embedding, nodes[j].embedding)
                if sim > 0.55:
                    graph_edges.append({
                        "source": nodes[i].memory_id,
                        "target": nodes[j].memory_id,
                        "weight": round(sim, 2),
                    })

        return {
            "nodes": graph_nodes,
            "edges": graph_edges,
            "total_nodes": len(graph_nodes),
            "total_edges": len(graph_edges),
        }
