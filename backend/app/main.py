import json
import logging

import httpx
import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from redis import Redis
from redis.backoff import NoBackoff
from redis.exceptions import RedisError
from redis.retry import Retry

from app.config import Settings

app = FastAPI(title="Failure Forensics API")
logger = logging.getLogger("failure_forensics")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(
            {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "event": record.getMessage(),
            }
        )


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False


def check_postgres(settings: Settings) -> bool:
    if settings.postgres_password is None:
        return False

    try:
        with psycopg.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password.get_secret_value(),
            connect_timeout=2,
            options="-c statement_timeout=2000",
            autocommit=True,
        ) as connection:
            connection.execute("SELECT 1")
        return True
    except psycopg.Error:
        return False


def check_redis(settings: Settings) -> bool:
    try:
        with Redis.from_url(
            settings.redis_url,
            socket_connect_timeout=2,
            socket_timeout=2,
            retry=Retry(NoBackoff(), 0),
        ) as client:
            return client.ping() is True
    except (RedisError, ValueError):
        return False


def check_minio(settings: Settings) -> bool:
    try:
        url = f"{settings.minio_url.rstrip('/')}/minio/health/ready"
        return httpx.get(url, timeout=2.0).status_code == 200
    except (httpx.RequestError, httpx.InvalidURL):
        return False


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> JSONResponse:
    try:
        settings = Settings()
    except ValidationError:
        logger.warning("readiness_configuration_invalid")
        return JSONResponse({"status": "not_ready"}, status_code=503)

    checks = {
        "postgres": check_postgres(settings),
        "redis": check_redis(settings),
        "minio": check_minio(settings),
    }
    failed = [service for service, passed in checks.items() if not passed]
    if failed:
        logger.warning("readiness_failed: %s", ", ".join(failed))

    return JSONResponse(
        {"status": "not_ready" if failed else "ready", "checks": checks},
        status_code=503 if failed else 200,
    )
