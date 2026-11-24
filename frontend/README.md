# Failure Forensics Console (frontend)

Next.js + React + TypeScript (strict) + Tailwind CSS.

## Run it

    npm install
    npm run dev        # open http://localhost:3000

## Checks (the same ones CI runs)

    npm run lint
    npm run type-check
    npm run test
    npm run build
    npm run format     # auto-format code with Prettier

## Where things are

- `src/app/globals.css`: theme tokens (colours, fonts)
- `src/components/AppShell.tsx`: base layout (header, left menu, session)
- `src/lib/navigation.ts`: the 9 menu entries and their routes
- `src/lib/session.tsx`: session stub (`useSession()`); no login yet
- `src/lib/api/client.ts`: typed API client (`api.GET("/v1/traces", ...)`)
- `src/lib/api/schema.d.ts`: generated types, do not edit by hand
- `openapi/openapi.json`: provisional API spec until KAN-35 publishes contract v1

## API client

Types are generated from the OpenAPI spec with
[openapi-typescript](https://openapi-ts.dev/) and called through
[openapi-fetch](https://openapi-ts.dev/openapi-fetch/).

    npm run api:generate   # regenerate src/lib/api/schema.d.ts after the spec changes
    npm run api:check      # what CI runs: regenerate, then fail if the file changed

Set `NEXT_PUBLIC_API_URL` to point at the backend (default `http://localhost:8000`).

`openapi/openapi.json` is a console-side draft based on `docs/design/data-model.md`.
When KAN-35 publishes the real contract, replace this file with it (or point
`api:generate` at its path) and run `npm run api:generate`.
