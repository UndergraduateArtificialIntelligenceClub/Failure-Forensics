import { describe, expect, it, vi } from "vitest";
import { createApiClient, type TraceListResponse } from "./client";

const page: TraceListResponse = {
  items: [
    {
      id: "t1",
      project_id: "demo",
      started_at: "2026-11-20T10:00:00Z",
      status: "error",
      health: "failed",
      pipeline_version: "v1",
      feedback_status: "none",
    },
  ],
  page: 1,
  page_size: 25,
  total: 1,
};

function mockFetch(body: unknown, status = 200) {
  return vi.fn<typeof globalThis.fetch>(
    async () =>
      new Response(JSON.stringify(body), {
        status,
        headers: { "Content-Type": "application/json" },
      }),
  );
}

/** openapi-fetch calls fetch with a single Request object. */
function sentRequest(fetch: ReturnType<typeof mockFetch>): Request {
  return fetch.mock.calls[0][0] as Request;
}

describe("createApiClient", () => {
  it("sends typed query params and returns typed data", async () => {
    const fetch = mockFetch(page);
    const api = createApiClient({ baseUrl: "http://api.test", fetch });

    const { data, error } = await api.GET("/v1/traces", {
      params: { query: { health: "failed", pipeline_version: "v1", page: 2 } },
    });

    expect(error).toBeUndefined();
    expect(data?.items[0].id).toBe("t1");
    const request = sentRequest(fetch);
    const url = new URL(request.url);
    expect(url.origin + url.pathname).toBe("http://api.test/v1/traces");
    expect(url.searchParams.get("health")).toBe("failed");
    expect(url.searchParams.get("page")).toBe("2");
  });

  it("adds the API key as a bearer token when given", async () => {
    const fetch = mockFetch(page);
    const api = createApiClient({
      baseUrl: "http://api.test",
      apiKey: "ff_test",
      fetch,
    });

    await api.GET("/v1/traces");

    const request = sentRequest(fetch);
    expect(request.headers.get("Authorization")).toBe("Bearer ff_test");
  });

  it("returns the error body on a failed request", async () => {
    const fetch = mockFetch({ detail: "Trace not found" }, 404);
    const api = createApiClient({ baseUrl: "http://api.test", fetch });

    const { data, error } = await api.GET("/v1/traces/{trace_id}", {
      params: { path: { trace_id: "missing" } },
    });

    expect(data).toBeUndefined();
    expect(error?.detail).toBe("Trace not found");
  });
});
