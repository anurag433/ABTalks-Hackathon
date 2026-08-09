import logging
import threading
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from backend.config import settings
from backend.database.session import SessionLocal, utcnow
from backend.database.repository import ResearchRepository
from backend.workers.collectors import collector
from backend.agents.editor import editor_agent
from backend.agents.writer import writer_agent
from backend.agents.fact_checker import fact_checker_agent
from backend.memory.vector_store import VectorStoreService

logger = logging.getLogger("nexusai.scheduler")


class AutonomousResearchScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False
        self.interval_minutes = settings.SCHEDULE_INTERVAL_MINUTES
        self.lock = threading.Lock()

    def start(self):
        if not self.is_running:
            try:
                self.scheduler.add_job(
                    self.scheduled_sweep_wrapper,
                    "interval",
                    minutes=self.interval_minutes,
                    id="autonomous_research_loop",
                    replace_existing=True,
                )
                self.scheduler.start()
                self.is_running = True
                logger.info("Autonomous research scheduler started.")
            except Exception as e:
                logger.warning(f"Scheduler start warning: {e}")

    def stop(self):
        if self.is_running:
            try:
                self.scheduler.shutdown(wait=False)
            except Exception:
                pass
            self.is_running = False
            logger.info("Autonomous research scheduler stopped.")

    def scheduled_sweep_wrapper(self):
        """Wrapper for periodic background scheduler execution."""
        if not self.lock.acquire(blocking=False):
            logger.info("Sweep skipped: another sweep is currently in progress.")
            return
        try:
            self.run_sweep_sync()
        finally:
            self.lock.release()

    def trigger_immediate_sweep(self) -> Dict[str, Any]:
        """Manual API trigger for instant hackathon evaluation demo."""
        if not self.lock.acquire(blocking=False):
            return {"status": "busy", "message": "Autonomous sweep already in progress."}
        try:
            stats = self.run_sweep_sync()
            return {"status": "completed", "stats": stats}
        finally:
            self.lock.release()

    def run_sweep_sync(self) -> Dict[str, Any]:
        """
        Core autonomous research sweep:
        Collect -> Evaluate -> Query Memory -> Reject/Accept -> Write -> Fact Check -> Publish -> Index Memory.
        """
        db = SessionLocal()
        repo = ResearchRepository(db)
        vector_store = VectorStoreService(db)

        stats = {
            "discovered": 0,
            "accepted": 0,
            "rejected": 0,
            "published": 0,
            "errors": 0,
        }

        try:
            now = utcnow()
            next_run = now + timedelta(minutes=self.interval_minutes)
            repo.update_agent_status(
                phase="COLLECTING",
                status_message="Autonomous discovery sweep: collecting candidate topics across RSS & APIs...",
                set_last_run=True,
                set_next_run=next_run,
            )

            # 1. Collect candidate topics
            candidates = collector.collect_all_sources()
            stats["discovered"] = len(candidates)

            repo.update_agent_status(
                phase="EVALUATING",
                status_message=f"Editorial Engine evaluating {len(candidates)} candidate topics against standards...",
            )

            # 2. Process each candidate
            for cand in candidates:
                title = cand["title"]
                summary = cand["summary"]
                url = cand["url"]
                source_name = cand["source_name"]
                category = cand["category"]

                # Memory Check: is duplicate or evolving?
                is_dup, matched_post, sim_score, evo_status, related_list = vector_store.check_duplicate(
                    title, summary, similarity_threshold=settings.DUPLICATE_SIMILARITY_THRESHOLD
                )
                matched_title = matched_post["title"] if matched_post else ""

                # Editorial Decision Engine
                eval_res = editor_agent.evaluate_topic(
                    title=title,
                    summary=summary,
                    url=url,
                    source_name=source_name,
                    category=category,
                    similarity_score=sim_score,
                    evolution_status=evo_status,
                    matched_title=matched_title,
                )

                decision = eval_res["decision"]
                reason = eval_res["reason"]
                composite_score = eval_res["composite_score"]

                if decision == "REJECT":
                    # Record rejection for audit & transparency
                    repo.create_rejected_topic(
                        title=title,
                        url=url,
                        category=eval_res.get("category", category),
                        editorial_score=composite_score,
                        rejection_reason=reason,
                    )
                    stats["rejected"] += 1
                else:
                    stats["accepted"] += 1
                    # Senior AI Researcher Writer Synthesis
                    repo.update_agent_status(
                        phase="WRITING",
                        status_message=f"Staff AI Researcher synthesizing brief: '{title[:35]}...' ({evo_status})",
                    )
                    draft = writer_agent.write_post(
                        title=title,
                        summary=summary,
                        url=url,
                        source_name=source_name,
                        category=eval_res.get("category", category),
                        editorial_score=composite_score,
                        evolution_status=evo_status,
                        related_title=matched_title,
                    )

                    # Fact-Checker Guardrail
                    verified_draft = fact_checker_agent.verify_and_sanitize(draft, summary)

                    # Commit to database
                    published_post = repo.create_published_post(
                        title=verified_draft["title"],
                        summary=verified_draft["summary"],
                        technical_deep_dive=verified_draft["technical_deep_dive"],
                        why_it_matters=verified_draft["why_it_matters"],
                        rationale=verified_draft.get("rationale", ""),
                        category=verified_draft["category"],
                        keywords=verified_draft["keywords"],
                        sources=verified_draft["sources"],
                        editorial_score=composite_score,
                        status="published",
                    )

                    # Index in Vector Memory
                    vector_store.store_post_memory(
                        post_id=published_post.id,
                        title=published_post.title,
                        summary=f"{published_post.summary} {published_post.why_it_matters}",
                    )

                    stats["published"] += 1

            # Sweep complete
            repo.update_agent_status(
                phase="IDLE",
                status_message=f"Autonomous loop completed. Published {stats['published']} briefs, rejected {stats['rejected']} noise items.",
                incr_discovered=stats["discovered"],
                incr_published=stats["published"],
                incr_rejected=stats["rejected"],
                set_initialized=True,
            )

        except Exception as e:
            stats["errors"] += 1
            logger.error(f"Error during autonomous research sweep: {e}", exc_info=True)
            repo.update_agent_status(
                phase="IDLE",
                status_message=f"Autonomous loop paused after encounter: {str(e)[:100]}",
            )
        finally:
            db.close()

        return stats

    def initialize_agent(
        self,
        persona: Optional[Dict[str, str]] = None,
        db: Any = None,
    ) -> Dict[str, Any]:
        """
        Implements POST /api/agent/init logic:
        - Accepts optional persona (name, domain).
        - Seeds baseline knowledge if feed is empty.
        - Triggers the first autonomous sweep and starts scheduler.
        """
        session_created = False
        if db is None:
            db = SessionLocal()
            session_created = True

        try:
            repo = ResearchRepository(db)
            status = repo.get_agent_status()
            
            p_name = "NexusAI"
            p_domain = "AI & Technology Research"
            if persona and isinstance(persona, dict):
                p_name = persona.get("name", p_name)
                p_domain = persona.get("domain", p_domain)

            # Generate semantic agentId based on persona domain
            clean_domain = p_domain.lower().replace(" ", "-").replace("&", "").replace("--", "-")
            agent_id = f"agent-{clean_domain}-01"

            # Run initial autonomous sweep
            stats = self.run_sweep_sync()

            status = repo.update_agent_status(
                phase="IDLE",
                status_message=f"Autonomous Agent '{p_name}' ({p_domain}) initialized. Loop active.",
                set_initialized=True,
                set_last_run=True,
                persona_name=p_name,
                persona_domain=p_domain,
                agent_id=agent_id,
            )

            # Start scheduler if not already running
            self.start()

            return {
                "agentId": agent_id,
                "status": "success",
                "message": f"Autonomous AI Creator '{p_name}' initialized successfully in domain '{p_domain}'.",
                "agent_status": status,
                "initial_sweep_stats": stats,
            }
        finally:
            if session_created:
                db.close()


autonomous_scheduler = AutonomousResearchScheduler()
