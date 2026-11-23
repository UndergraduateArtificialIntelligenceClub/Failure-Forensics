/** Display helpers shared by console pages. */

export function formatLatency(ms: number | null | undefined): string {
  if (ms == null) return "–";
  return ms < 1000 ? `${ms} ms` : `${(ms / 1000).toFixed(1)} s`;
}

/** Cost comes from the API as a decimal string to avoid float rounding. */
export function formatCost(usd: string | null | undefined): string {
  if (usd == null) return "–";
  const value = Number(usd);
  if (!Number.isFinite(value)) return "–";
  return `$${value.toFixed(value < 0.01 ? 4 : 3)}`;
}

export function formatRelativeTime(iso: string, now = Date.now()): string {
  const seconds = Math.max(0, Math.round((now - Date.parse(iso)) / 1000));
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} min ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} h ago`;
  const days = Math.floor(hours / 24);
  return `${days} d ago`;
}
