"use client";

import React from "react";
import { 
  Layers, 
  X, 
  Cpu, 
  Database, 
  ShieldCheck, 
  RefreshCw, 
  Terminal, 
  CheckCircle2, 
  GitBranch 
} from "lucide-react";

interface ArchitectureModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ArchitectureModal({
  isOpen,
  onClose,
}: ArchitectureModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-2xl border border-slate-700 bg-[#0c121e] shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 px-6 py-4 sticky top-0 bg-[#0c121e] z-10">
          <div className="flex items-center space-x-2">
            <Layers className="h-5 w-5 text-sky-400" />
            <h3 className="text-lg font-bold text-white">
              NexusAI Frontier Research — Autonomous System Architecture
            </h3>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6 text-sm text-slate-300">
          {/* Executive Flowchart */}
          <div className="rounded-xl border border-slate-800 bg-slate-950/80 p-5 font-mono text-xs">
            <h4 className="font-bold text-sky-400 uppercase tracking-wider mb-3">
              1. AUTONOMOUS COGNITIVE PIPELINE FLOW
            </h4>
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 text-center">
              <div className="flex-1 rounded-lg border border-sky-500/30 bg-sky-500/10 p-2.5">
                <p className="font-semibold text-sky-300">DISCOVERY</p>
                <p className="text-[10px] text-slate-400 mt-0.5">
                  ArXiv, HN, HF, AI Labs
                </p>
              </div>
              <span className="text-slate-500 font-bold">&rarr;</span>

              <div className="flex-1 rounded-lg border border-purple-500/30 bg-purple-500/10 p-2.5">
                <p className="font-semibold text-purple-300">EDITORIAL ENGINE</p>
                <p className="text-[10px] text-slate-400 mt-0.5">
                  Novelty • Impact • Trust
                </p>
              </div>
              <span className="text-slate-500 font-bold">&rarr;</span>

              <div className="flex-1 rounded-lg border border-amber-500/30 bg-amber-500/10 p-2.5">
                <p className="font-semibold text-amber-300">VECTOR MEMORY</p>
                <p className="text-[10px] text-slate-400 mt-0.5">
                  Cosine Sim &gt; 0.85 Filter
                </p>
              </div>
              <span className="text-slate-500 font-bold">&rarr;</span>

              <div className="flex-1 rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-2.5">
                <p className="font-semibold text-emerald-300">STAFF RESEARCHER</p>
                <p className="text-[10px] text-slate-400 mt-0.5">
                  Synthesis &amp; Fact Guardrail
                </p>
              </div>
            </div>
          </div>

          {/* Key Components Breakdown */}
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-xl border border-slate-800/80 bg-slate-900/40 p-4 space-y-2">
              <h5 className="font-semibold text-white flex items-center space-x-2">
                <GitBranch className="h-4 w-4 text-purple-400" />
                <span>Editorial Decision Matrix (7.0 Threshold)</span>
              </h5>
              <p className="text-xs text-slate-400 leading-relaxed">
                Every topic is scored across 6 independent dimensions: Novelty (25%), Engineering Impact (25%), Research Value (20%), Confidence (15%), Community Interest (10%), and Urgency (5%). Topics below 7.0/10 are automatically rejected and logged.
              </p>
            </div>

            <div className="rounded-xl border border-slate-800/80 bg-slate-900/40 p-4 space-y-2">
              <h5 className="font-semibold text-white flex items-center space-x-2">
                <Database className="h-4 w-4 text-sky-400" />
                <span>Semantic Vector Memory &amp; Deduplication</span>
              </h5>
              <p className="text-xs text-slate-400 leading-relaxed">
                Before synthesis, topics are embedded into 1536-dimensional semantic vectors. If cosine similarity exceeds 0.85 without a major version upgrade, the topic is rejected as already covered. Evolving stories are linked to historical posts.
              </p>
            </div>
          </div>

          {/* Hackathon Endpoints Table */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Mandatory Hackathon API Specifications
            </h4>
            <div className="rounded-xl border border-slate-800 overflow-hidden text-xs">
              <table className="w-full text-left">
                <thead className="bg-slate-900 text-slate-300">
                  <tr>
                    <th className="px-4 py-2.5">Method</th>
                    <th className="px-4 py-2.5">Endpoint</th>
                    <th className="px-4 py-2.5">Specification</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 bg-slate-950/60 font-mono">
                  <tr>
                    <td className="px-4 py-2.5 text-emerald-400 font-bold">POST</td>
                    <td className="px-4 py-2.5 text-sky-300">/api/agent/init</td>
                    <td className="px-4 py-2.5 text-slate-400 font-sans">
                      Initializes autonomous loop and seeds baseline research intelligence.
                    </td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2.5 text-sky-400 font-bold">GET</td>
                    <td className="px-4 py-2.5 text-sky-300">/api/agent/feed</td>
                    <td className="px-4 py-2.5 text-slate-400 font-sans">
                      Returns published research briefs ordered by newest first with UTC timestamps.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end border-t border-slate-800 bg-slate-950/40 px-6 py-3">
          <button
            onClick={onClose}
            className="rounded-lg bg-sky-500 px-4 py-1.5 text-xs font-semibold text-white hover:bg-sky-400"
          >
            Close Documentation
          </button>
        </div>
      </div>
    </div>
  );
}
