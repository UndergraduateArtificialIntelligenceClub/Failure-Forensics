# Failure-Forensics

An AI-powered failure forensics platform that analyzes software incidents, identifies root causes, reconstructs failure timelines, and generates actionable insights to improve system reliability.

## Local development services (Docker Compose)

Run PostgreSQL, Redis, and MinIO locally with Docker Compose. Run the commands from the repository root with Docker running.

### First-time setup

- Docker with the Compose plugin. Run `docker compose version` to check that it’s available.
- Git and `make` to build the MinIO image.
- Go 1.24 or newer. Follow the [Go installation instructions](https://go.dev/doc/install) for your operating system. On macOS with Homebrew, you can run `brew install go`. Verify the installation with `go version`.

The commands use a Bash-compatible shell. On Windows, use WSL 2 with Docker integration enabled and install Git, Go, and `make` inside WSL.

Build the MinIO image once per machine. This compiles the pinned release in a temporary checkout and tags the image used by `compose.yml`.

```bash
(
  set -e
  minio_build_dir=$(mktemp -d)
  git clone --depth 1 --branch RELEASE.2025-10-15T17-29-55Z \
    https://github.com/minio/minio.git "$minio_build_dir"
  cd "$minio_build_dir"

  make build GOOS=linux

  docker build -t minio-local:RELEASE.2025-10-15T17-29-55Z -f - . <<'DOCKERFILE'
FROM alpine:3.22
RUN apk add --no-cache ca-certificates curl
COPY minio /usr/local/bin/minio
ENTRYPOINT ["/usr/local/bin/minio"]
DOCKERFILE

  docker run --rm minio-local:RELEASE.2025-10-15T17-29-55Z --version
)
```

Create `.env` with the example settings for local development.

```bash
if [ ! -f .env ]; then
  cp .env.example .env
fi

docker compose config --quiet
```

### Start and stop the services

- Start the stack with `docker compose up -d --wait`.
- Check status with `docker compose ps`. All three services should show `healthy`.
- Stop the stack with `docker compose down`. PostgreSQL and MinIO keep their data in named volumes for the next startup.

| Service       | Local address           |
| ------------- | ----------------------- |
| PostgreSQL    | `127.0.0.1:5432`        |
| Redis         | `127.0.0.1:6379`        |
| MinIO S3 API  | `http://127.0.0.1:9000` |
| MinIO console | `http://127.0.0.1:9001` |

Use `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` from `.env` to connect to PostgreSQL. Sign in to the MinIO console with `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` from `.env`.

If startup fails, run `docker compose ps -a` to check container status and `docker compose logs --tail=50` to see recent logs.

## Frontend (Next.js console)

Setup and commands, run from the `frontend` folder:

- Install packages: `npm install`
- Start the dev server: `npm run dev` (opens at http://localhost:3000)
- Build: `npm run build`
- Lint: `npm run lint`
- Tests: `npm test`

Stack: Next.js, TypeScript (strict), Tailwind CSS, ESLint, Prettier, Vitest.
