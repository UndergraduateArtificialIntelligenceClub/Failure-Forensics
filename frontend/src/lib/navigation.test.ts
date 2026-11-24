import { describe, expect, it } from "vitest";
import { getNavItem, isActive, navItems } from "./navigation";

describe("navigation", () => {
  it("has 9 entries with unique routes", () => {
    expect(navItems).toHaveLength(9);
    expect(new Set(navItems.map((item) => item.href)).size).toBe(9);
  });

  it("matches Overview only on the root path", () => {
    expect(isActive("/", "/")).toBe(true);
    expect(isActive("/", "/traces")).toBe(false);
  });

  it("matches a section and its child pages but not look-alike paths", () => {
    expect(isActive("/traces", "/traces")).toBe(true);
    expect(isActive("/traces", "/traces/t1")).toBe(true);
    expect(isActive("/traces", "/tracesx")).toBe(false);
  });

  it("throws for an unknown route", () => {
    expect(() => getNavItem("/nope")).toThrow();
  });
});
