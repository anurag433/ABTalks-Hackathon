"use client";

import React, { useState } from "react";
import { PublishedPost } from "@/types";
import { 
  FileText, 
  ExternalLink, 
  ShieldCheck, 
  ChevronDown, 
  ChevronUp, 
  Tag, 
  Clock, 
  Award, 
  Layers,
  Cpu,
  Bookmark,
  Sparkles
} from "lucide-react";

interface FeedSectionProps {
  posts: PublishedPost[];
  isLoading: boolean;
}

const CATEGORY_TABS = [
  "All",
  "LLMs & Architectures",
  "CUDA & Hardware",
  "Robotics",
  "AI Security",
  "Infrastructure",
  "SSMs & Transformers",
  "Open Source",
];

export default function FeedSection({ posts, isLoading }: FeedSectionProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [expandedIds, setExpandedIds] = useState<Record<string, boolean>>({});

  const toggleExpand = (id: string) => {
    setExpandedIds((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const filteredPosts =
    selectedCategory === "All"
      ? posts
      : posts.filter((p) => {
          const cat = p.category || "AI Research";
          return cat.toLowerCase().includes(selectedCategory.toLowerCase().split(" ")[0]);
        });

  const formatDateUTC = (iso: string | undefined) => {
    if (!iso) return "UTC";
    try {
      const d = new Date(iso);
      return (
        d.toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
          year: "numeric",
          timeZone: "UTC",
        }) +
        " • " +
        d.toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
          timeZone: "UTC",
        }) +
        " UTC"
      );
    } catch {
      return iso;
    }
  };

  return (
    <div className="space-y-6">
      {/* Feed Header & Category Filters */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center space-x-2">
            <span>Published Technology Intelligence</span>
            <span className="rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-mono font-medium text-emerald-400 border border-emerald-500/20">
              {filteredPosts.length} BRIEFS
            </span>
          </h2>
          <p className="text-xs text-slate-400">
            Synthesized by Staff-Level AI Researcher Persona • Ordered by newest first (UTC)
          </p>
        </div>

        {/* Categories */}
        <div className="flex flex-wrap gap-1.5">
          {CATEGORY_TABS.map((cat) => {
            const isActive = selectedCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`rounded-lg px-2.5 py-1 text-xs font-medium transition ${
                  isActive
                    ? "bg-sky-500 text-white shadow-sm"
                    : "bg-slate-900/60 text-slate-400 hover:bg-slate-800 hover:text-slate-200 border border-slate-800/80"
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-800/60 bg-slate-900/40 p-12 text-center">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-sky-400 border-t-transparent mb-4" />
          <p className="text-sm font-medium text-slate-300">
            Retrieving published intelligence from NexusAI database...
          </p>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && filteredPosts.length === 0 && (
        <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-800/60 bg-slate-900/40 p-12 text-center">
          <FileText className="h-10 w-10 text-slate-600 mb-3" />
          <h3 className="text-base font-semibold text-slate-300">
            No research briefs in this category yet
          </h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm">
            The autonomous scheduler continuously monitors AI preprints and GitHub repositories.
          </p>
        </div>
      )}

      {/* Posts List */}
      <div className="space-y-4">
        {filteredPosts.map((post) => {
          const isExpanded = !!expandedIds[post.id];
          const publishedTime = post.createdAt || post.published_at;
          const displayScore = post.editorial_score || 8.5;
          const displayCategory = post.category || "AI Research";
          const displayTitle = post.title || "Autonomous Technology Intelligence Brief";
          const displaySummary = post.summary || post.text?.slice(0, 200) + "..." || "";
          const displayKeywords = post.keywords || ["AI", "Research", displayCategory];

          return (
            <article
              key={post.id}
              className="glass-card glass-card-hover rounded-2xl p-5 sm:p-6 transition-all duration-200"
            >
              {/* Header metadata */}
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-3 mb-3">
                <div className="flex items-center space-x-2">
                  <span className="rounded-md border border-sky-500/30 bg-sky-500/10 px-2 py-0.5 text-[11px] font-mono font-medium text-sky-400">
                    {displayCategory}
                  </span>
                  <span className="flex items-center space-x-1 text-xs text-slate-400">
                    <Clock className="h-3 w-3 text-slate-500" />
                    <span>{formatDateUTC(publishedTime)}</span>
                  </span>
                </div>

                {/* Editorial Score Badge */}
                <div
                  className="flex items-center space-x-1.5 rounded-lg border border-purple-500/30 bg-purple-500/10 px-2.5 py-1 font-mono text-xs text-purple-300"
                  title="Composite Editorial Score (Novelty, Impact, Rigor, Trust)"
                >
                  <Award className="h-3.5 w-3.5 text-purple-400" />
                  <span className="font-semibold">{displayScore.toFixed(1)}</span>
                  <span className="text-slate-400">/ 10</span>
                </div>
              </div>

              {/* Title */}
              <h3 className="text-lg font-bold leading-snug text-white group-hover:text-sky-300">
                {displayTitle}
              </h3>

              {/* Executive Summary */}
              <p className="mt-2 text-sm leading-relaxed text-slate-300">
                {displaySummary}
              </p>

              {/* Publishing Rationale Box */}
              {post.rationale && (
                <div className="mt-3 rounded-xl border border-sky-500/20 bg-sky-500/5 p-3 text-xs text-sky-300 font-mono flex items-start space-x-2">
                  <Sparkles className="h-4 w-4 text-sky-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold uppercase tracking-wider text-sky-400">
                      Publishing Rationale:{" "}
                    </span>
                    <span>{post.rationale}</span>
                  </div>
                </div>
              )}

              {/* Expandable Deep Dive & Why It Matters */}
              {isExpanded && (
                <div className="mt-4 space-y-4 rounded-xl border border-slate-800/80 bg-slate-950/60 p-4 text-xs sm:text-sm text-slate-300">
                  {post.technical_deep_dive && (
                    <div>
                      <h4 className="flex items-center space-x-1.5 font-semibold text-sky-400 mb-1.5">
                        <Cpu className="h-4 w-4" />
                        <span>Technical Deep Dive (Architectural Mechanics)</span>
                      </h4>
                      <div className="whitespace-pre-line leading-relaxed text-slate-300 font-mono text-xs">
                        {post.technical_deep_dive}
                      </div>
                    </div>
                  )}

                  {post.why_it_matters && (
                    <div className="border-t border-slate-800/60 pt-3">
                      <h4 className="flex items-center space-x-1.5 font-semibold text-emerald-400 mb-1.5">
                        <ShieldCheck className="h-4 w-4" />
                        <span>Why It Matters (Engineering &amp; Systems Impact)</span>
                      </h4>
                      <div className="whitespace-pre-line leading-relaxed text-slate-300 font-mono text-xs">
                        {post.why_it_matters}
                      </div>
                    </div>
                  )}

                  {/* Sources List */}
                  {post.sources && post.sources.length > 0 && (
                    <div className="border-t border-slate-800/60 pt-3">
                      <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                        Verified Sources &amp; Citations:
                      </span>
                      <div className="mt-1 flex flex-wrap gap-2">
                        {post.sources.map((src, i) => {
                          const url = typeof src === "string" ? src : src.url;
                          const label = typeof src === "string" ? "Source" : src.name || "Source";
                          return (
                            <a
                              key={i}
                              href={url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex items-center space-x-1 rounded-md border border-slate-700 bg-slate-800/80 px-2 py-1 text-xs text-sky-400 hover:border-sky-500 hover:text-sky-300"
                            >
                              <span>{label}</span>
                              <ExternalLink className="h-3 w-3" />
                            </a>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Footer actions: Keywords & Toggle */}
              <div className="mt-4 flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-800/50">
                <div className="flex flex-wrap gap-1.5">
                  {displayKeywords.slice(0, 4).map((kw, i) => (
                    <span
                      key={i}
                      className="inline-flex items-center space-x-1 rounded-md bg-slate-800/60 px-2 py-0.5 text-[11px] text-slate-400"
                    >
                      <Tag className="h-2.5 w-2.5 text-slate-500" />
                      <span>{kw}</span>
                    </span>
                  ))}
                </div>

                <button
                  onClick={() => toggleExpand(post.id)}
                  className="flex items-center space-x-1 text-xs font-semibold text-sky-400 hover:text-sky-300"
                >
                  <span>{isExpanded ? "Collapse Brief" : "Read Technical Brief"}</span>
                  {isExpanded ? (
                    <ChevronUp className="h-4 w-4" />
                  ) : (
                    <ChevronDown className="h-4 w-4" />
                  )}
                </button>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
