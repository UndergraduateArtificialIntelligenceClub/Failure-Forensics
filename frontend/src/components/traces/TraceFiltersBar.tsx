"use client";

import type { TraceHealth, TraceStatus } from "@/lib/api/client";
import {
  DATE_RANGES,
  TRACE_HEALTHS,
  TRACE_STATUSES,
  hasActiveFilters,
  type DateRange,
  type TraceFilters,
} from "@/lib/traces/filters";

const fieldClass =
  "border-border bg-surface h-9 rounded-md border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary";

export function TraceFiltersBar({
  filters,
  onChange,
}: {
  filters: TraceFilters;
  /** Called with the changed fields; the page number resets to 1. */
  onChange: (next: Partial<TraceFilters>) => void;
}) {
  // Typed text is applied on Enter or when the field loses focus, not on
  // every keystroke, so the list does not reload per letter.
  const applyVersion = (text: string) => {
    const value = text.trim() || undefined;
    if (value !== filters.pipelineVersion) onChange({ pipelineVersion: value });
  };

  return (
    <div
      role="search"
      aria-label="Filter traces"
      className="flex flex-wrap items-center gap-3"
    >
      <select
        aria-label="Health"
        className={fieldClass}
        value={filters.health ?? ""}
        onChange={(event) =>
          onChange({ health: (event.target.value || undefined) as TraceHealth })
        }
      >
        <option value="">Health: any</option>
        {TRACE_HEALTHS.map((health) => (
          <option key={health} value={health}>
            Health: {health}
          </option>
        ))}
      </select>

      <select
        aria-label="Status"
        className={fieldClass}
        value={filters.status ?? ""}
        onChange={(event) =>
          onChange({ status: (event.target.value || undefined) as TraceStatus })
        }
      >
        <option value="">Status: any</option>
        {TRACE_STATUSES.map((status) => (
          <option key={status} value={status}>
            Status: {status}
          </option>
        ))}
      </select>

      <select
        aria-label="Date"
        className={fieldClass}
        value={filters.date}
        onChange={(event) =>
          onChange({ date: event.target.value as DateRange })
        }
      >
        <option value="all">Date: any time</option>
        {Object.entries(DATE_RANGES).map(([value, { label }]) => (
          <option key={value} value={value}>
            Date: {label.toLowerCase()}
          </option>
        ))}
      </select>

      <input
        // Re-mount when the URL value changes (e.g. "Clear filters").
        key={filters.pipelineVersion ?? ""}
        aria-label="Pipeline version"
        placeholder="Pipeline version, e.g. v1.2"
        className={`${fieldClass} w-56`}
        defaultValue={filters.pipelineVersion ?? ""}
        onBlur={(event) => applyVersion(event.currentTarget.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter") applyVersion(event.currentTarget.value);
        }}
      />

      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={filters.flagged}
          onChange={(event) => onChange({ flagged: event.target.checked })}
        />
        Flagged only
      </label>

      {hasActiveFilters(filters) && (
        <button
          type="button"
          className="text-primary text-sm underline"
          onClick={() =>
            onChange({
              status: undefined,
              health: undefined,
              pipelineVersion: undefined,
              date: "all",
              flagged: false,
            })
          }
        >
          Clear filters
        </button>
      )}
    </div>
  );
}
