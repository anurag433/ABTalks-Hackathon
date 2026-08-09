"use client";

import React, { useState } from "react";
import { Terminal, Play, ExternalLink, CheckCircle2, AlertCircle, X, Code2 } from "lucide-react";

export default function HackathonApiBar() {
  const [apiOutput, setApiOutput] = useState<string | null>(null);
  const [apiTitle, setApiTitle] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const handleTestInit = async () => {
    setIsLoading(true);
    setApiTitle("POST /api/agent/init — Initializing Autonomous Creator");
    setIsOpen(true);
    try {
      const res = await fetch("/api/agent/init", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          persona: {
            name: "Ada",
            domain: "AI Security",
          },
        }),
      });
      const data = await res.json();
      setApiOutput(JSON.stringify(data, null, 2));
    } catch (err: any) {
      setApiOutput(JSON.stringify({ error: err.message || "Request failed" }, null, 2));
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestFeed = async () => {
    setIsLoading(true);
    setApiTitle("GET /api/agent/feed?agentId=agent-ai-security-01 — Retrieving Feed");
    setIsOpen(true);
    try {
      const res = await fetch("/api/agent/feed?agentId=agent-ai-security-01");
      const data = await res.json();
      setApiOutput(JSON.stringify(data, null, 2));
    } catch (err: any) {
      setApiOutput(JSON.stringify({ error: err.message || "Request failed" }, null, 2));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mb-6 rounded-2xl border border-sky-500/30 bg-gradient-to-r from-slate-900/90 via-slate-900/80 to-purple-950/40 p-4 shadow-lg backdrop-blur-md">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="flex items-start space-x-3">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-sky-500/10 border border-sky-500/30 text-sky-400">
            <Code2 className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-sm font-bold text-white">
                Hackathon Evaluator API Controls
              </span>
              <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-mono font-semibold text-emerald-400 border border-emerald-500/30">
                MANDATORY ENDPOINTS
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Judges can test <code className="text-sky-300">POST /api/agent/init</code> &amp; <code className="text-sky-300">GET /api/agent/feed</code> directly from this page:
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={handleTestInit}
            className="flex items-center space-x-1.5 rounded-lg bg-gradient-to-r from-sky-500 to-purple-600 px-3.5 py-1.5 text-xs font-semibold text-white shadow-md hover:opacity-95 transition"
          >
            <Play className="h-3 w-3" />
            <span>POST /api/agent/init</span>
          </button>

          <button
            onClick={handleTestFeed}
            className="flex items-center space-x-1.5 rounded-lg border border-slate-700 bg-slate-800/80 px-3.5 py-1.5 text-xs font-semibold text-slate-200 hover:border-sky-500 hover:text-white transition"
          >
            <Terminal className="h-3.5 w-3.5 text-sky-400" />
            <span>GET /api/agent/feed (JSON)</span>
          </button>

          <a
            href="/api/agent/feed"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 rounded-lg border border-slate-700 bg-slate-800/80 px-3 py-1.5 text-xs font-medium text-slate-300 hover:border-slate-600 hover:text-white transition"
          >
            <span>Raw Endpoint</span>
            <ExternalLink className="h-3 w-3" />
          </a>
        </div>
      </div>

      {/* JSON Response Drawer / Modal */}
      {isOpen && (
        <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-xs shadow-inner">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-2 mb-3 text-slate-400">
            <div className="flex items-center space-x-2">
              <Terminal className="h-4 w-4 text-sky-400" />
              <span className="font-semibold text-sky-300">{apiTitle}</span>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-white"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center py-8 text-slate-400">
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-sky-400 border-t-transparent mr-2" />
              <span>Sending HTTP request to backend agent...</span>
            </div>
          ) : (
            <pre className="max-h-72 overflow-y-auto text-emerald-400 whitespace-pre-wrap leading-relaxed">
              {apiOutput}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}
