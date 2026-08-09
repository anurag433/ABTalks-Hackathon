# Topic Ranking Prompt Template

TOPIC_RANKING_PROMPT = """
You are the Prioritization Engine for NexusAI Frontier Research.
Given a batch of accepted candidate topics, rank them by overall architectural significance and publication urgency.

CANDIDATES:
{candidates_json}

Return a JSON array of candidate IDs ordered from highest priority to lowest priority, along with a brief explanation of why the top candidate was ranked #1.
"""
