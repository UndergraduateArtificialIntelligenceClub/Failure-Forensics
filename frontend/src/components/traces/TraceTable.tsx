"use client";

import type { Trace } from "@/lib/api/client";
import { formatCost, formatLatency, formatRelativeTime } from "@/lib/format";
import { HealthBadge } from "./HealthBadge";

const headers = [
  "Trace ID",
  "Health",
  "Status",
  "Latency",
  "Cost",
  "Flag",
  "Pipeline",
  "Started",
];

export function TraceTable({ traces, now }: { traces: Trace[]; now: number }) {
  return (
    <table className="w-full text-left text-sm">
      <thead className="border-border text-muted border-b">
        <tr>
          {headers.map((header) => (
            <th key={header} scope="col" className="px-4 py-3 font-medium">
              {header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {traces.map((trace) => (
          <tr key={trace.id} className="border-border border-b last:border-0">
            <td className="px-4 py-3 font-mono text-xs">{trace.id}</td>
            <td className="px-4 py-3">
              <HealthBadge health={trace.health} />
            </td>
            <td className="px-4 py-3">{trace.status}</td>
            <td className="px-4 py-3">
              {formatLatency(trace.total_latency_ms)}
            </td>
            <td className="px-4 py-3">
              {formatCost(trace.estimated_cost_usd)}
            </td>
            <td className="px-4 py-3">
              {trace.feedback_status === "flagged" ? "flagged" : "–"}
            </td>
            <td className="px-4 py-3">{trace.pipeline_version}</td>
            <td className="text-muted px-4 py-3">
              <time dateTime={trace.started_at} title={trace.started_at}>
                {formatRelativeTime(trace.started_at, now)}
              </time>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export function TraceTableSkeleton({ rows = 8 }: { rows?: number }) {
  return (
    <div role="status" aria-label="Loading traces" className="p-4">
      {Array.from({ length: rows }, (_, index) => (
        <div
          key={index}
          className="bg-border/60 mb-3 h-6 animate-pulse rounded last:mb-0"
        />
      ))}
    </div>
  );
}
