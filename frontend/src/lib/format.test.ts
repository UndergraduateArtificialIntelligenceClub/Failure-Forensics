import { describe, expect, it } from "vitest";
import { formatCost, formatLatency, formatRelativeTime } from "./format";

describe("format", () => {
  it("formats latency", () => {
    expect(formatLatency(450)).toBe("450 ms");
    expect(formatLatency(2140)).toBe("2.1 s");
    expect(formatLatency(null)).toBe("–");
  });

  it("formats cost from a decimal string", () => {
    expect(formatCost("0.014000")).toBe("$0.014");
    expect(formatCost("0.004321")).toBe("$0.0043");
    expect(formatCost(null)).toBe("–");
    expect(formatCost("abc")).toBe("–");
  });

  it("formats relative time", () => {
    const now = Date.parse("2026-11-22T12:00:00Z");
    expect(formatRelativeTime("2026-11-22T11:59:30Z", now)).toBe("just now");
    expect(formatRelativeTime("2026-11-22T11:51:00Z", now)).toBe("9 min ago");
    expect(formatRelativeTime("2026-11-22T09:00:00Z", now)).toBe("3 h ago");
    expect(formatRelativeTime("2026-11-20T12:00:00Z", now)).toBe("2 d ago");
  });
});
