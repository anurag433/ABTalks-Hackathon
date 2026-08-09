import json
import re
from typing import Dict, Any, Tuple
from backend.config import settings
from backend.prompts.editorial_prompts import EDITORIAL_EVALUATION_PROMPT

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class EditorialAgent:
    def __init__(self):
        self.openai_client = None
        if settings.OPENAI_API_KEY and OpenAI:
            try:
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception:
                self.openai_client = None

    def evaluate_topic(
        self,
        title: str,
        summary: str,
        url: str,
        source_name: str,
        category: str,
        similarity_score: float = 0.0,
        evolution_status: str = "NOVEL",
        matched_title: str = "",
    ) -> Dict[str, Any]:
        """
        Evaluates a candidate topic using an LLM (if key is present) or a deterministic high-depth NLP heuristic engine.
        """
        if self.openai_client:
            try:
                prompt = EDITORIAL_EVALUATION_PROMPT.format(
                    title=title,
                    source_name=source_name,
                    url=url,
                    summary=summary,
                    category=category,
                    similarity_score=similarity_score,
                    evolution_status=evolution_status,
                    matched_title=matched_title or "None",
                )
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are the Chief Editorial Engine for NexusAI Frontier Research. Output JSON only."},
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                )
                result = json.loads(response.choices[0].message.content)
                return self._normalize_result(result, title, summary, category, similarity_score, evolution_status)
            except Exception:
                pass

        return self._deterministic_evaluation(
            title, summary, url, source_name, category, similarity_score, evolution_status, matched_title
        )

    def _normalize_result(
        self, res: Dict[str, Any], title: str, summary: str, category: str, similarity_score: float, evolution_status: str
    ) -> Dict[str, Any]:
        comp = float(res.get("composite_score", 7.5))
        dec = str(res.get("decision", "ACCEPT")).upper()
        if comp < settings.EDITORIAL_SCORE_THRESHOLD:
            dec = "REJECT"
        if evolution_status == "DUPLICATE":
            dec = "REJECT"
            res["reason"] = "Duplicate: Topic already covered with high semantic similarity."
        return {
            "novelty_score": round(float(res.get("novelty_score", 7.5)), 2),
            "engineering_impact": round(float(res.get("engineering_impact", 8.0)), 2),
            "research_value": round(float(res.get("research_value", 7.8)), 2),
            "community_interest": round(float(res.get("community_interest", 7.5)), 2),
            "confidence_score": round(float(res.get("confidence_score", 8.5)), 2),
            "urgency_score": round(float(res.get("urgency_score", 7.0)), 2),
            "composite_score": round(comp, 2),
            "decision": dec,
            "reason": res.get("reason", "Meets high engineering and architectural standards."),
            "category": res.get("category", category),
        }

    def _deterministic_evaluation(
        self,
        title: str,
        summary: str,
        url: str,
        source_name: str,
        category: str,
        similarity_score: float,
        evolution_status: str,
        matched_title: str,
    ) -> Dict[str, Any]:
        """
        Sophisticated rule-based AI research evaluation engine.
        Analyzes technical keyword density, rejection trigger words, source reliability, and evolution state.
        """
        text = f"{title} {summary} {category}".lower()

        # 1. Check for immediate rejection triggers (Celebrity AI Drama, Hype, Clickbait)
        rejection_triggers = [
            "celebrity", "sam altman", "elon musk", "tweet", "gossip",
            "rumor", "drama", "shocking", "you won't believe", "mind-blowing",
            "stock price", "unsubstantiated", "clickbait", "speculation"
        ]
        for trigger in rejection_triggers:
            if trigger in text:
                return {
                    "novelty_score": 3.2,
                    "engineering_impact": 2.5,
                    "research_value": 2.0,
                    "community_interest": 4.0,
                    "confidence_score": 4.5,
                    "urgency_score": 3.0,
                    "composite_score": 3.1,
                    "decision": "REJECT",
                    "reason": f"Rejected: Low engineering value; detected clickbait/celebrity AI drama ('{trigger}').",
                    "category": category,
                }

        # 2. Check for duplicate topic
        if evolution_status == "DUPLICATE":
            return {
                "novelty_score": 4.0,
                "engineering_impact": 6.5,
                "research_value": 6.0,
                "community_interest": 6.5,
                "confidence_score": 8.5,
                "urgency_score": 4.0,
                "composite_score": 5.8,
                "decision": "REJECT",
                "reason": f"Rejected: Duplicate topic already published in memory ('{matched_title[:40]}...').",
                "category": category,
            }

        # 3. Assess technical keyword density for Engineering & Research Value
        tech_keywords = {
            "cuda": (9.5, 9.0),
            "kernel": (9.0, 8.8),
            "transformer": (8.8, 8.9),
            "attention": (8.7, 9.1),
            "ssm": (9.2, 9.4),
            "mamba": (9.1, 9.3),
            "mixture of experts": (9.0, 9.0),
            "moe": (8.8, 8.8),
            "quantization": (9.2, 8.5),
            "fp8": (9.1, 8.6),
            "int4": (8.9, 8.3),
            "lora": (8.6, 8.4),
            "rlhf": (8.5, 8.8),
            "dpo": (8.7, 8.9),
            "reasoning": (8.9, 9.2),
            "agent": (8.7, 8.6),
            "benchmark": (8.5, 8.5),
            "open source": (8.8, 8.5),
            "weights": (8.9, 8.6),
            "pytorch": (8.6, 8.3),
            "arxiv": (8.8, 9.2),
            "vulnerability": (9.2, 8.9),
            "jailbreak": (8.8, 8.7),
            "robotics": (8.6, 8.8),
            "embodied": (8.7, 8.9),
            "vla": (8.9, 9.1),
        }

        max_eng = 7.2
        max_res = 7.4

        for kw, (eng_w, res_w) in tech_keywords.items():
            if kw in text:
                max_eng = max(max_eng, eng_w)
                max_res = max(max_res, res_w)

        # Boost source trustworthiness
        source_lower = source_name.lower()
        conf_score = 8.5
        if any(s in source_lower for s in ["arxiv", "hugging face", "github", "deepmind", "openai", "anthropic", "meta ai"]):
            conf_score = 9.4

        novelty = 8.6 if evolution_status == "NOVEL" else 7.9
        community = 8.5
        urgency = 8.1 if "security" in text or "vulnerability" in text or "release" in text else 7.5

        composite = (
            0.25 * novelty
            + 0.25 * max_eng
            + 0.20 * max_res
            + 0.15 * conf_score
            + 0.10 * community
            + 0.05 * urgency
        )

        reason = "High engineering impact and scientific novelty for systems architects."
        if evolution_status == "EVOLVING":
            reason = f"Accepted: Significant evolving development on previously covered research ('{matched_title[:35]}...')."

        return {
            "novelty_score": round(novelty, 2),
            "engineering_impact": round(max_eng, 2),
            "research_value": round(max_res, 2),
            "community_interest": round(community, 2),
            "confidence_score": round(conf_score, 2),
            "urgency_score": round(urgency, 2),
            "composite_score": round(composite, 2),
            "decision": "ACCEPT" if composite >= settings.EDITORIAL_SCORE_THRESHOLD else "REJECT",
            "reason": reason,
            "category": category,
        }


editor_agent = EditorialAgent()
