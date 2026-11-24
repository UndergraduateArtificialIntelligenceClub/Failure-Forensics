import { describe, expect, it } from "vitest";
import {
  DEFAULT_FILTERS,
  PAGE_SIZE,
  filtersToQuery,
  filtersToSearchParams,
  hasActiveFilters,
  parseFilters,
} from "./filters";

describe("trace filters", () => {
  it("reads every filter from the URL", () => {
    const filters = parseFilters(
      new URLSearchParams(
        "status=error&health=failed&pipeline_version=v1.2&date=7d&flagged=true&page=3",
      ),
    );
    expect(filters).toEqual({
      status: "error",
      health: "failed",
      pipelineVersion: "v1.2",
      date: "7d",
      flagged: true,
      page: 3,
    });
  });

  it("ignores unknown or broken values", () => {
    const filters = parseFilters(
      new URLSearchParams("status=nope&health=bad&date=1y&page=-2&flagged=yes"),
    );
    expect(filters).toEqual(DEFAULT_FILTERS);
  });

  it("round-trips through the URL and leaves out defaults", () => {
    expect(filtersToSearchParams(DEFAULT_FILTERS).toString()).toBe("");
    const params = new URLSearchParams("health=degraded&date=24h&page=2");
    expect(filtersToSearchParams(parseFilters(params)).toString()).toBe(
      params.toString(),
    );
  });

  it("builds the API query, turning the date range into started_after", () => {
    const now = Date.parse("2026-11-22T12:00:00Z");
    const query = filtersToQuery(
      { ...DEFAULT_FILTERS, date: "24h", flagged: true, page: 2 },
      now,
    );
    expect(query).toMatchObject({
      started_after: "2026-11-21T12:00:00.000Z",
      flagged: true,
      page: 2,
      page_size: PAGE_SIZE,
    });
    expect(filtersToQuery(DEFAULT_FILTERS, now).flagged).toBeUndefined();
  });

  it("knows when filters are active, ignoring the page number", () => {
    expect(hasActiveFilters({ ...DEFAULT_FILTERS, page: 4 })).toBe(false);
    expect(hasActiveFilters({ ...DEFAULT_FILTERS, health: "failed" })).toBe(
      true,
    );
  });
});
