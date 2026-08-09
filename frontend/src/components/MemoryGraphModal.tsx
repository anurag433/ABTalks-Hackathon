"use client";

import React from "react";
import { MemoryNode, KnowledgeGraphData } from "@/types";
import { 
  Network, 
  X, 
  Clock, 
  Database, 
  Share2, 
  Cpu, 
  ShieldCheck 
} from "lucide-react";

interface MemoryGraphModalProps {
  isOpen: boolean;
  onClose: () => void;
  timeline: MemoryNode[];
  graph: KnowledgeGraphData | null;
  isLoading: boolean;
}

export default function MemoryGraphModal({
  isOpen,
  onClose,
  timeline,
  graph,
  isLoading,
}: MemoryGraphModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="relative w-full max-w-5xl max-h-[90vh] overflow-hidden rounded-2xl border border-slate-700 bg-[#0c121e] shadow-2xl flex flex-col">
        {/* Modal Header */}
        <div className="flex items-center justify-between border-b border-slate-800 px-6 py-4">
          <div className="flex items-center space-x-2">
            <Network className="h-5 w-5 text-purple-400" />
            <h3 className="text-lg font-bold text-white">
              Semantic Vector Memory &amp; Knowledge Graph
            </h3>
            <span className="rounded-full bg-purple-500/10 px-2 py-0.5 text-[10px] font-mono text-purple-300 border border-purple-500/30">
              1536-DIM VECTORS
            </span>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Modal Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {isLoading && (
            <div className="flex flex-col items-center justify-center p-12">
              <div className="h-8 w-8 animate-spin rounded-full border-2 border-purple-400 border-t-transparent mb-3" />
              <p className="text-sm text-slate-400">Loading semantic vector graph...</p>
            </div>
          )}

          {!isLoading && graph && (
            <div>
              <div className="mb-4 flex items-center justify-between text-xs text-slate-400">
                <span>
                  Semantic relationships computed via high-dimensional cosine similarity (&gt; 0.55 overlap)
                </span>
                <span className="font-mono text-purple-400">
                  {graph.total_nodes} Nodes • {graph.total_edges} Semantic Edges
                </span>
              </div>

              {/* SVG Knowledge Graph */}
              <div className="relative w-full rounded-xl border border-slate-800 bg-slate-950/80 p-6 flex items-center justify-center overflow-x-auto">
                <svg
                  viewBox="0 0 800 320"
                  className="w-full max-w-3xl h-72"
                  style={{ minWidth: "600px" }}
                >
                  <defs>
                    <linearGradient id="edge-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.6" />
                      <stop offset="100%" stopColor="#a855f7" stopOpacity="0.6" />
                    </linearGradient>
                  </defs>

                  {/* Edges */}
                  {graph.edges.map((edge, idx) => {
                    const srcIndex = graph.nodes.findIndex((n) => n.id === edge.source);
                    const tgtIndex = graph.nodes.findIndex((n) => n.id === edge.target);
                    if (srcIndex === -1 || tgtIndex === -1) return null;

                    const x1 = 100 + (srcIndex % 4) * 200;
                    const y1 = 70 + Math.floor(srcIndex / 4) * 110;
                    const x2 = 100 + (tgtIndex % 4) * 200;
                    const y2 = 70 + Math.floor(tgtIndex / 4) * 110;

                    return (
                      <g key={idx}>
                        <line
                          x1={x1}
                          y1={y1}
                          x2={x2}
                          y2={y2}
                          stroke="url(#edge-grad)"
                          strokeWidth={Math.max(1, edge.weight * 3)}
                          strokeDasharray="4 2"
                        />
                      </g>
                    );
                  })}

                  {/* Nodes */}
                  {graph.nodes.map((node, idx) => {
                    const x = 100 + (idx % 4) * 200;
                    const y = 70 + Math.floor(idx / 4) * 110;

                    return (
                      <g key={node.id} className="cursor-pointer group">
                        <circle
                          cx={x}
                          cy={y}
                          r={24}
                          fill="#0f172a"
                          stroke="#38bdf8"
                          strokeWidth={2}
                          className="transition-all duration-200 group-hover:r-28 group-hover:stroke-purple-400"
                        />
                        <circle cx={x} cy={y} r={6} fill="#38bdf8" />
                        <text
                          x={x}
                          y={y + 38}
                          textAnchor="middle"
                          fill="#cbd5e1"
                          fontSize={11}
                          fontFamily="monospace"
                          className="select-none font-medium"
                        >
                          {node.label.length > 22
                            ? node.label.slice(0, 22) + "..."
                            : node.label}
                        </text>
                        <text
                          x={x}
                          y={y + 52}
                          textAnchor="middle"
                          fill="#64748b"
                          fontSize={9}
                          fontFamily="monospace"
                          className="select-none"
                        >
                          {node.category}
                        </text>
                      </g>
                    );
                  })}
                </svg>
              </div>
            </div>
          )}

          {/* Memory Timeline List */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-300 mb-3 flex items-center space-x-2">
              <Clock className="h-4 w-4 text-sky-400" />
              <span>Semantic Memory Timeline ({timeline.length} nodes indexed)</span>
            </h4>

            <div className="space-y-2.5 max-h-60 overflow-y-auto pr-2">
              {timeline.map((node) => (
                <div
                  key={node.memory_id}
                  className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-900/60 p-3 text-xs"
                >
                  <div className="flex-1 pr-4">
                    <p className="font-semibold text-slate-200">{node.title}</p>
                    <p className="text-slate-400 line-clamp-1 mt-0.5 font-mono text-[11px]">
                      {node.summary}
                    </p>
                  </div>
                  <span className="rounded bg-purple-500/10 px-2 py-0.5 font-mono text-[10px] text-purple-300 border border-purple-500/20 whitespace-nowrap">
                    INDEXED
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="flex items-center justify-end border-t border-slate-800 bg-slate-950/40 px-6 py-3">
          <button
            onClick={onClose}
            className="rounded-lg bg-slate-800 px-4 py-1.5 text-xs font-semibold text-white hover:bg-slate-700"
          >
            Close Graph
          </button>
        </div>
      </div>
    </div>
  );
}
