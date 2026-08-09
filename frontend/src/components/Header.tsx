"use client";

import React, { useState, useEffect } from "react";
import { AgentStatusData } from "@/types";
import { 
  Cpu, 
  Activity, 
  RefreshCw, 
  Terminal, 
  ShieldCheck, 
  Database,
  Layers,
  Network
} from "lucide-react";

interface HeaderProps {
  status: AgentStatusData | null;
  onTriggerSweep: () => Promise<void>;
  onOpenGraph: () => void;
  onOpenArchitecture: () => void;
  isTriggering: boolean;
}

export default function Header({
  status,
  onTriggerSweep,
  onOpenGraph,
  onOpenArchitecture,
  isTriggering,
}: HeaderProps) {
  const [countdown, setCountdown] = useState<string>("00:00");

  useEffect(() => {
    if (!status?.next_run_at) return;

    const updateTimer = () => {
      const nextTime = new Date(status.next_run_at!).getTime();
      const now = new Date().getTime();
      const diff = Math.max(0, Math.floor((nextTime - now) / 1000));

      const mins = Math.floor(diff / 60);
      const secs = diff % 60;
      setCountdown(
        `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`
      );
    };

    updateTimer();
    const timer = setInterval(updateTimer, 1000);
    return () => clearInterval(timer);
  }, [status?.next_run_at]);

  const phaseColor =
    status?.current_phase === "IDLE"
      ? "text-emerald-400 border-emerald-500/30 bg-emerald-500/10"
      : "text-amber-400 border-amber-500/30 bg-amber-500/10 animate-pulse";

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-[#080c14]/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        {/* Brand Identity */}
        <div className="flex items-center space-x-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-sky-400 to-purple-600 shadow-lg shadow-sky-500/20">
            <Cpu className="h-6 w-6 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-bold tracking-tight text-white">
                NexusAI <span className="gradient-text-accent">Frontier</span>
              </span>
              <span className="rounded-full border border-sky-500/30 bg-sky-500/10 px-2 py-0.5 text-[10px] font-mono font-medium text-sky-400">
                AUTONOMOUS CREATOR v2.0
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Principal AI Research &amp; Technology Intelligence Platform
            </p>
          </div>
        </div>

        {/* Brain Activity Badge & Countdown */}
        <div className="hidden items-center space-x-4 md:flex">
          <div className="flex items-center space-x-2 rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-1.5 font-mono text-xs text-slate-300">
            <Activity className="h-3.5 w-3.5 text-sky-400" />
            <span>AUTONOMOUS CLOCK:</span>
            <span className="font-semibold text-sky-400">{countdown}</span>
          </div>

          <div
            className={`flex items-center space-x-2 rounded-lg border px-3 py-1.5 text-xs font-mono font-medium ${phaseColor}`}
          >
            <span className="h-2 w-2 rounded-full bg-current"></span>
            <span>PHASE: {status?.current_phase || "STANDBY"}</span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-2">
          <button
            onClick={onOpenGraph}
            className="flex items-center space-x-1.5 rounded-lg border border-slate-800 bg-slate-900/80 px-3 py-1.5 text-xs font-medium text-slate-300 transition hover:border-slate-700 hover:text-white"
            title="Semantic Memory & Knowledge Graph"
          >
            <Network className="h-3.5 w-3.5 text-purple-400" />
            <span className="hidden sm:inline">Memory Graph</span>
          </button>

          <button
            onClick={onOpenArchitecture}
            className="flex items-center space-x-1.5 rounded-lg border border-slate-800 bg-slate-900/80 px-3 py-1.5 text-xs font-medium text-slate-300 transition hover:border-slate-700 hover:text-white"
            title="System Architecture Diagram"
          >
            <Layers className="h-3.5 w-3.5 text-sky-400" />
            <span className="hidden sm:inline">Architecture</span>
          </button>

          <button
            onClick={onTriggerSweep}
            disabled={isTriggering}
            className="flex items-center space-x-1.5 rounded-lg bg-gradient-to-r from-sky-500 to-purple-600 px-3.5 py-1.5 text-xs font-semibold text-white shadow-md shadow-sky-500/20 transition hover:opacity-95 disabled:opacity-50"
          >
            <RefreshCw
              className={`h-3.5 w-3.5 ${isTriggering ? "animate-spin" : ""}`}
            />
            <span>{isTriggering ? "Evaluating..." : "Trigger Sweep"}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
