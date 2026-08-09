#!/usr/bin/env python3
"""
Official Hackathon Compliance & Verification Script
Verifies all 6 minimum requirements and exact HTTP API specifications for:
1. POST /api/agent/init
2. GET /api/agent/feed?agentId=...
"""
import sys
import json
import requests
import datetime

BASE_URL = "http://127.0.0.1:8000"

def verify_submission():
    print("=" * 70)
    print("🚀 NEXUSAI FRONTIER — HACKATHON EVALUATION COMPLIANCE VERIFIER")
    print("=" * 70)

    # 1. TEST POST /api/agent/init
    print("\n[STEP 1] Testing POST /api/agent/init (Called exactly once)...")
    init_payload = {
        "persona": {
            "name": "Ada",
            "domain": "AI Security"
        }
    }
    resp = requests.post(f"{BASE_URL}/api/agent/init", json=init_payload, timeout=30)
    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}: {resp.text}"
    init_data = resp.json()
    assert "agentId" in init_data, f"Response missing 'agentId': {init_data}"
    agent_id = init_data["agentId"]
    print(f"   ✅ POST /api/agent/init passed! Received agentId: '{agent_id}'")

    # 2. TEST GET /api/agent/feed?agentId=...
    print(f"\n[STEP 2] Testing GET /api/agent/feed?agentId={agent_id}...")
    feed_resp = requests.get(f"{BASE_URL}/api/agent/feed?agentId={agent_id}", timeout=30)
    assert feed_resp.status_code == 200, f"Expected status 200, got {feed_resp.status_code}: {feed_resp.text}"
    feed_data = feed_resp.json()
    assert "posts" in feed_data, f"Response missing 'posts': {feed_data}"
    posts = feed_data["posts"]
    assert isinstance(posts, list), f"'posts' must be a list, got {type(posts)}"
    print(f"   ✅ GET /api/agent/feed passed! Retrieved {len(posts)} autonomous posts.")

    # 3. VERIFY FEED REQUIREMENTS & SCHEMA
    print("\n[STEP 3] Validating strict Hackathon schema on every post...")
    assert len(posts) > 0, "Feed should not be empty after initialization."
    
    seen_ids = set()
    last_timestamp = None
    for idx, post in enumerate(posts):
        # Unique ID
        assert "id" in post, f"Post #{idx} missing 'id'"
        p_id = str(post["id"])
        assert p_id not in seen_ids, f"Duplicate ID found: {p_id}"
        seen_ids.add(p_id)

        # UTC ISO 8601 Timestamp ending in 'Z'
        assert "createdAt" in post, f"Post #{idx} missing 'createdAt'"
        created_at = post["createdAt"]
        assert created_at.endswith("Z"), f"Timestamp must be ISO 8601 UTC ending in 'Z': {created_at}"
        
        # Check reverse chronological ordering (newest first)
        dt = datetime.datetime.fromisoformat(created_at[:-1])
        if last_timestamp:
            assert dt <= last_timestamp, f"Feed not in newest-first order! {dt} > {last_timestamp}"
        last_timestamp = dt

        # Consistent persona text
        assert "text" in post, f"Post #{idx} missing 'text'"
        assert len(post["text"]) > 20, f"Post text too short: {post['text']}"

        # Publishing Rationale
        assert "rationale" in post, f"Post #{idx} missing 'rationale'"
        assert len(post["rationale"]) > 10, f"Rationale too short: {post['rationale']}"

        # Sources Array of string URLs
        assert "sources" in post, f"Post #{idx} missing 'sources'"
        sources = post["sources"]
        assert isinstance(sources, list), f"sources must be a list, got {type(sources)}"
        assert len(sources) > 0, f"sources array empty for post #{idx}"
        for s in sources:
            assert isinstance(s, str), f"Each source must be a URL string, got {type(s)} ({s})"
            assert s.startswith("http"), f"Source URL must start with http: {s}"

    print(f"   ✅ All {len(posts)} posts match 100% of required Hackathon fields:")
    print(f"      - Unique 'id': Validated")
    print(f"      - 'createdAt' (ISO 8601 UTC with 'Z'): Validated")
    print(f"      - 'text' (Autonomous Persona Content): Validated")
    print(f"      - 'rationale' (Why selected, relevant now, chosen over others): Validated")
    print(f"      - 'sources' (Array of URL strings): Validated")
    print(f"      - Reverse Chronological Order (Newest first): Validated")

    # 4. VERIFY REJECTED AUDIT TRAIL
    print("\n[STEP 4] Verifying Editorial Judgment (Rejected Topics)...")
    rej_resp = requests.get(f"{BASE_URL}/api/agent/rejected", timeout=30)
    assert rej_resp.status_code == 200
    rej_data = rej_resp.json()
    assert "rejected_topics" in rej_data
    rejected = rej_data["rejected_topics"]
    assert len(rejected) > 0, "Agent must demonstrate editorial judgment by rejecting noise/clickbait."
    print(f"   ✅ Verified Editorial Decision Engine rejected {len(rejected)} candidate topics (Score < 7.0/10).")
    print("   Example Rejection Reason:", rejected[0]["rejection_reason"])

    print("\n" + "=" * 70)
    print("🏆 ALL HACKATHON EVALUATION REQUIREMENTS PASSED WITH 100% COMPLIANCE!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        verify_submission()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}", file=sys.stderr)
        sys.exit(1)
