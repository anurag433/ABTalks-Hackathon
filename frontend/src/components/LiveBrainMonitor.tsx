"use client";

import React from "react";
import { AgentStatusData } from "@/types";
import { 
  BrainCircuit, 
  Terminal, 
  ShieldCheck, 
  CheckCircle2, 
  XCircle, 
  Search,
  Zap,
  Lock,
  BarChart2
} from "lucide-react";

interface LiveBrainMonitorProps {
  status: AgentStatusData | null;
}

export default function LiveBrainMonitor({ status }: LiveBrainMonitorProps) {
  const isWorking = status?.current_phase !== "IDLE";

  const totalDiscovered = status?.total_discovered || 0;
  const totalPublished = status?.total_published || 0;
  const totalRejected = status?.total_rejected || 0;
  const acceptanceRate =
    totalDiscovered > 0
      ? Math.round((totalPublished / totalDiscovered) * 100)
      : 88;

  return (
    <div className="glass-card mb-8 overflow-hidden rounded-2xl border border-slate-800/80 p-5 sm:p-6">
      <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
        {/* Left Column: Brain State & Live Reasoning Terminal */}
        <div className="flex-1 space-y-3">
          <div className="flex items-center space-x-2">
            <div
              className={`flex h-8 w-8 items-center justify-center rounded-lg border ${
                isWorking
                  ? "border-amber-500/40 bg-amber-500/10 text-amber-400 animate-pulse"
                  : "border-sky-500/40 bg-sky-500/10 text-sky-400"
              }`}
            >
              <BrainCircuit className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-200">
                AI Cognitive Research Engine
              </h3>
              <p className="text-xs text-slate-400">
                Autonomous Discovery • Editorial Decision Engine • Semantic Vector Memory
              </p>
            </div>
          </div>

          {/* Reasoning Viewer Terminal */}
          <div className="relative rounded-xl border border-slate-800 bg-slate-950/90 p-3.5 font-mono text-xs text-slate-300 shadow-inner">
            <div className="flex items-center justify-between border-b border-slate-800/60 pb-2 mb-2 text-[10px] text-slate-500">
              <div className="flex items-center space-x-1.5">
                <Terminal className="h-3 w-3 text-sky-400" />
                <span>NEXUSAI-REASONING-LOG // STAFF-ANALYST</span>
              </div>
              <span className="text-emerald-400">GUARDRAIL: ACTIVE</span>
            </div>
            <p className="line-clamp-2 leading-relaxed text-slate-200">
              {status?.status_message ||
                "System initialized. Monitoring ArXiv, Hacker News, Hugging Face, and AI Lab feeds."}
            </p>
          </div>
        </div>

        {/* Right Column: Key Autonomous Metrics & Confidence Meter */}
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:w-auto">
          {/* Discovered */}
          <div className="flex flex-col justify-center rounded-xl border border-slate-800/80 bg-slate-900/50 p-3 text-center">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
              Discovered
            </span>
            <span className="mt-1 font-mono text-xl font-bold text-white">
              {totalDiscovered}
            </span>
            <span className="text-[9px] text-slate-500">Raw Feed Items</span>
          </div>

          {/* Published */}
          <div className="flex flex-col justify-center rounded-xl border border-slate-800/80 bg-slate-900/50 p-3 text-center">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
              Published
            </span>
            <span className="mt-1 font-mono text-xl font-bold text-emerald-400">
              {totalPublished}
            </span>
            <span className="text-[9px] text-slate-500">Research Briefs</span>
          </div>

          {/* Rejected */}
          <div className="flex flex-col justify-center rounded-xl border border-slate-800/80 bg-slate-900/50 p-3 text-center">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
              Rejected
            </span>
            <span className="mt-1 font-mono text-xl font-bold text-rose-400">
              {totalRejected}
            </span>
            <span className="text-[9px] text-slate-500">Hype &amp; Noise</span>
          </div>

          {/* Confidence Meter */}
          <div className="flex flex-col justify-center rounded-xl border border-slate-800/80 bg-slate-900/50 p-3 text-center">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
              Accept Rate
            </span>
            <span className="mt-1 font-mono text-xl font-bold text-sky-400">
              {acceptanceRate}%
            </span>
            <span className="text-[9px] text-slate-500">Signal Ratio</span>
          </div>
        </div>
      </div>
    </div>
  );
}
