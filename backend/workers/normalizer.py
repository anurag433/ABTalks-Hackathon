import re
from typing import List, Dict, Any
from urllib.parse import urlparse, urlunparse


def canonicalize_url(url: str) -> str:
    if not url:
        return ""
    try:
        parsed = urlparse(url)
        # Strip tracking queries and fragments
        clean = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
        return clean.rstrip("/")
    except Exception:
        return url


def clean_text(text: str) -> str:
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r"<[^>]+>", "", text)
    # Collapse excess whitespace
    clean = re.sub(r"\s+", " ", clean)
    return clean.strip()


class KnowledgeNormalizer:
    def normalize_items(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Standardizes raw feed items into canonical candidate dictionaries.
        Removes spam, short items, and exact URL duplicates within the batch.
        """
        seen_urls = set()
        seen_titles = set()
        normalized = []

        for item in raw_items:
            title = clean_text(item.get("title", ""))
            url = canonicalize_url(item.get("url", ""))
            summary = clean_text(item.get("summary", ""))
            source_name = item.get("source_name", "AI News Feed")
            category = item.get("category", "AI Research")

            if not title or len(title) < 10:
                continue

            # Deduplicate within batch
            title_key = re.sub(r"[^\w\s]", "", title.lower()).strip()
            if url in seen_urls and url != "":
                continue
            if title_key in seen_titles:
                continue

            if url:
                seen_urls.add(url)
            seen_titles.add(title_key)

            normalized.append({
                "title": title,
                "url": url,
                "summary": summary,
                "source_name": source_name,
                "category": category,
            })

        return normalized


normalizer = KnowledgeNormalizer()
