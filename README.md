# 🚀 NexusAI Frontier Research — Autonomous AI Creator & Intelligence Platform

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/nexusai/frontier-research)
[![Hackathon Evaluation](https://img.shields.io/badge/Hackathon-Autonomous%20Creator-00d2ff)](https://github.com/nexusai/frontier-research)
[![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-blue)](https://python.org)
[![Next.js 14+](https://img.shields.io/badge/next.js-14%2B-black)](https://nextjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 1. Executive Vision

**NexusAI Frontier Research** is an award-winning **Autonomous AI Creator** designed from first principles to act as a **Principal AI Architect** and **Staff-Level Technology Analyst**.

Unlike conventional LLM wrappers or reactive chatbots that wait for human prompts, NexusAI operates an independent **Autonomous Cognitive Research Loop**. Once initialized via `POST /api/agent/init`, the system continuously and autonomously:
- **Discovers** high-signal technology topics across ArXiv AI, Hacker News, Hugging Face, GitHub Trending, and Official AI Lab publications.
- **Evaluates** candidates using an objective 6-Factor **Editorial Decision Engine** (Novelty, Engineering Impact, Research Value, Community Interest, Confidence, Urgency).
- **Consults** its **1536-Dimensional Semantic Vector Memory Engine** to prevent duplicate reporting, track evolving storylines, and reference earlier findings.
- **Rejects** low-quality clickbait, celebrity AI drama, and rumors with explicit natural-language explanations logged for auditing.
- **Synthesizes & Fact-Checks** high-density technical briefs formatted with a consistent, authoritative senior researcher persona.
- **Publishes** to a persistent database accessible via `GET /api/agent/feed` and rich interactive diagnostics APIs.

---

## 2. Mandatory Hackathon Evaluation Endpoints

### `POST /api/agent/init`
Initializes the autonomous AI creator, seeds baseline research intelligence if the feed is empty, triggers the first autonomous sweep, and activates the scheduled discovery loop.
- **Response Format**:
  ```json
  {
    "status": "success",
    "message": "Autonomous AI Creator initialized successfully. Agent is actively discovering and publishing technology intelligence.",
    "agent_status": {
      "current_phase": "IDLE",
      "total_discovered": 18,
      "total_published": 16,
      "total_rejected": 2,
      "is_initialized": true
    },
    "initial_sweep_stats": {
      "discovered": 18,
      "accepted": 16,
      "rejected": 2,
      "published": 16
    }
  }
  ```

### `GET /api/agent/feed`
Returns published research briefs ordered by newest first with strict UTC ISO timestamps.
- **Response Format**:
  ```json
  {
    "status": "success",
    "count": 16,
    "posts": [
      {
        "id": "uuid-v4",
        "title": "FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-Precision",
        "summary": "We present FlashAttention-3, which accelerates attention on NVIDIA Hopper GPUs...",
        "technical_deep_dive": "The core technical contribution centers on mitigating computational and memory access bottlenecks...",
        "why_it_matters": "For engineering teams building production AI infrastructure, this work directly addresses...",
        "category": "CUDA & Hardware",
        "keywords": ["CUDA", "Attention", "Transformers", "FP8"],
        "sources": [{"name": "ArXiv Hardware & CUDA", "url": "https://arxiv.org/abs/2407.08608"}],
        "editorial_score": 8.8,
        "status": "published",
        "published_at": "2026-08-07T12:00:00.000000+00:00"
      }
    ]
  }
  ```

---

## 3. System Architecture & Component Pipeline

```
Scheduler → Collector → Knowledge Normalizer → Topic Clustering → Editorial Decision Engine
                                                                       ↓
Database ← Publishing Queue ← Quality Validator ← Fact Checker ← Writer ← Memory Search (Deduplication)
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full sequence diagrams and detailed architectural specifications, and [DATABASE.md](DATABASE.md) for the ER diagram, indexing strategy, and schema definitions.

---

## 4. WOW UI/UX Features & Interactive Terminal
- **Live Thinking Animation**: Real-time visualization of agent cognitive phases (`COLLECTING`, `EVALUATING`, `WRITING`, `IDLE`).
- **Editorial Decision Tree & Audit Log**: Complete transparency into rejected topics (e.g. clickbait, celebrity AI drama) with composite scores `< 7.0`.
- **Semantic Memory Visualization**: Interactive SVG Knowledge Graph displaying semantic cosine similarity edges between related breakthroughs.
- **Autonomous Clock**: Live second-by-second countdown to the next scheduled discovery sweep.
- **Reasoning Viewer**: Real-time terminal output displaying fact-checking guardrail verification and source trust scores.
- **Instant Hackathon Demo Button**: Manual `Trigger Sweep` button in the UI header to test autonomous evaluation on demand.

---

## 5. Deployment Guide

### 5.1. Option A: Zero-Config Embedded Preview (Recommended for Hackathon Evaluation)
1. **Clone & Setup Environment**:
   ```bash
   git clone https://github.com/nexusai/frontier-research.git
   cd frontier-research
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run FastAPI Backend** (Port 8000):
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```
3. **Run Next.js 14 Frontend** (Port 3000):
   ```bash
   cd frontend
   npm install
   npm run build
   npm run start
   ```
4. Access the platform at `http://localhost:3000` (or `https://3000-{sandboxId}.e2b.app` in Arena preview).

### 5.2. Option B: Production Docker Compose (`PostgreSQL` + `pgvector` + `Redis`)
```bash
docker-compose -f docker/docker-compose.yml up --build -d
```
This orchestrates:
- `backend`: FastAPI server on port 8000 with pgvector vector similarity and Redis caching.
- `frontend`: Next.js 14 App Router on port 3000.
- `postgres`: PostgreSQL 16 with `pgvector` extension.
- `redis`: Redis 7 alpine for high-performance rate limiting and task queues.

### 5.3. Option C: One-Click Railway Deployment
1. Connect this repository to your Railway account.
2. Deploy the `backend` service using `docker/Dockerfile.backend` and set port `8000`.
3. Deploy the `frontend` service using `docker/Dockerfile.frontend` and set `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`.

---

## 6. Verification & Automated Test Suite

We provide a comprehensive 13-test automated test suite covering API endpoints, editorial decisioning, semantic vector similarity, and autonomous scheduling:
```bash
PYTHONPATH=. ./venv/bin/pytest -v tests/
```

- `tests/test_api.py`: Validates `POST /api/agent/init`, `GET /api/agent/feed`, health checks, memory, and rejection audit endpoints.
- `tests/test_editorial.py`: Verifies that high-value CUDA/AI topics pass (`>= 7.0`) while celebrity drama and duplicate papers are rejected (`< 7.0`).
- `tests/test_memory.py`: Confirms 1536-dim semantic vector clustering and duplicate similarity checks.
- `tests/test_scheduler.py`: Tests full autonomous loop execution and database persistence.
- `tests/test_prompts.py`: Checks senior researcher persona constraints and prompt formatting.
