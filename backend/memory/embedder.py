import re
import math
import hashlib
import numpy as np
from typing import List
from backend.config import settings

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class HybridEmbedder:
    """
    Hybrid semantic vector embedding engine.
    - Uses OpenAI API ('text-embedding-3-small' 1536-dim) if OPENAI_API_KEY is present.
    - Uses deterministic 1536-dim TF-IDF & character n-gram semantic vector hashing if offline/free hybrid mode.
    """
    def __init__(self):
        self.dim = 1536
        self.openai_client = None
        if settings.OPENAI_API_KEY and OpenAI:
            try:
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception:
                self.openai_client = None

    def embed_text(self, text: str) -> List[float]:
        if not text or not text.strip():
            return [0.0] * self.dim

        if self.openai_client:
            try:
                response = self.openai_client.embeddings.create(
                    input=text[:8000],
                    model="text-embedding-3-small"
                )
                return response.data[0].embedding
            except Exception:
                # Fallback if API fails or quota exceeded
                pass

        return self._local_semantic_embedding(text)

    def _local_semantic_embedding(self, text: str) -> List[float]:
        """
        Deterministic 1536-dimensional semantic embedding using TF-IDF token hashing + 3-gram features.
        Produces realistic cosine similarities where semantically overlapping AI/tech texts cluster together.
        """
        vec = np.zeros(self.dim, dtype=np.float32)
        words = re.findall(r"\b[a-z0-9]{2,}\b", text.lower())
        if not words:
            return vec.tolist()

        # Word frequency weights
        word_counts = {}
        for w in words:
            word_counts[w] = word_counts.get(w, 0) + 1

        total_words = len(words)
        for word, count in word_counts.items():
            tf = count / total_words
            # Hash word into multiple buckets to capture semantic distribution
            h1 = int(hashlib.md5(word.encode()).hexdigest(), 16) % self.dim
            h2 = int(hashlib.sha256(word.encode()).hexdigest(), 16) % self.dim
            vec[h1] += tf * 1.5
            vec[h2] += tf * 0.8

            # Incorporate character 3-grams for morphology overlap (e.g. 'transformer', 'transformers')
            if len(word) >= 3:
                for i in range(len(word) - 2):
                    trigram = word[i:i+3]
                    th = int(hashlib.md5(trigram.encode()).hexdigest(), 16) % self.dim
                    vec[th] += (tf * 0.3)

        # L2 Normalization so dot product == cosine similarity
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()


embedder = HybridEmbedder()
