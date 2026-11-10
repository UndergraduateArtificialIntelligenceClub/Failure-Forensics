import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AppShell } from "./AppShell";

describe("AppShell", () => {
  it("shows the app name, navigation and page content", () => {
    render(
      <AppShell>
        <p>hello</p>
      </AppShell>,
    );
    expect(screen.getByText("Failure Forensics")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Traces" })).toBeInTheDocument();
    expect(screen.getByText("hello")).toBeInTheDocument();
  });
});
