import { describe, expect, it } from "vitest";
import { createApiClient } from "./client";
import { createMockFetch, getMockTraces, listMockTraces } from "./mock";

describe("mock API", () => {
  const traces = getMockTraces(Date.parse("2026-11-22T12:00:00Z"));

  it("filters by health, status, version and flag", () => {
    const params = new URLSearchParams(
      "health=failed&status=error&pipeline_version=v1.2&flagged=true&page_size=100",
    );
    const { items, total } = listMockTraces(params, traces);
    expect(total).toBe(items.length);
    expect(items.length).toBeGreaterThan(0);
    for (const trace of items) {
      expect(trace.health).toBe("failed");
      expect(trace.status).toBe("error");
      expect(trace.pipeline_version).toBe("v1.2");
      expect(trace.feedback_status).toBe("flagged");
    }
  });

  it("filters by date and paginates", () => {
    const after = "2026-11-21T12:00:00.000Z";
    const recent = listMockTraces(
      new URLSearchParams(`started_after=${after}&page_size=100`),
      traces,
    );
    expect(recent.total).toBeLessThan(traces.length);
    expect(recent.items.every((trace) => trace.started_at >= after)).toBe(true);

    const page2 = listMockTraces(
      new URLSearchParams("page=2&page_size=25"),
      traces,
    );
    expect(page2.items[0]).toEqual(traces[25]);
    expect(page2.total).toBe(traces.length);
  });

  it("serves the typed client, including the error scenario", async () => {
    const ok = createApiClient({
      baseUrl: "http://mock",
      fetch: createMockFetch({ scenario: () => "normal", latencyMs: 0 }),
    });
    const { data } = await ok.GET("/v1/traces", {
      params: { query: { page_size: 5 } },
    });
    expect(data?.items).toHaveLength(5);

    const failing = createApiClient({
      baseUrl: "http://mock",
      fetch: createMockFetch({ scenario: () => "error", latencyMs: 0 }),
    });
    const { error, response } = await failing.GET("/v1/traces");
    expect(response.status).toBe(500);
    expect(error?.detail).toBe("Mock server error");
  });
});
