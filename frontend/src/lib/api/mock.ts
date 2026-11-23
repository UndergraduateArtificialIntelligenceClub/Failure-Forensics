import type { components } from "./schema";

/**
 * In-browser mock of the Failure Forensics API (KAN-47).
 *
 * Used until the KAN-35 mock server and the real backend exist. It answers the
 * same paths and shapes as openapi/openapi.json, so pages written against it
 * work unchanged once NEXT_PUBLIC_API_MODE=live.
 *
 * For reviewing edge states, add `?mock=empty`, `?mock=error` or
 * `?mock=slow` to the page URL.
 */
type Trace = components["schemas"]["Trace"];
type TraceDetail = components["schemas"]["TraceDetail"];

export type MockScenario = "normal" | "empty" | "error" | "slow";

const MOCK_TRACE_COUNT = 137;
const PIPELINE_VERSIONS = ["v1.0", "v1.1", "v1.2"];

/** Small seeded PRNG so the fake data is the same on every load. */
function seeded(seed: number) {
  let state = seed;
  return () => {
    state = (state * 1664525 + 1013904223) % 4294967296;
    return state / 4294967296;
  };
}

let cache: { traces: Trace[]; createdAt: number } | null = null;

/** Builds the fake traces once, relative to when they are first requested. */
export function getMockTraces(now = Date.now()): Trace[] {
  if (cache && Math.abs(cache.createdAt - now) < 60 * 60 * 1000) {
    return cache.traces;
  }
  const random = seeded(42);
  const traces: Trace[] = [];
  let startedAt = now - 2 * 60 * 1000;

  for (let index = 0; index < MOCK_TRACE_COUNT; index++) {
    const roll = random();
    const health: Trace["health"] =
      roll < 0.62
        ? "healthy"
        : roll < 0.8
          ? "degraded"
          : roll < 0.95
            ? "failed"
            : "unknown";
    const status: Trace["status"] =
      health === "failed" && random() < 0.6
        ? "error"
        : random() < 0.04
          ? "incomplete"
          : "ok";
    const latency = Math.round(900 + random() * 3600);
    const flagged = health === "failed" && random() < 0.7;
    const id = `tr_${Math.floor(random() * 0xffffff)
      .toString(16)
      .padStart(6, "0")}${index.toString(16).padStart(2, "0")}`;

    traces.push({
      id,
      project_id: "demo",
      external_trace_id: null,
      started_at: new Date(startedAt).toISOString(),
      ended_at: new Date(startedAt + latency).toISOString(),
      status,
      health,
      root_span_id: `${id}_root`,
      total_latency_ms: status === "incomplete" ? null : latency,
      total_input_tokens: Math.round(800 + random() * 3000),
      total_output_tokens: Math.round(100 + random() * 600),
      estimated_cost_usd: (0.006 + random() * 0.018).toFixed(6),
      pipeline_version:
        PIPELINE_VERSIONS[
          index < 40 ? 2 : Math.floor(random() * PIPELINE_VERSIONS.length)
        ],
      git_commit: null,
      tags: {},
      feedback_status: flagged ? "flagged" : "none",
    });

    // Gaps between traces grow so the list spans about a month.
    startedAt -= Math.round((3 + random() * 12) * 60 * 1000 * (1 + index / 8));
  }

  cache = { traces, createdAt: now };
  return traces;
}

function json(body: unknown, status = 200, headers: HeadersInit = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...headers },
  });
}

function scenarioFromLocation(): MockScenario {
  if (typeof window === "undefined") return "normal";
  const value = new URLSearchParams(window.location.search).get("mock");
  return value === "empty" || value === "error" || value === "slow"
    ? value
    : "normal";
}

export function listMockTraces(
  params: URLSearchParams,
  traces: Trace[] = getMockTraces(),
) {
  const status = params.get("status");
  const health = params.get("health");
  const version = params.get("pipeline_version");
  const after = params.get("started_after");
  const before = params.get("started_before");
  const flagged = params.get("flagged");
  const page = Math.max(1, Number(params.get("page") ?? 1) || 1);
  const pageSize = Math.min(
    100,
    Math.max(1, Number(params.get("page_size") ?? 25) || 25),
  );

  const matches = traces.filter(
    (trace) =>
      (!status || trace.status === status) &&
      (!health || trace.health === health) &&
      (!version || trace.pipeline_version === version) &&
      (!after || trace.started_at >= after) &&
      (!before || trace.started_at <= before) &&
      (flagged !== "true" || trace.feedback_status === "flagged"),
  );
  const start = (page - 1) * pageSize;

  return {
    items: matches.slice(start, start + pageSize),
    page,
    page_size: pageSize,
    total: matches.length,
  };
}

function delay(ms: number, signal?: AbortSignal | null) {
  return new Promise<void>((resolve, reject) => {
    const timer = setTimeout(resolve, ms);
    signal?.addEventListener("abort", () => {
      clearTimeout(timer);
      reject(new DOMException("Aborted", "AbortError"));
    });
  });
}

export function createMockFetch({
  scenario = scenarioFromLocation,
  latencyMs = 350,
}: {
  scenario?: () => MockScenario;
  latencyMs?: number;
} = {}): typeof globalThis.fetch {
  return async (input, init) => {
    const request = new Request(input, init);
    const url = new URL(request.url);
    const mode = scenario();

    await delay(mode === "slow" ? 3000 : latencyMs, request.signal);

    if (mode === "error") {
      return json({ detail: "Mock server error" }, 500, {
        "x-request-id": "req_mock500",
      });
    }

    if (request.method === "GET" && url.pathname === "/health") {
      return json({ status: "ok" });
    }

    if (request.method === "GET" && url.pathname === "/v1/traces") {
      const traces = mode === "empty" ? [] : getMockTraces();
      return json(listMockTraces(url.searchParams, traces));
    }

    const detail = url.pathname.match(/^\/v1\/traces\/([^/]+)$/);
    if (request.method === "GET" && detail) {
      const trace = getMockTraces().find((item) => item.id === detail[1]);
      if (!trace) return json({ detail: "Trace not found" }, 404);
      const body: TraceDetail = { ...trace, spans: [], links: [] };
      return json(body);
    }

    return json({ detail: `Mock has no route for ${url.pathname}` }, 404);
  };
}
