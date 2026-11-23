"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  api as defaultApi,
  type ApiClient,
  type Trace,
} from "@/lib/api/client";
import {
  PAGE_SIZE,
  filtersToQuery,
  filtersToSearchParams,
  hasActiveFilters,
  parseFilters,
  type TraceFilters,
} from "@/lib/traces/filters";
import { TraceFiltersBar } from "./TraceFiltersBar";
import { TraceTable, TraceTableSkeleton } from "./TraceTable";

type Result =
  | { kind: "error"; message: string; requestId?: string }
  | { kind: "ready"; items: Trace[]; total: number; loadedAt: number };

type LoadState = { kind: "loading" } | Result;

export function TracesView({ client = defaultApi }: { client?: ApiClient }) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const query = searchParams.toString();
  const filters = useMemo(
    () => parseFilters(new URLSearchParams(query)),
    [query],
  );

  const [attempt, setAttempt] = useState(0);
  // Each result remembers which request it answers. Until the result for the
  // current filters (and retry attempt) arrives, the page shows loading.
  const requestKey = `${query}#${attempt}`;
  const [result, setResult] = useState<{ key: string; value: Result }>();
  const state: LoadState =
    result?.key === requestKey ? result.value : { kind: "loading" };

  useEffect(() => {
    const controller = new AbortController();
    const setState = (value: Result) => setResult({ key: requestKey, value });

    client
      .GET("/v1/traces", {
        params: { query: filtersToQuery(filters) },
        signal: controller.signal,
      })
      .then(({ data, error, response }) => {
        if (controller.signal.aborted) return;
        if (data) {
          setState({
            kind: "ready",
            items: data.items,
            total: data.total,
            loadedAt: Date.now(),
          });
        } else {
          setState({
            kind: "error",
            message: error?.detail ?? `Request failed (${response.status})`,
            requestId: response.headers.get("x-request-id") ?? undefined,
          });
        }
      })
      .catch((cause: unknown) => {
        if (controller.signal.aborted) return;
        setState({
          kind: "error",
          message:
            cause instanceof Error
              ? cause.message
              : "The server did not respond.",
        });
      });

    return () => controller.abort();
  }, [client, filters, requestKey]);

  const updateFilters = useCallback(
    (next: Partial<TraceFilters>) => {
      const merged: TraceFilters = { ...filters, page: 1, ...next };
      const search = filtersToSearchParams(merged);
      // Keep the dev-only ?mock= switch while filtering.
      const mock = new URLSearchParams(query).get("mock");
      if (mock) search.set("mock", mock);
      const suffix = search.toString();
      router.replace(suffix ? `${pathname}?${suffix}` : pathname, {
        scroll: false,
      });
    },
    [filters, pathname, query, router],
  );

  return (
    <div>
      <h1 className="text-2xl font-semibold">Traces</h1>
      <p className="text-muted mt-1 text-sm">
        Search and filter traces by status, health, version and date.
      </p>

      <div className="mt-4">
        <TraceFiltersBar filters={filters} onChange={updateFilters} />
      </div>

      <div className="border-border bg-surface mt-4 rounded-lg border">
        {state.kind === "loading" && <TraceTableSkeleton />}

        {state.kind === "error" && (
          <EmptyPanel
            tone="error"
            title="Could not load traces"
            body={`${state.message.replace(/[.!?]?$/, ".")} Your filters were kept.`}
            detail={state.requestId && `Request ID: ${state.requestId}`}
            action={
              <button
                type="button"
                className="bg-primary text-background rounded-md px-4 py-2 text-sm font-medium"
                onClick={() => setAttempt((count) => count + 1)}
              >
                Try again
              </button>
            }
          />
        )}

        {state.kind === "ready" &&
          state.items.length === 0 &&
          (hasActiveFilters(filters) || filters.page > 1 ? (
            <EmptyPanel
              title="No traces match these filters"
              body="Try a wider date range or clear some filters."
              action={
                <button
                  type="button"
                  className="border-border rounded-md border px-4 py-2 text-sm"
                  onClick={() =>
                    updateFilters({
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
              }
            />
          ) : (
            <EmptyPanel
              title="No traces yet"
              body="Send your first trace with the Python SDK."
            />
          ))}

        {state.kind === "ready" && state.items.length > 0 && (
          <TraceTable traces={state.items} now={state.loadedAt} />
        )}
      </div>

      {state.kind === "ready" && state.total > 0 && (
        <Pagination
          page={filters.page}
          total={state.total}
          onPage={(page) => updateFilters({ page })}
        />
      )}
    </div>
  );
}

function Pagination({
  page,
  total,
  onPage,
}: {
  page: number;
  total: number;
  onPage: (page: number) => void;
}) {
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const first = (page - 1) * PAGE_SIZE + 1;
  const last = Math.min(page * PAGE_SIZE, total);
  const button =
    "border-border rounded-md border px-4 py-2 text-sm disabled:opacity-40";

  return (
    <nav
      aria-label="Pagination"
      className="mt-3 flex items-center justify-between"
    >
      <p className="text-muted text-sm">
        Showing {first}–{last} of {total}
      </p>
      <div className="flex items-center gap-2">
        <button
          type="button"
          className={button}
          disabled={page <= 1}
          onClick={() => onPage(page - 1)}
        >
          Prev
        </button>
        <span className="text-muted text-sm">
          Page {page} of {pages}
        </span>
        <button
          type="button"
          className={button}
          disabled={page >= pages}
          onClick={() => onPage(page + 1)}
        >
          Next
        </button>
      </div>
    </nav>
  );
}

function EmptyPanel({
  title,
  body,
  detail,
  action,
  tone = "neutral",
}: {
  title: string;
  body: string;
  detail?: string | false;
  action?: ReactNode;
  tone?: "neutral" | "error";
}) {
  return (
    <div
      role={tone === "error" ? "alert" : "status"}
      className="flex flex-col items-center gap-2 px-6 py-20 text-center"
    >
      {tone === "error" && (
        <span
          aria-hidden="true"
          className="bg-danger flex h-10 w-10 items-center justify-center rounded-full text-lg font-bold text-white"
        >
          !
        </span>
      )}
      <h2 className="text-lg font-semibold">{title}</h2>
      <p className="text-muted text-sm">{body}</p>
      {detail && <p className="text-muted text-xs">{detail}</p>}
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
}
