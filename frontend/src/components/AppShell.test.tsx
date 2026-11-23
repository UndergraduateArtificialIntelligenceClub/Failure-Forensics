import { render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { AppShell } from "./AppShell";

const pathname = vi.hoisted(() => ({ current: "/" }));
vi.mock("next/navigation", () => ({ usePathname: () => pathname.current }));

const expectedNav = [
  "Overview",
  "Traces",
  "Failures",
  "Compare",
  "Evaluations",
  "Experiments",
  "Datasets",
  "Analytics",
  "Settings",
];

function renderShell() {
  render(
    <AppShell>
      <p>hello</p>
    </AppShell>,
  );
  return within(screen.getByRole("navigation", { name: "Main" }));
}

describe("AppShell", () => {
  beforeEach(() => {
    pathname.current = "/";
  });

  it("shows the app name and page content", () => {
    renderShell();
    expect(screen.getByText("Failure Forensics")).toBeInTheDocument();
    expect(screen.getByText("hello")).toBeInTheDocument();
  });

  it("has all 9 nav entries in wireframe order", () => {
    const nav = renderShell();
    const labels = nav.getAllByRole("link").map((link) => link.textContent);
    expect(labels).toEqual(expectedNav);
  });

  it("marks the current section as active, including child pages", () => {
    pathname.current = "/traces/abc123";
    const nav = renderShell();
    expect(nav.getByRole("link", { name: "Traces" })).toHaveAttribute(
      "aria-current",
      "page",
    );
    expect(nav.getByRole("link", { name: "Overview" })).not.toHaveAttribute(
      "aria-current",
    );
  });

  it("shows the stub session in the header", () => {
    renderShell();
    expect(screen.getByText("Demo project")).toBeInTheDocument();
    expect(screen.getByText("Dev session")).toBeInTheDocument();
  });
});
