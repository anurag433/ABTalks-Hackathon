"use client";

import React from "react";
import { RejectedTopic } from "@/types";
import { 
  XCircle, 
  ShieldAlert, 
  ExternalLink, 
  Clock, 
  Filter 
} from "lucide-react";

interface RejectedTopicsPanelProps {
  rejected: RejectedTopic[];
  isLoading: boolean;
}

export default function RejectedTopicsPanel({
  rejected,
  isLoading,
}: RejectedTopicsPanelProps) {
  const formatDateUTC = (iso: string) => {
    try {
      const d = new Date(iso);
      return (
        d.toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
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
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center space-x-2">
            <span>Rejected Topics Audit Trail</span>
            <span className="rounded-full bg-rose-500/10 px-2.5 py-0.5 text-xs font-mono font-medium text-rose-400 border border-rose-500/20">
              {rejected.length} REJECTED
            </span>
          </h2>
          <p className="text-xs text-slate-400">
            Transparency log • Topics rejected by the Editorial Decision Engine for failing standards
          </p>
        </div>
      </div>

      {isLoading && (
        <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-800/60 bg-slate-900/40 p-12 text-center">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-rose-400 border-t-transparent mb-4" />
          <p className="text-sm font-medium text-slate-300">
            Loading editorial rejection audit logs...
          </p>
        </div>
      )}

      {!isLoading && rejected.length === 0 && (
        <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-800/60 bg-slate-900/40 p-12 text-center">
          <ShieldAlert className="h-10 w-10 text-slate-600 mb-3" />
          <h3 className="text-base font-semibold text-slate-300">
            No rejected topics logged yet
          </h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm">
            All recently evaluated topics met or exceeded our minimum editorial score threshold (7.0/10).
          </p>
        </div>
      )}

      <div className="grid gap-3 sm:grid-cols-2">
        {rejected.map((item) => (
          <div
            key={item.id}
            className="rounded-xl border border-rose-500/20 bg-slate-900/60 p-4 transition hover:border-rose-500/40"
          >
            <div className="flex items-center justify-between text-xs mb-2">
              <span className="rounded bg-rose-500/10 px-2 py-0.5 font-mono text-[10px] font-semibold text-rose-400 border border-rose-500/20">
                SCORE: {item.editorial_score.toFixed(1)} / 10
              </span>
              <span className="flex items-center space-x-1 text-[11px] text-slate-500">
                <Clock className="h-3 w-3" />
                <span>{formatDateUTC(item.rejected_at)}</span>
              </span>
            </div>

            <h4 className="text-sm font-semibold text-slate-200 line-clamp-2">
              {item.title}
            </h4>

            <div className="mt-2.5 rounded-lg border border-slate-800 bg-slate-950/80 p-2.5 text-xs text-rose-300 font-mono">
              <span className="font-semibold uppercase tracking-wider text-rose-400">
                Editorial Rejection:{" "}
              </span>
              {item.rejection_reason}
            </div>

            {item.url && item.url.startsWith("http") && (
              <div className="mt-2 text-right">
                <a
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-1 text-[11px] text-slate-400 hover:text-slate-200"
                >
                  <span>View Origin</span>
                  <ExternalLink className="h-2.5 w-2.5" />
                </a>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
