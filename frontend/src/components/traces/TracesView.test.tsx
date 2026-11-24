import { fireEvent, render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { createApiClient } from "@/lib/api/client";
import { createMockFetch, type MockScenario } from "@/lib/api/mock";
import { TracesView } from "./TracesView";

const nav = vi.hoisted(() => ({
  search: "",
  replace: vi.fn<(href: string, options?: object) => void>(),
}));
vi.mock("next/navigation", () => ({
  usePathname: () => "/traces",
  useSearchParams: () => new URLSearchParams(nav.search),
  useRouter: () => ({ replace: nav.replace }),
}));

function client(scenario: MockScenario = "normal") {
  return createApiClient({
    baseUrl: "http://mock",
    fetch: createMockFetch({ scenario: () => scenario, latencyMs: 0 }),
  });
}

describe("TracesView", () => {
  beforeEach(() => {
    nav.search = "";
    nav.replace.mockReset();
  });

  it("shows loading, then a page of traces with pagination", async () => {
    render(<TracesView client={client()} />);
    expect(
      screen.getByRole("status", { name: "Loading traces" }),
    ).toBeInTheDocument();

    const table = await screen.findByRole("table");
    // 25 rows + header row
    expect(within(table).getAllByRole("row")).toHaveLength(26);
    expect(screen.getByText(/Showing 1–25 of \d+/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Prev" })).toBeDisabled();
  });

  it("only shows traces matching the filters in the URL", async () => {
    nav.search = "health=failed";
    render(<TracesView client={client()} />);
    const table = await screen.findByRole("table");
    const rows = within(table).getAllByRole("row").slice(1);
    expect(rows.length).toBeGreaterThan(0);
    for (const row of rows) {
      expect(within(row).getByText("failed")).toBeInTheDocument();
    }
  });

  it("writes filter changes to the URL and resets to page 1", async () => {
    nav.search = "page=3";
    render(<TracesView client={client()} />);
    await screen.findByRole("table");

    fireEvent.change(screen.getByLabelText("Health"), {
      target: { value: "degraded" },
    });
    expect(nav.replace).toHaveBeenLastCalledWith("/traces?health=degraded", {
      scroll: false,
    });

    fireEvent.click(screen.getByLabelText("Flagged only"));
    expect(nav.replace).toHaveBeenLastCalledWith("/traces?flagged=true", {
      scroll: false,
    });
  });

  it("moves to the next page", async () => {
    render(<TracesView client={client()} />);
    await screen.findByRole("table");
    fireEvent.click(screen.getByRole("button", { name: "Next" }));
    expect(nav.replace).toHaveBeenLastCalledWith("/traces?page=2", {
      scroll: false,
    });
  });

  it("shows the first-trace empty state when there is no data", async () => {
    render(<TracesView client={client("empty")} />);
    expect(await screen.findByText("No traces yet")).toBeInTheDocument();
  });

  it("shows the no-match state when filters exclude everything", async () => {
    nav.search = "pipeline_version=v9.9";
    render(<TracesView client={client()} />);
    expect(
      await screen.findByText("No traces match these filters"),
    ).toBeInTheDocument();
    fireEvent.click(
      screen.getAllByRole("button", { name: "Clear filters" })[0],
    );
    expect(nav.replace).toHaveBeenLastCalledWith("/traces", { scroll: false });
  });

  it("shows the error state with request ID, and retries", async () => {
    let scenario: MockScenario = "error";
    const flaky = createApiClient({
      baseUrl: "http://mock",
      fetch: createMockFetch({ scenario: () => scenario, latencyMs: 0 }),
    });
    render(<TracesView client={flaky} />);

    const alert = await screen.findByRole("alert");
    expect(
      within(alert).getByText("Could not load traces"),
    ).toBeInTheDocument();
    expect(
      within(alert).getByText("Request ID: req_mock500"),
    ).toBeInTheDocument();

    scenario = "normal";
    fireEvent.click(screen.getByRole("button", { name: "Try again" }));
    expect(await screen.findByRole("table")).toBeInTheDocument();
  });
});
