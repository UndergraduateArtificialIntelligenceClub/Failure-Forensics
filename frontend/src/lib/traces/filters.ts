import type { TraceHealth, TraceStatus } from "@/lib/api/client";

/**
 * Trace list filters (KAN-47). The filters live in the page URL so a filtered
 * view can be shared and survives a refresh, e.g. /traces?health=failed&page=2
 */
export const TRACE_STATUSES: readonly TraceStatus[] = [
  "ok",
  "error",
  "incomplete",
];
export const TRACE_HEALTHS: readonly TraceHealth[] = [
  "healthy",
  "degraded",
  "failed",
  "unknown",
];
export const DATE_RANGES = {
  "24h": { label: "Last 24 hours", ms: 24 * 60 * 60 * 1000 },
  "7d": { label: "Last 7 days", ms: 7 * 24 * 60 * 60 * 1000 },
  "30d": { label: "Last 30 days", ms: 30 * 24 * 60 * 60 * 1000 },
} as const;
export type DateRange = keyof typeof DATE_RANGES | "all";

export const PAGE_SIZE = 25;

export type TraceFilters = {
  status?: TraceStatus;
  health?: TraceHealth;
  pipelineVersion?: string;
  date: DateRange;
  flagged: boolean;
  page: number;
};

export const DEFAULT_FILTERS: TraceFilters = {
  date: "all",
  flagged: false,
  page: 1,
};

function oneOf<T extends string>(
  value: string | null,
  allowed: readonly T[],
): T | undefined {
  return allowed.find((item) => item === value);
}

/** Reads filters from the page URL, ignoring values it does not recognise. */
export function parseFilters(params: URLSearchParams): TraceFilters {
  const date = params.get("date");
  const page = Number(params.get("page"));
  const version = params.get("pipeline_version")?.trim();

  return {
    status: oneOf(params.get("status"), TRACE_STATUSES),
    health: oneOf(params.get("health"), TRACE_HEALTHS),
    pipelineVersion: version || undefined,
    date: date && date in DATE_RANGES ? (date as DateRange) : "all",
    flagged: params.get("flagged") === "true",
    page: Number.isInteger(page) && page > 1 ? page : 1,
  };
}

/** Writes filters back to URL params, leaving out defaults to keep URLs short. */
export function filtersToSearchParams(filters: TraceFilters): URLSearchParams {
  const params = new URLSearchParams();
  if (filters.status) params.set("status", filters.status);
  if (filters.health) params.set("health", filters.health);
  if (filters.pipelineVersion)
    params.set("pipeline_version", filters.pipelineVersion);
  if (filters.date !== "all") params.set("date", filters.date);
  if (filters.flagged) params.set("flagged", "true");
  if (filters.page > 1) params.set("page", String(filters.page));
  return params;
}

/** Turns filters into the query for GET /v1/traces. */
export function filtersToQuery(filters: TraceFilters, now = Date.now()) {
  return {
    status: filters.status,
    health: filters.health,
    pipeline_version: filters.pipelineVersion,
    started_after:
      filters.date === "all"
        ? undefined
        : new Date(now - DATE_RANGES[filters.date].ms).toISOString(),
    flagged: filters.flagged || undefined,
    page: filters.page,
    page_size: PAGE_SIZE,
  };
}

/** True when any filter other than the page number is set. */
export function hasActiveFilters(filters: TraceFilters): boolean {
  return Boolean(
    filters.status ||
    filters.health ||
    filters.pipelineVersion ||
    filters.date !== "all" ||
    filters.flagged,
  );
}
