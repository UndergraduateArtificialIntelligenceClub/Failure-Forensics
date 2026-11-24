import type { TraceHealth } from "@/lib/api/client";

// Colour follows docs/ux-ui.md; the label is always shown as text too.
const styles: Record<TraceHealth, string> = {
  healthy: "border-success/40 bg-success/10 text-success",
  degraded: "border-warning/40 bg-warning/10 text-warning",
  failed: "border-danger/40 bg-danger/10 text-danger",
  unknown: "border-border bg-border/40 text-muted",
};

export function HealthBadge({ health }: { health: TraceHealth }) {
  return (
    <span
      className={`inline-block rounded-full border px-2 py-0.5 text-xs font-medium ${styles[health]}`}
    >
      {health}
    </span>
  );
}
