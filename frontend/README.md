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
- `src/components/AppShell.tsx`: base layout (header and left menu)
