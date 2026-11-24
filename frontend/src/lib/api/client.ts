import createClient, { type Middleware } from "openapi-fetch";
import { createMockFetch } from "./mock";
import type { components, paths } from "./schema";

/**
 * Typed API client (KAN-46).
 *
 * Types come from `schema.d.ts`, which is generated from
 * `openapi/openapi.json` by `npm run api:generate`. Never edit schema.d.ts by
 * hand: CI regenerates it and fails if the committed copy is out of date.
 *
 * Usage:
 *   const { data, error } = await api.GET("/v1/traces", {
 *     params: { query: { health: "failed", page: 1 } },
 *   });
 */
export const DEFAULT_API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type ApiClientOptions = {
  baseUrl?: string;
  /** Project API key. Optional while the session is a stub. */
  apiKey?: string;
  fetch?: typeof globalThis.fetch;
};

export function createApiClient({
  baseUrl = DEFAULT_API_URL,
  apiKey,
  fetch,
}: ApiClientOptions = {}) {
  const client = createClient<paths>({ baseUrl, fetch });

  if (apiKey) {
    const auth: Middleware = {
      onRequest({ request }) {
        request.headers.set("Authorization", `Bearer ${apiKey}`);
        return request;
      },
    };
    client.use(auth);
  }

  return client;
}

/**
 * "mock" (default until the backend serves /v1/traces) answers requests in the
 * browser from src/lib/api/mock.ts. Set NEXT_PUBLIC_API_MODE=live to call the
 * real API at NEXT_PUBLIC_API_URL.
 */
export const API_MODE: "mock" | "live" =
  process.env.NEXT_PUBLIC_API_MODE === "live" ? "live" : "mock";

export const api = createApiClient(
  API_MODE === "mock" ? { fetch: createMockFetch() } : {},
);

export type ApiClient = ReturnType<typeof createApiClient>;

// Short names for the schemas pages use most.
type Schemas = components["schemas"];
export type Trace = Schemas["Trace"];
export type TraceDetail = Schemas["TraceDetail"];
export type TraceListResponse = Schemas["TraceListResponse"];
export type TraceStatus = Schemas["TraceStatus"];
export type TraceHealth = Schemas["TraceHealth"];
export type Span = Schemas["Span"];
export type SpanLink = Schemas["SpanLink"];
export type ApiError = Schemas["Error"];
